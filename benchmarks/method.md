# Benchmark Method

This document defines the recommended benchmark process for GRIT.

## Objective

Measure whether GRIT improves frontend generation quality and efficiency compared to a baseline prompt.

The benchmark should answer:

- Does GRIT produce stronger first-pass output?
- Does GRIT reduce the number of revisions needed?
- Does GRIT create more visually specific results?
- Does GRIT outperform baseline prompts across multiple tasks, not just one example?

## Test Design

Use an A/B comparison:

- `A`: baseline prompt
- `B`: GRIT prompt

Run both against the same task.

For each task, keep these constant:

- model
- temperature or equivalent settings if exposed
- tech stack
- prompt task content
- output format

Only the prompting method should change.

## Minimum Recommended Sample

Start with:

- 5 tasks
- 2 conditions per task
- 3 to 5 evaluators if possible

This is enough to get directional evidence without turning the repo into a research project.

## Evaluation Modes

### 1. Blind quality comparison

Hide which output used GRIT.
Ask evaluators to score both outputs using [`rubric.md`](/Users/macintoshhd/Documents/grit/benchmarks/rubric.md:1).

Best for:

- win rate
- average score uplift
- acceptance rate

### 2. Workflow efficiency tracking

Measure:

- number of prompt iterations until acceptable
- total time to acceptable output
- amount of manual cleanup required after generation

Best for:

- iteration reduction
- time reduction
- editing effort reduction

### 3. Style differentiation test

Use the same task with multiple GRIT style modules.
Then assess whether the results feel meaningfully different from one another.

Best for:

- proving the modules produce distinct visual directions

## Metrics

### Win rate

Definition:
The percentage of A/B comparisons where GRIT is judged better overall.

Formula:

```text
win_rate = grit_wins / total_comparisons * 100
```

### Average rubric score uplift

Definition:
The average percentage improvement in rubric score from baseline to GRIT.

Formula:

```text
uplift_percent = (grit_score - baseline_score) / baseline_score * 100
```

### Acceptance rate

Definition:
The percentage of outputs that meet the benchmark's minimum acceptable quality threshold.

Example threshold:

- mean total score >= 4.0 out of 5

Formula:

```text
acceptance_rate = accepted_outputs / total_outputs * 100
```

### Iteration reduction

Definition:
The percentage reduction in prompt rounds needed to reach an acceptable result.

Formula:

```text
iteration_reduction = (baseline_iterations - grit_iterations) / baseline_iterations * 100
```

## Benchmark Rules

- Do not change the task content between baseline and GRIT runs.
- Do not cherry-pick only the strongest GRIT outputs.
- Do not compare outputs generated on different product goals.
- Keep artifact naming consistent.
- Record evaluator count and scoring method in every summary.

## Suggested Reporting Format

For each benchmark round, record:

- task name
- baseline prompt used
- GRIT prompt used
- number of evaluators
- mean baseline score
- mean GRIT score
- win rate
- acceptance rate
- prompt iterations
- notes on major qualitative differences

Use [`templates/result-summary.md`](/Users/macintoshhd/Documents/grit/benchmarks/templates/result-summary.md:1) as the starting template.
