"""
Shared third-party imports and global matplotlib style.
"""

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

# colour-blind-friendly defaults
plt.rcParams["image.cmap"] = "cividis"
plt.rcParams["figure.dpi"]  = 120