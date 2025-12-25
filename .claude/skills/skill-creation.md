# Skill Creation Guide

---
description: Meta-skill for creating new Claude skills for the CCM platform
activation_triggers:
  - "create a new skill"
  - "write a skill"
  - "add a skill for"
  - "skill template"
related_skills: []
---

## When to Use

- Creating a new skill for a recurring CCM workflow
- Documenting expertise that Claude should internalize
- Standardizing how a task should be approached

## When NOT to Use

- One-off tasks (just do them directly)
- Tasks that change frequently (skills should be stable)
- Simple tasks that don't need expertise transfer

## The 4 Core Truths

Every skill must embody these principles:

| Truth | Meaning | Test |
|-------|---------|------|
| **Expertise Transfer, Not Instructions** | Make Claude *think* like an expert | Does it explain *why*, not just *how*? |
| **Flow, Not Friction** | Produce output directly | Does it avoid intermediate steps? |
| **Voice Matches Domain** | Sound like a practitioner | Would a CCM developer say this? |
| **Focused Beats Comprehensive** | Every section earns its place | Can you remove anything? |

## Skill Structure

```markdown
# Skill Name

---
description: One-line description of what this skill does
activation_triggers:
  - "phrase that should activate this skill"
  - "another trigger phrase"
related_skills:
  - other-skill-name
---

## When to Use
- Specific scenario 1
- Specific scenario 2

## When NOT to Use
- Anti-scenario 1 (use X instead)
- Anti-scenario 2 (use Y instead)

## You Are
One paragraph establishing expert identity and what you know.

## [Core Content Sections]
The actual expertise. Use tables, code blocks, specific values.

## Anti-Patterns
| Don't | Why | Do Instead |
|-------|-----|------------|
| Bad pattern | Reason | Good pattern |

## Output
Where/how to produce results.
```

## Writing Guidelines

### Metadata Section

```yaml
---
description: Build browser-based journalism tools  # 10 words max
activation_triggers:
  - "create a new tool"      # Exact phrases users say
  - "build a journalism tool"
  - "add a tool to /tools/"
related_skills:
  - react-components         # Skills to chain to
  - report-generator
---
```

### "You Are" Section

Bad (too generic):
> You are an expert developer who can build tools.

Good (specific expertise):
> A CCM developer who has built 8 journalism tools. You know the exact patterns, CDN imports, and design system. You produce working single-file HTML apps that match existing tools perfectly.

### Quantitative Framing

Bad:
> Batch processing saves money.

Good:
> Batch API saves 50%. A 3,600 post analysis costs ~$10-16 total with batching vs. $20-32 real-time.

### Anti-Patterns Table

Always include. Format:

```markdown
| Don't | Why | Do Instead |
|-------|-----|------------|
| Skip checkpointing | Lose progress on API failures | Checkpoint every 10 items |
| Use real-time API for bulk | 2x cost | Use Batch API |
```

## Constraints

- **< 500 lines**: Skills should fit in context without overwhelming
- **No placeholders**: Every value should be specific (colors, paths, costs)
- **Testable claims**: "50% cost savings" not "significant savings"
- **Actionable**: Reader should be able to act immediately

## Skill Quality Checklist

Before finalizing a skill, verify:

- [ ] Metadata has description, triggers, and related skills
- [ ] "When to Use" has 3-5 specific scenarios
- [ ] "When NOT to Use" redirects to correct skill
- [ ] "You Are" establishes specific expertise
- [ ] Code examples are copy-pasteable (real paths, real values)
- [ ] Anti-patterns table exists with at least 3 rows
- [ ] Total length < 500 lines
- [ ] Passes the "would a CCM developer say this?" test

## File Location

Save skills to: `/.claude/skills/[skill-name].md`

Naming convention:
- Lowercase with hyphens: `journalism-tool-builder.md`
- Descriptive but concise: `content-analyzer.md` not `social-media-content-semantic-and-sentiment-analyzer.md`

## Example: Creating a New Skill

If asked to create a skill for "database migrations":

1. **Identify the expertise**: What does a CCM developer know about migrations?
2. **Find the patterns**: Look at existing migration code in the codebase
3. **Extract specific values**: Actual commands, paths, configurations
4. **Write anti-patterns**: What mistakes have been made before?
5. **Test the "You Are"**: Does it sound like someone who's done this?

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Write generic advice | Doesn't transfer expertise | Use specific CCM examples |
| Include everything | Overwhelms context | Focus on what matters most |
| Use vague quantities | Not actionable | "50% savings" not "big savings" |
| Skip "When NOT to Use" | User picks wrong skill | Always redirect to correct skill |
| Write > 500 lines | Degrades performance | Cut ruthlessly |
