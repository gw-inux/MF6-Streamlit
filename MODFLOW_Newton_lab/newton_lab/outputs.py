"""Native heads, full external budgets and diagnostic counts.

Budgets come from binary cell flows. Rates are separated into IN/OUT before
aggregation. Cumulative volumes integrate each solved end-step rate over its
native time interval; the SS initialization period is never integrated.
"""

import re
from pathlib import Path

import flopy
import numpy as np
import pandas as pd

from .config import DAY

NUMBER = r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[EeDd][-+]?\d+)?"
TERMS = {
    "CONSTANT HEAD": "CHD",
    "CHD": "CHD",
    "WELLS": "WEL",
    "WEL": "WEL",
    "RECHARGE": "RCH",
    "RCHA": "RCH",
    "STORAGE": "STO",
    "STO-SS": "STO",
    "STO-SY": "STO",
}


def clean_heads(s, values):
    heads = np.asarray(values, dtype=float).copy()
    heads[(~np.isfinite(heads)) | (np.abs(heads) > 1e20)] = np.nan
    heads[..., ~s.active_mask()] = np.nan
    if not s.confined:
        heads = np.where(heads <= s.botm[:, None, None] + 1e-6, np.nan, heads)
    return heads


def groundwater_surface(s, heads):
    """Uppermost wet-cell head; no head is clipped to the aquifer top.

    Confined columns display a potentiometric head, not a physical water table.
    For convertible columns, above-top heads also indicate confined conditions.
    """
    heads = clean_heads(s, heads)
    valid = np.isfinite(heads)
    index = valid.argmax(axis=0)
    surface = np.take_along_axis(heads, index[None, ...], axis=0)[0]
    surface[~valid.any(axis=0)] = np.nan
    return surface


def read_heads(directory, s):
    with flopy.utils.HeadFile(Path(directory) / "flow.hds", precision="auto") as reader:
        precision = reader.precision
        times = np.asarray(reader.get_times(), dtype=float)
        keys = reader.get_kstpkper()
        heads = np.stack([reader.get_data(kstpkper=key) for key in keys])
    expected = sum(p.steps for p in s.periods())
    if len(times) != expected:
        raise ValueError(
            f"Incomplete heads: {len(times)} of {expected} time steps were saved."
        )
    if not np.isclose(times[-1], sum(p.seconds for p in s.periods()), rtol=1e-6):
        raise ValueError("The head file does not reach the requested end time.")
    days = (times - 1.0) / DAY if s.transient else np.zeros_like(times)
    return days, keys, clean_heads(s, heads), precision


def _flows(record):
    """CBC arrays, lists or layer-indicator/data pairs to actual flow values."""
    if isinstance(record, np.ndarray) and record.dtype.names:
        return np.asarray(record["q"], dtype=float)
    if isinstance(record, (list, tuple)) and len(record) == 2:
        return np.asarray(record[1], dtype=float).ravel()
    return np.asarray(np.ma.filled(record, 0), dtype=float).ravel()


