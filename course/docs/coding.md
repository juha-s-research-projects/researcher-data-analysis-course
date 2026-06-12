<!-- SCAFFOLD — ideas/topics only. Author writes these bullets into prose.
Per-module shape: Concept → Why it bites (failure story) → What we
recommend (one opinionated answer) → A taste (short example) → Go deeper.
This is the keystone chapter — it has the most decided detail (the pinned-
environment principle + the layered fallback table). -->

# Coding

This is not a programming tutorial. We will just go over the minimum, most impactful software engineering tips that will make your life easier when making research pipelines.
There are four non-negotiable habits and the environment, when writing your own pipelines.

## Scripts over clicks

If there is something that toucheds data, it should be a script, and it should be able to run from start to finish and not be some kind of clicks in some kind of graphical interface.
Any manual steps are places where you risk making errors. Humans are clumsy. Knowing later on what exact manual steps were taken with what settings is probably impossible.
This is why every transformation is in code, which leaves documentation / a trace for afterward.
Ideally you should also have one entrypoint to your pipeline, like [architecture](architecture.md)'s `run.sh`. 

## Determinism

Same inputs should lead to the same outputs, each and every time, on all machines.
There are two threats to this, the first one is randomness without a seed. Randomness can occur in sampling, shuffling, bootstrapping, training, etc. and should always have a fixed seed. This way you also know what results change due to code changes, and what results change due to data / methodology.
Another threat to determinism is any kind of hidden state. Many notebooks might have the ability to run cells out of order, or keep a variable in memory from an earlier experiment, breaking determinism.

You should always have scripts for any kind of pipeline. A notebook is fine for exploration, as a scratchpad. For the serious analysis, it should happen as a script in a more disciplined fashion.

## Use variables to your advantage

Instead of having `df[df.score > 0.85]`, it is way clearer to have `INCLUSION_THRESHOLD = 0.85  # pre-registered cutoff, see protocol §3`, and later `df[df.score > INCLUSION_THRESHOLD]`.
Future you and other people will read the code and instantly understand what the point is.

## Pin the environment, and it will work on any machine

If you just send your code to somebody else without the environment configuration, it might be quite difficult for somebody else to get it to run like it ran for you. They might have a different Python version, different package version, and you might have had a dependency you installed on your whole system several years ago without remembering.

You should:
1. Declare any dependencies that the project needs **explicitly**, in a requirements file for example
2. Lock the dependencies to exact versions, saying `pandas==3.0.3` instead of `pandas` (which will result in the newest mainstream release to be installed)
3. Pin the language version (Python interpreter, R, Julia)
4. Isolate the environment: each project has its own environment and dependencies. This way two projects can have different versions of e.g. pandas without conflict.

The tool I recommend is `uv`. It does everything in one tool.
You declare dependencies in `pyproject.toml`, it writes an `uv.lock`, pins the interpreter via `.python-version` and isolates in a per-project `.venv`.
This version manager is intended to be used with Python.
uv is easy to switch to pip, another very used tool, as both understand the same kind of `pyproject.toml` files. This again is a standard you will benefit from learning.

You should also, whenever possible, pick one language for your project. This makes any environment simpler and easier to maintain.
The four principles stay the same in different languages, but the tools might change.

| Situation | Recommended tool |
|---|---|
| Python project | **uv** |
| R project | renv (+ rig to pin the R version) |
| Mixed-language / heavy native deps / CUDA userspace | Pixi (conda-forge) |
| Stata | no env manager — pin the Stata version, vendor the `.ado` files, script everything in `.do` |
| Bit-for-bit reproducibility across anything (incl. proprietary) | a container (Docker) |

## Small example of using an environment manager

```bash
# declare + lock + pin + isolate, in four commands
uv init
uv add pandas statsmodels matplotlib          # declares + locks (SQLite is stdlib)
uv run src/01_load_raw.py                      # runs inside the pinned env
```

=== "macOS / Linux"

    ```bash
    # run.sh — the one command (sketch)
    #!/usr/bin/env bash
    set -euo pipefail
    uv run src/01_load_raw.py
    uv run src/02_clean.py
    uv run src/03_analysis.py
    ```

=== "Windows"

    ```powershell
    # run.ps1 — the one command (sketch)
    $ErrorActionPreference = "Stop"
    uv run src/01_load_raw.py
    uv run src/02_clean.py
    uv run src/03_analysis.py
    ```
