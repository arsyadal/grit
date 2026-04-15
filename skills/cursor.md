# Cursor Integration

## Use Case
Use this workflow when applying GRIT inside Cursor as rules, project instructions, or a recurring prompt prefix for frontend generation.

## Recommended Flow
1. Add `core/grit.instruction` to project rules or use it as a reusable prompt block.
2. Keep style modules in `styles/` ready to paste depending on the screen being built.
3. Pair the prompt with concrete file/task context so Cursor generates code in the right place.
4. Use follow-up prompts to tighten hierarchy, spacing, and component consistency instead of asking for "make it prettier."

## Prompt Stack
```text
Apply the GRIT system instruction.

Apply this style module:
[paste one file from styles/]

Task:
Implement [component/page] in [file/path].
Product context: [what this screen does]
User goal: [what the user needs to achieve]
Tech stack: [React/Next/Tailwind/etc.]
Constraints: [responsive, accessibility, brand, design system]
```

## Good Usage Pattern
```text
Apply the GRIT system instruction and the Modern Corporate Landing module.

Implement the marketing homepage in `src/app/page.tsx`.
Product context: enterprise procurement analytics
User goal: establish trust, show operational depth, and drive demo bookings
Constraints: Next.js, Tailwind, desktop and mobile support
Avoid generic SaaS landing page patterns.
```

## Notes
- Cursor works best when GRIT is combined with exact file targets and implementation constraints.
- Ask for one screen or component at a time if the output starts losing system coherence.
- Use follow-up prompts like "tighten the type hierarchy" or "make the spacing system more decisive" rather than vague aesthetic feedback.
