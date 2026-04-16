# GRIT [v0.1.0]
> Frontend prompts with character.

GRIT is a modular prompt system for generating frontend work that feels directed, structured, and visually specific.

It is not a component library.
It is not a design system.
It is not a one-style aesthetic pack.

GRIT helps you steer AI away from generic startup UI habits and toward sharper execution.

The user chooses the visual direction.
GRIT enforces the quality of execution.

## Why This Exists
Most AI-generated interfaces collapse into the same defaults:

- soft corners
- safe gradients
- generic hero sections
- weak hierarchy
- visually acceptable but forgettable layouts

GRIT exists to counter that.

It gives you a repeatable way to combine:

- one core behavior override
- one aesthetic direction
- one or two structural rules
- one clear implementation task

The result should feel less auto-generated and more art-directed.

## What Is In This Repo
```text
grit/
├── core/                 # Base instruction layer
├── styles/               # Visual direction modules
├── layouts/              # Composition and spacing modules
├── skills/               # Tool-specific usage guides
└── examples/             # Prompt stacks and comparisons
```

## Quick Start
If you only want the simplest way to try GRIT, do this:

1. Copy [`core/grit.instruction`](/Users/macintoshhd/Documents/grit/core/grit.instruction:1).
2. Pick one file from [`styles/`](/Users/macintoshhd/Documents/grit/styles).
3. Optionally pick one file from [`layouts/`](/Users/macintoshhd/Documents/grit/layouts).
4. Add your task prompt with product context, target screen, stack, and constraints.
5. Generate the screen in your AI coding tool.

That is the whole system.

Base formula:

```text
core/grit.instruction
+ one styles/ module
+ optional one or two layouts/ modules
+ final task prompt
```

## Fastest First Workflow
Use this when you want the shortest path from zero to a stronger result.

### 1. Start with the core
Inject [`core/grit.instruction`](/Users/macintoshhd/Documents/grit/core/grit.instruction:1) as your base instruction or prompt prefix.

This is the non-generic behavior layer.

### 2. Choose a style only if visual direction matters
Pick one module from [`styles/`](/Users/macintoshhd/Documents/grit/styles) when you want the output to clearly feel like something specific.

Use `styles/` when:

- you want a defined aesthetic
- you want stronger visual identity
- you want different prompts to produce meaningfully different looks
- the screen needs tone, mood, or brand character

Examples:

- [`styles/brutalist-button.md`](/Users/macintoshhd/Documents/grit/styles/brutalist-button.md:1)
- [`styles/modern-corporate-landing.md`](/Users/macintoshhd/Documents/grit/styles/modern-corporate-landing.md:1)
- [`styles/swiss-editorial.md`](/Users/macintoshhd/Documents/grit/styles/swiss-editorial.md:1)
- [`styles/glass-product-ui.md`](/Users/macintoshhd/Documents/grit/styles/glass-product-ui.md:1)

### 3. Add a layout module when the issue is structure, not taste
Pick one or two modules from [`layouts/`](/Users/macintoshhd/Documents/grit/layouts) when the main risk is weak composition, spacing, grid logic, or section rhythm.

Use `layouts/` when:

- the output feels visually generic because the structure is weak
- you want stricter control over page composition
- you need denser or cleaner information framing
- the design has the right mood but the wrong layout discipline

Examples:

- [`layouts/hero-composition.md`](/Users/macintoshhd/Documents/grit/layouts/hero-composition.md:1)
- [`layouts/grid-rhythm.md`](/Users/macintoshhd/Documents/grit/layouts/grid-rhythm.md:1)
- [`layouts/dashboard-density.md`](/Users/macintoshhd/Documents/grit/layouts/dashboard-density.md:1)
- [`layouts/form-clarity.md`](/Users/macintoshhd/Documents/grit/layouts/form-clarity.md:1)
- [`layouts/section-transitions.md`](/Users/macintoshhd/Documents/grit/layouts/section-transitions.md:1)

### 4. Finish with a concrete implementation task
Your last block should say exactly what to build.

Include:

- file or screen target
- product context
- user goal
- tech stack
- constraints

Good task framing beats vague prompts like "make it prettier."

## Copy-Paste Starter Stack
This is the fastest usable starting prompt:

```text
First apply the GRIT system instruction from core/grit.instruction.

Apply this style module:
styles/modern-corporate-landing.md

Apply this layout module:
layouts/hero-composition.md

Task:
Implement a responsive marketing homepage for an enterprise analytics platform.

Product context:
The product helps operations leaders monitor supply chain risk and performance.

User goal:
Build trust quickly, explain the product clearly, and drive demo requests.

Tech stack:
Next.js + React + Tailwind CSS

Constraints:
- desktop and mobile support
- strong typography and hierarchy
- avoid generic SaaS landing page patterns
- keep the palette restrained
- output complete usable frontend code
```

