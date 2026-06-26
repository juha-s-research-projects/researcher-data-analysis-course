# The one command on Windows. Mirrors run.sh: fetch the raw data, load it,
# clean it, run the analysis — rebuilding every figure and table in outputs/
# from the untouched raw files. Re-run it after any change.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

uv run src/00_fetch.py;    if ($LASTEXITCODE) { exit $LASTEXITCODE }  # raw -> data/raw/ (skips if present)
uv run src/01_load_raw.py; if ($LASTEXITCODE) { exit $LASTEXITCODE }  # messy files -> *_raw tables
uv run src/02_clean.py;    if ($LASTEXITCODE) { exit $LASTEXITCODE }  # tidy tables + analysis panel
uv run src/03_analysis.py; if ($LASTEXITCODE) { exit $LASTEXITCODE }  # regressions -> outputs/

# To sync outputs to an Overleaf paper, add a `git -C paper push overleaf main`
# here — see the manuscript-pipeline chapter.
