# Claude Skills for CCM Journalism Platform

## Overview

Based on a comprehensive codebase review, these skills are designed to transfer expert knowledge for the CCM platform workflows, following the 4 Core Truths:

1. **Expertise Transfer, Not Instructions** → Think like a journalism tech expert
2. **Flow, Not Friction** → Produce working code/output directly
3. **Voice Matches Domain** → Sound like a CCM developer, not documentation
4. **Focused Beats Comprehensive** → Each skill does one thing excellently

---

## Skill 1: Social Media Content Analyzer

### Problem It Solves
The semantic and sentiment analysis pipeline in `/social-scraper/analysis/content_analysis/` requires understanding of:
- Multi-provider LLM orchestration (Claude, Gemini, OpenAI)
- Batch API cost optimization (50% savings)
- NJ-specific relevance scoring
- Content type classification for journalism research

### Where Claude Fails Without This Skill
- Doesn't know about the existing ContentAnalysis/SentimentResult dataclasses
- Misses the batch API pattern for 50% cost savings
- Doesn't apply NJ-specific relevance scoring (0-1 scale)
- Creates analysis that doesn't match the research methodology

### Key Expertise to Transfer
```
You are analyzing social media content for journalism research on NJ influencers.

ANALYSIS DIMENSIONS (match existing schema):
- main_topic, content_type (educational|entertainment|news|opinion|promotion|lifestyle)
- nj_relevance_score (0.0-1.0) based on: local mentions, NJ issues, geographic specificity
- sentiment_score (-1 to +1), primary_emotion, authenticity_score
- rhetorical_mode (informative|persuasive|entertaining|confrontational|inspirational)

BATCH API OPTIMIZATION:
- Use Claude Haiku 4.5 for cost efficiency ($0.50/MTok vs $1.00)
- Batch requests in groups of 100+ for 50% cost savings
- Checkpoint every 10 items for resumability

OUTPUT FORMAT:
Match the existing JSON schema in semantic_analyzer.py and sentiment_analyzer.py
```

---

## Skill 2: Journalism Tool Builder

### Problem It Solves
Creating new browser-based journalism tools following the established pattern:
- 8 tools use identical architecture (inline React + Tailwind + html2pdf.js)
- Consistent UX patterns, dark mode, PDF export
- Shared utilities for validation, storage, i18n

### Where Claude Fails Without This Skill
- Creates tools with different architecture than existing ones
- Misses the inline React + Babel CDN pattern
- Forgets shared utilities in `/tools/shared/utils/`
- Doesn't match the visual design system

### Key Expertise to Transfer
```
You are creating a new CCM journalism tool.

ARCHITECTURE (match existing tools):
- Single index.html file with inline React + Babel
- CDN imports: React 18, Tailwind CSS, html2pdf.js, Lucide icons
- No build step required - works directly in browser

TEMPLATE STRUCTURE:
<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tool Name - CCM Journalism Tools</title>
  <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
</head>

REQUIRED FEATURES:
- Dark mode toggle with localStorage persistence
- PDF export via html2pdf.js
- Form validation before export
- Mobile-responsive (16px minimum input font)
- CCM branding colors: primary #CA3553, accent #2A9D8F

SHARED UTILITIES (import from ../shared/utils/):
- darkMode.js: initDarkMode(), toggleDarkMode()
- storage.js: safeGetItem(), safeSetItem()
- validation.js: validateEmail(), validateRequired()
```

---

## Skill 3: Data Scraper Extender

### Problem It Solves
Adding new platform scrapers or extending existing ones following the base scraper pattern in `/social-scraper/scrapers/`.

### Where Claude Fails Without This Skill
- Doesn't inherit from BaseScraper correctly
- Misses rate limiting and error recovery patterns
- Forgets checkpoint system for resumability
- Creates inconsistent output formats

