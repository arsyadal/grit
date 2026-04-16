# GRIT

> Frontend prompts with character.

GRIT is a modular prompt system for generating frontend work that feels directed, structured, and visually specific.

It is not a component library.  
It is not a design system.  
It is not a one-style aesthetic pack.

GRIT helps you steer AI away from generic startup UI habits and toward sharper execution.

**Quick links:** [Quick Start](#quick-start) • [How It Works](#how-it-works) • [Examples](#examples) • [Benchmarks](#benchmarks) • [Tool Integrations](#tool-integrations) • [Codex Skill](#codex-skill) • [Contributing](#contributing)

## Why GRIT

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
- one concrete implementation task

The user chooses the visual direction.  
GRIT enforces the quality of execution.

## Before / After

**Baseline prompt**

```text
Create a responsive landing page for a B2B security platform using React and Tailwind CSS.
```

**GRIT prompt stack**

```text
core/grit.instruction
+ styles/swiss-editorial.md
+ layouts/hero-composition.md
+ task: implement a responsive landing page for a B2B security platform in React + Tailwind CSS with strong hierarchy, restrained contrast, and no generic startup sections
```

**What should change**

- hierarchy becomes clearer
- layout feels more intentional
- typography has a stronger point of view
- sections feel less template-like
- mobile adapts with structure, not just stacked blocks

## Quick Start

If you only want the fastest path to trying GRIT:

1. Copy [core/grit.instruction](/Users/macintoshhd/Documents/grit/core/grit.instruction:1).
2. Pick one module from [styles/](/Users/macintoshhd/Documents/grit/styles).
3. Optionally pick one or two modules from [layouts/](/Users/macintoshhd/Documents/grit/layouts).
4. Add your task prompt with product context, target screen, stack, and constraints.
5. Generate the screen in your AI coding tool.

Base formula:

```text
core/grit.instruction
+ one styles/ module
+ optional one or two layouts/ modules
+ final task prompt
```

## Copy-Paste Starter Stack

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

## How It Works

Use GRIT like layers, not like one giant prompt dump.

- `core/` sets behavior
- `styles/` sets visual direction
- `layouts/` sets structural discipline
- `examples/` shows working combinations
- `skills/` shows how to use GRIT in specific tools

If the output is too generic:

- strengthen the style module
- add a layout module
- make the task constraints more explicit

If the output is too noisy:

- remove extra modules
- tighten the task
- keep one visual direction and one structural goal

## When To Use `styles/`

Pick one module from [styles/](/Users/macintoshhd/Documents/grit/styles) when you want the output to clearly feel like something specific.

Use `styles/` when:

- you want a defined aesthetic
- you want stronger visual identity
- you want different prompts to produce meaningfully different looks
- the screen needs tone, mood, or brand character

Examples:

- [styles/brutalist-button.md](/Users/macintoshhd/Documents/grit/styles/brutalist-button.md:1)
- [styles/modern-corporate-landing.md](/Users/macintoshhd/Documents/grit/styles/modern-corporate-landing.md:1)
- [styles/swiss-editorial.md](/Users/macintoshhd/Documents/grit/styles/swiss-editorial.md:1)
- [styles/glass-product-ui.md](/Users/macintoshhd/Documents/grit/styles/glass-product-ui.md:1)

## When To Use `layouts/`

Pick one or two modules from [layouts/](/Users/macintoshhd/Documents/grit/layouts) when the main risk is weak composition, spacing, grid logic, or section rhythm.

Use `layouts/` when:

- the output feels generic because the structure is weak
- you want stricter control over page composition
- you need denser or cleaner information framing
- the design has the right mood but the wrong layout discipline

Examples:

- [layouts/hero-composition.md](/Users/macintoshhd/Documents/grit/layouts/hero-composition.md:1)
- [layouts/grid-rhythm.md](/Users/macintoshhd/Documents/grit/layouts/grid-rhythm.md:1)
- [layouts/dashboard-density.md](/Users/macintoshhd/Documents/grit/layouts/dashboard-density.md:1)
- [layouts/form-clarity.md](/Users/macintoshhd/Documents/grit/layouts/form-clarity.md:1)
- [layouts/section-transitions.md](/Users/macintoshhd/Documents/grit/layouts/section-transitions.md:1)

## Recommended Workflow

1. Decide what screen or component you want to generate.
2. Add [core/grit.instruction](/Users/macintoshhd/Documents/grit/core/grit.instruction:1) to your prompt or tool rules.
3. Choose one style module if you want a specific aesthetic.
4. Choose one or two layout modules if you need stronger structure.
5. Write the final task with product context, target file, stack, and constraints.
6. Generate the first version.
7. Refine with specific feedback such as `tighten hierarchy`, `make spacing more decisive`, or `remove generic card patterns`.

Practical rule:

- use `styles/` to control visual direction
- use `layouts/` to control structural discipline
- use both when you want the strongest result

## Examples

Start here if you want end-to-end prompt chains and comparisons:

- [examples/end-to-end-enterprise-homepage.md](/Users/macintoshhd/Documents/grit/examples/end-to-end-enterprise-homepage.md:1)
- [examples/before-vs-after.md](/Users/macintoshhd/Documents/grit/examples/before-vs-after.md:1)
- [examples/end-to-end-glass-dashboard.md](/Users/macintoshhd/Documents/grit/examples/end-to-end-glass-dashboard.md:1)

## Benchmarks

GRIT includes a benchmark kit and an automated benchmark runner in [benchmarks/](/Users/macintoshhd/Documents/grit/benchmarks).

Use it to measure:

- win rate versus baseline prompts
- average rubric score uplift
- iteration reduction
- acceptance rate
- style differentiation
- technical metrics such as Lighthouse and axe

Start here:

- [benchmarks/README.md](/Users/macintoshhd/Documents/grit/benchmarks/README.md:1)
- [benchmarks/method.md](/Users/macintoshhd/Documents/grit/benchmarks/method.md:1)
- [benchmarks/rubric.md](/Users/macintoshhd/Documents/grit/benchmarks/rubric.md:1)
- [benchmarks/automation/README.md](/Users/macintoshhd/Documents/grit/benchmarks/automation/README.md:1)

Current local benchmark snapshot:

- `5` task types
- `3` repeats per task
- `15` automated runs
- `100%` GRIT win rate in the local heuristic benchmark
- `13.33%` average score uplift

This is useful directional evidence, not a final scientific claim. The current automated pipeline still uses local generation and heuristic judging unless you connect a live model provider.

## Tool Integrations

GRIT includes usage guides for:

- [Claude](/Users/macintoshhd/Documents/grit/skills/claude.md:1)
- [Gemini](/Users/macintoshhd/Documents/grit/skills/gemini.md:1)
- [Cursor](/Users/macintoshhd/Documents/grit/skills/cursor.md:1)

Use these when you want GRIT inside a real prompting workflow instead of pasting modules manually each time.

## Codex Skill

This repo includes an installable Codex skill:

- [SKILL.md](/Users/macintoshhd/Documents/grit/SKILL.md:1)
- [agents/openai.yaml](/Users/macintoshhd/Documents/grit/agents/openai.yaml:1)

If you install this repo as a Codex skill, invoke it as `$grit`.

Example:

```text
Use $grit to implement a responsive pricing page for a B2B security platform.
Visual direction: Swiss editorial with high trust and restrained contrast.
Stack: Next.js + React + Tailwind CSS.
Avoid generic startup sections and keep the layout highly structured.
```

## Repo Structure

```text
grit/
├── core/                 # Base instruction layer
├── styles/               # Visual direction modules
├── layouts/              # Composition and spacing modules
├── skills/               # Tool-specific usage guides
├── examples/             # Prompt stacks and comparisons
└── benchmarks/           # Evaluation kit and automation runner
```

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
- a benchmark kit and automation runner

The repo is currently optimized for onboarding, repeatability, and proof of impact.

## Core Principles

- anti-generic bias over safe defaults
- strong hierarchy over decorative filler
- structural clarity over random spacing
- specific visual direction over interchangeable SaaS aesthetics
- modularity over one locked house style

## Contributing

If you want to add new modules, examples, or workflow improvements, read [CONTRIBUTING.md](/Users/macintoshhd/Documents/grit/CONTRIBUTING.md:1).

Strong contributions should be:

- modular
- practical
- visually specific
- easy to reuse
- aligned with the anti-generic thesis

## License

GRIT is released under the terms in [LICENSE](/Users/macintoshhd/Documents/grit/LICENSE:1), if present in this repository.

## In One Sentence

GRIT is a prompt stack for making AI-generated frontend work feel intentional instead of default.