def read_budget(directory, s, precision="auto"):
    rows = []
    with flopy.utils.CellBudgetFile(
        Path(directory) / "flow.cbc", precision=precision
    ) as reader:
        names = [n.strip() for n in reader.get_unique_record_names(decode=True)]
        for key, native_time in zip(
            reader.get_kstpkper(), reader.get_times(), strict=True
        ):
            step, period = key
            row = dict(
                time_days=(native_time - 1.0) / DAY if s.transient else 0.0,
                native_seconds=native_time,
                step=step,
                period=period,
            )
            for term in ("CHD", "WEL", "RCH", "STO"):
                row[term + "_IN"] = 0.0
                row[term + "_OUT"] = 0.0
            for name in names:
                term = TERMS.get(name.upper())
                if term is None:
                    continue  # exclude internal face flows
                for record in reader.get_data(kstpkper=key, text=name):
                    q = _flows(record)
                    if not np.isfinite(q).all():
                        raise ValueError("Non-finite native budget flow.")
                    row[term + "_IN"] += q[q > 0].sum()
                    row[term + "_OUT"] -= q[q < 0].sum()
            row["TOTAL_IN"] = sum(row[t + "_IN"] for t in ("CHD", "WEL", "RCH", "STO"))
            row["TOTAL_OUT"] = sum(
                row[t + "_OUT"] for t in ("CHD", "WEL", "RCH", "STO")
            )
            denom = 0.5 * (row["TOTAL_IN"] + row["TOTAL_OUT"])
            row["discrepancy_pct"] = (
                100 * (row["TOTAL_IN"] - row["TOTAL_OUT"]) / denom if denom else 0.0
            )
            row["requested_well"] = s.total_well_rate(s.periods()[period])
            row["actual_well"] = row["WEL_IN"] - row["WEL_OUT"]
            rows.append(row)
    if len(rows) != sum(p.steps for p in s.periods()):
        raise ValueError("Incomplete budget output.")
    budget = pd.DataFrame(rows)
    rate_columns = [
        t + suffix for t in ("CHD", "WEL", "RCH", "STO") for suffix in ("_IN", "_OUT")
    ]
    dt = np.diff(np.r_[0.0, budget.native_seconds.to_numpy()])
    dt[budget.period.to_numpy() == 0] = 0.0
    for column in rate_columns:
        budget[column + "_CUM"] = np.cumsum(budget[column].to_numpy() * dt)
    return budget


def diagnostics(directory, engine):
    directory = Path(directory)
    listing = "\n".join(
        p.read_text(errors="replace")
        for p in sorted(directory.iterdir())
        if p.suffix.lower() in (".list", ".lst")
    )
    counts = dict(outer=None, inner=None, listing=listing)
    percentages = re.findall(
        r"PERCENT DISCREPANCY\s*=\s*(" + NUMBER + ")", listing, re.I
    )
    counts["native_discrepancy_pct"] = (
        float(percentages[-1].replace("D", "E")) if percentages else None
    )
    if engine == "mf2005":
        outer = re.findall(r"(\d+)\s+CALLS TO PCG ROUTINE", listing)
        inner = re.findall(r"(\d+)\s+TOTAL ITERATIONS", listing)
        counts.update(
            outer=sum(map(int, outer)) if outer else None,
            inner=sum(map(int, inner)) if inner else None,
        )
    elif engine == "mfnwt":
        outer = re.findall(r"NWT REQUIRED\s+(\d+)\s+OUTER ITERATIONS", listing)
        inner = re.findall(r"AND A TOTAL OF\s+(\d+)\s+INNER ITERATIONS", listing)
        counts.update(
            outer=sum(map(int, outer)) if outer else None,
            inner=sum(map(int, inner)) if inner else None,
        )
    else:
        for filename, kind in (("outer.csv", "outer"), ("inner.csv", "inner")):
            path = directory / filename
            if path.is_file() and path.stat().st_size:
                try:
                    table = pd.read_csv(path)
                    table.columns = table.columns.str.strip().str.lower()
                    if kind == "outer":
                        counts[kind] = len(table)
                    elif "total_inner_iterations" in table and len(table):
                        counts[kind] = int(table.total_inner_iterations.max())
                except (
                    pd.errors.EmptyDataError,
                    pd.errors.ParserError,
                    ValueError,
                    OverflowError,
                ):
                    pass
    return counts


def head_timeseries(s, days, heads):
    # Each well reports its uppermost wet-cell head, not a borehole water level.
    surfaces = np.stack([groundwater_surface(s, h) for h in heads])
    series = {"time_days": days}
    series.update({well.name: surfaces[:, well.row, well.col] for well in s.wells})
    series.update(
        {obs.name: heads[:, obs.layer, obs.row, obs.col] for obs in s.observations}
    )
    return pd.DataFrame(series)
