# Parallel AI Content Analysis Orchestrator

---
description: Orchestrate large-scale content analysis across Claude, Gemini, and OpenAI with checkpointing, cost optimization, and result merging
activation_triggers:
  - "parallel AI analysis"
  - "multi-provider content analysis"
  - "batch API analysis"
  - "resume analysis"
  - "merge analysis results"
  - "AI analysis checkpoint"
  - "cost-optimized analysis"
related_skills:
  - ai-orchestrator
  - content-analyzer
  - research-pipeline
---

## When to Use This Skill

- Analyzing 100+ social media posts with semantic and sentiment analysis
- Need to optimize for cost (50% savings via batch APIs) or speed (parallel providers)
- Want to resume interrupted analysis without re-running completed posts
- Merging results from multiple provider runs into unified datasets
- Generating visualizations from AI analysis results
- Troubleshooting failed batches or checkpoint issues

## When NOT to Use

- Small analyses (<50 items)—use single provider with `run_ai_analysis.py` directly
- Need real-time streaming responses—batch APIs are async (up to 24 hours)
- Only one provider is available—parallel processing adds complexity

## You Are

An AI pipeline engineer at CCM who has processed 3,600+ posts across Claude, Gemini, and OpenAI. You understand checkpoint management, batch API mechanics, cost optimization strategies, and how to merge heterogeneous results without data loss.

## Architecture Overview

```
Input: analysis/data/all_posts.csv (from consolidate.py)
  ↓
Single Provider Analysis (run_ai_analysis.py)
  ├→ Claude (Haiku 4.5): Semantic + Sentiment
  ├→ Gemini (3 Flash): Semantic + Sentiment
  └→ OpenAI (GPT-5.1): Semantic + Sentiment
  ↓
Parallel Multi-Provider (run_parallel_analysis.py)
  ├→ Splits dataset across providers
  ├→ Runs each with checkpointing
  └→ Merges results by video_id
  ↓
Output: analysis/ai_results_merged/
  ├→ all_semantic_results.json
  ├→ all_sentiment_results.json
  └→ sentiment_aggregate_stats.json
  ↓
Visualization: generate_visualizations.py
  └→ analysis/figures/*.png
```

## Provider Cost & Speed Characteristics

| Provider | Model | Cost (Real-time) | Cost (Batch) | Speed | Best Use Case |
|----------|-------|------------------|--------------|-------|---------------|
| Claude | Haiku 4.5 | $0.50/$2.50 MTok | $0.25/$1.25 MTok | ~7s/post | **Default for bulk (batch)** |
| Gemini | 3 Flash | $0.10/$0.40 MTok | $0.05/$0.20 MTok | ~3s/post | Fast screening, low budget |
| OpenAI | GPT-5.1 Instant | $2.50/$10.00 MTok | $1.25/$5.00 MTok | ~4s/post | Complex edge cases |

**Cost calculation** (3,600 posts @ ~800 tokens/post):
- Real-time Claude only: ~$35-50
- **Batch Claude only: ~$17-25 (50% savings)**
- Gemini only: ~$3-5
- OpenAI only: ~$15-20
- **Mixed batch strategy: ~$10-16**

## Step 1: Prepare Input Data

All analysis requires consolidated post data first:

```bash
cd /home/user/ccm/social-scraper
source venv/bin/activate

# Consolidate scraped posts into single CSV
python analysis/consolidate.py

# Verify output
ls -lh analysis/data/all_posts.csv
```

**Expected output**: `analysis/data/all_posts.csv` with columns:
- `post_id` (becomes `video_id` in analysis)
- `influencer_name`
- `platform` (tiktok, instagram, youtube)
- `title`, `caption`, `description`
- `duration_seconds`

## Step 2: Single Provider Analysis (Real-time)

For quick testing or single-provider runs:

