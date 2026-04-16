# Automated Benchmark Runner

This folder scaffolds an automated benchmark workflow for GRIT.

It is designed to support full pipeline automation with clear interfaces:

1. initialize a run
2. generate baseline and GRIT outputs
3. render local HTML and capture screenshots
4. collect technical metrics
5. ask a judge model to score both outputs
6. compute metrics automatically
7. generate a markdown report

The scripts here do not force one rendering stack or one model provider.
They define the contracts that the rest of the pipeline should obey.

## Folder Layout

```text
benchmarks/automation/
├── README.md
├── package.json
├── artifacts/
│   └── README.md
├── prompts/
│   └── judge_prompt.md
├── schemas/
│   ├── output-artifact.schema.json
│   ├── run.schema.json
│   ├── technical-metrics.schema.json
│   └── judge-result.schema.json
└── scripts/
    ├── benchmark_runner.py
    └── run_technical_audit.mjs
```

## What Gets Automated

The runner automates:

- run folder creation
- benchmark metadata scaffolding
- local template-based HTML generation
- screenshot capture
- Lighthouse audits
- axe audits
- local heuristic judging
- metric calculation
- markdown report generation

The runner assumes another layer will handle:

- model-provider generation if you want real LLM output instead of local template output
- model-as-judge execution if you want stronger benchmark credibility

## Suggested End-To-End Flow

1. Create a run:

```bash
python3 benchmarks/automation/scripts/benchmark_runner.py init \
  --task landing-page-b2b-security \
  --model gpt-5.4 \
  --reasoning medium \
  --style styles/modern-corporate-landing.md \
  --layout layouts/hero-composition.md
```

2. Run everything:

```bash
python3 benchmarks/automation/scripts/benchmark_runner.py run-all \
  --run benchmarks/automation/artifacts/<run-id>
```

This command performs:

- generate baseline
- generate GRIT
- capture screenshots
- run Lighthouse and axe
- judge outputs
- score results
- generate the markdown report

## Manual Artifact Input

Use this mode when you generate baseline and GRIT HTML manually in ChatGPT/Codex and do not want the runner to generate them.

1. Create a run:

```bash
python3 benchmarks/automation/scripts/benchmark_runner.py init \
  --task landing-page-b2b-security \
  --model gpt-5.4 \
  --reasoning medium \
  --style styles/modern-corporate-landing.md \
  --layout layouts/hero-composition.md
```

2. Attach your baseline HTML:

```bash
python3 benchmarks/automation/scripts/benchmark_runner.py attach \
  --run benchmarks/automation/artifacts/<run-id> \
  --condition baseline \
  --html /absolute/path/to/baseline.html
```

3. Attach your GRIT HTML:

```bash
python3 benchmarks/automation/scripts/benchmark_runner.py attach \
  --run benchmarks/automation/artifacts/<run-id> \
  --condition grit \
  --html /absolute/path/to/grit.html
```

4. Run the rest of the pipeline:

```bash
python3 benchmarks/automation/scripts/benchmark_runner.py run-manual \
  --run benchmarks/automation/artifacts/<run-id>
```

This command performs:

- capture screenshots
- run Lighthouse and axe
- judge outputs
- score results
- generate the markdown report

## Manual Flow

If you want full control over each stage, use this sequence instead.

1. Generate the local HTML artifacts:

```bash
python3 benchmarks/automation/scripts/benchmark_runner.py generate \
  --run benchmarks/automation/artifacts/<run-id> \
  --condition baseline \
  --provider local
```

Run the same command for `--condition grit`.

2. Capture screenshots:

```bash
python3 benchmarks/automation/scripts/benchmark_runner.py capture \
  --run benchmarks/automation/artifacts/<run-id> \
  --condition baseline
```

Run the same command for `--condition grit`.

3. Run technical audits:

```bash
python3 benchmarks/automation/scripts/benchmark_runner.py audit \
  --run benchmarks/automation/artifacts/<run-id> \
  --condition baseline
```

Run the same command for `--condition grit`.

