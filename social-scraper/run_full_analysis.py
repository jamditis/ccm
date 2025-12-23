#!/usr/bin/env python3
"""
Run full AI analysis on all posts with progress tracking.
Processes in batches of 500, using checkpointing to resume.
"""

import subprocess
import sys
import time
from pathlib import Path

BATCH_SIZE = 500
TOTAL_POSTS = 3364

def get_checkpoint_count(checkpoint_path):
    """Get number of completed items from checkpoint."""
    import json
    try:
        with open(checkpoint_path) as f:
            data = json.load(f)
            return len(data.get("completed_ids", []))
    except:
        return 0

def run_batch(limit):
    """Run analysis up to specified limit."""
    print(f"\n{'='*60}")
    print(f"RUNNING ANALYSIS UP TO {limit} POSTS")
    print(f"{'='*60}\n")

    cmd = [
        sys.executable,
        "run_ai_analysis.py",
        "--limit", str(limit),
        "--provider", "claude",
        "--output", "analysis/ai_results"
    ]

    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    return result.returncode == 0

def main():
    print("\n" + "="*60)
    print("FULL DATASET AI ANALYSIS")
    print(f"Processing all {TOTAL_POSTS} posts in batches of {BATCH_SIZE}")
    print("="*60 + "\n")

    # Check current progress
    semantic_checkpoint = Path("analysis/ai_results/semantic/analysis_checkpoint.json")
    sentiment_checkpoint = Path("analysis/ai_results/sentiment/sentiment_checkpoint.json")

    semantic_done = get_checkpoint_count(semantic_checkpoint)
    sentiment_done = get_checkpoint_count(sentiment_checkpoint)

    print(f"Current progress:")
    print(f"  Semantic: {semantic_done} posts")
    print(f"  Sentiment: {sentiment_done} posts")

    # Calculate batches needed
    current = min(semantic_done, sentiment_done)

    # Run batches until complete
    batch_num = (current // BATCH_SIZE) + 1

    while current < TOTAL_POSTS:
        next_limit = min(current + BATCH_SIZE, TOTAL_POSTS)

        print(f"\n--- Batch {batch_num}: Processing up to {next_limit} posts ---")
        start_time = time.time()

        success = run_batch(next_limit)

        elapsed = time.time() - start_time
        print(f"Batch {batch_num} completed in {elapsed/60:.1f} minutes")

        if not success:
            print("ERROR: Batch failed. Check logs.")
            sys.exit(1)

        # Update progress
        current = next_limit
        batch_num += 1

        # Brief pause between batches
        if current < TOTAL_POSTS:
            print("Pausing 10 seconds before next batch...")
            time.sleep(10)

    print("\n" + "="*60)
    print("ALL BATCHES COMPLETE!")
    print(f"Total posts analyzed: {TOTAL_POSTS}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
