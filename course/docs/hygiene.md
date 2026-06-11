# Data hygiene

When you download data from different sources and harmonize them to fit the whole analysis, there are loads of choices to make.
Different data have different decimal conventions, different ways of indicating missing values (like Null, -1 or N/A), different date formats, different column names and, unfortunately, plenty more.
Picture this: you begin by downloading the data and opening it in your favourite spreadsheet software.
There, you drop a couple of outliers, deal with the missing values and rename columns.
When you are done, you export it to a .csv file somewhere else, and forget about the original copy or the steps needed to get to this cleaned version.
Now it's time for the fun part of researching: tinkering with your analysis.
After half a year of hard work, your analysis has come to fruition and led to a nice paper.

You are happy as you prepare to submit it, but your co-author still wants to do a double-check on everything before the final submission.
As you did the harmonization manually, your co-author also has to do it manually, which she is not too excited to do, given that you have not documented the exact process.
She wants to know what happened to those few outliers and the missing values, but reconstructing what you actually did takes a long time, if you can manage it at all.
Your only memory is that you dropped a couple of outliers and did the harmonization by hand to make things line up.
Unfortunately, this will lead to some frustration and time spent on tedious and stressful work instead of doing something you deem either more useful or more enjoyable.

To avoid something like this becoming reality, you should follow the data hygiene rules detailed in this chapter.
In the architecture chapter, we talked about the shape of the project, like file structure and how data flows, but this chapter will be about the data itself, structuring it so that it is usable, trustworthy, and stable.
We have two halves in this chapter: we first protect the raw data, and only then do we transform a copy of the data so that it is usable for our own analysis.
The later chapters, like the one on storage, assume this has been done.
Without the steps detailed here, you will hit problems downstream that are annoying to debug.

Notice that this time the enemy is not a messy folder, but rather that the entire cleaning process was done by your hands and lives only in your memory - human memory is unreliable and human hands make mistakes.
This is why it is better to have every cleaning decision live in code, as well as a copy of the raw data, because then *you* can later on rerun everything and understand exactly what was done.


## Raw data is immutable and sacred

The single most important rule in all of this material: **you never edit raw data by hand.**
The raw data is evidence, treat it like you would treat a museum specimen or crime-scene evidence.
The architecture chapter had the principle of data flowing only to one direction: here we talk about how to implement it in your behaviour.

Why this is rule is important and will most definitely bite you back in any larger project:

- Let's say you "just fix something small" directly in the raw CSV. Now in the worst case, there is no true original, and you cannot even re-download the data later on. Future-you will not be able to tell what has changed, when or why. Somebody else could do the fix differently. The change is invisible, unversioned and not documented. There is no chance of somebody else replicating what has been done.
- You open `raw/survey.xlsx` just to quickly have a look. Unfortunately, Excel might auto-convert a date or interpret some variable as a date when it is a numerical value upon startup, or something else. Out of habit, you just click save, and now your raw data is polluted with corruptions that will cause headaches later on.
- Months ago you delete two outliers from the raw file, and forgot about it. An eagle-eyed reviewer asks what they were, but you have no original information left about it anymore.

My recommendation is:

- All files in the raw data directory (i.e. `data/raw`) are **read-only**. On all operating systems you can set the file permissions such, that the data can only be read by other programs. This ensures that on a binary level, the data stays exactly the same as it originally was, and ensures that the files are safe from mistakes in your code, or you opening it with statistical software that does something you don't want it to do.
- All changes to the raw data should be performed on a copy of it, and expressed as a rule in code. This is because the code functions as documentation on what steps were taken and what was exactly done. With version control, all the steps also become versioned over time. You should never open a cell and delete it by hand, but instead writing something like `delete from participants where age > 120`. This is explicit, reversible, reviewable and you can even add a comment into the code for the "why" if it is a bigger decision.


On unix-like systems the previously described steps might look something like this:

- As the last step of acquiring a raw data file, freeze the file. Right after downloading or copying a file into `data/raw`, you should mark it as read-only by writing the following to your terminal:
  ```bash
  chmod a-w data/raw/survey_2024.csv
  ```
  Now the operating system will make sure that it is not overwritten or edited - being safe from a mistake in your code or from statistical software doing things you don't want it to do. The directory is still writeable, so you can add new files. Think of it as a ritual: get the file, freeze it, and maybe document where it came from. This is an extra layer against accidents, and does not take more than a couple seconds to do.

- Any subsequent steps happen then on a *copy* of the file, performed by program code, leaving any raw files as they were when you got them. Here is a small example of how you could remove a couple erraneous outliers:
  ```python
  # src/02_clean.py
  con.execute("""
      DELETE FROM equity_returns WHERE return < -1.0
      """)
  ```
  This code deletes returns from equity returns that are less than -100%.


