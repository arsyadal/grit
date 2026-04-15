# End-to-End Example: Glass Product Dashboard

This example shows a full GRIT workflow using a more extreme style direction:
- `core/grit.instruction`
- `styles/glass-product-ui.md`
- `layouts/dashboard-density.md`
- `layouts/form-clarity.md`
- a final task prompt

## Scenario
You want an AI model to generate a premium settings and workspace dashboard for an AI collaboration product.

The risk without GRIT:
- flashy but shallow glass effects
- weak hierarchy under translucent layers
- unreadable panels
- generic dashboard cards with no material logic
- a concept-shot aesthetic instead of a usable product UI

## Step 1: Inject The Core
Paste:

```text
[Use the contents of core/grit.instruction]
```

Purpose:
- suppress default generic UI output
- force stronger hierarchy, consistency, and production-minded frontend decisions

## Step 2: Add The Style Module
Paste:

```text
[Use the contents of styles/glass-product-ui.md]
```

Purpose:
- define the material language
- keep the glass treatment premium, restrained, and product-grade

## Step 3: Add Layout Modules
Paste:

```text
[Use the contents of layouts/dashboard-density.md]
```

Then:

```text
[Use the contents of layouts/form-clarity.md]
```

Purpose:
- keep the dashboard information-rich without becoming cluttered
- ensure settings and controls stay understandable under the visual treatment

## Step 4: Final Task Prompt
```text
Create a responsive settings and workspace dashboard for a premium AI collaboration platform.

Context:
- The product helps teams organize agents, conversations, documents, and automations in one workspace.
- The audience includes product teams, operators, and technical managers.
- The interface should feel premium, intelligent, and operationally credible.

Goals:
- Make the dashboard feel high-end and polished
- Preserve strong readability across translucent surfaces
- Make it obvious where users can manage workspace settings, agent controls, usage, and billing

Content requirements:
- Sidebar or top navigation
- Workspace summary panel
- Usage or activity metrics
- Agent management section
- Settings form area
- Billing or plan card

Design constraints:
- Use premium glassmorphism, but keep it restrained
- Avoid neon-heavy concept art aesthetics
- Preserve strong contrast and hierarchy
- Panels, controls, and overlays must feel like one material system
- Dense areas should remain scannable
- Mobile layout must remain practical

Technical constraints:
- Use React + Tailwind CSS
- Output production-usable frontend code
- Keep semantic structure and accessibility intact

After the code, include a short explanation of the material system, hierarchy, and density choices.
```

## Why This Stack Works
- `core` keeps the model from falling into generic UI habits
- `glass-product-ui` defines the visual surface language
- `dashboard-density` protects the interface from becoming empty or noisy
- `form-clarity` keeps controls understandable inside a visually rich UI

## Expected Result
Compared with a default prompt, this stack should produce a dashboard that is:
- more premium
- more coherent
- more readable
- less gimmicky
- stronger in hierarchy
- closer to a real product interface than a concept mockup

## Practical Reuse Pattern
Use this formula:

```text
core instruction
+ one style module
+ one density or composition module
+ one clarity module
+ final task prompt with product context and technical constraints
```

This pattern is useful for visually expressive product UIs that still need to be usable.
