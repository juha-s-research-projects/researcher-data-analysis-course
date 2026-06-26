#!/usr/bin/env bash
# The one command: fetch the raw data, load it, clean it, run the analysis.
# Re-run this after any change — new data, or a reviewer's tweak to 02_clean.py —
# and every figure and table in outputs/ is rebuilt from the untouched raw files.
set -euo pipefail
cd "$(dirname "$0")"

uv run src/00_fetch.py      # raw data -> data/raw/ (idempotent; skips if present)
uv run src/01_load_raw.py   # messy files -> *_raw tables in the database
uv run src/02_clean.py      # tidy tables + the analysis panel
uv run src/03_analysis.py   # regressions -> outputs/tables/, outputs/figures/

# To sync the fresh figures and tables to an Overleaf paper, add a
# `git -C paper push overleaf main` here — see the manuscript-pipeline chapter.
