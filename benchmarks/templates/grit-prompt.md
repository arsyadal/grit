# GRIT Prompt Template

Use this as the benchmark treatment prompt.

```text
First apply the GRIT system instruction from core/grit.instruction.

Apply this style module:
[choose one file from styles/]

Optional layout module:
[choose one file from layouts/ if needed]

Task:
Create a responsive [screen/component] for [product].

Product context:
[describe what the product does]

User goal:
[describe what the user needs to achieve]

Requirements:
- [requirement 1]
- [requirement 2]
- [requirement 3]

Tech stack:
[React / Next.js / Tailwind / etc.]

Constraints:
- [constraint 1]
- [constraint 2]
- [constraint 3]
- avoid generic UI defaults
```

## Rule

Use the same task content as the baseline run.
Only the prompting method should differ.