4. Run the local judge:

```bash
python3 benchmarks/automation/scripts/benchmark_runner.py judge \
  --run benchmarks/automation/artifacts/<run-id> \
  --provider heuristic
```

5. Fill or enrich the generated run folder with:

- `outputs/baseline.json`
- `outputs/grit.json`
- `metrics/technical.json`
- `judge/judge-result.json`

6. Compute summary metrics:

```bash
python3 benchmarks/automation/scripts/benchmark_runner.py score \
  --run benchmarks/automation/artifacts/<run-id>
```

7. Generate the markdown report:

```bash
python3 benchmarks/automation/scripts/benchmark_runner.py report \
  --run benchmarks/automation/artifacts/<run-id>
```

## Required Files Per Run

### `outputs/baseline.json`

Stores the baseline prompt and generated output metadata.
See [`schemas/output-artifact.schema.json`](/Users/macintoshhd/Documents/grit/benchmarks/automation/schemas/output-artifact.schema.json:1).
For screenshot capture, `generate` fills `render_target_path` automatically. You can still override it with `--html`.
If you use manual mode, `attach` fills `code_path` and `render_target_path` from your HTML artifact.

### `outputs/grit.json`

Stores the GRIT prompt and generated output metadata.
See [`schemas/output-artifact.schema.json`](/Users/macintoshhd/Documents/grit/benchmarks/automation/schemas/output-artifact.schema.json:1).

### `metrics/technical.json`

Stores machine-collected signals such as:

- build pass
- lint pass
- Lighthouse scores
- accessibility issue count
- axe violations
- iteration count
- elapsed time

### `judge/judge-result.json`

Stores the rubric scores from the judge layer for:

- Output A
- Output B

The report script maps those back to baseline and GRIT using the run metadata.

## Provider Modes

### Local mode

Use this when you want the pipeline to be fully testable without external APIs.

- `generate --provider local`
- `judge --provider heuristic`

This mode uses:

- template HTML generation
- local screenshot capture
- local Lighthouse audits
- local axe audits
- heuristic scoring

### Manual artifact mode

Use this when generation happens outside the runner.

- `attach`
- `run-manual`

This mode uses:

- user-supplied HTML artifacts
- local screenshot capture
- local Lighthouse audits
- local axe audits
- heuristic scoring or OpenAI judge mode

### OpenAI mode

Use this when you want real model generation and model-based judging.

Required environment:

- `OPENAI_API_KEY`
- optional `OPENAI_BASE_URL`
- optional `OPENAI_JUDGE_MODEL`

Example:

```bash
python3 benchmarks/automation/scripts/benchmark_runner.py generate \
  --run benchmarks/automation/artifacts/<run-id> \
  --condition baseline \
  --provider openai
```

And:

```bash
python3 benchmarks/automation/scripts/benchmark_runner.py judge \
  --run benchmarks/automation/artifacts/<run-id> \
  --provider openai
```

OpenAI mode uses the Responses API.
The current script passes the run model and reasoning effort through to the API call.

## Blindness Rule

For fairness, the judge should not know which output is baseline and which is GRIT.

Use:

- `output_a`
- `output_b`

Then use the run metadata to record whether `output_a` maps to baseline or GRIT.

## Output Files Produced By The Runner

After capture:

- `screenshots/baseline-desktop.png`
- `screenshots/baseline-mobile.png`
- `screenshots/grit-desktop.png`
- `screenshots/grit-mobile.png`

After technical audits:

- `metrics/baseline-audit.json`
- `metrics/grit-audit.json`

After scoring:

- `summary/summary.json`
- `summary/report.md`

These files can be committed selectively or copied elsewhere for dashboards.

## Practical Note

This scaffold gives you a stable evaluation contract first.
You can later wire it to:

- OpenAI Responses API
- Playwright screenshot capture
- Lighthouse CI
- custom React renderers
- any model-as-judge pipeline

## Install

Install the local audit dependencies once:

```bash
cd benchmarks/automation
npm install
```
