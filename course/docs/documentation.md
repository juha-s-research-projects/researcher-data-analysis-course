# Documentation

The documentation is what makes a project survive. It is quite important.
Many might think at first sight that good documentation needs to be large, but this is a misconception.
Good documentation is concise. It should tell the *why*, not the *what*.
If your code is half-decent, people can inspect the source code to learn the *what*.
Documentation does not need to be a second thesis. 
It is enough to have a couple lines for installation / running instructions, dependencies and things to note.

Documentation is the first thing that a stranger sees when they open your project (the readme). It is an easy way to make a good impression to somebody that just happens to come by your project.

Picture this. You zip the whole project folder, send it to a person that can ask you no questions but is competent.
Can they get it up and running? Can they understand most of what you have done? Can they understand the outputs? If the answer is yes to all, you have done a good job.


## The README

This should be short. Answer the core questions: what is this, how do I run it, what do I need to run it.
Shorter is better (quicker to read through, less prose to process). It could have commands to run it, prerequisites like uv and git and where the outputs are written.
A long readme document might indicate that the project contains too many manual steps.

## The data dictionary

This is the most valuable document for research pipelines, but underdocumented.
The document should contain, for every column, an explanation of its name, meaning, units, allowed values and a missing-data convention.
This is essential for others trying to replicate your research.
A simple table written with markdown can satisfy everything that this needs. You can have one row per variable.

## Where did this data come from?

For each raw dataset, there should be a record of

- the source
- date obtained
- who obtained
- how (download / query)
- license and terms of use

Raw data is evidence, and if your evidence (on which your analysis is based on) does not have the necessary documentation, it weakens the whole foundation making any argument you build on top more shaky.
This is also very important for your study to be replicable later on.

## Why, not what

The program code already contains the information of what, but it does not contain the why. You should include in the source code or a read me document some kind of information on the "why".
You should never document what a row does when it's very obvious, like `i = i + 1 #increase i by 1`.
These comments decrease the value of the other, meaningful comments, and make the whole file harder to read for somebody else reading it.

## A README skeleton:

```markdown
# Survey 2024 — effect of X on Y

Reproduces every figure and table in the paper from immutable raw data.

## Run
    ./run.sh        # env → db → clean → analysis → outputs/

## Needs
git, uv. Outputs land in `outputs/`; the manuscript builds in `paper/`.
```

- A codebook row (table form):

| column | meaning | units | allowed values | missing |
|---|---|---|---|---|
| `age` | respondent age at survey | years | 18–120 | blank = not given |
