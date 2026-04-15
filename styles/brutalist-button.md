# Brutalist Button Module

Use this prompt after injecting `core/grit.instruction`.

## Intent
Generate a button component with a brutalist interface language: hard edges, obvious contrast, assertive typography, and zero softness unless explicitly requested.

## Prompt Template
```text
Create a brutalist button component for [brand/product/use case].

Requirements:
- Visual direction: neo-brutalist, sharp, editorial, confident
- No soft shadows
- No glass effects
- No pill shapes
- Use hard edges or very small radius only if justified
- Strong border weight
- High contrast between surface, text, and border
- Typography should feel loud, intentional, and slightly raw
- Hover state must feel mechanical and visible, not subtle
- Active state must feel tactile
- Focus state must remain accessible and obvious
- The component should feel designed, not default-browser and not generic Tailwind

Deliver:
- Button component code
- Primary, secondary, and disabled variants
- Hover, active, and focus-visible states
- Short explanation of the visual logic
```

## Output Criteria
- Border, padding, type scale, and interaction states must feel like one system
- The button must still be practical in a real product UI
- The result should look opinionated at a glance

## Notes
If the model starts producing rounded SaaS-style buttons, tighten the prompt with:

```text
Reject soft UI defaults. Prioritize flat planes, hard outlines, rigid spacing, and assertive type hierarchy.
```
