# LLMs

For the last couple of years, large language models have been all the hype. 
They have improved rapidly especially in the last couple of years, and may continue to improve further as hardware improves.
In my opinion, almost any researcher could benefit from the use of LLMs to some degree, but it is critical to understand and use them properly.
The most important thing is that the mission critical code should be reviewed very diligently - just like with human programmers.
Mission critical code will look different for different domains. For an economics or finance researcher, it will be any statistical analysis.


## Good and bad examples of LLM use

There are some good places to use LLMs as a researcher, where the risks are clearly lower, as well as the benefit is higher.
The following is a list of examples:

- Help with LaTeX formatting
- Vibe coding a survey, or info website, that is easy to test to see that it works as intended
- Helping with parts of the pipeline that are tedious to write, but have benefit if done, and are easily verifiable, for example, you could have your pipeline automatically emit LaTeX coded tables containing numbers computed in-code, and have these automatically cascade to your document
- Improving how plots and figures look (line size, colors, etc., in the realm of "make this more legible" where you might not even know as an economics researcher what would be the optimum color palette for that)
- Coming up with new ideas on what *could* be possible
- Finding bugs / mistakes in code, code-audits

Following list of examples are uses where an LLM will probably bite at some point:

- Using it (often) for something you are supposed to be an expert in (you should read up on this topic to become better than the LLM, or at least good enough to know where to find information without the LLM)
- Using it for mission critical code: for economics or finance research that is the statistical analysis, for some other field it could be a central algorithm
- Anything that is difficult to verify by just testing (statistical analysis!)

## Things to do to improve

- You should work by committing code one by one, structured in logical changes. This helps you go back in case something breaks down. The chats you might have had, should not be recorded, the output is the artefact.
- Most often when working with LLMs the prompt will not become better by pasting raw data, but rather giving the schema of the data (data types, column names etc.) Easy habit to pick up that helps when you are working with data that should be kept private.
- Plan first, generate code only then. LLMs make silent assumptions on things you do not explicitly tell them to do about your code, which is where you might have differing expectations from the code outputted.
- Use claude code, openai codex or the like. Context and execution capabilities are crucial to have, and LLMs are pretty good at looping until they get something right. You should give them that ability
- Use Andrej Karpathy inspired [claude.md](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/CLAUDE.md) (can be used with other LLMs as well, not just claude) to make your LLM behave a bit better as a "system prompt".

## Hallucination

At the moment of writing, in 2026, the state of LLMs is that they will hallucinate. This is due to how they work: they model probability distributions over the next word, sample that next word and then sample a new word based on another probability distribution (at random!). If you are not comfortable or okay with the possibility of hallucination, you should not use the LLM for such tasks. Let's imagine you have a massive corpus: you have around a million documents and want to go through them, and just find one question. LLMs are really good at understanding sentiment (compared to regex) and context, in complicated real world documents, where classifiers might fail. Still, out of the million documents, there will be a couple percentage points where you might disagree with the LLM. Depending on your research question or the purpose, this might be completely fine, and can be treated as a measurement error. But for some other purposes, it might be that you won't be able to treat it as a measurement error, if it could happen that you are trying to find something very specific in each document, and if even one or two of them fail, it has big consequences for your research question.
