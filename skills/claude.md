# Claude Integration

## Use Case
Use this workflow when running GRIT inside Claude or Claude Code as a persistent instruction layer before asking for frontend output.

## Recommended Flow
1. Paste `core/grit.instruction` into the system or custom instruction field.
2. Add one relevant module from `styles/` when a specific aesthetic is needed.
3. Write the task prompt with product context, user goal, screen type, and constraints.
4. Ask Claude to explain the layout logic briefly only if needed. Otherwise prioritize direct output.

## Prompt Stack
```text
[System / Custom Instructions]
Paste core/grit.instruction

[Optional Style Module]
Paste one file from styles/

[Task Prompt]
Create a [page/component] for [product/use case].
Goal: [business or UX goal]
Audience: [target user]
Constraints: [tech stack, responsiveness, accessibility, brand notes]
```

## Good Usage Pattern
```text
First apply the GRIT instruction and the Swiss Editorial module.

Now create a responsive landing page for a B2B cybersecurity platform.
Audience: CTOs and security leads
Goal: establish trust and product credibility fast
Stack: React + Tailwind
Keep it sharp, minimal, and executive-facing.
```

## Notes
- Claude tends to respond well to explicit tone and structural constraints.
- If the result becomes too safe, repeat the anti-generic requirement in the task prompt.
- If the result becomes too conceptual, restate that the output must be production-usable frontend code.
