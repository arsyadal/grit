# GRIT [v0.1.0]
> **Frontend prompts with character.**

---

## [!] THE PROBLEM
AI-generated UIs are becoming predictable: rounded corners by default, safe pastels, generic spacing, and interchangeable layouts. Most LLMs are trained toward "safe" design outputs, which leads to interfaces that look clean enough but feel anonymous.

## [x] THE SOLUTION
**GRIT** is a high-precision prompt engine for frontend generation.

It does not lock output into one aesthetic. It gives the user control over direction, whether that is **Neo-Brutalism**, **Glassmorphism**, **Modern Corporate**, **Swiss Typography**, or something else, while forcing the model to execute with sharper decisions, stronger hierarchy, and less generic AI behavior.

GRIT is the controller.
You choose the vibe.
GRIT enforces the execution.

---

## -> REPOSITORY STRUCTURE
```text
grit/
├── core/                 # The "brain" - master instructions that override AI defaults
├── styles/               # Aesthetic modules (Brutalist, Swiss, Glass, Corporate, etc.)
├── layouts/              # Grid, spacing, rhythm, and structural composition rules
├── skills/               # Integrations for Claude Code, Gemini, Cursor, and other tooling
└── examples/             # Before (generic AI) vs after (GRIT-enhanced)
```

## -> CORE PRINCIPLES
GRIT works by injecting strict frontend constraints into the model context:

- **Anti-Generic Bias**  
  Forces the AI away from default Tailwind/Bootstrap-looking patterns and overused visual tropes.

- **Structural Integrity**  
  Defines explicit border weights, spacing scales, layout ratios, and composition rules.

- **Typographic Hierarchy**  
  Hardens decisions around tracking, leading, scale, contrast, and font pairing.

- **User Intent**  
  The user decides the aesthetic direction. GRIT ensures the result still feels deliberate, sharp, and non-generic.

## -> THE GRIT STACK
GRIT works best as a layered prompt stack:

1. `core/grit.instruction`
   This is the base behavior override. It suppresses generic AI frontend habits and enforces hierarchy, typography, structure, and consistency.

2. One style module from `styles/`
   This defines the aesthetic direction.
   Examples:
   - `styles/brutalist-button.md`
   - `styles/modern-corporate-landing.md`
   - `styles/swiss-editorial.md`
   - `styles/glass-product-ui.md`

3. One or two structural modules from `layouts/`
   These tighten composition independently from visual taste.
   Examples:
   - `layouts/hero-composition.md`
   - `layouts/grid-rhythm.md`
   - `layouts/dashboard-density.md`

4. A final task prompt
   This supplies product context, screen goal, content requirements, and technical constraints.

This is the core formula:

```text
core instruction
+ one style module
+ one or two layout modules
+ final task prompt
```

## -> HOW TO USE
### Option 1: The Inject Method
Copy the content of `core/grit.instruction` and use it as a system prompt in Gemini, Claude, Cursor, or other AI coding/design tools.

### Option 2: Style-Specific Generation
Use the modules in `styles/` to generate components or screens with a chosen visual direction.

Example:
`styles/brutalist-button.md`

### Option 3: Full Stack Generation
Use the full GRIT stack for stronger results:

- inject `core/grit.instruction`
- add one module from `styles/`
- add one or two modules from `layouts/`
- finish with a task-specific implementation prompt

See:
`examples/end-to-end-enterprise-homepage.md`

## -> AVAILABLE MODULES
### Core
- `core/grit.instruction`

### Styles
- `styles/brutalist-button.md`
- `styles/modern-corporate-landing.md`
- `styles/swiss-editorial.md`
- `styles/glass-product-ui.md`

### Layouts
- `layouts/hero-composition.md`
- `layouts/grid-rhythm.md`
- `layouts/dashboard-density.md`

### Skills
- `skills/claude.md`
- `skills/gemini.md`
- `skills/cursor.md`

### Examples
- `examples/before-vs-after.md`
- `examples/end-to-end-enterprise-homepage.md`

## -> TOOL INTEGRATIONS
GRIT currently includes workflow guides for:

- Claude / Claude Code
- Gemini
- Cursor

These guides are stored in `skills/` and show how to layer GRIT into real prompting workflows instead of using it as a one-off prompt fragment.

## -> MANIFESTO
AI can generate code.
GRIT pushes it toward intent.

We do not settle for "good enough" generated interfaces.
We want sharper systems, stronger visual character, and output that feels directed rather than auto-completed.

## [!] CONTRIBUTING
Have a style module, layout system, or instruction set that makes AI output better? Open a PR.

Contribution format and review standard:
`CONTRIBUTING.md`

Build with GRIT.
