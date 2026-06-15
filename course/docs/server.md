# ei alotettu



<!-- SCAFFOLD / BRIEF — authored by ANTTI (server admin), in his voice.
This is my scaffold + brief, with my tips marked as author callouts for Antti
to keep or cut. Per COURSE-NOTES: conditional appendix, "when you outgrow the
laptop." Same per-module shape as the rest. Antti writes the prose. -->

# Server

!!! note "Conditional appendix — when you outgrow the laptop"
    Most projects in this course never need this chapter. Read it only when a
    real constraint pushes you off your own machine. Authored by Antti
    (server / HPC admin).

<!-- BRIEF FOR ANTTI:
- Audience is the same smart non-programmer as the rest of the course.
- Keep the spine: the architecture does NOT change when you move to a server —
  same one-directional pipeline, same one command, bigger machine. That's the
  reassuring throughline; please keep it.
- Same module shape: Concept → why it bites → what you recommend → a taste →
  go deeper. -->

## When do you actually need a server?

- The honest gate first: list the concrete signals that justify leaving the laptop, so nobody cargo-cults an HPC account they don't need.
  - Data too big for local disk/RAM even after letting the DB do the work ([performance](performance.md)).
  - Jobs that run for hours/days, or must keep running after you close the lid / lose wifi.
  - Compute you don't have locally (many cores, big RAM, GPUs).
  - A store several people must share as one source of truth.

> **Author tip (callout):** if none of these is true, stay on the laptop. The
> course's whole point is that the laptop setup is already disciplined and
> reproducible — a server is a scaling decision, not a virtue.

## The shared store

- Antti: the institutional/shared place the canonical data lives; how a project's `data/raw/` relates to it (a working copy pulled from the shared store, not a second master). Ties to [datahub](datahub.md).

## Compute that outlives your session (HPC / batch)

- Antti: the mental model of a job scheduler (submit a job, it runs without you, you collect results) — SLURM-style, at whatever level of detail fits a non-CS reader.
- The reproducibility bridge: containers for bit-for-bit runs on shared hardware — **Apptainer** on HPC (callback to [coding](coding.md)'s layered-fallback table, where Docker/Apptainer is the "bit-for-bit across anything" option).

> **Author tip (callout):** the same `run.sh` should still be the entrypoint on
> the cluster. If moving to HPC forces you to rewrite the pipeline, something
> upstream wasn't portable — fix that, don't fork the project.

## A taste

- Antti: one minimal, real example — e.g. a tiny SLURM submit script that runs `run.sh` inside an Apptainer container — kept short, like the other chapters' tastes.

## Go deeper

- Antti: links to the local cluster's docs / onboarding; Apptainer docs.
