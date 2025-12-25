# Multi-Provider AI Orchestrator

Manage parallel AI analysis across Claude, Gemini, and OpenAI with cost optimization. Use when running large-scale content analysis.

## You Are

A ML engineer at CCM who has processed 3,600+ posts across three AI providers. You know the exact cost tradeoffs, batch API patterns, and how to merge results efficiently.

## Provider Characteristics

| Provider | Model | Input Cost | Output Cost | Speed | Best For |
|----------|-------|------------|-------------|-------|----------|
| Claude | Haiku 4.5 | $0.50/MTok | $2.50/MTok | ~7s | Nuanced analysis |
| Claude Batch | Haiku 4.5 | $0.25/MTok | $1.25/MTok | <1hr | **Bulk (50% off)** |
| Gemini | 3 Flash | $0.10/MTok | $0.40/MTok | ~3s | Fast screening |
| OpenAI | GPT-5.1 | $2.50/MTok | $10/MTok | ~4s | Structured extraction |

**Default strategy**: Claude Batch API for everything possible.

## Batch API Implementation

```python
import anthropic

client = anthropic.Anthropic()

# Build batch requests
requests = []
for i, post in enumerate(posts):
    requests.append({
        "custom_id": f"post_{post['video_id']}",
        "params": {
            "model": "claude-haiku-4-5-20250901",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": build_prompt(post)}]
        }
    })

# Submit batch
batch = client.beta.messages.batches.create(requests=requests)
print(f"Batch {batch.id} submitted with {len(requests)} requests")

# Poll until complete
while True:
    batch = client.beta.messages.batches.retrieve(batch.id)
    if batch.processing_status == "ended":
        break
    print(f"Status: {batch.request_counts}")
    time.sleep(60)

# Retrieve results
results = list(client.beta.messages.batches.results(batch.id))
```

## Parallel Processing Pattern

Run semantic + sentiment analysis in parallel:
```python
import asyncio

async def run_parallel_analysis(posts):
    # Split workload
    semantic_batch = create_semantic_batch(posts)
    sentiment_batch = create_sentiment_batch(posts)

    # Submit both batches
    semantic_result = await submit_batch(semantic_batch)
    sentiment_result = await submit_batch(sentiment_batch)

    # Wait for both
    semantic_data = await poll_until_complete(semantic_result.id)
    sentiment_data = await poll_until_complete(sentiment_result.id)

    # Merge by video_id
    return merge_results(semantic_data, sentiment_data)
```

## Cost Tracking

Track costs per video:
```python
processing_summary = {
    "total_videos": len(posts),
    "total_input_tokens": 0,
    "total_output_tokens": 0,
    "cost_usd": 0.0,
    "provider_breakdown": {
        "claude_batch": {"videos": 0, "cost": 0.0},
        "gemini": {"videos": 0, "cost": 0.0},
        "openai": {"videos": 0, "cost": 0.0}
    }
}

# Update after each batch
def update_costs(batch_result, provider):
    tokens = batch_result.usage
    if provider == "claude_batch":
        cost = (tokens.input * 0.25 + tokens.output * 1.25) / 1_000_000
    # ... etc
```

## Retry Strategy

Handle failed requests:
```python
def process_with_retry(batch_results):
    failed = [r for r in batch_results if r.result.type == "errored"]

    if failed:
        # Create retry batch with only failed items
        retry_requests = [
            {"custom_id": r.custom_id, "params": original_params[r.custom_id]}
            for r in failed
        ]
        retry_batch = client.beta.messages.batches.create(requests=retry_requests)
        # ... poll and merge
```

## Checkpointing

```python
def save_checkpoint(completed_ids, provider, analysis_type):
    checkpoint = {
        "completed_ids": list(completed_ids),
        "provider": provider,
        "analysis_type": analysis_type,
        "timestamp": datetime.now().isoformat(),
        "total_processed": len(completed_ids)
    }
    path = f"checkpoint_{provider}_{analysis_type}.json"
    with open(path, "w") as f:
        json.dump(checkpoint, f, indent=2)

def load_checkpoint(provider, analysis_type):
    path = f"checkpoint_{provider}_{analysis_type}.json"
    if os.path.exists(path):
        with open(path) as f:
            return set(json.load(f)["completed_ids"])
    return set()
```

## Result Merging

Consolidate results from multiple providers:
```python
def merge_provider_results(claude_results, gemini_results, openai_results):
    merged = {}

    # Priority: Claude > OpenAI > Gemini (for quality)
    for results, provider in [
        (gemini_results, "gemini"),
        (openai_results, "openai"),
        (claude_results, "claude")
    ]:
        for r in results:
            merged[r["video_id"]] = {**r, "provider": provider}

    return list(merged.values())
```

## Output Files

Save to `/social-scraper/analysis/`:
- `ai_results_claude/semantic_analysis.json`
- `ai_results_gemini/semantic_analysis.json`
- `ai_results_openai/semantic_analysis.json`
- `consolidated/all_analysis.json`
- `processing_summary.json`
