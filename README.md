# Reproducible CMIP6 Effective Radiative Forcing Analysis

## Scientific context
CMIP6 multi-model experiments provide estimates of Effective Radiative Forcing (ERF) from various anthropogenic drivers.  
Understanding ERF variability is key to constraining climate sensitivity.

## Internship objectives
1. **Ingest** raw CMIP6 NetCDF outputs (`ERF_EMI_DMS`, `siconc`, …).  
2. **Compute** regional and global ERF statistics.  
3. **Visualise** spatial patterns and temporal trends with colour-blind-safe maps.  
4. **Publish** fully reproducible code, data-retrieval instructions, and archived outputs.

## Quick-start (reproduction instructions)
```bash
# 1️⃣ Clone & create env
git clone <REPO_URL>
cd cmip6-analysis
mamba env create -f environment.yml
mamba activate cmip6-analysis

# 2️⃣ Download data (~2 GB)
python src/load_data.py --download-full  # ESGF credentials required

# 3️⃣ Run the notebook
jupyter lab notebooks/CMIP6_14May.ipynb

## Contributors
| Role | Name | ORCID | Contribution |
|------|------|-------|--------------|
| Lead developer | **<YOUR NAME>** | <ORCID> | Conceptualisation, coding, data analysis, visualisation, writing |
| Scientific supervisor | **<SUPERVISOR NAME>** | <ORCID> | Methodology review, climate-science guidance |
| Internship mentor | **<MENTOR NAME>** | <ORCID> | Project framing, feedback on narrative |
| IT / ESGF support | **<SYSADMIN NAME>** | – | Infrastructure, data-transfer troubleshooting |

_Contributions follow the [all-contributors](https://allcontributors.org/) specification.  
Open a PR to add yourself if you’ve helped!_

---

## Material

This repository ships everything needed to **reproduce** the CMIP6 ERF analysis:

1. **`notebooks/`** – executable Jupyter notebooks with clear objectives, narrative, captions and conclusions.  
2. **`src/`** – reusable Python package (`load_cmip6`, `plot_global_map`, `compute_erf_statistics`, …) with full doc-strings.  
3. **`docs/`** –  
   * `DATA.md`: input/output dataset catalogue, download instructions, licences, preservation plan.  
   * this README.  
4. **`environment.yml`** – pinned Conda environment (Python 3.11, xarray 2024.5 +, etc.).  
5. **`tests/`** – `pytest`/`nbval` smoke test that runs the main notebook in mock-data mode.  
6. **`.zenodo.json` + `CHANGELOG.md`** – metadata for long-term archiving and version history.  
7. **`data/`** – folder created on first download; remains empty in the repo to keep size small.

---

## Licence

| Scope | Licence | File(s) | Terms |
|-------|---------|---------|-------|
| **Source code & notebooks** | **MIT** | Entire repo (see `LICENSE`) | Permissive: free use, modification & distribution with attribution. |
| **Generated output data & figures** | **CC-BY-4.0** | NetCDFs in `data/processed/`, PNG/SVG plots | Share-alike not required; attribution to this repo. |
| **Upstream CMIP6 input NetCDFs** | CMIP6 Terms of Use | Downloaded via ESGF (`load_data.py --download-full`) | Free for non-commercial research; cite original modelling centres. |

By cloning, using or contributing to this project you agree to abide by these licences.  
If you need a different licensing arrangement, open an issue to discuss before using the material commercially.