## Step-by-Step Usage
If you want a cleaner workflow to follow every time, use this sequence:

1. Decide what kind of screen or component you want to generate.
2. Add [`core/grit.instruction`](/Users/macintoshhd/Documents/grit/core/grit.instruction:1) to your prompt or tool rules.
3. Choose one style module if you want a specific aesthetic.
4. Choose one or two layout modules if you need stronger structure.
5. Write the final task with product context, target file, stack, and constraints.
6. Generate the first version.
7. Refine using direct feedback like "tighten hierarchy," "make spacing more decisive," or "reduce generic card patterns."

Practical rule:

- use `styles/` to control visual direction
- use `layouts/` to control structural discipline
- use both when you want the strongest result

## Simplest Recommended Workflow
If you are new to GRIT, start here:

1. Use the core instruction.
2. Add one style module.
3. Skip layout modules on the first try unless the output needs tighter structure.
4. Generate one screen only.
5. Iterate once or twice with precise feedback.

That will usually teach you the system faster than stacking too many modules immediately.

## End-to-End Example
For a full prompt chain example, start here:

- [`examples/end-to-end-enterprise-homepage.md`](/Users/macintoshhd/Documents/grit/examples/end-to-end-enterprise-homepage.md:1)

For before-vs-after comparison:

- [`examples/before-vs-after.md`](/Users/macintoshhd/Documents/grit/examples/before-vs-after.md:1)

For another complete example:

- [`examples/end-to-end-glass-dashboard.md`](/Users/macintoshhd/Documents/grit/examples/end-to-end-glass-dashboard.md:1)

## Benchmarking GRIT
GRIT now includes a lightweight benchmark kit in [`benchmarks/`](/Users/macintoshhd/Documents/grit/benchmarks).

Use it to measure:

- win rate versus baseline prompts
- average rubric score uplift
- iteration reduction
- acceptance rate
- style differentiation

Start here:

- [`benchmarks/README.md`](/Users/macintoshhd/Documents/grit/benchmarks/README.md:1)
- [`benchmarks/method.md`](/Users/macintoshhd/Documents/grit/benchmarks/method.md:1)
- [`benchmarks/rubric.md`](/Users/macintoshhd/Documents/grit/benchmarks/rubric.md:1)

## Tool Integrations
GRIT includes usage guides for:

- [Claude](/Users/macintoshhd/Documents/grit/skills/claude.md:1)
- [Gemini](/Users/macintoshhd/Documents/grit/skills/gemini.md:1)
- [Cursor](/Users/macintoshhd/Documents/grit/skills/cursor.md:1)

Use these when you want to fit GRIT into a real prompting workflow instead of pasting modules manually each time.

## Use As A Codex Skill
This repo now includes an installable skill:

- [`SKILL.md`](/Users/macintoshhd/Documents/grit/SKILL.md:1)
- [`agents/openai.yaml`](/Users/macintoshhd/Documents/grit/agents/openai.yaml:1)

If you install this repo as a Codex skill, invoke it as `$grit`.

Recommended usage:

1. invoke `$grit`
2. describe the screen or component you want
3. specify a visual direction if you have one
4. include stack and constraints

Example:

```text
Use $grit to implement a responsive pricing page for a B2B security platform.
Visual direction: Swiss editorial with high trust and restrained contrast.
Stack: Next.js + React + Tailwind CSS.
Avoid generic startup sections and keep the layout highly structured.
```

## How To Think About The Modules
Use the modules like layers, not like a giant prompt dump.

- `core/` sets behavior
- `styles/` sets taste
- `layouts/` sets structure
- `examples/` show working combinations
- `skills/` show how to run the system inside specific tools

If the output is too generic:

- strengthen the style module
- add a layout module
- make the task constraints more explicit

If the output is too noisy:

- remove extra modules
- tighten the task
- keep one direction and one structural goal

## Core Principles
- Anti-generic bias over safe defaults
- Strong hierarchy over decorative filler
- Structural clarity over random spacing
- Specific visual direction over interchangeable SaaS aesthetics
- Modularity over one locked house style

## Who This Is For
- frontend engineers using AI to generate screens or components
- designers exploring art-directed prompt workflows
- indie hackers who want more distinctive UI output
- agencies and product teams experimenting with AI-assisted interface generation
- prompt engineers building reusable frontend stacks

## Current Scope
GRIT currently ships with:

- one core instruction
- multiple style modules
- multiple layout modules
- tool integration guides
- end-to-end examples

The repo is focused on becoming easier to use, not just larger.

## Contributing
If you want to add new modules, examples, or workflow improvements, read:

- [`CONTRIBUTING.md`](/Users/macintoshhd/Documents/grit/CONTRIBUTING.md:1)

Strong contributions should be:

- modular
- practical
- visually specific
- easy to reuse
- aligned with the anti-generic thesis

## In One Sentence
GRIT is a prompt stack for making AI-generated frontend work feel intentional instead of default.