### Key Expertise to Transfer
```
You are extending the social media scraper system.

BASE PATTERN (scrapers/base.py):
class BaseScraper(ABC):
    @abstractmethod
    async def scrape(self, url: str, output_dir: Path) -> dict
    @abstractmethod
    def validate_url(self, url: str) -> bool

IMPLEMENTATION REQUIREMENTS:
- Inherit from BaseScraper
- Implement validate_url() with regex for platform
- Handle rate limits: detect 429, implement exponential backoff
- Save checkpoint after each successful scrape
- Output structure: {platform}/{content_id}.{ext} + metadata.json

OUTPUT METADATA FORMAT:
{
  "post_id": str,
  "platform": str,
  "view_count": int,
  "like_count": int,
  "comment_count": int,
  "caption": str,
  "upload_date": "YYYY-MM-DD",
  "duration_seconds": float (if video)
}

ERROR RECOVERY:
- Log failures to scraping_report.json
- Continue with next item on non-fatal errors
- Retry network errors with exponential backoff (2s, 4s, 8s)
```

---

## Skill 4: Research Report Generator

### Problem It Solves
Creating interactive web reports from analysis data, matching the style of `/social-scraper/reports/njinfluencers-deploy/`.

### Where Claude Fails Without This Skill
- Doesn't match the dark/light theme system
- Misses the animated stat counters
- Forgets Chart.js theme awareness
- Creates static instead of interactive reports

### Key Expertise to Transfer
```
You are generating an interactive research report.

THEME SYSTEM:
CSS custom properties with [data-theme="dark"] selector
--bg, --card, --text, --border variables
Toggle button persists preference to localStorage

STAT COUNTERS:
Animated number counters using JavaScript
Display key metrics prominently at top

CHART.JS INTEGRATION:
- Theme-aware colors that switch with dark mode
- Common chart types: pie (sentiment), bar (topics), scatter (correlations)
- Responsive canvas sizing

REQUIRED SECTIONS:
1. Executive summary with animated stats
2. Methodology description
3. Key findings with visualizations
4. Case studies with embedded content
5. Appendix with raw data access

TYPOGRAPHY:
- Display: Cormorant Garamond
- Body: DM Sans
- Mono: JetBrains Mono
```

---

## Skill 5: Video Processing Pipeline

### Problem It Solves
Processing scraped videos through transcription, frame extraction, and OCR following `/social-scraper/analysis/video_processor/`.

### Where Claude Fails Without This Skill
- Doesn't know the 4-stage pipeline (audio → transcript → frames → OCR)
- Misses Whisper model selection tradeoffs
- Forgets Gemini Vision API for OCR
- Creates inefficient batch processing

### Key Expertise to Transfer
```
You are processing video content for analysis.

4-STAGE PIPELINE:
1. audio_extractor.py: Extract WAV, apply 2x speedup
2. transcriber.py: Whisper transcription (tiny/base/small/medium/large)
3. frame_extractor.py: Extract frames at 1 FPS
4. ocr_processor.py: Gemini Vision API for text extraction

WHISPER MODEL SELECTION:
- tiny: Fastest, lowest quality (development/testing)
- base: Good balance for short content
- small: Production quality for most content
- large: Maximum accuracy (long-form, poor audio)

BATCH CONFIGURATION:
- Process 100 videos per batch
- Track Gemini API costs per video
- Checkpoint after each video
- Resume from checkpoint on restart

OUTPUT PER VIDEO:
{video_name}_transcript.json (segments with timestamps)
{video_name}.srt (subtitle file)
frames/ (PNG images at 1 FPS)
ocr/ (extracted text per frame)
```

---

## Skill 6: Multi-Provider AI Orchestrator

### Problem It Solves
Managing parallel AI analysis across Claude, Gemini, and OpenAI with cost optimization.

### Where Claude Fails Without This Skill
- Doesn't optimize for provider-specific strengths
- Misses batch API opportunities (50% cost savings)
- Creates sequential instead of parallel processing
- Forgets cost tracking and checkpointing

