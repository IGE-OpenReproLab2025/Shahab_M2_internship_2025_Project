# Input & Output Data

| Variable | Source experiment | ESGF DRS example | DOI / URL |
|----------|------------------|------------------|-----------|
| `ERF_EMI_DMS` | ssp245 | ssp245_AERmon_MPI-ESM1-2-LR_r1i1p1f1_gn_2015-2100.nc | <DOI_1> |
| `siconc` | historical | historical_SImon_CanESM5_r1i1p1f1_gn_1850-2014.nc | <DOI_2> |
| … | … | … | … |

All original NetCDFs are licensed under the **CMIP6 Terms of Use** (free for non-commercial research).

## Retrieval

```bash
pip install clef
clef --login
clef cmip6 --variable ERF_EMI_DMS --experiment ssp245 --latest