## Tidy data: one row is one observation

Hadley Wickham writes in his 2014 article *Tidy data*, in Journal of Statistical Software about the principles of tidy data. The core principles are the following: each variable is a column, each observation is one row, and each unit of observation is its own table.
Often data arrives formatted for *humans* instead of for *machines*. This means merged cells, one column per year, meaning conveyed by text color, total rows mixed with data rows, free-text notes alongside the data, multi-row headers. These look nice to the eye, but are unusable for a computer.

The following is an example of before and after, using daily stock returns. 
The messy version is a spreadsheet by a human that combines two categorically different things - metalevel information about each company as well as daily returns, with a derived row for an average.

| Date       | AAPL  | MSFT  | XOM    |
|------------|-------|-------|--------|
| Sector     | Tech  | Tech  | Energy |
| 2023-01-31 | 1.2%  | 0.8%  | -0.5%  |
| 2023-02-28 | -0.7% | 1.1%  | 2.3%   |
| Average    | 0.3%  | 0.9%  | 0.6%   |

This breaks the principles of tidy data on many levels, and is quite messy to read. Even the returns are stored as text ("1.2%") instead of a number format like 0.012 that the computer can do calculations on.

In the following tidy version we split this to two tables. Each column is a dimension of the observation, and adding more observations always means adding more rows. The returns are also in a numeric format, so that we do not need to worry about dealing with strings or percentage conversions later on.

`returns` — one row per stock per day:

| ticker | date       | return |
|--------|------------|--------|
| AAPL   | 2023-01-31 | 0.012  |
| MSFT   | 2023-01-31 | 0.008  |
| XOM    | 2023-01-31 | -0.005 |
| AAPL   | 2023-02-28 | -0.007 |
| MSFT   | 2023-02-28 | 0.011  |
| XOM    | 2023-02-28 | 0.023  |

`securities` — one row per stock (the metadata):

| ticker | company         | sector     |
|--------|-----------------|------------|
| AAPL   | Apple Inc.      | Technology |
| MSFT   | Microsoft Corp. | Technology |
| XOM    | Exxon Mobil     | Energy     |

Now you can still join the two tables on `ticker` if you need both sector and returns information, so we have not lost any functionality with the modification.

I recommend the following:

- Store any data in the tidy format in your database. Everything the computer does, is easier to do with the tidy, long format. Converting data into nice human format tables should happen as the very last step, to present a table of final results for example, but this should never be the format in your data storage.
- You should have only one kind of unit per table, this will keep your tables narrower (and thus faster) as well as make them easier to handle. Instead of having stock meta-level information like currency, headquarters, stock exchange and returns in the same table, just make a returns table with stock id and returns, and another table for any stock metadata you might need for your research. You can join these two tables together when information from both is needed.
- Tidy data is what makes SQL clauses like `GROUP BY`, `JOIN` as well as one liner plotting work easily, and messy data format is a common reason why people fall back to manual work with the spreadsheet.


## Names and values that don't lie and don't drift

You should name your variables descriptively. The name of a variable is a promise of what that variable is, but there are two different modes of failure that can happen

A name that lies: `age` column containing birth years, `income_usd` in thousands or a yes/no field stored as a mix of `Yes` / `y` / `TRUE` / `1`.
A name that drifts: the same concept being `subject_id` in one file, `ID` in the next and participant `participant` in the third. This makes it more difficult to work with the data and adds cognitive overhead.

I recommend you to do the following:

- Pick one naming convention, and stick to it, for example lowercase `snake_case`, no spaces, no special characters, ASCII only (this matters to non-coders as spaces, uppercase and unicodem ight break code, SQL, and filenames.)
- One concept gets one name, everywhere and till the end of the project. If it is the same variable, it has to have the same name.
- You can indicate units with variable names, like `weight_kg` or `returns_usd`.
- You should document and list the exact meaning of variables and their units to your own short documentation to make it easier for others to follow along (including your future-self).

You should also consider values. 
For dates, use `YYYY-MM-DD` always as it sorts correctly as text, and is unambiguous to everybody. 
For country codes you can do something similar: instead of `Finland` / `finland` / `FIN` / `FI` you can stick to one convention, like `FI`/`FR`/`DE`/`CH` (ISO 3166-1 A-2).
For missing data: remember to be intentional about your codes. Blank vs `NA` vs `999` vs `-1` vs `N/A` should not be used interchangeably. Many times you might have missing data due to many different reasons, like "missing" (no response in a survey), "zero" (numerical value of zero) or "not applicable" (the hair colour of a bald person).

## Recap

Remember that

