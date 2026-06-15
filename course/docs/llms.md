# ei alotettu


<!-- SCAFFOLD — ideas/topics only. Author writes these bullets into prose.
NOTE on this chapter's role (from COURSE-NOTES): LLMs are taught by CAMEO in
the running example, NOT here. This page is the short consolidation/checklist
of rules already demonstrated inline — the receipts, one place to find them.
It is NOT a vibe-coding chapter and NOT the teaching vehicle. Keep it tight. -->

# LLMs

<!-- Intro framing — short paragraph:
- Set expectations immediately: this is not a "how to code with AI" chapter
  and not a tutorial. The running example already showed an LLM walking on
  twice at natural moments. This page just collects the rules it demonstrated,
  so there's one place to find them.
- Tone: calm and bounded. LLMs are a useful scaffolding tool with a few hard
  rules, not a co-author of the pipeline. -->

## How this course treats LLMs

- The stance: the LLM is a **scaffold-time assistant**, not part of the pipeline. It helps you *write* deterministic code faster; it never sits *inside* the reproducible run.
- Where you've already seen it: two cameos in the running example (recapped below). This page is the checklist, not a re-teach.

## Where LLMs are genuinely good — and where they bite

- **Good fit:** well-specified, boilerplate, and **visually verifiable** work — e.g. "turn this regression output into a booktabs LaTeX table." You can look at the result and immediately tell if it's right.
- **Bad fit / bites:** anything you can't readily check; anything touching governed or raw data; anything where a confident-but-wrong answer slips silently into a result. The danger isn't that it's useless — it's that it's *plausible*.

## The rules (the checklist)

- **Committed code is the artifact; the chat is not.** What goes in the repo and runs in the pipeline is the code you reviewed and committed. The conversation that produced it is scaffolding — disposable, not provenance. The pipeline stays deterministic.
- **Don't paste governed or raw data. Paste the schema + the question.** The model needs the *shape* of the data (column names, types), not the rows. This protects participants/governance and is usually all the model needed anyway.
- **Verify against a known result first.** You already have a ground truth — your pipeline produces one. Before trusting an LLM-extended analysis, check it reproduces a number you already know is right.
- **Debugging: paste the traceback + minimal context, never the dataset.** The error and a few lines around it are enough; the data is not part of the question.

## The two cameos (pointers back to the running example)

- **Touchpoint 1 — generate the table-generating code.** The LLM writes the boilerplate that turns regression output into a `booktabs` `.tex` table. Ideal job: well-specified, boilerplate, visually verifiable. Rule demonstrated: *committed code is the artifact, the chat is not.*
- **Touchpoint 2 — expand the analysis.** Add a control variable / extend a spec. Rules demonstrated: *paste schema + question, not the data*; *verify against the known result first.*
- (Optional touchpoint 3 — debugging a traceback — same rules, smaller.)

## Go deeper

- Your institution's policy on AI tools and research data (governance first).
- One short, sober piece on LLM limitations for analysis (hallucination, verification).