```bash
# Test with first 50 posts (Claude)
python run_ai_analysis.py \
  --limit 50 \
  --provider claude \
  --output analysis/ai_results_test

# Full run with Gemini (fastest)
python run_ai_analysis.py \
  --limit 0 \
  --provider gemini \
  --output analysis/ai_results_gemini

# Semantic analysis only (faster)
python run_ai_analysis.py \
  --limit 500 \
  --provider claude \
  --semantic-only \
  --output analysis/ai_results_semantic
```

**Parameters**:
- `--limit N`: Analyze first N posts (0 = all)
- `--provider`: claude, gemini, or openai
- `--output DIR`: Output directory
- `--semantic-only`: Skip sentiment analysis
- `--sentiment-only`: Skip semantic analysis
- `--offset N`: Skip first N posts (for manual parallelization)

**Checkpointing**: Progress auto-saved every 10 posts to:
- `analysis/ai_results/semantic/analysis_checkpoint.json`
- `analysis/ai_results/sentiment/sentiment_checkpoint.json`

**Resume interrupted run**: Just re-run same command. Checkpoint is loaded automatically.

## Step 3: Batch API Analysis (50% Cost Savings)

For large datasets, use Claude's Batch API for 50% savings:

```bash
# Submit all posts as batch (async, ~1 hour turnaround)
python run_ai_analysis.py \
  --batch-mode \
  --limit 0 \
  --output analysis/ai_results_batch

# Monitor batch status
python -m analysis.content_analysis.batch_analyzer status --batch-id msgbatch_xxx

# List recent batches
python -m analysis.content_analysis.batch_analyzer list

# Cancel a batch
python -m analysis.content_analysis.batch_analyzer cancel --batch-id msgbatch_xxx
```

**How batch mode works**:
1. Submits semantic + sentiment batches to Claude API
2. Polls every 60 seconds for completion (typically <1 hour)
3. Auto-retrieves results when done
4. Exports to JSON + CSV in output directory

**Batch API limits**:
- Max 100k requests per batch
- Max 256MB per batch
- Results available for 29 days
- Custom IDs must be unique and ≤64 chars

## Step 4: Parallel Multi-Provider Analysis

Split dataset across providers for fastest wall-clock time:

```bash
# Set API keys first
export ANTHROPIC_API_KEY="your-key"
export GEMINI_API_KEY="your-key"
export OPENAI_API_KEY="your-key"

# Run parallel analysis (auto-splits dataset)
python run_parallel_analysis.py
```

**What happens**:
1. **API key detection**: Checks which providers have keys configured
2. **Dataset splitting**: Divides posts evenly across available providers
3. **Sequential execution**: Each provider processes its range (with checkpointing)
4. **Result merging**: Consolidates outputs by `video_id`, avoiding duplicates

**Output structure**:
```
analysis/
├── ai_results_claude/
│   ├── semantic/
│   │   ├── semantic_analysis_full.json
│   │   ├── semantic_analysis_summary.csv
│   │   └── analysis_checkpoint.json
│   └── sentiment/
│       ├── sentiment_analysis_full.json
│       ├── sentiment_summary.csv
│       └── sentiment_checkpoint.json
├── ai_results_gemini/
│   └── (same structure)
├── ai_results_openai/
│   └── (same structure)
└── ai_results_merged/
    ├── all_semantic_results.json
    ├── all_sentiment_results.json
    └── sentiment_aggregate_stats.json
```

## Step 5: Checkpoint Monitoring & Resumption

### Check current progress

```bash
# View checkpoint for Claude semantic analysis
cat analysis/ai_results_claude/semantic/analysis_checkpoint.json | jq '{completed: (.completed_ids | length), total: 3600}'

# View all provider progress
for provider in claude gemini openai; do
  echo "=== $provider ==="
  for type in semantic sentiment; do
    ckpt="analysis/ai_results_$provider/$type/${type}_checkpoint.json"
    if [ -f "$ckpt" ]; then
      count=$(jq '.completed_ids | length' "$ckpt")
      echo "  $type: $count completed"
    fi
  done
done
```

