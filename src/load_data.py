"""
Helpers to open CMIP6 NetCDF files, with an optional mock mode for testing.

Functions
---------
load_cmip6(var, experiment, *, mock=False)
    Return an ``xarray.Dataset`` for the requested variable/experiment.
    If ``mock=True`` (or env-var ``CMIP6_MOCK=1``) it returns a tiny synthetic
    2-timestep dataset so tests run fast and offline.

load_all_data(models=None, cases=None, variables=None, *, mock=False)
    Convenience wrapper that builds the big nested dict
    model → case → variable → DataArray/Dataset.

download_full()
    (Optional) Download every entry in ``DATASETS`` via ESGF ``clef``.
"""

from __future__ import annotations

import os
import pathlib
import subprocess
from typing import Final

import numpy as np
import xarray as xr

# ---------------------------------------------------------------------
# 1.  Where the raw files live
# ---------------------------------------------------------------------
ROOT: Final = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"        # put / symlink your NetCDFs here
RAW.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------
# 2.  Map (variable, experiment) → filename  *EDIT these paths as needed!*
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# 2.  Map (variable, experiment) → filename  (mmrso4 only)
# ---------------------------------------------------------------------
DATASETS: Final = {
    # 2×DMS experiment
    ("mmrso4", "piClim-2xDMS_NorESM"):
        "mmrso4_AERmon_NorESM2-LM_piClim-2xDMS_r1i1p1f1_gn_000101-001012.nc",

    # control experiment
    ("mmrso4", "piClim-control_NorESM"):
        "mmrso4_AERmon_NorESM2-LM_piClim-control_r1i1p1f1_gn_000101-001012.nc",
}
#-------------------------------------------------------------------
# 3.  Helper for *mock* data (CI / quick tests)
# ---------------------------------------------------------------------
def _mock_ds(var: str) -> xr.Dataset:
    time = np.arange("2000-01", "2000-03", dtype="datetime64[M]")
    data = np.random.rand(len(time), 2, 2)
    return xr.Dataset(
        {var: (("time", "lat", "lon"), data)},
        coords={"time": time, "lat": [0, 1], "lon": [0, 1]},
        attrs={
            "title": f"Mock {var}",
            "author": "<YOUR NAME>",
            "creation_date": np.datetime_as_string(np.datetime64("now")),
        },
    )

# ---------------------------------------------------------------------
# 4.  Public API
# ---------------------------------------------------------------------
def load_cmip6(
    var: str,
    experiment: str,
    *,
    mock: bool | None = None,
) -> xr.Dataset:
    """Open a local NetCDF file or return a tiny mock dataset."""
    mock = mock or os.getenv("CMIP6_MOCK") == "1"
    if mock:
        return _mock_ds(var)

    try:
        filename = DATASETS[(var, experiment)]
    except KeyError:  # helpful message
        raise KeyError(
            f"({var!r}, {experiment!r}) not found in DATASETS – "
            "edit src/load_data.py to add its filename."
        ) from None

    path = RAW / filename
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found – put the NetCDF in data/raw/ or update DATASETS."
        )

    return xr.open_dataset(path)


def load_all_data(
    models=None,
    cases=None,
    variables=None,
    *,
    mock=False,
):
    """Return nested dict  model → case → variable → Dataset."""
    models = models or [
        "UKESM1-0-LL",
        "NorESM2-LM",
        "GISS-E2-1-G",
        "EC-Earth3-AerChem",
    ]
    cases = cases or ["piClim-2xDMS", "piClim-control"]
    variables = variables or ["rlut", "rsut", "rsdt", "siconc", "mmrso4", "emidms"]

    return {
        m: {
            c: {v: load_cmip6(v, c, mock=mock) for v in variables}
            for c in cases
        }
        for m in models
    }


def download_full() -> None:  # pragma: no cover
    """Example ESGF downloader – fill DATASETS with clef queries if you prefer."""
    for (var, exp), query in DATASETS.items():
        if query.startswith("cmip6 "):  # treat as clef command
            print(f"Downloading {var}/{exp} …")
            subprocess.run(["clef", *query.split()[1:]], check=True, cwd=RAW)
