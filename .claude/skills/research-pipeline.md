# Research Pipeline Orchestration

---
description: Orchestrate multi-stage research pipelines from data acquisition to publication
activation_triggers:
  - "run the research pipeline"
  - "process influencer data"
  - "end-to-end analysis"
  - "acquire → analyze → publish"
  - "research workflow"
related_skills:
  - data-scraper
  - content-analyzer
  - video-processor
  - ai-orchestrator
  - report-generator
---

## When to Use

- Running a complete research project from data collection to publication
- Orchestrating multiple stages that must run in sequence
- Need to track costs, progress, and intermediate outputs across stages
- Want idempotent, resumable processing that survives failures

## When NOT to Use

- Single-stage tasks (use the specific skill instead)
- Quick ad-hoc analysis (just run the relevant script directly)
- Building tools for end users (use journalism-tool-builder)

## You Are

A research engineer at CCM who has run the NJ Influencer project end-to-end: 41 influencers, 3,650 posts, $10-16 in AI costs, and a published interactive report. You know which stages depend on which, where failures happen, and how to recover.

## The 5-Stage Pipeline

```
ACQUIRE → PREPARE → PROCESS → PARSE → RENDER
```

| Stage | What | CCM Implementation | Output |
|-------|------|-------------------|--------|
| **Acquire** | Collect raw data | `main.py` scrapers | `output/{influencer}/` |
| **Prepare** | Consolidate & clean | `consolidate.py` | `all_posts.csv` |
| **Process** | AI analysis (expensive) | `run_ai_analysis.py` | `ai_results_*/` |
| **Parse** | Structure results | `batch_analyzer.py` | `consolidated/` |
| **Render** | Generate outputs | `generate_visualizations.py` | `reports/` |

## Critical: Validate Before Automating

Before running any pipeline:

```python
# 1. Test one item manually
sample_post = posts[0]
response = analyze_single_post(sample_post)

# 2. Evaluate output quality
assert response.nj_relevance_score is not None
assert 0 <= response.sentiment_score <= 1
assert response.analysis_confidence > 0.7

# 3. Estimate total cost
estimated_cost = len(posts) * avg_tokens_per_post * price_per_token
print(f"Estimated cost: ${estimated_cost:.2f}")
```

**If manual test fails, fix the prompt/model before scaling.**

## Stage Dependencies

```
┌─────────┐
│ ACQUIRE │ ← Scrape TikTok, Instagram, YouTube
└────┬────┘
     │ Depends on: URLs CSV, API credentials
     ▼
┌─────────┐
│ PREPARE │ ← Parse JSON, consolidate CSVs
└────┬────┘
     │ Depends on: Scraped files exist
     ▼
┌───────────────┐
│ VIDEO PROCESS │ ← Extract audio, transcribe, OCR
└──────┬────────┘
       │ Depends on: Video files exist
       ▼
┌─────────┐
│ PROCESS │ ← AI semantic/sentiment analysis
└────┬────┘
     │ Depends on: Transcripts, OCR text, API keys
     ▼
┌─────────┐
│  PARSE  │ ← Structure and validate JSON
└────┬────┘
     │ Depends on: AI responses complete
     ▼
┌─────────┐
│ RENDER  │ ← Generate charts, reports
└─────────┘
     │ Depends on: Parsed results
```

## State Management Pattern

Use file-system state, not databases:

```
output/
├── Influencer_Name/
│   ├── tiktok/
│   │   ├── video_123.mp4          # Stage: ACQUIRE
│   │   └── video_123.info.json    # Stage: ACQUIRE
│   └── youtube/
│       └── ...
├── analysis/
│   ├── data/
│   │   ├── all_posts.csv          # Stage: PREPARE
│   │   └── influencer_metrics.csv # Stage: PREPARE
│   ├── video_results/
│   │   ├── video_123_transcript.json  # Stage: VIDEO PROCESS
│   │   └── checkpoint.json
│   ├── ai_results_claude/
│   │   ├── semantic_analysis.json     # Stage: PROCESS
│   │   └── checkpoint.json
│   └── consolidated/
│       └── all_analysis.json          # Stage: PARSE
└── reports/
    └── njinfluencers-deploy/
        └── index.html                 # Stage: RENDER
```

**Benefit**: Check completion by file existence. Resume by skipping existing files.

## Cost Tracking

Track costs at each expensive stage:

```python
pipeline_costs = {
    "acquire": {"api_calls": 0, "cost_usd": 0.0},  # Free (scraping)
    "prepare": {"api_calls": 0, "cost_usd": 0.0},  # Free (local)
    "video_process": {
        "whisper_minutes": 0,    # Free if local
        "gemini_ocr_calls": 0,   # ~$0.0001/call
        "cost_usd": 0.0
    },
    "process": {
        "claude_batch_tokens": 0,  # $0.25-1.25/MTok
        "gemini_tokens": 0,        # $0.10-0.40/MTok
        "cost_usd": 0.0
    },
    "render": {"api_calls": 0, "cost_usd": 0.0}  # Free (local)
}
```

**Reality from NJ Influencer project**:
- 3,650 posts analyzed
- ~$10-16 total AI cost (with batch API)
- Video processing: ~$3 Gemini OCR
- Most cost is in PROCESS stage

## Resumability Pattern

Every stage must be idempotent:

```python
def run_stage(stage_name, items, process_fn, checkpoint_path):
    # Load checkpoint
    completed = load_checkpoint(checkpoint_path)

    # Skip already processed
    remaining = [i for i in items if i.id not in completed]

    for item in remaining:
        try:
            result = process_fn(item)
            save_result(item.id, result)
            completed.add(item.id)

            # Checkpoint every 10
            if len(completed) % 10 == 0:
                save_checkpoint(checkpoint_path, completed)
        except Exception as e:
            log_error(item.id, e)
            continue  # Don't fail entire pipeline

    return completed
```

## Running the Full Pipeline

```bash
# Stage 1: Acquire
python main.py --input influencers.csv --output output/

# Stage 2: Prepare
python analysis/consolidate.py --input output/ --output analysis/data/

# Stage 3: Video Processing
python analysis/video_processor/batch_process.py \
  --input output/ --output analysis/video_results/

# Stage 4: Process (AI Analysis)
python analysis/run_ai_analysis.py \
  --input analysis/data/all_posts.csv \
  --provider claude \
  --batch

# Stage 5: Parse & Render
python analysis/generate_visualizations.py \
  --input analysis/consolidated/ \
  --output reports/
```

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Run pipeline without manual test | Waste money on bad prompts | Test 1 item first |
| Skip cost estimation | Surprise bills | Estimate before running |
| Use database for state | Harder to debug/resume | Use filesystem |
| Process all items if one fails | Lose all progress | Checkpoint + continue |
| Run expensive stages in parallel | Can't track costs | Run sequentially |
| Forget to deduplicate inputs | Waste money | Check for duplicate IDs |

## LLM Task Suitability

Before adding AI to a stage, ask:

| Suited for LLM | Not Suited |
|----------------|------------|
| Synthesis across sources | Precise calculation |
| Subjective judgment with criteria | Real-time requirements |
| Batch processing with error tolerance | Perfect accuracy needed |
| Classification/tagging | Structured data transformation |

**Example**: NJ relevance scoring is suited (subjective judgment). Engagement rate calculation is not (use pandas).
