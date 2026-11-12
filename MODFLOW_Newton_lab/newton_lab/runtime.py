"""Bounded native execution with auditable outputs and failure preservation."""

import json
import re
import subprocess
import time
from dataclasses import asdict
from pathlib import Path

import numpy as np

from .models import build_model
from .outputs import diagnostics, head_timeseries, read_budget, read_heads


def run_model(scenario, solver, directory, executable):
    directory = Path(directory).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    result = dict(
        scenario=scenario,
        solver=solver,
        directory=directory,
        success=False,
        status="failed",
        heads=None,
        budget=None,
        timeseries=None,
        wall_seconds=0.0,
        build_seconds=0.0,
        outer=None,
        inner=None,
        active_cells=int(scenario.active_mask().sum()),
        wet_cells=None,
        dry_cells=None,
        discrepancy_pct=None,
        error="",
    )
    (directory / "configuration.json").write_text(
        json.dumps(
            {
                "scenario": asdict(scenario),
                "solver": asdict(solver),
                "executable": executable,
            },
            indent=2,
        )
    )
    start = time.perf_counter()
    try:
        command = build_model(scenario, solver, directory, executable)
        result["build_seconds"] = time.perf_counter() - start
        start = time.perf_counter()
        # Write to a file, avoiding pipe backpressure and unbounded UI output.
        with (directory / "stdout.txt").open("w") as log:
            process = subprocess.run(
                command,
                cwd=directory,
                stdout=log,
                stderr=subprocess.STDOUT,
                timeout=solver.timeout,
                check=False,
                shell=False,
            )
        result["returncode"] = process.returncode
    except subprocess.TimeoutExpired:
        result.update(
            status="timed_out", error="Native run exceeded the selected time limit."
        )
    except (OSError, ValueError, RuntimeError, KeyError) as error:
        result["error"] = str(error)
    finally:
        result["wall_seconds"] = time.perf_counter() - start
    result.update(diagnostics(directory, solver.engine))
    logpath = directory / "stdout.txt"
    stdout = logpath.read_text(errors="replace") if logpath.exists() else ""
    combined = stdout + "\n" + result["listing"]
    failed = re.search(
        r"FAILED TO (?:CONVERGE|MEET)|CONVERGENCE FAILURE|FAILURE TO CONVERGE|ABNORMAL TERMINATION",
        combined,
        re.I,
    )
    success = (
        not result["error"]
        and result.get("returncode") == 0
        and "normal termination" in stdout.lower()
        and not failed
    )
    if success:
        try:
            days, keys, heads, precision = read_heads(directory, scenario)
            budget = read_budget(directory, scenario, precision=precision)
            wet = np.isfinite(heads[-1]) & scenario.active_mask()
            result.update(
                days=days,
                keys=keys,
                heads=heads,
                budget=budget,
                timeseries=head_timeseries(scenario, days, heads),
                wet_cells=int(wet.sum()),
                dry_cells=int((scenario.active_mask() & ~wet).sum()),
                discrepancy_pct=float(budget.discrepancy_pct.iloc[-1]),
                max_discrepancy_pct=float(budget.discrepancy_pct.abs().max()),
                success=True,
                status="converged",
            )
            budget.to_csv(directory / "budget.csv", index=False)
            result["timeseries"].to_csv(directory / "heads_over_time.csv", index=False)
        except (ValueError, OSError, EOFError, IndexError, KeyError) as error:
            result["error"] = f"Output validation: {error}"
    if failed and not result["error"]:
        result["error"] = "Native solver reported nonconvergence; inspect the listing."
    if not result["success"] and not result["error"]:
        result["error"] = "No validated normal termination; inspect the native output."
    return result


def history_row(result, run_id):
    """Small diagnostic record; independent of retained full result arrays."""
    s, cfg = result["scenario"], result["solver"]
    method = (
        "PCG"
        if cfg.engine == "mf2005"
        else ("GMRES" if cfg.nwt_method == 1 else "XMD")
        if cfg.engine == "mfnwt"
        else ("IMS / Newton" if cfg.newton and not s.confined else "IMS / Picard")
    )
    return dict(
        run=run_id,
        engine=cfg.engine,
        method=method,
        status=result["status"],
        transient=s.transient,
        confined=s.confined,
        combined=s.combined,
        grid=f"{s.nlay} × {s.nrow} × {s.ncol}",
        conductivity=s.conductivity,
        ss=s.ss,
        sy=s.sy,
        recharge=s.recharge,
        requested_first_rate_lps=s.total_well_rate(s.periods()[1 if s.transient else 0])
        * 1000,
        well_count=len(s.wells),
        pumping_lps=s.pumping_lps,
        injection_lps=s.injection_lps,
        active=result["active_cells"],
        wet=result["wet_cells"],
        dry=result["dry_cells"],
        outer=result["outer"],
        inner=result["inner"],
        runtime_s=result["wall_seconds"],
        discrepancy_pct=result["discrepancy_pct"],
        max_discrepancy_pct=result.get("max_discrepancy_pct"),
        head_close=cfg.head_close,
        flow_close=cfg.flow_close,
    )