- Raw data is sacred, thus all edits happen on copies, and the raw data is preserved as is. Each step is in code for reproducability as well as so that the steps can be understood later.
- Try to pick conventions for variable names and variable values, document these and follow the tidy principles for your data tables.
- Following these steps makes your work easier to follow, your arguments look more professional as well as more credible, and easier for the whole world to listen to and be interested in.

## Let's continue with our example

- The architecture chapter left us with a scaffolded `phd-project/`: folders, empty pipeline files, a stub `run.sh`, first commits. Now the project gets its actual data.
- The toy study (so the data choices make sense): does an industry's monthly return move with the overall market, and does the relationship change in recessions? Industry portfolio returns regressed on the market factor, recession dummy as a control. We will make the regression in a later chapter, the following example is about giving that a clean starting point.

For our example, we pick three freely available sources that are from different data providers to illustrate the harmonization for real:
    - **Fama-French 3 factors** (monthly) — Kenneth French's data library. The market return we regress on.
    - **10 industry portfolios** (monthly) — same library. The returns we explain.
    - **USREC** — NBER recession indicator via FRED. The control variable.



### Step 0: fetch in code, then freeze

The following examples fetch the files in code. 
This is one way to do it, quite tedious, a more realistic way to do it would be to just go and click download, and diligently document the source upon downloading.
After downloading, crucially also setting the file permissions to read only. Doing this in code has the benefit that the code file functions as the documentation, we do not really need a separate documentation.
When downloading files, the most important thing is that A) you know and document where you got the files from (url and timestamp) and B) you set the files to read only as the first thing after saving them to the desired location.

The below code does all the steps needed. Notice, that we put the raw data folder files to .gitignore: this means they are not tracked by git, and if we link the repo to somebody else, we do not accidentally redistribute the files, as with these files their licence allows free use but not redistribution. We add the script to git anyway. Remember that if you later just share your project folder as a compressed zip, the data in the raw section will be included, and thus you might redistribute the data. Make sure you have a permission to distribute it, or otherwise make sure you know what licence terms you are breaking and the risks you assume doing this.

```python
# src/00_fetch.py  (condensed — full provenance lives in the file's docstring)
SOURCES = {
    # name in data/raw  ->  (kind, url)
    "F-F_Research_Data_Factors.csv": ("zip", "https://mba.tuck.dartmouth.edu/...zip"),
    "10_Industry_Portfolios.csv":    ("zip", "https://mba.tuck.dartmouth.edu/...zip"),
    "USREC.csv":                     ("csv", "https://fred.stlouisfed.org/graph/fredgraph.csv?id=USREC"),
}

READ_ONLY = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH   # r--r--r--

for name, (kind, url) in SOURCES.items():
    dest = RAW / name
    if dest.exists():
        continue                  # already fetched: never re-touch raw
    blob = _download(url)         # (zips are unpacked to the inner csv)
    dest.write_bytes(blob)
    dest.chmod(READ_ONLY)         # freeze: raw is immutable from here on
```

- After one run, the evidence locker looks like this — note the `r--r--r--`:

```text
$ uv run src/00_fetch.py && ls -l data/raw/
-r--r--r--  1 alexis alexis 493812  10_Industry_Portfolios.csv
-r--r--r--  1 alexis alexis  52333  F-F_Research_Data_Factors.csv
-r--r--r--  1 alexis alexis  26777  USREC.csv
```

- And `.gitignore` grows one line (data not redistributable + regenerable from the script — both reasons point the same way):

```gitignore
data/raw/
```

### Now look at what we actually downloaded

<!-- Talking points: this is the chapter's "messy data" section made concrete.
     Every sin below maps to a section above — name the mapping in prose. -->

- These files are formatted for humans reading them on a website, not for machines. The factors file, verbatim:

```text
This file was created using the 202604 CRSP database.
The 1-month TBill rate data until 202405 are from Ibbotson Associates. ...

,Mkt-RF,SMB,HML,RF
192607,   2.89,  -2.55,  -2.39,   0.22
192608,   2.64,  -1.14,   3.81,   0.25
```

- The catalogue of sins, per file:
    - **Factors:** prose preamble before the data; dates as `192607` (`YYYYMM`); returns in percent (`2.89` means 2.89%); and a *second* table ("Annual Factors") stacked further down in the same file.
    - **Industry portfolios:** all of the above, plus the data is **wide** (one column per industry — one row is ten observations, not one), plus *six* tables stacked in one file (value-weighted, equal-weighted, annual, firm size, ...), plus `-99.99` / `-999` as missing-value codes.
    - **USREC:** actually tidy (FRED is machine-friendly) — but it speaks a different dialect: dates as `1854-12-01`, a column named `USREC`. Harmless alone; a join key mismatch the moment we combine it with the French data. This is the harmonization problem in miniature.

### Let's load the data

<!-- Talking points -->

