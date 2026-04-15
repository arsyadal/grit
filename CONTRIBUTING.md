# Contributing to GRIT

GRIT is not a dump of aesthetic prompt fragments.
Every contribution should make AI-generated frontend output more precise, more intentional, and less generic.

## What Belongs Here
Good contributions:
- new style modules with a clear visual identity
- layout modules that improve structure and hierarchy
- tool integrations that make GRIT easier to use in real workflows
- examples that clearly demonstrate the difference between default AI output and GRIT-guided output
- edits that improve clarity, consistency, and practical usability

Weak contributions:
- vague inspiration language without execution rules
- style prompts that are visually indistinct from existing modules
- generic "make it beautiful" or "make it modern" prompt advice
- examples with no clear before-vs-after value

## Contribution Principles
- Be specific
- Be reusable
- Be structurally useful
- Avoid generic wording
- Prefer prompt constraints over aesthetic fluff

## File Standards
### Style modules in `styles/`
Each file should include:
- title
- intent
- prompt template
- output criteria
- optional notes for tightening the result

### Layout modules in `layouts/`
Each file should include:
- title
- intent
- structural prompt template
- output criteria or checklist
- optional notes for correcting drift

### Tool guides in `skills/`
Each file should include:
- use case
- recommended flow
- prompt stack
- one good usage pattern
- notes about model/tool behavior

### Examples in `examples/`
Each file should include:
- task context
- default prompt
- GRIT-enhanced prompt
- expected difference
- practical workflow or takeaway

## Style Rules for Writing
- Write in direct, practical language
- Keep the tone sharp and controlled
- Avoid generic hype language
- Avoid over-explaining obvious ideas
- Optimize for immediate reuse

## Module Quality Bar
Before opening a PR, check:
- Does this module create a clearer or stronger result?
- Is it materially different from existing files?
- Does it give concrete execution guidance?
- Can another user copy it into a prompt workflow without rewriting half of it?
- Does it strengthen the GRIT thesis instead of diluting it?

## Suggested PR Format
Use this structure in your PR description:

```text
## What changed
[short summary]

## Why it matters
[how this improves GRIT]

## File type
[style module / layout module / skill / example / docs]

## What makes it distinct
[how this differs from existing modules]
```

## Review Standard
PRs should be judged on:
- clarity
- distinctiveness
- practical reuse
- alignment with the repo thesis
- usefulness in real prompting workflows

If a contribution sounds good but executes weakly, it should not be merged.
