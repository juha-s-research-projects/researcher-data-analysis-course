# Version control

Git is the best cure for the file-naming horror from index.md. This chapter gives a short introduction to using version control.
Thanks to git, we can know who changed what, when and why, and how to go back.

## git is memory and provenance (the cure for `final_v2_FINAL`)

Many people might do version control by filename and end up with files like `analysis_version-2-final-FINAL (1)_use-this-one.xlsx`. This is not good, as you will have too many files unnecessarily and you will be unsure what the last version was. You might not even be able to go back in time when you want to. Git is a more efficient way to do that, as it gives a complete, attributable and reversible history.
You might think it is a developer tool, but it should be used by others as well. 

## What belongs in git — and what emphatically does not

You should keep in git small text files that describe how to build everything, like source code, lock files, version files, gitignore files, shell scripts, tex code, references, readmes, and configuration files.
Big raw data dump do not belong to git, as git is built for small text and not for large binaries. Git will slow down with bigger t ext files. Raw data should bea rchived and governed elsewhere, and raw data files should be added to .gitignore as entries, that tell git to not track them.
Anything that can be generated should not be tracked by git either. Neither should database files, .venv files, built pdfs.

## Commits as a research log

Commits can be made a reserach log. In each commit message, you should detail why you are making the change. Over time, the messages will be able to make a coherent history of how your reasoning moved from one to other.
You should strive to make small commits with one logical change each. With these it is easier to make the history more readable, and thus a more believable trail.
If you use git properly, a year from now you can do `git log` and read through the history, which will be way more detailed than any memories you might have of it.

## Data versioning

"Should I version my data in git too?"

Most often not. Git is intended for text and code, raw data should be immutable anyway and the point of git is version control.
If you need versioned datasets, you can use git-LFS, git-annex and DVC. Remember that you can also add metadata to your DB like timestamps of download to each dataset.


## The Overleaf exception (same story as architecture + manuscript-pipeline)

The `run.sh` does a `git push` to Overleaf, but Overleaf is not a second version control system. Overleaf just exposes git as the only way to push artefacts to it. It should be thought of as a transport pipe that speaks git.

## A taste

```bash
git init
git add src/02_clean.py
git commit -m "Drop two pre-registered outliers (protocol §3)"

git log --oneline        # the research log, at a glance
git revert <commit>      # undo a change without erasing history
```
The most typical workflow will look something like this: `git init` on the very first time to make the folder you are in, a git repository.
After that, you add the files, one by one (or git add --all for all of them at once) with git add <file>, that will be picked up to the next commit (to staging).
git commit -m <message> is like a checkpoint in a game. A checkpoint will be created here, and you can return if you want to, pretty easily.
A useful command is `git status`, this gives you a short status printout to see what the current situation is.
There are graphical implementations of git, but I recommend you start with the terminal version, it is easier to use (no kidding!)
A program called gitk is good for visualizing git history, if you wish to do that.

## .gitignore

Here, you can tell what git ignores. You can `git add` and commit files ignored by gitignore, but files in .gitignore will be ignored by default.
Each line is its own entry:

```gitignore
docs/
.env
*.log
scratchpad/embarrassing.md
```

The above are some example entries for .gitignore, read more here:

- [The official .gitignore reference](https://git-scm.com/docs/gitignore) — complete syntax for gitignore (wildcards, negation with `!`, directory-only rules).
- [Atlassian's .gitignore tutorial](https://www.atlassian.com/git/tutorials/saving-changes/gitignore) — a gentle walkthrough of the first one
- [github/gitignore](https://github.com/github/gitignore) — ready-made templates per language/tool

## Remotes and branches

A remote is a copy of your repository somewhere else, most popularly GitHub, GitLab or something else.
The local version of your repository is complete as is, and has full history, works offline. The remote version just mirrors the local version.
There are two reasons you might want to have a remote. The first one is to be a backup: it is a very simple, off-site backup of the code and all its history.
No need to worry about losing a project due to one laptop dying, you can just resume development on another machine (which is a second benefit).
Remotes make working on multiple machines easy.
The third reason to have a remote is to make it easy to share the whole project folder to others, and to collaborate with others working on the same code base alongside you.

You should have one remote for simplicity, and name it `origin` (which is the convention).
On `git push origin <branch name>`, git pushes any changes to the remote, and on `git pull origin <branch name>` git pulls any changes that have been pushed to the remote by others.

A branch on the other hand, is a parallel line of history. They can be used to try something risky, without touching a "main" version that works.
They are cheap to create, instant to switch to and from.
For a solo researcher, most of the time you will develop on a single branch (named often `main` or `master`), and branches are most useful with risky restructuring that you might also abandon at some point, as well as when you want to revise and redo the analysis without disturbing a main submitted version.
When the divergent branches are brought together, it is called merging. Sometimes there are merge conflicts, so both branches have the same file, but with different contents, and then it has to be solved manually what lines of code are discarded and what are kept.
Sometimes you might have a failed experiment on another branch, and when you don't want to have it anymore, you can just delete the branch.

In today's day and age of vibe coding and super rapid development, branches, remotes, and git commits are super important to keep the project safe and not breaking.

```bash
# remotes: publish/back up your history
git remote add origin git@github.com:you/phd-project.git   # connect, once
git push -u origin main          # first push; afterwards just `git push`
git pull                         # bring a co-author's commits down

# branches: a safe place for an experiment
git switch -c reviewer2-robustness   # create + switch to a new branch
# ...edit, run, commit as usual...
git switch main                  # back to the safe version
git merge reviewer2-robustness   # keep the experiment (it worked)
git branch -d reviewer2-robustness   # tidy up the label afterwards
```

## Additional materials

- [Software Carpentry: Version Control with Git](https://swcarpentry.github.io/git-novice/) — intro course for git.
- [Learn Git Branching](https://learngitbranching.js.org) — an interactive, visual sandbox for practicing branches and remotes in the browser. Makes the whole logic click easily.
- [Oh Shit, Git!?!](https://ohshitgit.com) — short recipes for the most common "I broke something" moments, in plain language. This is worth bookmarking.
