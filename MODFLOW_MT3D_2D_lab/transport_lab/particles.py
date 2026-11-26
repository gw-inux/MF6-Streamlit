"""MODPATH 7 advective particle comparison.

Particles carry bookkeeping mass weights only. MODPATH does not solve dispersion
or a concentration equation, so neither concentration nor a solute mass-balance
error is attributed to it. Pulse/continuous release uses equal-time midpoint
batches; increase release_groups to refine this temporal quadrature.
"""
from dataclasses import dataclass, field
from pathlib import Path
import subprocess
import os
import time

import flopy
import numpy as np
import pandas as pd


@dataclass
class ParticleResult:
    paths: pd.DataFrame
    timepoints: pd.DataFrame
    endpoints: pd.DataFrame
    releases: pd.DataFrame
    arrivals: pd.DataFrame
    metrics: dict
    warnings: list = field(default_factory=list)


def _local_points(number, dimensions=3):
    """Exactly number deterministic Cartesian midpoints, never on cell faces."""
    if not isinstance(number, (int, np.integer)) or number < 1:
        raise ValueError('Particles per source cell must be a positive integer.')
    factors = np.ones(dimensions, dtype=int)
    remainder = int(number)
    divisor = 2
    while remainder > 1:
        while remainder % divisor == 0:
            factors[np.argmin(factors)] *= divisor
            remainder //= divisor
        divisor += 1
    axes = [(np.arange(n) + 0.5) / n for n in factors]
    if dimensions == 2:
        axes.append(np.array([0.5]))
    return np.array(np.meshgrid(*axes, indexing='ij')).reshape(3, -1).T


def release_schedule(config):
    """Times and injected masses (g) for each release group."""
    if config.source_kind == 'dirac':
        return np.array([0.]), np.array([config.source_mass])
    count = int(config.release_groups)
    if count < 1:
        raise ValueError('At least one particle release group is required.')
    active = min(config.duration, config.pulse_duration) if config.source_kind == 'pulse' else config.duration
    dt = active / count
    return (np.arange(count) + 0.5) * dt, np.full(count, config.mass_rate * dt)


def build_releases(config):
    """Return FloPy groups plus zero-based group/local-id release metadata.

    Solute mass is apportioned by source pore volume, exactly as in MT3D's
    initially uniform concentration or pore-volume-weighted mass loading.
    """
    cells = config.source_cells()
    n = int(config.particles_per_cell)
    points = _local_points(n, dimensions=2 if config.nlay == 1 else 3)
    times, masses = release_schedule(config)
    if len(cells) * n * len(times) > 100_000:
        raise ValueError('Reduce source size, particles per cell, or release groups (100,000 particles maximum).')
    porosity = config.arrays()[2]
    pore_volumes = np.array([porosity[k, i, j] * config.dx * config.dy * config.dz for k, i, j in cells])
    fractions = pore_volumes / pore_volumes.sum()
    partlocs = [cell for cell in cells for _ in range(n)]
    local = np.tile(points, (len(cells), 1))
    groups, records = [], []
    for group, (release_time, mass) in enumerate(zip(times, masses)):
        pdata = flopy.modpath.ParticleData(
            partlocs=partlocs, structured=True, localx=local[:, 0],
            localy=local[:, 1], localz=local[:, 2], timeoffset=0.0, drape=0,
        )
        groups.append(flopy.modpath.ParticleGroup(
            particlegroupname=f'release_{group+1}', releasedata=float(release_time), particledata=pdata,
        ))
        for cell_idx, (k, i, j) in enumerate(cells):
            for p, (lx, ly, lz) in enumerate(points):
                records.append({
                    'particlegroup': group, 'particleidloc': cell_idx * n + p,
                    'release_time': float(release_time), 'weight_g': float(mass * fractions[cell_idx] / n),
                    'x0': (j + lx) * config.dx,
                    'y0': config.width - (i + 1 - ly) * config.dy,
                    'z0': config.thickness - (k + 1 - lz) * config.dz,
                    'source_layer': k, 'source_row': i, 'source_column': j,
                })
    return groups, pd.DataFrame(records)


def _records(data):
    if isinstance(data, list):
        data = np.concatenate(data) if data else np.empty(0)
    return pd.DataFrame.from_records(np.atleast_1d(data))


def _add_release_metadata(frame, releases):
    cols = ['particlegroup', 'particleidloc', 'release_time', 'weight_g']
    frame = frame.merge(releases[cols], how='left', on=cols[:2], validate='many_to_one')
    if frame['weight_g'].isna().any():
        raise RuntimeError('MODPATH particle identifiers do not match the release definition.')
    return frame


