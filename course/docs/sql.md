<!-- SCAFFOLD — ideas/topics only. Author writes these bullets into prose.
Per-module shape: Concept → Why it bites (failure story) → What we
recommend (one opinionated answer) → A taste (short example) → Go deeper. -->

# SQL

In the storage chapter, we got one a single-file contained queryable store.
SQL is the language for querying it, and communicating to the machine what and how you want data fetched.
This skill is very transferable: in any real world data work, where we are not playing around but have actually big volumes of data, knowing some SQL is mandatory.
This small, stable language has outlived all tools it runs on. It first appeared in 1973, and was standardised in 1986 by ANSI and 1987 by ISO.
In enterprise transactional workloads, and analytics workloads, a rough estimate of its popularity could be perhaps around 80% (this number is very difficult to approximate, take it with a pinch of salt. the point is that it is the dominant, most popular, standard choice).

Whenever you build a pivot table or a vlookup in your favourite spreadsheet software, you have already had the same mental model as SQL. SQL is just saying it precisely, and with the added benefit that in program code, the statements remain as artefacts for later.
You do not need to learn a language, or to learn how to program, to use SQL. By learning what five, pretty descriptively named verbs do, you already can read and understand 90% of SQL statements written by others. By having a cheat sheet and nice resources, you can also write your own SQL queries when needed. The language itself is tiny, and can be used with Postgres, SQL databases, DuckDB, etc.

## Pivot tables and VLOOKUP were always trying to be these

SQL is superior to a spreadhseet having a chain of vlookups, as the programmatic version can be more easily audited. A spreadsheet might after a data update have half of the vlookups point to wrong rows
A pivot table needs to be rebuilt by hand every time data changes.
You can see that the solutions made by those are inherently fragile, as well as will cause some manual work and grey hair.

The core idea with SQL is that it is declarative, meaning you describe what you want, say "average score per country, for adults". It is then the job of the database to figure out how to get it. The same query can be re-run on new data, and it just works, and there is no manual rebuild. 


## The core five verbs that cover around 90% of research needs

- `SELECT` — pick columns (and compute new ones).
- `WHERE` — keep only the rows you want (filter).
- `GROUP BY` + an aggregate (`count`, `sum`, `avg`, `min`, `max`) — collapse many rows into per-group summaries. This is comparable to what pivot table has as the function.
- `JOIN` — combine two tables on a shared key. This is comparable to VLOOKUP
- `ORDER BY` — sort the result.

## A statement dissected

Below is a diagram, for the anatomy of a statement. There is some terminology used when talking about SQL and these come up in error messages.

![Anatomy of an SQL statement: an UPDATE statement decomposed into clauses, which contain expressions and a predicate built from columns and literals](assets/sql-anatomy.svg)

