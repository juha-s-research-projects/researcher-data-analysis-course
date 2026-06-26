# Industry betas — do industries move with the market?

Reproduces the figure and table from immutable raw data with one command. For
each of 10 industries we regress its excess return on the market factor (its
*beta*), controlling for NBER recessions.

## Run

```bash
./run.sh      # macOS / Linux
.\run.ps1     # Windows (PowerShell)
```

It fetches the raw data, loads it, cleans it, and runs the analysis:

```text
src/00_fetch.py     # download raw data → data/raw/, then freeze it read-only
src/01_load_raw.py  # carve the messy files into *_raw tables in the database
src/02_clean.py     # tidy: percent→decimal, ISO dates, missing codes → NULL, one panel
src/03_analysis.py  # one regression per industry → outputs/
```

## Needs

[uv](https://docs.astral.sh/uv/) (it pins Python and the packages for you).
Everything else — including SQLite — comes with Python.

Outputs land in `outputs/`:

- `outputs/tables/industry_betas.tex` — the results table, ready to `\input`
- `outputs/figures/industry_betas.pdf` — betas as a bar chart

The clean data lives in `data/project.sqlite`; the analysis panel is its `panel`
table. Run `python verify.py` after the pipeline to check the database invariants.

## Where the data comes from

`data/raw/` is fetched by `00_fetch.py`, never committed (it derives from
restricted CRSP data), and frozen read-only — it is immutable evidence.

| file | source | obtained | how | terms |
|---|---|---|---|---|
| `F-F_Research_Data_Factors.csv` | Kenneth R. French Data Library, Dartmouth | by `00_fetch.py` | download | free for research use; built from CRSP, not redistributed |
| `10_Industry_Portfolios.csv` | Kenneth R. French Data Library, Dartmouth | by `00_fetch.py` | download | free for research use; built from CRSP, not redistributed |
| `USREC.csv` | NBER recession indicator via FRED (St. Louis Fed) | by `00_fetch.py` | download | public domain |

## The panel (codebook)

One row per industry-month in the `panel` table.

| column | meaning | units | notes |
|---|---|---|---|
| `month` | first day of the month | ISO `YYYY-MM-01` text | SQLite has no date type; ISO text sorts correctly |
| `industry` | one of the 10 industry portfolios | name | e.g. `Manuf`, `HiTec` |
| `ret` | value-weighted monthly return | decimal | `NULL` where the source had a `-99.99`/`-999` missing code |
| `mkt_rf` | market excess return (factor) | decimal | from the Fama-French factors |
| `smb`, `hml` | size and value factors | decimal | carried along; not used by the toy regression |
| `rf` | risk-free rate | decimal | monthly |
| `recession` | NBER recession that month | 0 or 1 | 1 = recession |