### Resume from checkpoint

**Automatic resumption**: Just re-run the original command. The analyzer:
1. Loads checkpoint file
2. Builds set of completed IDs
3. Skips posts already analyzed
4. Continues from where it stopped

```bash
# This will auto-resume from checkpoint
python run_ai_analysis.py \
  --limit 0 \
  --provider claude \
  --output analysis/ai_results_claude
```

### Manual checkpoint repair

If checkpoint is corrupted or you want to force re-analysis:

```bash
# Delete checkpoint to start fresh
rm analysis/ai_results_claude/semantic/analysis_checkpoint.json

# Or edit checkpoint to remove specific IDs
jq '.completed_ids |= map(select(. != "problematic-video-id"))' \
  analysis/ai_results_claude/semantic/analysis_checkpoint.json > tmp.json
mv tmp.json analysis/ai_results_claude/semantic/analysis_checkpoint.json
```

## Step 6: Result Merging & Deduplication

The merge logic in `run_parallel_analysis.py`:

```python
def merge_results():
    merged_semantic = []
    merged_sentiment = []
    seen_ids = set()

    for provider, config in PROVIDERS.items():
        # Semantic: dedup by video_id (first provider wins)
        semantic_path = config["output_dir"] / "semantic" / "semantic_analysis_full.json"
        if semantic_path.exists():
            data = json.load(open(semantic_path))
            for item in data:
                if item["video_id"] not in seen_ids:
                    item["_analyzed_by"] = provider
                    merged_semantic.append(item)
                    seen_ids.add(item["video_id"])

        # Sentiment: include all (no dedup needed)
        sentiment_path = config["output_dir"] / "sentiment" / "sentiment_analysis_full.json"
        if sentiment_path.exists():
            data = json.load(open(sentiment_path))
            for item in data:
                item["_analyzed_by"] = provider
                merged_sentiment.append(item)

    # Save to analysis/ai_results_merged/
    save_merged_results(merged_semantic, merged_sentiment)
```

**Deduplication strategy**:
- **Semantic**: First provider wins (prevents duplicate topics)
- **Sentiment**: Keep all (allows multi-provider comparison)
- **Tracking**: `_analyzed_by` field added to each result

### Manual merging

If you need to merge results manually:

```bash
cd /home/user/ccm/social-scraper

# Merge semantic results
jq -s 'add | unique_by(.video_id)' \
  analysis/ai_results_*/semantic/semantic_analysis_full.json \
  > analysis/ai_results_merged/semantic/all_semantic_results.json

# Merge sentiment (no dedup)
jq -s 'add' \
  analysis/ai_results_*/sentiment/sentiment_analysis_full.json \
  > analysis/ai_results_merged/sentiment/all_sentiment_results.json
```

## Step 7: CSV Generation & Export

Convert JSON results to analysis-ready CSV:

```python
import pandas as pd
import json

# Load merged semantic results
with open('analysis/ai_results_merged/all_semantic_results.json') as f:
    semantic = json.load(f)

df = pd.DataFrame(semantic)

# Export summary CSV
df[['video_id', 'influencer', 'platform', 'main_topic', 'content_type',
    'nj_relevance_score', 'tone', 'analysis_confidence']].to_csv(
    'analysis/semantic_summary.csv', index=False
)

# Filter to news content
news_df = df[df['content_type'].isin(['news', 'opinion', 'educational'])]
news_df.to_csv('analysis/news_content_only.csv', index=False)

# High NJ relevance posts
local_df = df[df['nj_relevance_score'] >= 0.7]
local_df.to_csv('analysis/high_nj_relevance.csv', index=False)
```

**Pre-built CSV exports**: The analyzers auto-generate:
- `semantic_analysis_summary.csv`: Core fields for each post
- `sentiment_summary.csv`: Sentiment scores and emotions

## Step 8: Visualization Generation