Source of the picture: SQL article on English Wikipedia (rendered from the article's math markup), https://en.wikipedia.org/wiki/SQL — CC BY-SA 4.0.

As marked in the picture, a *statement* is built from different *clauses*. A transaction contains one or multiple statements, and one transaction either fails (and does not change the data) or succeeds (changes/returns data).
Strictly speaking, a query returns data, but even update/alter statements are often called queries in everyday language.
Clauses are smaller pieces, that can for example update, set or filter values (UPDATE/SET/WHERE).
Expressions compute values from columns, and a predicate is a true/false test that picks which rows are touched.

SQL as a language is case insensitive in many places ("SELECT" = "Select" = "select"), but it is common practice to format the queries as shown for better readability.


The example in the picture is an update rather than a select statement.

A second example of an SQL query is in the below diagram. This time a select statement, which will be what you will most often be using.

![Anatomy of an SQL SELECT statement: SELECT, FROM, WHERE and ORDER BY clauses, with the columns, table, literal and predicate labelled, and the whole statement labelled as an SQL query](assets/sql-anatomy-select.svg)

This statement will return a table, with two columns: name and population, from a table containing country information, restricted to those countries with a population greater than a million, lastly ordered in a descending order by the population count.

## A couple more examples of different SQL statements

<!-- Talking points:
- The five verbs READ data. These four WRITE: they are the rest of what a
  researcher ever needs, and the reader has already met them without being
  told — every cleaning rule in the hygiene chapter was one of these
  (02_clean.py does DROP TABLE IF EXISTS + CREATE TABLE ... AS SELECT;
  the outlier example was a DELETE).
- Order below is a table's life cycle: the table is born (CREATE TABLE),
  rows go in (INSERT), wrong rows go out (DELETE), the table grows a column
  (ALTER), the table goes away (DROP).
- One caution worth a sentence: these run immediately and there is no undo.
  That is not scary in OUR setup — they only ever touch derived tables, and
  the pipeline rebuilds those from read-only raw files, so the worst case of
  a botched DELETE is "re-run the pipeline." This is the hygiene chapter
  paying rent.
- On CREATE TABLE, worth one extra sentence: there is also the
  CREATE TABLE ... AS SELECT variant — define-and-fill in one statement,
  with a plain SELECT inside. The running example builds every clean table
  that way in 02_clean.py.
- These diagrams are original compositions in the same visual style as
  the Wikipedia figure (rendered with the same Wikimedia formula renderer);
  the credit line above covers the styling's origin. -->

![Anatomy of an SQL CREATE TABLE statement: CREATE TABLE clause naming the new table, column definitions giving each column a name and a type](assets/sql-anatomy-create.svg)

![Anatomy of an SQL INSERT statement: INSERT INTO clause naming the table and columns, VALUES clause holding the literals](assets/sql-anatomy-insert.svg)

This statement inserts a pair into the countries table, the pair being ('Finland', 5600000). The first of the pair is the name column-row value and second is the population column value for this observation (row).

![Anatomy of an SQL DELETE statement: DELETE FROM clause naming the table, WHERE clause holding the predicate that picks the rows to remove](assets/sql-anatomy-delete.svg)

This statement deletes from the countries table any countries with a population fewer than a thousand.

![Anatomy of an SQL ALTER TABLE statement: ALTER TABLE clause naming the table, ADD COLUMN clause with the new column and its type](assets/sql-anatomy-alter.svg)

This statement *alters* the table structure in a profound way. It adds a new column of type text. the new columns will be initialized NULL, before we explicitly insert the continent information.

![Anatomy of an SQL DROP TABLE statement: DROP TABLE followed by the table name — deletes the whole table, data and all](assets/sql-anatomy-drop.svg)

This statement drops a table completely!


## Indices: same queries, but sped up

An index is an internal structure the database keeps to speed up queries, a bit like a book has a table of contents with page numbers, allowing you to find a section without reading through everything.
It can be created once, and the database keeps it up to date and uses automatically.
This does not change the query results, it just speeds them up.
You should add one for a column you repeatedly filter (WHERE) or use joins on. This is most important when you have more data.
I would encourage you to look into this first when you feel like your code needs to be faster.
There are costs with adding indices: inserts get slower and file size increases.

![Anatomy of an SQL CREATE INDEX statement: the index name, the table, and the column being indexed — changes no results, only their speed](assets/sql-anatomy-index.svg)

The above statement makes it quicker to filter countries on population.

## Joins: the thing spreadsheets do badly

If you follow the principles outlined in [hygiene](hygiene.md), there should always be one kind of unit per table. Joins are how we put them back together when we need, by key, instead of having everything in one giant sheet, denormalized.
It is good to know that **inner** join keeps only matched rows, whilst **left** join keeps every row on the left, even when there is no match (there are nulls). This is an answer to many "where did my rows go?" type of bugs that arise from using the wrong kind of join.
This beats a vlookup as it is traceable, reproducible, doesn't drop or duplicate rows without telling you, shrinks and grows as the underlying data shrinks and grows.

![Anatomy of an SQL SELECT with an INNER JOIN: columns written as table.column, FROM the first table, JOIN the second table ON the join condition — returns only the rows that match in both tables](assets/sql-anatomy-join-inner.svg)

This query selects a list of country, capital names. The country name is from table countries, and capital name is from table capitals, and the joining logic is based on the country names matching in both tables. Note that this could also be just a common "ID". The inner joins only returns countries that have a match between these two tables.

![Anatomy of the same SELECT with a LEFT JOIN: identical apart from the LEFT keyword — returns every row of the first table, with NULLs where the second table has no match](assets/sql-anatomy-join-left.svg)

The second statement is very similar, but has a LEFT JOIN instead. This will return a superset of the previous results, as it will also return zero or more results with no match, with capital being null when there is no match.

In the running example we have 02_clean.py building a panel with a join on the factors, where we use INNER JOIN because if we do not have a return observation, the factor data is useless. Later we use LEFT JOIN with a recession, as we want to keep every month, even those that have not been flagged.
These two decisions seem small, but for corresponding ones in a bigger project it is crucial to be able to later on go through and see what choices have been made, for verifying correctness.

## Subqueries: a query inside a query

Here is a diagram of a SELECT statement with a subquery:

![Anatomy of an SQL SELECT with a subquery: the WHERE clause compares a column against a parenthesised inner SELECT that runs first and returns one number](assets/sql-anatomy-subquery.svg)

Statements can be nested in the fashion of the example, where the subquery runs first, to then be able to evaluate the outer statement.
Anywhere where we could put a value/number we can put a select statement.
You could in theory make deep nested statements, but of then this is not wise, as they are somewhat more difficult to read beyond one deep nests.
Multiple, smaller statements often beat a gigantic statement. They are similar amount of work to write, but are way easier to read, which is the most important thing about program code.

## Where SQL ends (and Python takes over)

SQL is unbeatable for data work based on sets: filter, group, join, aggregate, reshape etc.
But SQL is not really the best choice for statistical modelling, like regressions, plots and so on. You should use Python, R, Julia, or something else for that.
In my opinion, the sanest way to divide responsibilities is to have SQL shape the data, whilst your favourite programming language runs any analysis you would like to do on it.

## Links

Here is a list of links for further study. I recommend very very strongly to spend some time practicing SQL queries if they are not familiar to you, even in the LLM age. Take one week, where you spend one or two hours per working day on these, and these will be easy after that.

<!-- All links checked live 2026-06-11. Suggested one-line pitches per link: -->

- [SQLBolt](https://sqlbolt.com) — interactive lessons in the browser. Start by practicing the five verbs here first.
- [Select Star SQL](https://selectstarsql.com) — a free interactive book that teaches SQL by analyzing a real dataset. This is close in spirit to research work, continue here.
- [SQL Murder Mystery](https://mystery.knightlab.com) — practice disguised as a detective game; joins and filters to catch a killer. Use this if you'd like to have some more dopamine whilst practicing.
- [SQLite's SQL documentation](https://sqlite.org/lang.html) — the reference for the exact dialect the course store speaks; where to check syntax once you're writing your own. This is the user manual.
- [Use The Index, Luke](https://use-the-index-luke.com) — if indices made you curious, this is the friendly book-length treatment of how databases actually find rows.
- [SQL Style Guide](https://www.sqlstyle.guide) — one sensible convention for formatting queries, for when your statements start living in version-controlled pipelines.
