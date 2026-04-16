# Automated Benchmark Report

## Run Info

- Run ID: `matrix-local-check-onboarding-form-hr-r01`
- Task: `onboarding-form-hr`
- Model: `gpt-5.4`
- Reasoning effort: `medium`
- Style module: `styles/swiss-editorial.md`
- Layout module: `layouts/form-clarity.md`

## Judge Outcome

- Preferred condition: `grit`
- Judge confidence: `0.4`
- Baseline mean score: `4.2857`
- GRIT mean score: `4.8571`
- Score uplift percent: `13.3333`
- Baseline acceptance rate: `100.0`
- GRIT acceptance rate: `100.0`

## Efficiency

- Baseline iteration count: `1.0`
- GRIT iteration count: `1.0`
- Iteration reduction percent: `0.0`
- Baseline elapsed seconds: `0.0008`
- GRIT elapsed seconds: `0.0005`

## Technical Checks

- Baseline build pass: `True`
- GRIT build pass: `True`
- Baseline lint pass: `True`
- GRIT lint pass: `True`
- Baseline Lighthouse performance: `100`
- GRIT Lighthouse performance: `100`
- Baseline Lighthouse accessibility: `100`
- GRIT Lighthouse accessibility: `91`
- Baseline axe violations: `0`
- GRIT axe violations: `1`
- Baseline manual edit LOC: `0`
- GRIT manual edit LOC: `0`

## Category Scores

### Baseline

```json
{
  "hierarchy_clarity": 4,
  "visual_specificity": 4,
  "spacing_and_layout_discipline": 5,
  "component_consistency": 4,
  "responsiveness_and_adaptability": 5,
  "implementation_readiness": 5,
  "style_fidelity": 3
}
```

### GRIT

```json
{
  "hierarchy_clarity": 4,
  "visual_specificity": 5,
  "spacing_and_layout_discipline": 5,
  "component_consistency": 5,
  "responsiveness_and_adaptability": 5,
  "implementation_readiness": 5,
  "style_fidelity": 5
}
```

## Judge Notes

### Strengths Of Output A

- Clearer visual direction and stronger surface treatment.
- Layout uses more deliberate grid and spacing signals.
- Responsive intent is visible through media-query and sizing choices.

### Strengths Of Output B

- Clearer visual direction and stronger surface treatment.
- Layout uses more deliberate grid and spacing signals.
- Responsive intent is visible through media-query and sizing choices.

### Deciding Factors

- Heuristic judge compared hierarchy, specificity, spacing, responsiveness, and implementation readiness.
- Mean score delta: 0.5714 in favor of GRIT.

### Risks Or Ambiguities

- This result comes from a local heuristic judge, not a model-as-judge review.
- Use a blind model judge for stronger benchmark credibility.
