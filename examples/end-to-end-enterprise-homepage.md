# End-to-End Example: Enterprise Homepage

This example shows a full GRIT workflow using:
- `core/grit.instruction`
- `styles/modern-corporate-landing.md`
- `layouts/hero-composition.md`
- `layouts/grid-rhythm.md`
- a final task prompt

## Scenario
You want an AI model to generate a homepage for an enterprise procurement analytics platform.

The risk without GRIT:
- generic SaaS hero
- soft cards
- weak hierarchy
- interchangeable social-proof sections
- a visually acceptable but forgettable page

## Step 1: Inject The Core
Paste:

```text
[Use the contents of core/grit.instruction]
```

Purpose:
- override default AI frontend habits
- enforce hierarchy, structure, typography, and anti-generic behavior

## Step 2: Add The Style Module
Paste:

```text
[Use the contents of styles/modern-corporate-landing.md]
```

Purpose:
- define the visual direction as modern corporate
- keep the page premium, restrained, and executive-facing

## Step 3: Add Layout Modules
Paste:

```text
[Use the contents of layouts/hero-composition.md]
```

Then:

```text
[Use the contents of layouts/grid-rhythm.md]
```

Purpose:
- force the opening screen to have a real focal hierarchy
- force the page structure to follow a disciplined grid and spacing rhythm

## Step 4: Final Task Prompt
```text
Create a responsive homepage for an enterprise procurement analytics platform.

Context:
- The product helps procurement and finance teams understand supplier performance, spending concentration, contract exposure, and operational risk.
- The audience is procurement leaders, finance executives, and operations teams at large companies.
- The homepage should communicate trust, clarity, and operational depth.

Goals:
- Establish authority in the first screen
- Show that the product is analytical, credible, and enterprise-ready
- Make the CTA toward booking a demo obvious but not aggressive

Content requirements:
- Hero
- Proof or credibility strip
- Product overview
- Capability grid
- One data-heavy or metrics-driven section
- Final CTA

Design constraints:
- Avoid generic startup landing page patterns
- Avoid decorative gradients that weaken trust
- Typography should carry the design
- Use one restrained accent color only
- Buttons, cards, and data modules must feel like one system
- Desktop and mobile layouts must both feel intentional

Technical constraints:
- Use React + Tailwind CSS
- Output production-usable frontend code
- Keep accessibility and semantic structure intact

After the code, include a short explanation of the hierarchy, grid, and type decisions.
```

## Why This Stack Works
- `core` prevents generic AI behavior
- `style` sets the visual direction
- `layout` modules strengthen structure independently of aesthetic taste
- the final task prompt supplies product context and implementation constraints

## Expected Result
Compared with a default prompt, this stack should produce a homepage that is:
- more specific
- more credible
- more structured
- less template-like
- easier to scan
- stronger in visual hierarchy

## Practical Reuse Pattern
Use this formula:

```text
core instruction
+ one style module
+ one or two layout modules
+ final task prompt with product context and technical constraints
```

This is the basic GRIT stack.
