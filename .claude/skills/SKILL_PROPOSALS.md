# Claude Skills for CCM Journalism Platform

## Design Philosophy

These skills follow principles from context engineering research and the 4 Core Truths:

| Truth | Implementation |
|-------|---------------|
| **Expertise Transfer** | Each skill positions Claude as a CCM practitioner who has done this work |
| **Flow, Not Friction** | Skills produce output directly—no intermediate planning documents |
| **Voice Matches Domain** | Written as a CCM developer would explain to a colleague |
| **Focused Beats Comprehensive** | Each skill < 500 lines, does one thing excellently |

## Skill Catalog

### Core Development Skills

| Skill | Description | Triggers |
|-------|-------------|----------|
| [journalism-tool-builder](journalism-tool-builder.md) | Browser-based tools (React + Tailwind + html2pdf) | "create a new tool", "build journalism tool" |
| [react-components](react-components.md) | React components for LLM Advisor | "create component", "React pattern" |
| [ci-cd-pipeline](ci-cd-pipeline.md) | GitHub Actions workflow maintenance | "update CI", "add workflow job" |

### Research & Analysis Skills

| Skill | Description | Triggers |
|-------|-------------|----------|
| [research-pipeline](research-pipeline.md) | End-to-end research orchestration | "run pipeline", "acquire → render" |
| [content-analyzer](content-analyzer.md) | Semantic/sentiment analysis with NJ relevance | "analyze content", "sentiment analysis" |
| [ai-orchestrator](ai-orchestrator.md) | Multi-provider AI with cost optimization | "batch API", "parallel providers" |
| [video-processor](video-processor.md) | Transcription + OCR pipeline | "transcribe video", "extract text" |
| [data-scraper](data-scraper.md) | Platform scraper extension | "add scraper", "scrape platform" |

### Output Skills

| Skill | Description | Triggers |
|-------|-------------|----------|
| [report-generator](report-generator.md) | Interactive web reports with Chart.js | "create report", "build dashboard" |

### Meta Skills

| Skill | Description | Triggers |
|-------|-------------|----------|
| [skill-creation](skill-creation.md) | Guide for creating new skills | "create a skill", "skill template" |

## Skill Structure

Every skill follows this format:

```markdown
# Skill Name

---
description: One-line description
activation_triggers:
  - "trigger phrase 1"
  - "trigger phrase 2"
related_skills:
  - other-skill
---

## When to Use
- Scenario 1
- Scenario 2

## When NOT to Use
- Anti-scenario 1 (use X instead)

## You Are
Expert identity paragraph.

## [Core Content]
Tables, code blocks, specific values.

## Anti-Patterns
| Don't | Why | Do Instead |

## Output
Where/how to produce results.
```

## Skill Selection Guide

```
User Request
    │
    ├─► "create/build tool" ──────► journalism-tool-builder
    │
    ├─► "analyze content" ────────► content-analyzer
    │       └─► "batch/cost" ─────► ai-orchestrator
    │
    ├─► "process video" ──────────► video-processor
    │
    ├─► "scrape/extend scraper" ──► data-scraper
    │
    ├─► "create report" ──────────► report-generator
    │
    ├─► "run pipeline" ───────────► research-pipeline
    │
    ├─► "React component" ────────► react-components
    │
    ├─► "CI/CD/workflow" ─────────► ci-cd-pipeline
    │
    └─► "create skill" ───────────► skill-creation
```

## Quality Standards

All skills must pass these checks:

- [ ] Has metadata (description, triggers, related_skills)
- [ ] "When to Use" has 3-5 specific scenarios
- [ ] "When NOT to Use" redirects to correct alternative
- [ ] "You Are" establishes specific CCM expertise
- [ ] Code examples use real paths and values
- [ ] Anti-patterns table has 3+ rows
- [ ] Total length < 500 lines
- [ ] Would a CCM developer recognize this voice?

## Quantitative Reference

From the NJ Influencer research project:

| Metric | Value |
|--------|-------|
| Posts analyzed | 3,650 |
| AI analysis cost | $10-16 (with batch API) |
| Batch API savings | 50% |
| Video processing cost | ~$3 (Gemini OCR) |
| NJ relevance ≥0.7 | 49% of content |
| Core local news | 7.6% of content |
| Self-hosted video budget | 33 MB (8 case studies) |

## Adding New Skills

1. Identify recurring workflow that requires expertise
2. Use [skill-creation](skill-creation.md) guide
3. Follow the structure template
4. Test against real scenario
5. Add to this catalog
