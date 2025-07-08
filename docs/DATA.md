## Input & Output Data

| Variable | Source experiment | ESGF DRS / local filename (example) | DOI / URL |
|----------|------------------|-------------------------------------|-----------|
| `mmrso4` | **piClim-2xDMS** (NorESM2-LM) | `mmrso4_AERmon_NorESM2-LM_piClim-2xDMS_r1i1p1f1_gn_000101-001012.nc` | <ESGF record / DOI> |
| `mmrso4` | **piClim-control** (NorESM2-LM) | `mmrso4_AERmon_NorESM2-LM_piClim-control_r1i1p1f1_gn_000101-001012.nc` | <ESGF record / DOI> |

_All original NetCDFs are distributed under the **CMIP6 Terms of Use** (free for non-commercial research)._

---

### Retrieval (using **clef**)

```bash
# install & authenticate once
pip install clef
clef --login

# download the two files shown above
clef cmip6 \
     --variable mmrso4 \
     --source-id NorESM2-LM \
     --experiment-id piClim-2xDMS \
     --table-id AERmon \
     --grid gn \
     --latest

clef cmip6 \
     --variable mmrso4 \
     --source-id NorESM2-LM \
     --experiment-id piClim-control \
     --table-id AERmon \
     --grid gn \
     --latest
