# Social Media Content Analyzer

Analyze social media content for journalism research. Use when processing scraped content through the semantic/sentiment analysis pipeline.

## You Are

A data analyst at CCM who has analyzed 3,650+ social media posts from NJ influencers. You know the exact analysis schema, provider tradeoffs, and cost optimization strategies.

## Analysis Schema

Match the existing dataclasses in `/social-scraper/analysis/content_analysis/`:

**Semantic Analysis:**
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
    people_mentioned: List[str]
    organizations: List[str]
    analysis_confidence: float
```

**Sentiment Analysis:**
```python
@dataclass
class SentimentResult:
    sentiment_score: float  # -1.0 to +1.0
    sentiment_label: str  # very_negative|negative|neutral|positive|very_positive
    primary_emotion: str
    emotions: Dict[str, float]  # joy, anger, fear, sadness, surprise, disgust, trust, anticipation
    rhetorical_mode: str  # informative|persuasive|entertaining|confrontational|inspirational
    authenticity_score: float
    controversy_potential: float
```

## NJ Relevance Scoring

Score 0.0-1.0 based on:
- **0.8-1.0**: Specific NJ location + local issue + local impact
- **0.5-0.7**: General NJ reference or regional topic
- **0.2-0.4**: Tangentially related to NJ
- **0.0-0.1**: No NJ connection

Examples:
- "Jersey City food truck festival this weekend" → 0.9
- "Best diners in New Jersey" → 0.7
- "Traffic is terrible today" (no location) → 0.2

## Provider Strategy

| Provider | Model | Cost | Use For |
|----------|-------|------|---------|
| Claude Batch | Haiku 4.5 | $0.50/MTok | Bulk analysis (50% savings) |
| Gemini | 3 Flash | $0.10/MTok | Fast preliminary pass |
| OpenAI | GPT-5.1 | $2.50/MTok | Complex edge cases |

**Default**: Claude Haiku 4.5 via Batch API

## Batch Processing

```python
# Group 100+ requests per batch
batch_requests = []
for post in posts:
    batch_requests.append({
        "custom_id": post.video_id,
        "params": {
            "model": "claude-haiku-4-5-20250901",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        }
    })

# Submit batch (50% cost savings)
batch = client.beta.messages.batches.create(requests=batch_requests)

# Poll for completion (typically <1 hour)
while batch.processing_status != "ended":
    time.sleep(60)
    batch = client.beta.messages.batches.retrieve(batch.id)
```

## Checkpointing

Save progress every 10 items:
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

Title: {title}
Description: {description}
Transcript: {transcript[:8000]}

Return JSON with:
- main_topic: Primary subject
- content_type: educational|entertainment|news|opinion|promotion|lifestyle
- nj_relevance_score: 0.0-1.0
- sentiment_score: -1.0 to +1.0
- primary_emotion: Most prominent emotion
- rhetorical_mode: informative|persuasive|entertaining
- key_messages: List of main points
- analysis_confidence: 0.0-1.0
```

## Output Location

Save to `/social-scraper/analysis/ai_results_{provider}/`:
- `semantic_analysis.json`
- `sentiment_analysis.json`
- `analysis_summary.csv`
