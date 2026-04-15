# Before vs After

This file shows the difference between a default AI frontend prompt and a GRIT-enhanced prompt.

## Example Task
Design a landing page for a digital investment platform.

## Before: Standard AI Prompt
```text
Create a modern responsive landing page for a digital investment platform using React and Tailwind CSS. Include a hero section, features section, testimonials, pricing, and a call to action. Make it clean and visually appealing.
```

## Typical Result
- Rounded everything
- Safe gradients
- Generic card grid
- Predictable hero with centered text and two buttons
- Interchangeable "SaaS startup" aesthetic
- Technically usable, visually forgettable

## After: GRIT-Enhanced Prompt
```text
First apply the GRIT system instruction.

Now create a landing page for a digital investment platform.

Visual direction:
- Modern corporate with editorial restraint
- Premium, high-trust, executive tone

Execution rules:
- Avoid generic startup gradients and soft-card SaaS defaults
- Use a disciplined grid and strong alignment logic
- Establish authority in the first screen
- Make typography do most of the persuasive work
- Keep the palette restrained with one controlled accent
- Prioritize hierarchy, spacing rhythm, and composition over decoration
- Buttons, cards, and data modules must share one design system
- Mobile should feel composed, not collapsed

Deliver full React + Tailwind code with a short explanation of the layout and type logic.
```

## Expected Difference
The GRIT version should:

- feel more directed and less auto-generated
- show stronger hierarchy at a glance
- use spacing more deliberately
- reflect a specific visual point of view
- avoid the visual cliches common in AI-generated frontend work

## Practical Workflow
1. Inject `core/grit.instruction`.
2. Add a style module from `styles/` if needed.
3. Write the task prompt with product context, content goals, and aesthetic direction.
4. Tighten the prompt again if the output starts drifting toward generic patterns.
