# Researcher data-analysis course

[![deploy-docs](https://github.com/juha-s-research-projects/researcher-data-analysis-course/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/juha-s-research-projects/researcher-data-analysis-course/actions/workflows/deploy-docs.yml)
[![example](https://github.com/juha-s-research-projects/researcher-data-analysis-course/actions/workflows/example-ci.yml/badge.svg)](https://github.com/juha-s-research-projects/researcher-data-analysis-course/actions/workflows/example-ci.yml)

An opinionated guide to the few software-engineering and data-management habits
that decide whether research survives review, replication, and future-you. It is
written for researchers, not computer scientists — the payload is judgment, not
syntax.

**The course is published here: <https://juha-s-research-projects.github.io/researcher-data-analysis-course/>**

That is the intended way to read it. The rest of this repo is the source.

## What's in the repo

```text
course/              # the course itself (Markdown), built with Zensical
  docs/              #   one Markdown file per chapter
  zensical.toml      #   site config + navigation
examples/
  phd-project/       # the worked running example the chapters quote from
  storage-benchmark/ # the CSV/Parquet/SQLite/Excel benchmark behind the storage chapter
```

## Build the course locally

You need Python and [uv](https://docs.astral.sh/uv/) (or any pip).

```bash
pip install -r reqs.txt    # installs Zensical
cd course
zensical serve             # live preview at http://127.0.0.1:8000
zensical build             # or render the static site into course/site/
```

Pushing to `master` rebuilds and redeploys the published site automatically
(`.github/workflows/deploy-docs.yml`).

## Run the worked example

See [`examples/phd-project/README.md`](examples/phd-project/README.md). It
reproduces an empirical-finance study (industry betas) from immutable raw data
with one command, and is smoke-tested on Linux, macOS and Windows on every
change (`.github/workflows/example-ci.yml`).