Generate publication-quality charts from analysis results:

```bash
cd /home/user/ccm/social-scraper

# Ensure merged results exist
ls -lh analysis/ai_results_merged/*.json

# Generate all visualizations
python analysis/generate_visualizations.py
```

**Generated charts** (saved to `analysis/figures/`):
- `00_summary_dashboard.png`: Multi-panel overview
- `01_sentiment_distribution.png`: Pie chart of sentiment labels
- `02_emotion_breakdown.png`: Bar chart of primary emotions
- `03_rhetorical_modes.png`: Horizontal bar chart
- `04_influencer_sentiment.png`: Grouped bar (sentiment vs authenticity)
- `05_content_topics.png`: Top 15 topics bar chart
- `06_content_types.png`: Content type distribution pie
- `07_nj_relevance.png`: Histogram + categorical buckets
- `08_sentiment_authenticity.png`: Scatter plot with controversy heatmap
- `09_energy_formality.png`: Side-by-side bar charts

**Customization**: Edit `analysis/generate_visualizations.py` to:
- Change color schemes (modify `PLATFORM_COLORS`, `color_map`)
- Adjust figure sizes (`figsize` parameter)
- Filter data before plotting (`df = df[df['platform'] == 'tiktok']`)
- Export to different formats (change `.png` to `.pdf`, `.svg`)

## Common Workflows

### Workflow 1: Fast 100-post test run

```bash
cd /home/user/ccm/social-scraper
source venv/bin/activate

# Quick test with Gemini (fastest)
python run_ai_analysis.py \
  --provider gemini \
  --limit 100 \
  --output analysis/test_run

# Check results
ls -lh analysis/test_run/semantic/
ls -lh analysis/test_run/sentiment/

# Generate visualizations
python analysis/generate_visualizations.py
```

### Workflow 2: Cost-optimized full analysis (batch)

```bash
# Set API key
export ANTHROPIC_API_KEY="your-key"

# Submit batch (50% savings)
python run_ai_analysis.py \
  --batch-mode \
  --limit 0 \
  --output analysis/ai_results_batch

# Wait for completion (~1 hour)
# Results auto-retrieved and saved

# Generate visualizations
python analysis/generate_visualizations.py
```

### Workflow 3: Speed-optimized parallel run

```bash
# Set all API keys
export ANTHROPIC_API_KEY="your-claude-key"
export GEMINI_API_KEY="your-gemini-key"
export OPENAI_API_KEY="your-openai-key"

# Run parallel (splits dataset automatically)
python run_parallel_analysis.py

# Results auto-merged to analysis/ai_results_merged/

# Generate visualizations
python analysis/generate_visualizations.py
```

### Workflow 4: Resume interrupted analysis

```bash
# Check checkpoint status
cat analysis/ai_results_claude/semantic/analysis_checkpoint.json | jq '.completed_ids | length'
# Output: 1234

# Resume (auto-continues from checkpoint)
python run_ai_analysis.py \
  --provider claude \
  --limit 0 \
  --output analysis/ai_results_claude

# Monitor progress
watch -n 5 'jq ".completed_ids | length" analysis/ai_results_claude/semantic/analysis_checkpoint.json'
```

## Troubleshooting Guide

### Issue: "No API key configured"

**Symptom**: `ERROR: ANTHROPIC_API_KEY not set`

**Solution**:
```bash
# Add to .env file
echo "ANTHROPIC_API_KEY=your-key-here" >> .env

# Or export directly
export ANTHROPIC_API_KEY="sk-ant-..."

# Verify
python -c "import os; print('Found' if os.getenv('ANTHROPIC_API_KEY') else 'Missing')"
```

### Issue: Checkpoint corruption / analysis repeating

**Symptom**: Same posts being analyzed twice, checkpoint not working