### Key Expertise to Transfer
```
You are orchestrating AI analysis across multiple providers.

PROVIDER CHARACTERISTICS:
| Provider | Model | Cost | Speed | Best For |
|----------|-------|------|-------|----------|
| Claude | Haiku 4.5 | $$ | ~7s | Nuanced analysis, batch |
| Gemini | 3 Flash | $ | ~3s | Fast bulk processing |
| OpenAI | GPT-5.1 | $$$ | ~4s | Structured extraction |

BATCH API STRATEGY (50% savings):
- Group 100+ requests per batch
- Use Anthropic Message Batches API
- Poll for completion (typically <1 hour)
- Retry failed items in separate batch

PARALLEL PROCESSING:
- Run semantic + sentiment in parallel
- Distribute across providers by content volume
- Merge results by video_id

COST OPTIMIZATION:
- Haiku for bulk analysis
- Sonnet only for complex reasoning
- Track costs per video in processing_summary.json

CHECKPOINTING:
- Save completed_ids every 10 items
- Resume from last checkpoint on restart
- Merge partial results from multiple runs
```

---

## Skill 7: React Component Developer

### Problem It Solves
Creating React components for the LLM Advisor and future React tools following established patterns.

### Where Claude Fails Without This Skill
- Doesn't use PropTypes correctly
- Forgets memoization patterns
- Creates class components instead of functional
- Misses the component organization structure

### Key Expertise to Transfer
```
You are developing React components for CCM tools.

COMPONENT STRUCTURE:
/components/
  ComponentName.jsx (one component per file, default export)
  index.js (re-exports all components)

FUNCTIONAL COMPONENT TEMPLATE:
import React, { useState, useMemo, useCallback } from 'react';
import PropTypes from 'prop-types';

function ComponentName({ prop1, prop2, onAction }) {
  const [state, setState] = useState(initialValue);

  const computed = useMemo(() => expensiveCalc(prop1), [prop1]);
  const handleClick = useCallback(() => onAction(state), [state, onAction]);

  return (
    <div className="tailwind-classes">
      {/* JSX */}
    </div>
  );
}

ComponentName.propTypes = {
  prop1: PropTypes.string.isRequired,
  prop2: PropTypes.number,
  onAction: PropTypes.func.isRequired,
};

ComponentName.defaultProps = {
  prop2: 0,
};

export default ComponentName;

PATTERNS:
- Destructure props in function parameters
- Use useMemo for expensive computations
- Use useCallback for event handlers passed to children
- Maximum 300 lines per component
- Mobile-first Tailwind classes
```

---

## Skill 8: CI/CD Pipeline Maintainer

### Problem It Solves
Maintaining and extending the GitHub Actions CI/CD pipeline in `.github/workflows/ci.yml`.

### Where Claude Fails Without This Skill
- Doesn't know existing job structure
- Misses security scanning integration
- Forgets Netlify preview deployment pattern
- Creates redundant or conflicting jobs

### Key Expertise to Transfer
```
You are maintaining the CCM CI/CD pipeline.

EXISTING JOBS:
1. lint-html: proof-html validator for tools/
2. test-llm-advisor: npm ci → lint → test → build → codecov
3. test-social-scraper: pip install → pytest → codecov
4. deploy-preview: Netlify preview on PRs
5. security-scan: Trivy + TruffleHog

JOB DEPENDENCIES:
- deploy-preview needs: lint-html, test-llm-advisor
- Most jobs: continue-on-error: true (non-blocking)

ADDING NEW JOBS:
- Use actions/checkout@v4, actions/setup-node@v4
- Cache dependencies (npm, pip)
- Upload coverage to Codecov
- Non-blocking security scans

SECRETS AVAILABLE:
- GITHUB_TOKEN (automatic)
- NETLIFY_AUTH_TOKEN, NETLIFY_SITE_ID
- CODECOV_TOKEN
```

---

## Implementation Priority

| Skill | Impact | Effort | Priority |
|-------|--------|--------|----------|
| Journalism Tool Builder | High | Medium | 1 |
| Social Media Content Analyzer | High | Medium | 2 |
| Multi-Provider AI Orchestrator | High | High | 3 |
| Research Report Generator | Medium | Medium | 4 |
| React Component Developer | Medium | Low | 5 |
| Data Scraper Extender | Medium | Medium | 6 |
| Video Processing Pipeline | Low | High | 7 |
| CI/CD Pipeline Maintainer | Low | Low | 8 |

---

## Next Steps

1. Review and approve skill priorities
2. Create individual `.md` files in `.claude/skills/` for each approved skill
3. Test each skill on a real scenario
4. Iterate based on feedback
5. Document usage examples
