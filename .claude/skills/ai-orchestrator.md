# Multi-Provider AI Orchestrator

---
description: Manage parallel AI analysis across Claude, Gemini, and OpenAI with cost optimization
activation_triggers:
  - "multi-provider analysis"
  - "batch API"
  - "cost optimization"
  - "parallel AI processing"
  - "orchestrate AI providers"
related_skills:
  - content-analyzer
  - research-pipeline
---

## When to Use

- Running large-scale analysis (100+ items) across multiple AI providers
- Need to optimize for cost (batch APIs) or speed (parallel providers)
- Want to merge results from different providers
- Managing retries and checkpoints for expensive API calls

## When NOT to Use

- Small analyses (<100 items)—just use single provider directly
- Need real-time responses—batch APIs take up to 24 hours
- Single-provider is sufficient—don't add complexity

## You Are

An ML engineer at CCM who has processed 3,600+ posts across three providers. You know the exact cost tradeoffs, when batch APIs are worth it, and how to recover from partial failures without re-running everything.

## Provider Characteristics

| Provider | Model | Input $/MTok | Output $/MTok | Speed | Best For |
|----------|-------|--------------|---------------|-------|----------|
| Claude Batch | Haiku 4.5 | $0.25 | $1.25 | <1hr batch | **Default for bulk** |
| Claude Real-time | Haiku 4.5 | $0.50 | $2.50 | ~7s/req | Interactive |
| Gemini | 3 Flash | $0.10 | $0.40 | ~3s/req | Fast screening |
| OpenAI | GPT-5.1 | $2.50 | $10.00 | ~4s/req | Complex cases |

**The math**: Batch API saves 50%. At 3,600 posts × ~500 tokens each:
- Real-time Claude: ~$25
- Batch Claude: ~$12
- Gemini: ~$7
- Mixed strategy: ~$10-16

## Batch API Implementation

```python
import anthropic
import time

client = anthropic.Anthropic()

def run_batch_analysis(posts, analysis_type="semantic"):
    # Build requests (max 100k per batch)
    requests = []
    for post in posts:
        requests.append({
            "custom_id": f"{post['video_id'][:60]}_{analysis_type}",  # Max 64 chars
            "params": {
                "model": "claude-haiku-4-5-20250901",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": build_prompt(post, analysis_type)}]
            }
        })

    # Submit batch
    batch = client.beta.messages.batches.create(requests=requests)
    print(f"Batch {batch.id}: {len(requests)} requests submitted")

    # Poll until complete (typically <1 hour, max 24 hours)
    while True:
        batch = client.beta.messages.batches.retrieve(batch.id)
        counts = batch.request_counts
        print(f"Processing: {counts.processing}, Succeeded: {counts.succeeded}, Failed: {counts.errored}")

        if batch.processing_status == "ended":
            break
        time.sleep(60)

    # Retrieve results
    results = list(client.beta.messages.batches.results(batch.id))
    return results
```

## Parallel Provider Strategy

Run semantic + sentiment in parallel across providers:

```python
import asyncio

async def run_parallel_analysis(posts):
    # Split by provider based on volume
    claude_posts = posts[:1500]   # Batch-optimized
    gemini_posts = posts[1500:2500]  # Fast
    openai_posts = posts[2500:]   # Complex

    # Run in parallel
    results = await asyncio.gather(
        run_claude_batch(claude_posts),
        run_gemini_streaming(gemini_posts),
        run_openai_batch(openai_posts),
    )

    # Merge by video_id
    return merge_results(*results)
```

## Cost Tracking

Track costs in real-time:

```python
cost_tracker = {
    "claude_batch": {"input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0},
    "gemini": {"input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0},
    "openai": {"input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0},
}

def update_cost(provider, usage):
    rates = {
        "claude_batch": (0.25, 1.25),
        "gemini": (0.10, 0.40),
        "openai": (2.50, 10.00),
    }
    input_rate, output_rate = rates[provider]
    cost = (usage.input_tokens * input_rate + usage.output_tokens * output_rate) / 1_000_000
    cost_tracker[provider]["cost_usd"] += cost
    return cost
```

## Retry Strategy

Handle partial failures without re-running everything:

```python
def process_with_retry(batch_results, max_retries=2):
    failed = [r for r in batch_results if r.result.type == "errored"]

    if not failed:
        return batch_results

    for attempt in range(max_retries):
        print(f"Retry attempt {attempt + 1}: {len(failed)} failed requests")

        retry_requests = [
            {"custom_id": r.custom_id, "params": original_params[r.custom_id]}
            for r in failed
        ]

        retry_batch = client.beta.messages.batches.create(requests=retry_requests)
        retry_results = poll_until_complete(retry_batch.id)

        # Merge successful retries
        for r in retry_results:
            if r.result.type == "succeeded":
                batch_results = [
                    r if br.custom_id == r.custom_id else br
                    for br in batch_results
                ]

        failed = [r for r in retry_results if r.result.type == "errored"]
        if not failed:
            break

    return batch_results
```

## Checkpointing

Save progress after each batch completes:

```python
def save_checkpoint(provider, analysis_type, completed_ids, results):
    checkpoint = {
        "provider": provider,
        "analysis_type": analysis_type,
        "completed_ids": list(completed_ids),
        "timestamp": datetime.now().isoformat(),
        "count": len(completed_ids)
    }

    path = f"checkpoint_{provider}_{analysis_type}.json"
    with open(path, "w") as f:
        json.dump(checkpoint, f, indent=2)

    # Also save results incrementally
    results_path = f"results_{provider}_{analysis_type}.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
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
        (claude_results, "claude"),
    ]:
        for r in results:
            video_id = r["video_id"]
            merged[video_id] = {**r, "provider": provider}

    return list(merged.values())
```

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Use real-time API for >100 items | 2x cost | Use Batch API |
| Process without cost estimation | Surprise bills | Estimate first: items × tokens × rate |
| Ignore failed requests | Incomplete data | Implement retry with exponential backoff |
| Re-run entire batch on failure | Waste money | Use checkpoints, retry only failed |
| Mix providers without tracking | Can't analyze cost/quality | Track provider per result |
| Submit >100k requests per batch | API limit | Split into multiple batches |

## Output

Save to `/social-scraper/analysis/`:
```
ai_results_claude/
├── semantic_analysis.json
├── sentiment_analysis.json
└── checkpoint.json
ai_results_gemini/
ai_results_openai/
consolidated/
└── all_analysis.json
processing_summary.json  # Cost tracking
```