**Solution**:
```bash
# Validate checkpoint JSON
jq '.' analysis/ai_results_claude/semantic/analysis_checkpoint.json

# If corrupted, delete and resume will rebuild
rm analysis/ai_results_claude/semantic/analysis_checkpoint.json

# If valid but stuck, check for duplicate IDs
jq '.completed_ids | group_by(.) | map({id: .[0], count: length}) | sort_by(-.count)' \
  analysis/ai_results_claude/semantic/analysis_checkpoint.json
```

### Issue: Batch stuck in "processing" status

**Symptom**: Batch API shows processing for >24 hours

**Solution**:
```bash
# Check batch status
python -m analysis.content_analysis.batch_analyzer status --batch-id msgbatch_xxx

# If expired/stuck, cancel and retry
python -m analysis.content_analysis.batch_analyzer cancel --batch-id msgbatch_xxx

# Check for failed requests in results
python -c "
import anthropic
client = anthropic.Anthropic()
results = list(client.messages.batches.results('msgbatch_xxx'))
errors = [r for r in results if r.result.type == 'errored']
print(f'Failed: {len(errors)}/{len(results)}')
"
```

### Issue: Merge produces no results

**Symptom**: `all_semantic_results.json` is empty or missing

**Solution**:
```bash
# Check individual provider results exist
for provider in claude gemini openai; do
  file="analysis/ai_results_$provider/semantic/semantic_analysis_full.json"
  if [ -f "$file" ]; then
    count=$(jq '. | length' "$file")
    echo "$provider: $count results"
  else
    echo "$provider: MISSING"
  fi
done

# If files exist but merge failed, run manually
python run_parallel_analysis.py  # Re-run merge step
```

### Issue: Visualization fails with KeyError

**Symptom**: `KeyError: 'nj_relevance_score'` or similar

**Solution**:
```bash
# Check data structure
jq '.[0] | keys' analysis/ai_results_merged/all_semantic_results.json

# If fields missing, check which provider produced results
jq '.[0]._analyzed_by' analysis/ai_results_merged/all_semantic_results.json

# Different providers may have different schemas—verify prompts match
```

### Issue: Out of memory during analysis

**Symptom**: Process killed, `MemoryError` in logs

**Solution**:
```bash
# Use offset to process in chunks
python run_ai_analysis.py --offset 0 --limit 500 --output analysis/chunk1
python run_ai_analysis.py --offset 500 --limit 500 --output analysis/chunk2
python run_ai_analysis.py --offset 1000 --limit 500 --output analysis/chunk3

# Then merge chunks manually
jq -s 'add' analysis/chunk*/semantic/semantic_analysis_full.json > merged.json
```

### Issue: Rate limiting errors

**Symptom**: `429 Too Many Requests` or `Rate limit exceeded`

**Solution**:
```bash
# Use batch mode instead (no rate limits)
python run_ai_analysis.py --batch-mode --limit 0

# Or add delay between requests (edit run_ai_analysis.py)
# Add: time.sleep(2)  # between each request

# Or split across providers
python run_parallel_analysis.py  # Spreads load
```

### Issue: Results missing video IDs

**Symptom**: Some posts not in output despite checkpoint showing completion

**Solution**:
```bash
# Cross-check completed IDs vs results
completed=$(jq '.completed_ids' analysis/ai_results_claude/semantic/analysis_checkpoint.json)
results=$(jq 'map(.video_id)' analysis/ai_results_claude/semantic/semantic_analysis_full.json)

# Find missing
comm -23 <(echo "$completed" | jq -r '.[]' | sort) \
         <(echo "$results" | jq -r '.[]' | sort)

# If IDs are missing, checkpoint may have saved but export failed
# Re-run merge: python run_parallel_analysis.py
```

## Cost Estimation

Before running large analyses, estimate costs:

```python
import json

# Load input data
with open('analysis/data/all_posts.csv') as f:
    num_posts = sum(1 for _ in f) - 1  # minus header

# Estimate tokens per post (avg: 600 input, 200 output)
avg_input_tokens = 600
avg_output_tokens = 200

# Calculate costs
providers = {
    'claude_batch': (0.25, 1.25),
    'claude_realtime': (0.50, 2.50),
    'gemini': (0.10, 0.40),
    'openai': (2.50, 10.00),
}

print(f"Analyzing {num_posts} posts:\n")
for name, (input_rate, output_rate) in providers.items():
    input_cost = (num_posts * avg_input_tokens * input_rate) / 1_000_000
    output_cost = (num_posts * avg_output_tokens * output_rate) / 1_000_000
    total = input_cost + output_cost
    print(f"{name:20s}: ${total:.2f}")
```

## Performance Benchmarks

Based on actual 3,600-post analysis:

| Strategy | Wall Clock Time | Total Cost | Cost/Post |
|----------|----------------|------------|-----------|
| Claude batch only | ~1 hour | $17-25 | $0.005-0.007 |
| Gemini realtime only | ~3 hours | $3-5 | $0.001-0.001 |
| OpenAI batch only | ~2 hours | $15-20 | $0.004-0.006 |
| Parallel (C+G+O) | ~1-1.5 hours | $10-16 | $0.003-0.004 |
| Sequential realtime | ~7-8 hours | $35-50 | $0.010-0.014 |

**Recommendation**: For >1000 posts, use Claude batch mode or parallel strategy.

## Advanced: Custom Analysis Prompts

Modify prompts in `analysis/content_analysis/semantic_analyzer.py`:

```python
ANALYSIS_PROMPT = """You are an expert media analyst...

CONTENT TO ANALYZE:
Platform: {platform}
Influencer: {influencer}
Title: {title}
Description: {description}
...

Provide analysis in JSON format:
{{
    "main_topic": "...",
    "subtopics": [...],
    "custom_field": "your_new_field"
}}
"""
```

After editing prompts:
1. Delete old checkpoints (prompts changed, results incompatible)
2. Re-run analysis with new prompts
3. Update CSV export logic if new fields added

## Integration with Existing Tools

### Export to research pipeline

```python
# Load AI analysis results
import pandas as pd
semantic = pd.read_json('analysis/ai_results_merged/all_semantic_results.json')
sentiment = pd.read_json('analysis/ai_results_merged/all_sentiment_results.json')

# Merge with original post data
posts = pd.read_csv('analysis/data/all_posts.csv')
enriched = posts.merge(semantic, left_on='post_id', right_on='video_id')
enriched = enriched.merge(sentiment, on='video_id')

# Export for Tableau/PowerBI
enriched.to_csv('analysis/full_enriched_dataset.csv', index=False)
```

### Feed into report generator

See `report-generator` skill for creating web reports from analysis results.

## References

- **Semantic analyzer**: `/home/user/ccm/social-scraper/analysis/content_analysis/semantic_analyzer.py`
- **Sentiment analyzer**: `/home/user/ccm/social-scraper/analysis/content_analysis/sentiment_analyzer.py`
- **Batch analyzer**: `/home/user/ccm/social-scraper/analysis/content_analysis/batch_analyzer.py`
- **Parallel orchestrator**: `/home/user/ccm/social-scraper/run_parallel_analysis.py`
- **Single provider runner**: `/home/user/ccm/social-scraper/run_ai_analysis.py`
- **Visualization generator**: `/home/user/ccm/social-scraper/analysis/generate_visualizations.py`

## Success Criteria

After running parallel analysis, you should have:
- ✅ `analysis/ai_results_merged/all_semantic_results.json` with 3600+ items
- ✅ `analysis/ai_results_merged/all_sentiment_results.json` with 3600+ items
- ✅ `analysis/figures/` with 10 PNG visualizations
- ✅ Total cost under $20 for full dataset
- ✅ Wall clock time under 2 hours
- ✅ Zero duplicate video_ids in semantic results
- ✅ All providers tracked in `_analyzed_by` field
