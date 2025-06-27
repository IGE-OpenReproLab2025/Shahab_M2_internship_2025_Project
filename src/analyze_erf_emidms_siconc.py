from src.common_imports import *          # xarray, numpy, etc.
import numpy as np
import xarray as xr
def analyze_mmrso4(model_data, time_slice=(None, None)):
    """
    Return area-weighted mean surface mmrso4 [kg kg⁻¹] for
    Global / Arctic / Antarctic.
    """
    regions = {"Global": (-90, 90), "Arctic": (66, 90), "Antarctic": (-90, -66)}
    mmrso4_results, mmrso4_data = {}, {}

    for model, mdl in model_data.items():
        mmrso4_results[model], mmrso4_data[model] = {}, {}

        for exp in ("control", "2xDMS"):
            if exp not in mdl:
                continue

            so4 = mdl[exp]["mmrso4"]          # ← was Dataset

            # ── NEW ────────────────────────────────────────────────
            # if it’s still a Dataset, pull out *only* 'mmrso4'
            if isinstance(so4, xr.Dataset):
                so4 = (
                    so4["mmrso4"]
                    if "mmrso4" in so4.data_vars
                    else so4.to_array().sel(variable="mmrso4")
                )
            # ───────────────────────────────────────────────────────

            if "lev" in so4.dims:                         # surface level
                so4 = so4.isel(lev=0).drop_vars("lev")

            if time_slice is not None and "time" in so4.dims:
                so4 = so4.isel(time=slice(*time_slice))
            so4 = so4.mean("time") if "time" in so4.dims else so4

            mmrso4_results[model][exp] = {}
            mmrso4_data[model][exp] = {}

            for reg, (lat0, lat1) in regions.items():
                band = so4.where((so4.lat >= lat0) & (so4.lat <= lat1), drop=True)
                mmrso4_data[model][exp][reg] = band

                # area weighting
                zon = band.mean("lon") if "lon" in band.dims else band
                w   = np.cos(np.deg2rad(zon.lat))
                mu  = zon.weighted(w).mean("lat", skipna=True)

                if {"bnds", "variable"} & set(mu.dims):
                    mu = mu.mean(("bnds", "variable"), skipna=True)

                mmrso4_results[model][exp][reg] = mu.item()

    return mmrso4_results, mmrso4_data





def print_results(results, label="ERF", unit="W/m²", precision=20, auto_prefix=False):
    """
    Print results for each model and experiment, optionally auto-scaling to an SI prefix.

    Parameters
    ----------
    results : dict
        Either {model: {region: value}} or {model: {experiment: {region: value}}}
    label : str
        Name of the variable (e.g. "ERF")
    unit : str
        Physical unit string (e.g. "W/m²")
    precision : int
        Number of decimal places in the mantissa
    auto_prefix : bool
        If True, automatically choose an SI prefix (n, µ, m, k, etc.)
    """
    import math

    # ——— embedded SI table ———
    si = {
        -24: "y",  # yocto
        -21: "z",  # zepto
        -18: "a",  # atto
        -15: "f",  # femto
        -12: "p",  # pico
         -9: "n",  # nano
         -6: "µ",  # micro
         -3: "m",  # milli
           0: "",   # (none)
          3: "k",  # kilo
          6: "M",  # mega
          9: "G",  # giga
         12: "T",  # tera
         15: "P",  # peta
         18: "E",  # exa
         21: "Z",  # zetta
         24: "Y",  # yotta
    }

    # decide scaling
    if auto_prefix:
        # gather all finite values
        vals = []
        for mdl, exps in results.items():
            if any(isinstance(v, dict) for v in exps.values()):
                for rd in exps.values():
                    vals += [v for v in rd.values() if math.isfinite(v)]
            else:
                vals += [v for v in exps.values() if math.isfinite(v)]

        if vals:
            m = max(abs(v) for v in vals)
            exp3 = int(math.floor(math.log10(m)/3)*3) if m>0 else 0
            # snap to nearest available exponent
            choices = sorted(si)
            exp3 = min(choices, key=lambda e: abs(e - exp3))
        else:
            exp3 = 0

        prefix = si[exp3]
        scale  = 10.0**(-exp3)
        unit   = f"{prefix}{unit}"
    else:
        scale = 1.0

    # printing
    for mdl, exps in results.items():
        print(f"\nModel: {mdl}")
        # nested? experiments→regions
        if isinstance(exps, dict) and any(isinstance(v, dict) for v in exps.values()):
            for exp_name, rd in exps.items():
                print(f"  Experiment: {exp_name}")
                for region, val in rd.items():
                    v = val * scale
                    print(f"    {region} {label}: {v:.{precision}e} {unit}")
        else:
            # flat: regions only
            for region, val in exps.items():
                v = val * scale
                print(f"  {region} {label}: {v:.{precision}e} {unit}")
def compute_erf_statistics(erf: xr.DataArray, siconc: xr.DataArray) -> xr.Dataset:
    """Return mean ERF per 10 % sea-ice-concentration bin."""
    bins = list(range(0, 110, 10))
    cat = xr.cut(siconc, bins, labels=bins[:-1])
    grouped = erf.groupby(cat).mean(dim=("lat", "lon"))
    grouped = grouped.rename({"siconc_bin": "siconc_pct"})
    grouped.attrs["units"] = erf.attrs.get("units", "")
    return grouped.to_dataset(name="ERF_mean")