def _observation_inside(config, x, y, z):
    return bool(np.isfinite([x, y, z]).all() and
                0 <= x <= config.length and 0 <= y <= config.width and
                0 <= z <= config.thickness)


def crossing_arrivals(paths, config):
    """First advective crossing of each observation's x-plane per particle.

    The y-z aperture corresponds to that observation's model cell. Times are
    linearly interpolated between MODPATH pathline records, so these are sampled
    advective arrivals, not concentrations or exact point-monitor predictions.
    Out-of-domain observations are skipped without renumbering later points.
    With flow reversal only the first plane crossing in either direction is
    counted, so a returning particle never contributes its mass twice.
    """
    columns = ['observation', 'particleid', 'time', 'y', 'z', 'weight_g', 'within_observation_cell']
    records = []
    for obs_idx, (xobs, yobs, zobs) in enumerate(config.observations):
        if not _observation_inside(config, xobs, yobs, zobs):
            continue
        k, i, _ = config.cell(xobs, yobs, zobs)
        ymin, ymax = config.width - (i + 1) * config.dy, config.width - i * config.dy
        zmin, zmax = config.thickness - (k + 1) * config.dz, config.thickness - k * config.dz
        for pid, path in paths.groupby('particleid', sort=False):
            path = path.sort_values('time')
            x, t = path.x.to_numpy(), path.time.to_numpy()
            if len(x) < 2:
                continue
            # Detect either direction, supporting transient flow reversal.
            cross = np.flatnonzero(((x[:-1] <= xobs) & (x[1:] >= xobs) | (x[:-1] >= xobs) & (x[1:] <= xobs)) & (x[1:] != x[:-1]))
            if not len(cross):
                continue
            j = cross[0]
            f = (xobs - x[j]) / (x[j + 1] - x[j])
            y = path.y.iloc[j] + f * (path.y.iloc[j + 1] - path.y.iloc[j])
            z = path.z.iloc[j] + f * (path.z.iloc[j + 1] - path.z.iloc[j])
            records.append({'observation': obs_idx + 1, 'particleid': int(pid),
                            'time': float(t[j] + f * (t[j + 1] - t[j])), 'y': float(y), 'z': float(z),
                            'weight_g': float(path.weight_g.iloc[0]),
                            'within_observation_cell': bool(ymin <= y <= ymax and zmin <= z <= zmax)})
    return pd.DataFrame(records, columns=columns)