- `01_load_raw.py` has one job: extract the one block we want out of each file and put it in the database as-is, into tables suffixed `_raw`. Units, dates, missing codes, shape — all still wrong, at this point. Loading and cleaning are separate steps, so when something looks odd later you can ask the database "what did the source actually say?" without re-opening the messy file.
- A taste of the extraction — the monthly rows are exactly the ones whose first field is a 6-digit `YYYYMM`, which quietly skips both the preamble and the stacked annual block:

```python
# src/01_load_raw.py — keep only the monthly block of the factors file
rows = [l.split(",") for l in lines if re.match(r"^\s*\d{6}\s*,", l)]
df = pd.DataFrame(rows, columns=["ym", "mkt_rf", "smb", "hml", "rf"])
df.to_sql("factors_raw", con, if_exists="replace", index=False)
```

- Note what already happened in that snippet, almost in passing: `Mkt-RF` became `mkt_rf` — one naming convention (lowercase snake_case) applied at the door, before drift gets a chance.

### Every fix is a rule in code

<!-- Talking points: 02_clean.py is the chapter's principles, one rule each.
     Walk the list; each bullet names the principle it implements. -->

- `02_clean.py` turns `*_raw` into clean tables. Every decision from this chapter is one visible, re-runnable, reviewable rule:
    - `192607` → `'1926-07-01'` — one date convention, ISO, sorts correctly as text (values that don't lie).
    - `CAST(... AS REAL) / 100` — percent → decimal, once, at the boundary (values that don't lie).
    - `-99.99` / `-999` → `NULL` — missing data gets the database's real missing value, not a magic number that would silently poison an average (intentional missing codes).
    - wide → long with one `melt` — one row per industry-month (tidy data).
    - three sources joined on the now-shared `month` key into one analysis-ready `panel` (harmonization paying off).

```python
# src/02_clean.py — the industry table: every fix is one labelled line
wide = pd.read_sql("SELECT * FROM industry_raw", con)
long = wide.melt(id_vars="ym", var_name="industry", value_name="ret")  # tidy: wide -> long
long["ret"] = pd.to_numeric(long["ret"])
long.loc[long["ret"] <= -99.98, "ret"] = float("nan")   # missing codes -> real NULL
long["ret"] = long["ret"] / 100                          # percent -> decimal
long["month"] = long["ym"].str[:4] + "-" + long["ym"].str[4:6] + "-01"  # -> ISO date
long[["month", "industry", "ret"]].to_sql("industry_returns", con,
                                          if_exists="replace", index=False)
```

- Before and after, with the project's real rows. `industry_raw` — formatted for a human, one row is ten observations, returns are percent strings:

| ym     | NoDur | Durbl | Manuf | Enrgy | ... | Other |
|--------|-------|-------|-------|-------|-----|-------|
| 192607 | 1.44  | 13.90 | 4.70  | -1.14 | ... | 2.14  |
| 192608 | 3.99  | 3.70  | 2.80  | 3.43  | ... | 4.35  |

- `industry_returns` — tidy, one row per industry per month, numbers the computer can compute on:

| month      | industry | ret     |
|------------|----------|---------|
| 1926-07-01 | NoDur    | 0.0144  |
| 1926-07-01 | Durbl    | 0.1390  |
| 1926-07-01 | Manuf    | 0.0470  |
| 1926-07-01 | Enrgy    | -0.0114 |

- And the payoff table, `panel` — one row per industry-month with everything the later regression needs, three sources speaking one dialect:

| month      | industry | ret    | mkt_rf | rf     | recession |
|------------|----------|--------|--------|--------|-----------|
| 1926-07-01 | NoDur    | 0.0144 | 0.0289 | 0.0022 | 0         |
| 1926-08-01 | NoDur    | 0.0399 | 0.0264 | 0.0025 | 0         |

### Did it work?

<!-- Talking points -->

- The whole thing is three commands, re-runnable from nothing by anyone with the repo:

```bash
uv run src/00_fetch.py      # download + freeze (skips files already present)
uv run src/01_load_raw.py   # messy files -> *_raw tables, faithfully
uv run src/02_clean.py      # rules in code -> factors, industry_returns, recession, panel
```

- One sanity check before declaring victory — does the panel's size equal what the structure promises? 1,198 months × 10 industries:

```sql
SELECT count(*) FROM panel;          -- 11980  ✓  (= 1198 months × 10 industries)
SELECT min(month), max(month) FROM panel;   -- 1926-07-01 .. 2026-04-01
```

Now, for us to reply to the question posed by our co-author, it is way easier to do it since we have evidence of each step.
Mistakes are way easier to debug and trace, and we do not need to end up in the situation where we talk and talk, but have nothing concrete to show (where did the data come from, how was it harmonized et cetera).
