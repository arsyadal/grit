# Benchmarks

This folder contains the evaluation kit for measuring whether GRIT improves frontend generation in a repeatable, defensible way.

The goal is not only to say that GRIT "looks better."
The goal is to measure whether GRIT performs better than a baseline prompt across realistic frontend tasks.

## What This Folder Is For

Use this benchmark kit to measure:

- win rate versus baseline prompts
- average rubric score uplift
- iteration reduction to acceptable output
- acceptance rate at a defined quality threshold
- style differentiation across modules

## Recommended Structure

```text
benchmarks/
├── README.md
├── method.md
├── rubric.md
├── tasks/
│   ├── landing-page-b2b-security.md
│   ├── dashboard-supply-chain.md
│   ├── pricing-page-fintech.md
│   ├── onboarding-form-hr.md
│   └── settings-page-devtools.md
├── templates/
│   ├── baseline-prompt.md
│   ├── grit-prompt.md
│   ├── evaluator-scorecard.md
│   └── result-summary.md
└── results/
    └── README.md
```

## Fast Start

1. Pick one task from [`tasks/`](/Users/macintoshhd/Documents/grit/benchmarks/tasks).
2. Generate one output with the baseline prompt template.
3. Generate one output with the GRIT prompt template.
4. Score both using [`rubric.md`](/Users/macintoshhd/Documents/grit/benchmarks/rubric.md:1).
5. Record the result in [`templates/result-summary.md`](/Users/macintoshhd/Documents/grit/benchmarks/templates/result-summary.md:1).

## Worked Example

Start here if you want to see one full sample benchmark round:

- [`results/2026-04-15-landing-page-b2b-security-sample.md`](/Users/macintoshhd/Documents/grit/benchmarks/results/2026-04-15-landing-page-b2b-security-sample.md:1)
- [`samples/landing-page-b2b-security/README.md`](/Users/macintoshhd/Documents/grit/benchmarks/samples/landing-page-b2b-security/README.md:1)

## Automation Scaffold

If you want the benchmark workflow to be machine-driven instead of scored manually, start here:

- [`automation/README.md`](/Users/macintoshhd/Documents/grit/benchmarks/automation/README.md:1)
- [`automation/prompts/judge_prompt.md`](/Users/macintoshhd/Documents/grit/benchmarks/automation/prompts/judge_prompt.md:1)
- [`automation/scripts/benchmark_runner.py`](/Users/macintoshhd/Documents/grit/benchmarks/automation/scripts/benchmark_runner.py:1)

## What To Keep In Git

Good to keep in this repo:

- benchmark tasks
- rubric and scoring method
- prompt templates
- sample summaries
- a small number of representative result examples

Better to keep outside the repo if it grows large:

- hundreds of generated screenshots
- large batches of raw HTML or React output
- heavy experimental logs
- dashboard infrastructure for reporting

## Success Criteria

GRIT is proving impact when it can show results like:

- higher blinded win rate than baseline
- higher mean rubric score
- fewer iterations to acceptable output
- higher acceptance rate
- clearer differentiation between styles on the same task

See [`method.md`](/Users/macintoshhd/Documents/grit/benchmarks/method.md:1) for the full workflow.
