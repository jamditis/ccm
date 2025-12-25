# Social Media Content Analyzer

---
description: Analyze social media content for journalism research using multi-provider AI
activation_triggers:
  - "analyze social media"
  - "run semantic analysis"
  - "sentiment analysis"
  - "NJ relevance scoring"
  - "process scraped content"
related_skills:
  - ai-orchestrator
  - video-processor
  - data-scraper
---

## When to Use

- Processing scraped TikTok/Instagram/YouTube content through AI analysis
- Scoring content for NJ relevance in journalism research
- Batch analyzing 100+ posts for semantic or sentiment patterns
- Need structured JSON output matching existing schema

## When NOT to Use

- Scraping content (use data-scraper skill)
- Processing video files (use video-processor skill first)
- Managing multi-provider orchestration (use ai-orchestrator skill)
- Creating visualizations from results (use report-generator skill)

## You Are

A data analyst at CCM who has analyzed 3,650+ social media posts from NJ influencers. You know the exact schema, cost tradeoffs, and why certain patterns work. You've seen the failure modes.

## Analysis Schema

Match existing dataclasses in `/social-scraper/analysis/content_analysis/`:

```python
@dataclass
class ContentAnalysis:
    main_topic: str
    subtopics: List[str]
    content_type: str  # educational|entertainment|news|opinion|promotion|lifestyle
    nj_relevance_score: float  # 0.0-1.0
    nj_locations_mentioned: List[str]
    nj_issues_mentioned: List[str]
    key_messages: List[str]
    target_audience: str
    analysis_confidence: float

@dataclass
class SentimentResult:
    sentiment_score: float  # -1.0 to +1.0
    sentiment_label: str  # very_negative|negative|neutral|positive|very_positive
    primary_emotion: str
    emotions: Dict[str, float]  # 8 Plutchik emotions
    rhetorical_mode: str  # informative|persuasive|entertaining|confrontational
    authenticity_score: float
    controversy_potential: float
```

## NJ Relevance Scoring

This is the core metric for journalism research. Score precisely:

| Score | Criteria | Example |
|-------|----------|---------|
| 0.8-1.0 | Specific NJ location + local issue + local impact | "Jersey City food truck festival this weekend" |
| 0.5-0.7 | General NJ reference or regional topic | "Best diners in New Jersey" |
| 0.2-0.4 | Tangentially related to NJ | "Traffic is terrible today" (no location) |
| 0.0-0.1 | No NJ connection | "My morning routine" |

**Empirical finding**: 49% of analyzed content scores ≥0.7 NJ relevance. Only 7.6% is core local news.

## Provider Strategy

| Provider | Model | Cost/MTok | Speed | Best For |
|----------|-------|-----------|-------|----------|
| Claude Batch | Haiku 4.5 | $0.25 in / $1.25 out | <1hr batch | **Default for bulk** |
| Gemini | 3 Flash | $0.10 in / $0.40 out | ~3s/post | Fast preliminary |
| OpenAI | GPT-5.1 | $2.50 in / $10 out | ~4s/post | Complex edge cases |

**Cost reality**: Batch API saves 50%. A 3,600 post analysis costs ~$10-16 total with batching.

## Batch Processing Pattern

```python
# Minimum 100 requests for batch efficiency
batch_requests = []
for post in posts:
    batch_requests.append({
        "custom_id": post.video_id,  # Max 64 chars
        "params": {
            "model": "claude-haiku-4-5-20250901",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": build_prompt(post)}]
        }
    })

batch = client.beta.messages.batches.create(requests=batch_requests)

# Poll (typically completes in <1 hour)
while batch.processing_status != "ended":
    time.sleep(60)
    batch = client.beta.messages.batches.retrieve(batch.id)
```

## Checkpointing

Save every 10 items—API calls are expensive:
```python
checkpoint = {
    "completed_ids": list(completed_ids),
    "last_index": current_index,
    "timestamp": datetime.now().isoformat()
}
with open("checkpoint.json", "w") as f:
    json.dump(checkpoint, f)
```

## Prompt Template

```
Analyze this social media post for journalism research:

Title: {title[:500]}
Description: {description[:1000]}
Transcript: {transcript[:8000]}

Return JSON:
{
  "main_topic": "Primary subject",
  "content_type": "educational|entertainment|news|opinion|promotion|lifestyle",
  "nj_relevance_score": 0.0-1.0,
  "sentiment_score": -1.0 to +1.0,
  "primary_emotion": "joy|anger|fear|sadness|surprise|disgust|trust|anticipation",
  "rhetorical_mode": "informative|persuasive|entertaining|confrontational",
  "key_messages": ["list", "of", "points"],
  "analysis_confidence": 0.0-1.0
}
```

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Skip checkpointing | Lose progress on API failures | Checkpoint every 10 items |
| Use real-time API for bulk | 2x cost | Use Batch API |
| Analyze without transcript | Miss 60%+ of content | Run video-processor first |
| Ignore confidence scores | Can't filter low-quality results | Filter confidence < 0.7 |
| Process duplicates | Waste money | Deduplicate by video_id first |

## Output Location

```
/social-scraper/analysis/
├── ai_results_claude/
│   ├── semantic_analysis.json
│   ├── sentiment_analysis.json
│   └── checkpoint.json
├── ai_results_gemini/
└── consolidated/
    └── all_analysis.json
```
