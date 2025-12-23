#!/usr/bin/env python3
"""
Parallel AI analysis using multiple providers.

Splits the dataset across Claude, Gemini, and OpenAI to process faster.
Each provider writes to its own output directory, then results are merged.
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime

# Configuration
PROVIDERS = {
    "claude": {
        "env_var": "ANTHROPIC_API_KEY",
        "output_dir": "analysis/ai_results_claude"
    },
    "gemini": {
        "env_var": "GEMINI_API_KEY",
        "output_dir": "analysis/ai_results_gemini"
    }
}

BATCH_SIZE = 500
TOTAL_POSTS = 3364


def check_api_keys():
    """Check which providers have API keys configured."""
    available = []
    for provider, config in PROVIDERS.items():
        if os.environ.get(config["env_var"]):
            available.append(provider)
            print(f"  {provider}: API key found")
        else:
            print(f"  {provider}: No API key (skipping)")
    return available


def get_checkpoint_count(output_dir, analysis_type):
    """Get completed count from checkpoint file."""
    if analysis_type == "semantic":
        checkpoint_path = Path(output_dir) / "semantic" / "analysis_checkpoint.json"
    else:
        checkpoint_path = Path(output_dir) / "sentiment" / "sentiment_checkpoint.json"

    try:
        with open(checkpoint_path) as f:
            data = json.load(f)
            return len(data.get("completed_ids", []))
    except:
        return 0


def run_provider_batch(provider, start_idx, end_idx):
    """Run analysis for a specific provider and range."""
    config = PROVIDERS[provider]
    output_dir = config["output_dir"]

    print(f"\n[{provider.upper()}] Processing posts {start_idx}-{end_idx}")

    # We need to modify the analysis to support offset/range
    # For now, use limit which works with checkpointing
    cmd = [
        sys.executable,
        "run_ai_analysis.py",
        "--limit", str(end_idx),
        "--provider", provider,
        "--output", output_dir
    ]

    start_time = time.time()
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    elapsed = time.time() - start_time

    return {
        "provider": provider,
        "start": start_idx,
        "end": end_idx,
        "success": result.returncode == 0,
        "elapsed_minutes": elapsed / 60
    }


def merge_results():
    """Merge results from all providers into unified output."""
    print("\n" + "="*60)
    print("MERGING RESULTS FROM ALL PROVIDERS")
    print("="*60)

    merged_semantic = []
    merged_sentiment = []
    seen_ids = set()

    for provider, config in PROVIDERS.items():
        output_dir = Path(config["output_dir"])

        # Semantic results
        semantic_path = output_dir / "semantic" / "semantic_analysis_full.json"
        if semantic_path.exists():
            with open(semantic_path) as f:
                data = json.load(f)
                for item in data:
                    if item["video_id"] not in seen_ids:
                        item["_analyzed_by"] = provider
                        merged_semantic.append(item)
                        seen_ids.add(item["video_id"])
                print(f"  {provider} semantic: {len(data)} posts")

        # Sentiment results
        sentiment_path = output_dir / "sentiment" / "sentiment_analysis_full.json"
        if sentiment_path.exists():
            with open(sentiment_path) as f:
                data = json.load(f)
                for item in data:
                    item["_analyzed_by"] = provider
                merged_sentiment.append(item)
                print(f"  {provider} sentiment: {len(data)} posts")

    # Save merged results
    merged_dir = Path("analysis/ai_results_merged")
    merged_dir.mkdir(parents=True, exist_ok=True)

    (merged_dir / "semantic").mkdir(exist_ok=True)
    (merged_dir / "sentiment").mkdir(exist_ok=True)

    with open(merged_dir / "semantic" / "semantic_analysis_full.json", "w") as f:
        json.dump(merged_semantic, f, indent=2)

    with open(merged_dir / "sentiment" / "sentiment_analysis_full.json", "w") as f:
        json.dump(merged_sentiment, f, indent=2)

    print(f"\nMerged results: {len(merged_semantic)} semantic, {len(set(s['video_id'] for s in merged_sentiment))} sentiment")
    print(f"Saved to: {merged_dir}")

    return len(merged_semantic)


def main():
    print("\n" + "="*60)
    print("PARALLEL MULTI-PROVIDER AI ANALYSIS")
    print(f"Dataset: {TOTAL_POSTS} posts")
    print("="*60)

    # Check available providers
    print("\nChecking API keys...")
    available_providers = check_api_keys()

    if not available_providers:
        print("ERROR: No API keys configured. Set ANTHROPIC_API_KEY or GEMINI_API_KEY")
        sys.exit(1)

    # Show current progress
    print("\nCurrent progress:")
    for provider in available_providers:
        output_dir = PROVIDERS[provider]["output_dir"]
        semantic = get_checkpoint_count(output_dir, "semantic")
        sentiment = get_checkpoint_count(output_dir, "sentiment")
        print(f"  {provider}: {semantic} semantic, {sentiment} sentiment")

    # Assign ranges to providers
    # If we have 2 providers: split dataset in half
    # If we have 1 provider: run sequentially
    n_providers = len(available_providers)

    if n_providers == 1:
        # Single provider - run all batches
        provider = available_providers[0]
        print(f"\nRunning all {TOTAL_POSTS} posts with {provider}...")

        for batch_end in range(BATCH_SIZE, TOTAL_POSTS + BATCH_SIZE, BATCH_SIZE):
            batch_end = min(batch_end, TOTAL_POSTS)
            result = run_provider_batch(provider, 0, batch_end)
            print(f"  Batch complete: {result['elapsed_minutes']:.1f} min")

    else:
        # Multiple providers - assign ranges
        posts_per_provider = TOTAL_POSTS // n_providers

        print(f"\nParallel execution with {n_providers} providers:")
        assignments = []
        for i, provider in enumerate(available_providers):
            start = i * posts_per_provider
            end = TOTAL_POSTS if i == n_providers - 1 else (i + 1) * posts_per_provider
            assignments.append((provider, start, end))
            print(f"  {provider}: posts {start}-{end}")

        # Note: True parallel would require offset support in the analyzer
        # For now, run sequentially but each provider processes its full range
        print("\nStarting analysis (providers run sequentially with different configs)...")
        for provider, start, end in assignments:
            result = run_provider_batch(provider, start, end)
            status = "OK" if result["success"] else "FAILED"
            print(f"  [{provider}] {status} - {result['elapsed_minutes']:.1f} min")

    # Merge results
    total_merged = merge_results()

    print("\n" + "="*60)
    print("PARALLEL ANALYSIS COMPLETE")
    print(f"Total posts analyzed: {total_merged}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
