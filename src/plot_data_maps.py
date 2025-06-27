"""
Plot helpers: colour-blind friendly, consistent styling.
"""

from pathlib import Path
from typing import Any

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import xarray as xr


# ──────────────────────────────────────────────────────────────────────
def _plot_single(
    da: xr.DataArray,
    *,
    vmin: float | None,
    vmax: float | None,
    title: str,
    region_name: str,
    cmap: str,
    save_dir: Path | None,
) -> None:
    """Draw a latitude profile (if no lon) or a map (Robinson / polar)."""

    # build a nice label:  <var> (units)
    units = da.attrs.get("units", "kg kg⁻¹")
    var   = da.name or "mmrso4"
    label = f"{var} ({units})" if units else var

    # ── 1-D latitude profile ─────────────────────────────────────────
    if "lon" not in da.dims:
        fig, ax = plt.subplots(figsize=(9, 4.5))
        da.squeeze().plot(ax=ax)
        ax.set_xlabel("Latitude (°)")
        ax.set_ylabel(label)
        ax.set_title(title)
        fig.tight_layout()
        if save_dir:
            save_dir.mkdir(parents=True, exist_ok=True)
            fname = title.replace(" ", "_") + ".png"
            plt.savefig(save_dir / fname, dpi=150, bbox_inches="tight")
            plt.close(); print(f"✔ saved {fname}")
        return

    # ── 2-D lat×lon map ─────────────────────────────────────────────
    extra = [d for d in da.dims if d not in ("lat", "lon")]
    if extra:
        da = da.mean(extra)

    # choose projection
    if region_name.lower().startswith("arctic"):
        proj, extent = ccrs.NorthPolarStereo(), (-180, 180, 60, 90)
    elif region_name.lower().startswith("antarctic"):
        proj, extent = ccrs.SouthPolarStereo(), (-180, 180, -90, -60)
    else:
        proj, extent = ccrs.Robinson(), None

    fig = plt.figure(figsize=(9, 4.5))
    ax = plt.axes(projection=proj)
    da.plot.pcolormesh(
        ax=ax,
        transform=ccrs.PlateCarree(),
        vmin=vmin, vmax=vmax,
        cmap=cmap,
        cbar_kwargs={"label": label},
    )
    ax.coastlines()
    if extent: ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.set_title(title)
    fig.tight_layout()
    if save_dir:
        save_dir.mkdir(parents=True, exist_ok=True)
        fname = title.replace(" ", "_").replace("•", "_") + ".png"
        plt.savefig(save_dir / fname, dpi=150, bbox_inches="tight")
        plt.close(); print(f"✔ saved {fname}")


# ──────────────────────────────────────────────────────────────────────
def plot_global_map(
    obj: Any,
    *,
    vmin: float | None = None,
    vmax: float | None = None,
    title: str = "",
    cmap: str = "cividis",
    save_dir: str | Path | None = None,
) -> None:
    """
    Plot every DataArray inside *obj* (nested dict or single DA).

    If *save_dir* is given, PNG files are written there; otherwise plots
    appear inline in the notebook.
    """
    save_path = Path(save_dir) if save_dir else None

    if isinstance(obj, xr.DataArray):          # single slice
        _plot_single(
            obj, vmin=vmin, vmax=vmax,
            title=title or obj.name or "map",
            region_name=title or "Unknown",
            cmap=cmap, save_dir=save_path,
        )
        return

    if isinstance(obj, dict):                  # nested {model→exp→region}
        for model, exps in obj.items():
            for exp, regions in exps.items():
                for region, da in regions.items():
                    auto_title = f"{model} • {exp} • {region}"
                    _plot_single(
                        da, vmin=vmin, vmax=vmax,
                        title=auto_title, region_name=region,
                        cmap=cmap, save_dir=save_path,
                    )
        return

    raise TypeError(
        "plot_global_map expects an xarray.DataArray or the nested dict "
        "produced by the analysis functions."
    )
