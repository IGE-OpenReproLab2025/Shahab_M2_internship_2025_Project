import importlib
import pathlib
import sys

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

# Add project root to PYTHONPATH
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

NOTEBOOK = pathlib.Path(__file__).parents[1] / "notebooks" / "CMIP6_14May.ipynb"


def test_notebook_runs(tmp_path):
    """Execute the notebook in mock-data mode and assert error-free run."""
    # Set env var so load_data.py returns synthetic data
    import os

    os.environ["CMIP6_MOCK"] = "1"

    nb = nbformat.read(NOTEBOOK, as_version=4)
    ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
    ep.preprocess(nb, {"metadata": {"path": NOTEBOOK.parent}})