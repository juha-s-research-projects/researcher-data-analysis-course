# ei alotettu



<!-- SCAFFOLD — ideas/topics only. Author writes these bullets into prose.
KEEP THIS CHAPTER SHORT (per COURSE-NOTES). One message, one mental model. -->

# Performance

<!-- Intro framing — one or two sentences:
- The whole chapter in a line: performance mostly doesn't matter until it
  does, and when it does there's exactly one mental model worth holding.
  Resist premature optimization. -->

## Premature optimization wastes the time you came to save

- The default posture: **don't optimize.** Correctness, clarity, and reproducibility first. Most research pipelines are plenty fast; time spent making a 3-second script take 1 second is time stolen from the actual research.
- Failure mode to name: rewriting working code to be "efficient" before there is any evidence it's slow — and making it buggier and harder to read in the process.

## The one mental model: working set vs memory

- The only performance idea most researchers need: **does the data you're touching fit in memory?**
  - If yes → stop thinking about performance. You're fine.
  - If no → don't try to load it all (the classic "read a 50 GB CSV into a pandas DataFrame" crash). **Let the database do the heavy lifting** — a database reads and aggregates straight from disk, pulling only the rows and columns a query needs instead of loading the whole table into a DataFrame. When data outgrows even that, it's the signal to reach for a heavier analytical engine (see [storage](storage.md)).
- One line to remember: when data outgrows memory, push the work *down into the store*, don't pull the store *up into memory*.

## When it does matter: measure, don't guess

- If something is genuinely too slow, **profile before optimizing.** The slow part is almost never where you'd guess. Find the actual bottleneck, fix that one thing, stop.

## A taste (optional)

```sql
-- let the database aggregate on disk; only the small result comes back to Python:
SELECT industry, avg(ret)
FROM industry_returns
GROUP BY industry;
```

## Go deeper

- When a single-file store stops keeping up: reaching for an analytical engine (see [storage](storage.md)).
- One short note on profiling in Python (`cProfile` / `time`).
