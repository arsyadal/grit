# Glass Product UI Module

Use this prompt after injecting `core/grit.instruction`.

## Intent
Generate a glassmorphism-based product UI that feels premium, controlled, and product-grade rather than trendy or overdecorated.

## Prompt Template
```text
Create a glass product UI for [app/product/dashboard/use case].

Visual direction:
- Premium glassmorphism
- Controlled depth
- High clarity
- Product-ready, not concept-art fluff

Requirements:
- Use transparency, blur, layering, and highlights deliberately
- Keep the palette tight and intentional
- Maintain strong text readability and interface clarity
- Glass surfaces should feel engineered, not randomly translucent
- Shadows, borders, glow, and blur must behave like one material system
- Avoid excessive neon, noise, or decorative gradients unless explicitly requested
- The design should still function as a serious UI, not just a Dribbble shot

Component rules:
- Navigation, panels, cards, inputs, and buttons must share one glass language
- Hover and active states should feel polished and tactile
- Focus states must remain obvious and accessible
- Use depth to communicate hierarchy, not just style

Layout rules:
- Preserve strong structure under the visual treatment
- The first screen should establish hierarchy immediately
- Mobile adaptation must simplify the layers without losing the material identity

Deliver:
- Full UI code
- Short explanation of the glass system, color logic, and contrast handling
```

## Output Criteria
- The result should feel expensive, calm, and controlled
- The interface must remain readable and practical
- The glass effect should reinforce hierarchy instead of muddying it

## Notes
If the output becomes too flashy, add:

```text
Reduce trend-driven effects. Keep the glass quieter, denser, and more product-oriented.
```
