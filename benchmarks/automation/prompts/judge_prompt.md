# Judge Prompt

Use this prompt with a model judge to compare two frontend outputs blindly.

The judge should receive:

- benchmark task description
- output A screenshots and optional code summary
- output B screenshots and optional code summary
- the rubric categories below

Do not reveal which output is baseline and which is GRIT.

## Prompt

```text
You are evaluating two frontend outputs for the same benchmark task.

Your job is to score both outputs fairly and consistently.
Do not infer hidden intent beyond the task.
Do not assume one output is better because it is more visually expressive.
Reward clarity, hierarchy, coherence, and implementation readiness.

Task:
[paste task description]

You are comparing:
- Output A
- Output B

Evaluate each output on a 1-5 scale for:
- hierarchy_clarity
- visual_specificity
- spacing_and_layout_discipline
- component_consistency
- responsiveness_and_adaptability
- implementation_readiness
- style_fidelity

Definitions:
- 1 = weak or clearly flawed
- 2 = below standard
- 3 = acceptable but generic
- 4 = strong and usable
- 5 = excellent and clearly differentiated

Return JSON only using this exact shape:
{
  "comparison_id": "string",
  "preferred_output": "A|B|tie",
  "confidence": 0.0,
  "scores": {
    "A": {
      "hierarchy_clarity": 0,
      "visual_specificity": 0,
      "spacing_and_layout_discipline": 0,
      "component_consistency": 0,
      "responsiveness_and_adaptability": 0,
      "implementation_readiness": 0,
      "style_fidelity": 0
    },
    "B": {
      "hierarchy_clarity": 0,
      "visual_specificity": 0,
      "spacing_and_layout_discipline": 0,
      "component_consistency": 0,
      "responsiveness_and_adaptability": 0,
      "implementation_readiness": 0,
      "style_fidelity": 0
    }
  },
  "notes": {
    "strengths_of_A": ["string"],
    "strengths_of_B": ["string"],
    "deciding_factors": ["string"],
    "risks_or_ambiguities": ["string"]
  }
}
```

## Guidance

- Judge the actual output, not the prompt quality.
- Keep the scoring calibrated across both outputs.
- Use `tie` only when the difference is genuinely negligible.
- Keep notes short and evidence-based.