def run_particles(config, flowmodel, executable, workspace=None):
    """Run real MODPATH 7 using an already-computed MODFLOW flow model.

    Inputs must include head and compact cell-budget records at every flow step.
    Output times use the transport lab's regular save times, plus pulse end.
    Particle groups are distinct to retain release weights without relying on
    MODPATH's global sequencing. All returned coordinates use x east, y north,
    and elevation z in metres; all tracking times are days since source onset.
    """
    workspace = Path(workspace or Path(flowmodel.model_ws) / 'particles').resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    groups, releases = build_releases(config)
    mp = flopy.modpath.Modpath7(
        modelname='particles', flowmodel=flowmodel, exe_name=str(executable),
        model_ws=str(workspace), verbose=False,
    )
    # FloPy prefixes HEAD/BUDGET with the flow workspace, but not DIS.
    mp.dis_file = os.path.relpath(Path(flowmodel.model_ws) / flowmodel.dis.file_name[0], workspace)
    flopy.modpath.Modpath7Bas(mp, porosity=config.arrays()[2])
    save_times = np.linspace(0., config.duration, config.outputs)
    if config.source_kind == 'pulse':
        save_times = np.unique(np.r_[save_times, config.pulse_duration])
    # Including t=0 preserves a Dirac source snapshot; future groups remain absent.
    flopy.modpath.Modpath7Sim(
        mp, simulationtype='combined', trackingdirection='forward',
        weaksinkoption='pass_through', weaksourceoption='pass_through',
        budgetoutputoption='summary', referencetime=0.0,
        stoptimeoption='specified', stoptime=float(config.duration),
        timepointdata=[len(save_times), save_times.tolist()], particlegroups=groups,
    )
    mp.write_input()
    log = workspace / 'particles.stdout.log'
    start = time.perf_counter()
    try:
        with log.open('w') as stream:
            result = subprocess.run([str(Path(executable).resolve()), mp.namefile], cwd=workspace,
                                    stdout=stream, stderr=subprocess.STDOUT,
                                    timeout=config.solver.timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f'MODPATH exceeded {config.solver.timeout} s. See {log}.') from exc
    runtime = time.perf_counter() - start
    text = log.read_text(errors='replace')
    if result.returncode != 0 or 'normal termination' not in text.lower():
        raise RuntimeError(f'MODPATH did not terminate normally.\n{text[-4000:]}')
    path_file, ts_file, end_file = [workspace / f'particles.{ext}' for ext in ('mppth', 'timeseries', 'mpend')]
    if not all(p.is_file() for p in (path_file, ts_file, end_file)):
        raise RuntimeError('MODPATH terminated without all required particle output files.')
    paths = _add_release_metadata(_records(flopy.utils.PathlineFile(str(path_file)).get_alldata()), releases)
    timepoints = _add_release_metadata(_records(flopy.utils.TimeseriesFile(str(ts_file)).get_alldata()), releases)
    endpoints = _add_release_metadata(_records(flopy.utils.EndpointFile(str(end_file)).get_alldata()), releases)
    if len(endpoints) != len(releases):
        raise RuntimeError(f'MODPATH returned {len(endpoints)} endpoints for {len(releases)} releases.')
    if not np.isfinite(paths[['x', 'y', 'z', 'time']].to_numpy()).all():
        raise RuntimeError('MODPATH returned nonfinite particle positions or times.')
    if paths.time.max() > config.duration + max(1e-4, config.duration * 1e-6):
        raise RuntimeError('MODPATH tracked beyond the requested simulation duration.')
    status_counts = {int(k): int(v) for k, v in endpoints.status.value_counts().items()}
    warnings = []
    if any(k in status_counts for k in (4, 5, 6, 7)):
        warnings.append('Some MODPATH particles have unreleased, stranded, or other abnormal status; inspect endpoints and listing.')
    if config.source_kind != 'dirac':
        warnings.append(f'Advective release is approximated with {config.release_groups} midpoint batches; it does not model dispersion.')
    if config.transient:
        warnings.append('MODPATH samples the saved transient flow field; refine flow time steps to assess tracking accuracy.')
    metrics = {
        'runtime_s': float(runtime), 'count': len(releases), 'endpoint_count': len(endpoints),
        'status_counts': status_counts, 'release_groups': len(groups),
        'represented_mass_g': float(releases.weight_g.sum()),
        'mass_balance_pct': None,
        'description': 'Advection only; particle weights are release bookkeeping, not a solute mass balance.',
    }
    return ParticleResult(paths, timepoints, endpoints, releases,
                          crossing_arrivals(paths, config), metrics, warnings)


def arrival_summary(result, config, observations=None):
    """Summary and per-particle data for observation-cell x-plane apertures.

    Passing new observation coordinates recomputes crossings without rerunning
    MODPATH. Weighted median is conditional on particles that have crossed by
    the end of the simulation. A zero crossed fraction is not zero MT3D
    concentration: dispersed solute can reach apertures that no advective path
    intersects.
    """
    from dataclasses import replace
    c = replace(config, observations=list(observations)) if observations is not None else config
    arrivals = crossing_arrivals(result.paths, c)
    source_mass = float(result.releases.weight_g.sum())
    rows = []
    for p, (x, y, z) in enumerate(c.observations, 1):
        inside = _observation_inside(c, x, y, z)
        if inside:
            layer, row, _ = c.cell(x, y, z)
            aperture_y = c.width - (row + 0.5) * c.dy
            aperture_z = c.thickness - (layer + 0.5) * c.dz
        else:
            aperture_y = aperture_z = np.nan
        subset = arrivals.loc[(arrivals.observation == p) & arrivals.within_observation_cell].sort_values('time')
        weight = float(subset.weight_g.sum()) if inside else np.nan
        if len(subset):
            cumulative = subset.weight_g.cumsum().to_numpy()
            middle = min(len(subset)-1, int(np.searchsorted(cumulative, weight / 2)))
            median = float(subset.time.iloc[middle])
            first, last = float(subset.time.min()), float(subset.time.max())
        else:
            median = first = last = np.nan
        rows.append({'Point': f'P{p}',
                     'Status': ('Crossing recorded' if len(subset) else 'No crossing by end') if inside else 'Outside stored model domain',
                     'Plane x (m)': x, 'Requested y (m)': y,
                     'Requested z (m)': z,
                     'Aperture centre y (m)': aperture_y, 'Aperture centre z (m)': aperture_z,
                     'Particles crossed': len(subset) if inside else np.nan,
                     'Represented mass crossed (g)': weight,
                     'Fraction of total release (%)': 100*weight/source_mass if source_mass else np.nan,
                     'First crossing (d)': first, 'Weighted median crossing (d)': median,
                     'Last crossing (d)': last})
    return pd.DataFrame(rows), arrivals
