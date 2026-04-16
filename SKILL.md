---
name: grit
description: Use when the user wants AI-generated frontend or UI work to feel less generic and more art-directed, with stronger hierarchy, clearer visual direction, sharper composition, and modular prompt guidance. Apply the GRIT workflow for landing pages, dashboards, forms, product screens, and frontend implementation tasks in React, Next.js, Tailwind, or similar stacks.
---

# GRIT Skill

Use this skill for frontend generation tasks where design character matters.

GRIT is a modular prompting workflow:

1. Apply the core behavior override in `core/grit.instruction`.
2. Add one module from `styles/` when the user wants a specific aesthetic.
3. Add one module from `layouts/` when the main problem is structure, spacing, grid logic, or composition.
4. Finish with a concrete implementation task and generate the code directly.

## When to use GRIT

Use this skill when the user wants:

- a landing page, dashboard, form, or screen that should feel designed rather than generic
- stronger hierarchy, typography, and spacing in frontend output
- a clear visual direction such as Swiss, brutalist, glass, or modern corporate
- React, Next.js, Tailwind, or similar frontend code with more intentional UI decisions
- help tightening a generic AI-generated interface

## Working method

Follow this order:

1. Identify the requested visual direction.
If the user does not specify one, choose a clear direction and state it briefly.

2. Read `core/grit.instruction`.
Treat it as the base execution layer.

3. Select modules only as needed.
- Use `styles/` to control taste and aesthetic identity.
- Use `layouts/` to control structural discipline.
- Start with one style and at most one or two layout modules.

4. Keep the prompt concrete.
Include:
- target file or screen
- product context
- user goal
- technical stack
- constraints such as responsiveness, accessibility, or brand tone

5. Produce the frontend output directly.
Prioritize implementation over long explanation unless the user asks for reasoning.

## Module selection guide

Use one file from `styles/` when the user needs visual specificity:

- `styles/modern-corporate-landing.md`
- `styles/swiss-editorial.md`
- `styles/glass-product-ui.md`
- `styles/brutalist-button.md`

Use one or two files from `layouts/` when the user needs stronger structure:

- `layouts/hero-composition.md`
- `layouts/grid-rhythm.md`
- `layouts/dashboard-density.md`
- `layouts/form-clarity.md`
- `layouts/section-transitions.md`

If the user asks for the simplest workflow, use:

- `core/grit.instruction`
- one `styles/` module
- final task prompt

If the output still feels generic, add one `layouts/` module.

## References

Read these only when relevant:

- `README.md` for onboarding and the starter stack
- `examples/end-to-end-enterprise-homepage.md` for a full prompt chain
- `examples/end-to-end-glass-dashboard.md` for another complete example
- `examples/before-vs-after.md` for prompt comparison
- `skills/cursor.md`, `skills/claude.md`, or `skills/gemini.md` for tool-specific usage

## Quality bar

Before finalizing, check:

- the design has a clear visual point of view
- hierarchy is obvious at a glance
- spacing and layout follow a system
- components feel related
- the output avoids generic startup UI defaults

If not, refine before responding.
