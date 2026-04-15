# Gemini Integration

## Use Case
Use this workflow when running GRIT inside Gemini through system instructions, Gems, or a structured prompt sequence.

## Recommended Flow
1. Inject `core/grit.instruction` as the main instruction layer.
2. Add one style module from `styles/` if the task requires a defined aesthetic.
3. Provide the task with explicit UX and visual goals.
4. Ask for implementation output first, explanation second.

## Prompt Stack
```text
System Instruction:
Paste core/grit.instruction

Optional Style Layer:
Paste one file from styles/

User Prompt:
Create a [page/component] for [product/use case].
Target outcome: [what the UI needs to achieve]
Visual direction: [style or mood]
Technical constraints: [framework, CSS approach, responsive requirement]
```

## Good Usage Pattern
```text
Apply the GRIT instruction and the Glass Product UI module.

Create a settings dashboard for a premium AI workspace app.
Target outcome: clarity, hierarchy, premium feel
Stack: Next.js + Tailwind
The result must feel product-grade, not like a visual experiment.
```

## Notes
- Gemini benefits from cleanly separated instruction layers.
- Keep the aesthetic direction explicit; otherwise it may drift toward generic modern UI.
- If the output gets verbose, ask Gemini to skip rationale and return code directly.
