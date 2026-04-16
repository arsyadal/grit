# Sample Benchmark Run: B2B Security Landing Page

This file is a worked example of a benchmark run for GRIT.

It is intentionally included as a `sample` so the repository shows the benchmark process end to end.
It should not be treated as a formal empirical result unless the prompts are actually run and scored by evaluators.

## Round Info

- Benchmark name: `sample-b2b-security-round-01`
- Date: `2026-04-15`
- Model: `gpt-5.4`
- Reasoning effort: `medium`
- Task: [`../tasks/landing-page-b2b-security.md`](/Users/macintoshhd/Documents/grit/benchmarks/tasks/landing-page-b2b-security.md:1)
- Number of evaluators: `TBD for real run`
- Status: `illustrative sample`

## Prompt Conditions

- Baseline prompt reference: [`../samples/landing-page-b2b-security/baseline-prompt.md`](/Users/macintoshhd/Documents/grit/benchmarks/samples/landing-page-b2b-security/baseline-prompt.md:1)
- GRIT prompt reference: [`../samples/landing-page-b2b-security/grit-prompt.md`](/Users/macintoshhd/Documents/grit/benchmarks/samples/landing-page-b2b-security/grit-prompt.md:1)
- Style module used: [`../../styles/modern-corporate-landing.md`](/Users/macintoshhd/Documents/grit/styles/modern-corporate-landing.md:1)
- Layout module used: [`../../layouts/hero-composition.md`](/Users/macintoshhd/Documents/grit/layouts/hero-composition.md:1)

## What This Sample Demonstrates

- how to define a benchmark round
- how to pair a fair baseline against a GRIT treatment
- how to document style and layout choices
- how to record scores and conclusions without cluttering the repo

## Expected Hypothesis

For this task, GRIT should outperform the baseline on:

- hierarchy clarity
- visual specificity
- trust signaling
- spacing and compositional discipline

The baseline may still perform adequately on:

- responsiveness
- implementation completeness
- section coverage

## Suggested Evaluation Setup

For a real run:

1. Generate one output from the baseline prompt.
2. Generate one output from the GRIT prompt.
3. Remove labels that reveal which output used GRIT.
4. Ask 3 to 5 evaluators to score both outputs using [`../rubric.md`](/Users/macintoshhd/Documents/grit/benchmarks/rubric.md:1).
5. Record the quantitative results below.

## Quantitative Results

Leave these blank until the run is real.

- Mean baseline score:
- Mean GRIT score:
- Score uplift percent:
- GRIT win rate:
- Baseline acceptance rate:
- GRIT acceptance rate:
- Baseline iterations to acceptable output:
- GRIT iterations to acceptable output:
- Iteration reduction percent:

## Qualitative Summary

Use this section after the real run.

- Main differences observed:
- Strongest advantage of GRIT:
- Where baseline still held up:
- Risks or ambiguity in the result:

## Decision

- Did GRIT outperform baseline for this task?
- Should this result be included as a representative benchmark sample?

## Notes

If this sample is turned into a real benchmark round, keep the same task and prompt structure, then replace the placeholders above with measured results.
