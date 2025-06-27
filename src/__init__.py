"""
Top-level package for CMIP6 ERF analysis.

Convenience imports let you do:

    from src import load_cmip6, plot_global_map, compute_erf_statistics
"""

from .load_data import load_cmip6                  # noqa: F401
from .plot_data_maps import plot_global_map        # noqa: F401
from .analyze_erf_emidms_siconc import (
    compute_erf_statistics,                        # noqa: F401
)