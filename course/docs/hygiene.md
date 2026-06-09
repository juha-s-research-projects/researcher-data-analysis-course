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
For dates, use `YYYY-MM-DD` always as it sorts correctly as text, is unambiguous to everybody. 
For country codes you can do something similar: instead of `Finland` / `finland` / `FIN` / `FI` you can stick to one convention, like `FI`/`FR`/`DE`/`CH` (ISO 3166-1 A-2).
For missing data: remember to be intentional about your codes. Blank vs `NA` vs `999` vs `-1` vs `N/A` should not be used interchangeably. Many times you might have missing data due to many different reasons, like "missing" (no response in a survey), "zero" (numerical value of zero) or "not applicable" (the hair colour of a bald person).

## Recap

Remember that

- Raw data is sacred, thus all edits happen on copies, and the raw data is preserved as is. Each step is in code for reproducability as well as so that the steps can be understood later.
- Try to pick conventions for variable names and variable values, document these and follow the tidy principles for your data tables.
- Following these steps makes your work easier to follow, your arguments look more professional as well as more credible, and easier for the whole world to listen to and be interested in.

## Let's continue with our example
