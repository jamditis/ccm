#!/usr/bin/env python3
"""
AI-Powered Content Analysis Runner

Uses Claude, Gemini, or OpenAI for semantic and sentiment analysis of NJ influencer content.
Analyzes post titles, descriptions, and captions.

Supports two modes:
- Real-time: Process one at a time with checkpointing (default)
- Batch mode: Submit all to Claude's Batch API for 50% cost savings (--batch-mode)
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add analysis module to path
sys.path.insert(0, str(Path(__file__).parent / "analysis"))
sys.path.insert(0, str(Path(__file__).parent / "analysis" / "content_analysis"))

import pandas as pd
from tqdm import tqdm
import json
from datetime import datetime

from content_analysis.semantic_analyzer import SemanticAnalyzer, ContentAnalysis
from content_analysis.sentiment_analyzer import SentimentAnalyzer


def load_posts(data_dir: str = "analysis/data") -> pd.DataFrame:
    """Load consolidated post data."""
    csv_path = Path(data_dir) / "all_posts.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Run consolidate.py first: {csv_path}")

    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} posts from {csv_path}")
    return df


def prepare_content_for_analysis(df: pd.DataFrame) -> list:
    """Prepare posts for AI analysis."""
    content_list = []

    for _, row in df.iterrows():
        # Combine title and description for analysis
        title = str(row.get('title', '') or row.get('caption', '') or '')
        description = str(row.get('description', '') or '')

        # Skip if no text content
        if not title.strip() and not description.strip():
            continue

        # Handle NaN values for duration
        duration_val = row.get('duration_seconds', 0)
        duration = int(duration_val) if pd.notna(duration_val) else 0

        content_list.append({
            "video_id": str(row.get('post_id', '')),
            "influencer": str(row.get('influencer_name', '')),
            "platform": str(row.get('platform', '')),
            "title": title[:500],  # Truncate for efficiency
            "description": description[:1000],
            "duration": duration,
            "transcript": "",  # We don't have transcripts for all
            "ocr_text": ""
        })

    return content_list


def run_semantic_analysis(
    content_list: list,
    output_dir: str,
    limit: int = 0,
    provider: str = "claude"
):
    """Run semantic analysis on content."""
    print(f"\n{'='*60}")
    print(f"SEMANTIC ANALYSIS (using {provider.upper()})")
    print(f"{'='*60}")

    if limit > 0:
        content_list = content_list[:limit]
        print(f"Analyzing {limit} posts (limited)")
    else:
        print(f"Analyzing all {len(content_list)} posts")

    analyzer = SemanticAnalyzer(provider=provider)

    output_path = Path(output_dir) / "semantic"
    output_path.mkdir(parents=True, exist_ok=True)

    results = analyzer.batch_analyze(content_list, str(output_path))

    print(f"\nSemantic analysis complete: {len(results)} posts analyzed")
    print(f"API calls made: {analyzer.total_api_calls}")

    return results


def run_sentiment_analysis(
    content_list: list,
    output_dir: str,
    limit: int = 0,
    provider: str = "claude"
):
    """Run sentiment analysis on content."""
    print(f"\n{'='*60}")
    print(f"SENTIMENT ANALYSIS (using {provider.upper()})")
    print(f"{'='*60}")

    if limit > 0:
        content_list = content_list[:limit]

    analyzer = SentimentAnalyzer(provider=provider)

    output_path = Path(output_dir) / "sentiment"
    output_path.mkdir(parents=True, exist_ok=True)

    results = analyzer.batch_analyze(content_list, str(output_path))

    print(f"\nSentiment analysis complete: {len(results)} posts analyzed")
    print(f"API calls made: {analyzer.api_calls}")

    return results


def run_batch_analysis(content_list: list, output_dir: str, limit: int = 0):
    """Run batch analysis using Claude's Batch API (50% cost savings)."""
    from content_analysis.batch_analyzer import ClaudeBatchAnalyzer

    print(f"\n{'='*60}")
    print("BATCH ANALYSIS MODE (Claude Haiku 4.5)")
    print("50% cost savings via Anthropic Batch API")
    print(f"{'='*60}")

    if limit > 0:
        content_list = content_list[:limit]
        print(f"Analyzing {limit} posts (limited)")
    else:
        print(f"Analyzing all {len(content_list)} posts")

    analyzer = ClaudeBatchAnalyzer()
    results = analyzer.run_full_batch_analysis(content_list, output_dir)

    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run AI-powered content analysis")
    parser.add_argument("--data-dir", default="analysis/data", help="Data directory")
    parser.add_argument("--output", default="analysis/ai_results", help="Output directory")
    parser.add_argument("--offset", type=int, default=0, help="Skip first N posts (for parallel processing)")
    parser.add_argument("--limit", type=int, default=50, help="Limit posts to analyze (0=all)")
    parser.add_argument("--provider", default="claude", choices=["claude", "gemini", "openai"])
    parser.add_argument("--semantic-only", action="store_true", help="Only run semantic analysis")
    parser.add_argument("--sentiment-only", action="store_true", help="Only run sentiment analysis")
    parser.add_argument("--batch-mode", action="store_true",
                        help="Use Claude Batch API for 50% cost savings (async, ~1hr)")

    args = parser.parse_args()

    # Load data
    df = load_posts(args.data_dir)
    content_list = prepare_content_for_analysis(df)
    total_posts = len(content_list)
    print(f"Prepared {total_posts} posts with text content for analysis")

    # Apply offset for parallel processing
    if args.offset > 0:
        content_list = content_list[args.offset:]
        print(f"Skipping first {args.offset} posts (offset), {len(content_list)} remaining")

    # Batch mode (Claude only, 50% cost savings)
    if args.batch_mode:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("ERROR: ANTHROPIC_API_KEY required for batch mode")
            sys.exit(1)
        run_batch_analysis(content_list, args.output, args.limit)
        return

    # Real-time mode - check API key
    if args.provider == "claude":
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("ERROR: ANTHROPIC_API_KEY not set")
            sys.exit(1)
        print(f"Using Claude (Anthropic API)")
    elif args.provider == "gemini":
        if not os.environ.get("GEMINI_API_KEY"):
            print("ERROR: GEMINI_API_KEY not set")
            sys.exit(1)
        print(f"Using Gemini 3 Flash (Google API)")
    elif args.provider == "openai":
        if not os.environ.get("OPENAI_API_KEY"):
            print("ERROR: OPENAI_API_KEY not set")
            sys.exit(1)
        print(f"Using GPT-5.1 Instant (OpenAI API)")

    # Create output directory
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)

    # Run analyses
    if not args.sentiment_only:
        run_semantic_analysis(content_list, args.output, args.limit, args.provider)

    if not args.semantic_only:
        run_sentiment_analysis(content_list, args.output, args.limit, args.provider)

    print(f"\n{'='*60}")
    print("AI ANALYSIS COMPLETE")
    print(f"{'='*60}")
    print(f"Results saved to: {args.output}")


if __name__ == "__main__":
    main()
