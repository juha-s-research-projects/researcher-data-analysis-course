# Motivation

This material is a small documentation for what to do when researching and what not to do.
It is essentially an opinionated guide on the few software engineering concepts that one should use when doing research in some other field.
The material will not teach you to code or python syntax, but it will include concepts that will help you in your workflows - sometimes this is coding related.

These concepts matter, because they will make your research:

- reproducible,
- easily extendable and shareable,
- easier to understand,
- and more.

Along the way, we will have a small toy example illustrating what we are doing and actually shipping it, so that you can examine the example and learn from it.

## Motivating example

Imagine this. You have been working really hard on your research project for maybe a year, and finally, you figure out what was missing and find interesting results. Your project is contained in one folder, with the following structure:

```text
PhD project/
├── data.xlsx
├── data (1).xlsx
├── data_new.xlsx
├── data_new_USE THIS.xlsx
├── Copy of data_new_USE THIS.xlsx
├── ~$data_new_USE THIS.xlsx
├── final data.csv
├── final_data_v2.csv
├── final_data_v2 (cleaned).csv
├── results.csv
├── results_2.csv
├── results_2_FIXED.csv
├── analysis.xlsx
├── analysis_version-1.xlsx
├── analysis_version-2-final.xlsx
├── analysis_version-2-final-FINAL.xlsx
├── analysis_version-2-final-FINAL (1).xlsx
├── analysis_version-2-final-FINAL_use-this-one.xlsx
├── Untitled spreadsheet.xlsx
├── Book1.xlsx
├── notes.docx
├── notes_old.docx
├── thesis_draft.docx
├── thesis_draft_final.docx
├── thesis_draft_final_comments_AB.docx
├── Figure1.png
├── Figure1_new.png
├── Figure1_new_bigger font.png
├── graph.png
├── graph2.png
├── graph_final.png
├── chart (3).jpeg
├── Screenshot 2024-11-03 at 16.42.51.png
├── plot.R
├── plot_old.R
├── script.py
├── script_final.py
├── Untitled.ipynb
├── Untitled1.ipynb
├── 1706911983.pdf
├── paper.pdf
├── paper2.pdf
├── important paper READ.pdf
├── sdarticle.pdf
├── 10.1038_s41586-020-2649-2.pdf
├── refs.docx
├── new folder/
├── new folder (2)/
├── old/
│   ├── data.xlsx
│   ├── data_old.xlsx
│   └── stuff/
├── backup/
│   └── PhD project - Copy/
└── do not delete/
```

Which one is the real dataset? Which figure went into the submitted paper, and which script produced it? You are unsure, but you can figure out if you go through all the files.

Now, you have written up your paper, and you have submitted it for review. After a couple weeks, a reviewer compliments your research, but they ask you to remove a couple outliers and update the figures and all the tables. Sounds pretty horrible, but this might be possible if you just put enough time into it, which you will do. You will have to be careful though, not to delete anything important, and it will take lots of cognitive capacity to follow the full path from removing the two outliers from calculations to inputting all plots and updating all numbers in a table. But you finally manage to do it, until, researcher 3 asks to add another control variable a week later. Again, tons of work. Your pipeline does not support adding one more variable to the important regressions without essentially going through everything again from the ground up.

Is there a better way?

## The better way

The same project, structured so that one command rebuilds everything from the
immutable raw data — and a reviewer's "remove two outliers" is a one-line change,
not a week of manual surgery:

```text
phd-project/
├── README.md                  # what this is, how to run it, in 10 lines
├── pyproject.toml             # declared dependencies + project metadata
├── uv.lock                    # exact, fully pinned dependency graph
├── .python-version            # pinned interpreter (e.g. 3.13)
├── .gitignore                 # ignores the venv, caches, build artefacts
├── run.sh                     # ONE command: env → db → analysis → outputs
│
├── data/
│   ├── raw/                   # immutable, read-only, NEVER hand-edited
│   │   └── survey_2024.csv    #   (the only true source of data)
│   └── project.sqlite         # single-file database: clean + derived tables
│
├── src/
│   ├── 00_fetch.py            # download the raw data → data/raw/, then freeze it
│   ├── 01_load_raw.py         # data/raw/*  →  project.sqlite
│   ├── 02_clean.py            # cleaning steps, in code, reproducible
│   └── 03_analysis.py         # regressions → writes tables + figures
│
├── outputs/                   # 100% generated, safe to delete & rebuild
│   ├── figures/
│   │   └── fig1_effect.pdf
│   └── tables/
│       └── tab1_summary.tex   # \input-able LaTeX, no hand-typed numbers
│
├── paper/                     # git-synced to Overleaf
│   ├── main.tex
│   ├── references.bib         # auto-exported by Zotero (Better BibTeX)
│   ├── figures/               # written here from outputs/ by run.sh
│   │   └── fig1_effect.pdf
│   └── tables/
│       └── tab1_summary.tex
│
├── references/                # PDFs + notes + tags, managed by Zotero
│
└── .git/                      # full history: every change, every version
```

You can notice, that the structure is now clear to anybody opening the directory for the first time. You will get some feeling of that "first time" when you open your project 10 years later. Here, raw data is always immutable. We have data in a relational format, where we can programmatically run queries, instead of having a sprawl of CSV files. When the reviewer asks to remove a couple observations, we edit the script `02_clean.py` to change which data points are in the analysis. Running everything again with new data means running `run.sh` once, and at this moment it imports the data, cleans it, runs all the analysis. Then, it writes all the figures, so that they are fresh, as well as the tables in `outputs/tables/`. Thanks to `git push` in the `run.sh`, the tables and figures have changes synced to Overleaf. Thus getting the new tables will be a matter of recompiling the LaTeX document, and downloading the new PDF. Sounds better, right? Also, thanks to Git, we do not need  `analysis_version-2-final-FINAL.xlsx`, but instead version history is managed by Git, and if we wish to go back to an old version, it is easy to do. All of these factors make you more productive, less stressed, and less prone to losing data or hard work.
