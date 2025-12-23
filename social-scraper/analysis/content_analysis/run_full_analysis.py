#!/usr/bin/env python3
"""
Full Content Analysis Pipeline

Master orchestrator that runs all analysis modules and generates
a unified research report.

Usage:
    # Full analysis with all modules
    python run_full_analysis.py path/to/data --output analysis/full_results

    # Skip expensive AI analysis
    python run_full_analysis.py path/to/data --skip-ai

    # Only run specific modules
    python run_full_analysis.py path/to/data --modules engagement trends
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

import pandas as pd


def check_dependencies():
    """Check that required dependencies are installed."""
    missing = []

    required = [
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('tqdm', 'tqdm'),
    ]

    for module, pip_name in required:
        try:
            __import__(module)
        except ImportError:
            missing.append(pip_name)

    if missing:
        print(f"Missing required packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False

    return True


def run_engagement_analysis(data_dir: str, output_dir: str) -> Dict[str, Any]:
    """Run engagement pattern analysis."""
    print("\n" + "="*60)
    print("ENGAGEMENT ANALYSIS")
    print("="*60)

    from engagement_analyzer import EngagementAnalyzer

    analyzer = EngagementAnalyzer()
    df = analyzer.load_data(data_dir)

    profiles = analyzer.calculate_engagement_profiles(df)
    summaries = analyzer.analyze_influencer_patterns(profiles)

    eng_output = Path(output_dir) / "engagement"
    analyzer.generate_report(str(eng_output))

    return {
        "total_profiles": len(profiles),
        "influencers_analyzed": len(summaries),
        "output_dir": str(eng_output)
    }


def run_cross_platform_analysis(data_dir: str, output_dir: str) -> Dict[str, Any]:
    """Run cross-platform analysis."""
    print("\n" + "="*60)
    print("CROSS-PLATFORM ANALYSIS")
    print("="*60)

    from cross_platform import CrossPlatformAnalyzer

    analyzer = CrossPlatformAnalyzer()
    df = analyzer.load_data(data_dir)

    profiles = analyzer.analyze_influencer_cross_platform(df)
    comparison = analyzer.compare_platforms(df)

    cp_output = Path(output_dir) / "cross_platform"
    analyzer.generate_report(str(cp_output))

    return {
        "influencers_analyzed": len(profiles),
        "platforms_compared": len(comparison.platforms_compared),
        "multi_platform_creators": len(comparison.multi_platform_creators),
        "output_dir": str(cp_output)
    }


def run_trend_analysis(data_dir: str, output_dir: str) -> Dict[str, Any]:
    """Run trend detection."""
    print("\n" + "="*60)
    print("TREND DETECTION")
    print("="*60)

    from trend_detector import TrendDetector

    detector = TrendDetector()
    df = detector.load_data(data_dir)

    patterns = detector.detect_temporal_patterns(df)
    trends = detector.detect_content_trends(df)

    trend_output = Path(output_dir) / "trends"
    detector.generate_report(str(trend_output))

    return {
        "temporal_patterns": len(patterns),
        "trends_detected": len(trends),
        "growing_trends": len([t for t in trends if t.current_status == "growing"]),
        "output_dir": str(trend_output)
    }


def run_semantic_analysis(
    processed_dir: str,
    output_dir: str,
    limit: int = 0
) -> Dict[str, Any]:
    """Run AI-powered semantic analysis."""
    print("\n" + "="*60)
    print("SEMANTIC CONTENT ANALYSIS (AI-Powered)")
    print("="*60)

    if not os.environ.get("GEMINI_API_KEY"):
        print("Warning: GEMINI_API_KEY not set. Skipping semantic analysis.")
        return {"skipped": True, "reason": "No API key"}

    from semantic_analyzer import SemanticAnalyzer, load_processed_content

    content = load_processed_content(processed_dir)
    print(f"Found {len(content)} processed videos")

    if limit > 0:
        content = content[:limit]
        print(f"Limited to {limit} videos")

    analyzer = SemanticAnalyzer()
    sem_output = Path(output_dir) / "semantic"
    results = analyzer.batch_analyze(content, str(sem_output))

    return {
        "videos_analyzed": len(results),
        "api_calls": analyzer.total_api_calls,
        "output_dir": str(sem_output)
    }


def run_sentiment_analysis(
    processed_dir: str,
    output_dir: str,
    limit: int = 0
) -> Dict[str, Any]:
    """Run AI-powered sentiment analysis."""
    print("\n" + "="*60)
    print("SENTIMENT & TONE ANALYSIS (AI-Powered)")
    print("="*60)

    if not os.environ.get("GEMINI_API_KEY"):
        print("Warning: GEMINI_API_KEY not set. Skipping sentiment analysis.")
        return {"skipped": True, "reason": "No API key"}

    from sentiment_analyzer import SentimentAnalyzer
    from semantic_analyzer import load_processed_content

    content = load_processed_content(processed_dir)

    if limit > 0:
        content = content[:limit]

    analyzer = SentimentAnalyzer()
    sent_output = Path(output_dir) / "sentiment"
    results = analyzer.batch_analyze(content, str(sent_output))

    return {
        "videos_analyzed": len(results),
        "api_calls": analyzer.api_calls,
        "output_dir": str(sent_output)
    }


def run_topic_modeling(
    data_dir: str,
    output_dir: str
) -> Dict[str, Any]:
    """Run topic modeling with embeddings."""
    print("\n" + "="*60)
    print("TOPIC MODELING (Embeddings + Clustering)")
    print("="*60)

    if not os.environ.get("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not set. Skipping topic modeling.")
        return {"skipped": True, "reason": "No API key"}

    from topic_modeler import TopicModeler

    # Load content
    df = pd.read_csv(Path(data_dir) / "all_posts.csv")

    content_list = []
    for _, row in df.iterrows():
        content_list.append({
            "video_id": str(row.get("post_id", "")),
            "influencer": row.get("influencer_name", ""),
            "platform": row.get("platform", ""),
            "title": row.get("title", "") or row.get("caption", ""),
            "transcript": "",
            "view_count": row.get("view_count", 0),
            "like_count": row.get("like_count", 0),
            "comment_count": row.get("comment_count", 0)
        })

    modeler = TopicModeler()
    topic_output = Path(output_dir) / "topics"
    result = modeler.build_topic_model(content_list, str(topic_output))

    return {
        "num_topics": result.num_topics,
        "videos_clustered": len(result.video_assignments),
        "output_dir": str(topic_output)
    }


def generate_unified_report(
    output_dir: str,
    results: Dict[str, Dict[str, Any]]
):
    """Generate unified research report combining all analyses."""
    output_path = Path(output_dir)

    report = {
        "title": "NJ Influencer Content Analysis Report",
        "generated": datetime.now().isoformat(),
        "modules_run": list(results.keys()),
        "results_summary": results
    }

    # Save JSON summary
    with open(output_path / "analysis_summary.json", "w") as f:
        json.dump(report, f, indent=2)

    # Generate unified markdown report
    with open(output_path / "FULL_ANALYSIS_REPORT.md", "w") as f:
        f.write("# NJ influencer content analysis report\n\n")
        f.write(f"Generated: {report['generated']}\n\n")
        f.write("---\n\n")

        f.write("## Executive summary\n\n")
        f.write("This report provides a comprehensive analysis of content from NJ-based social media influencers.\n\n")

        f.write("### Modules executed\n")
        for module in results.keys():
            f.write(f"- {module.replace('_', ' ').title()}\n")
        f.write("\n")

        f.write("## Analysis results\n\n")

        # Engagement
        if 'engagement' in results:
            eng = results['engagement']
            f.write("### Engagement analysis\n")
            f.write(f"- Profiles analyzed: {eng.get('total_profiles', 'N/A')}\n")
            f.write(f"- Influencers: {eng.get('influencers_analyzed', 'N/A')}\n")
            f.write(f"- Detailed report: `{eng.get('output_dir')}/ENGAGEMENT_REPORT.md`\n\n")

        # Cross-platform
        if 'cross_platform' in results:
            cp = results['cross_platform']
            f.write("### Cross-platform analysis\n")
            f.write(f"- Influencers analyzed: {cp.get('influencers_analyzed', 'N/A')}\n")
            f.write(f"- Platforms compared: {cp.get('platforms_compared', 'N/A')}\n")
            f.write(f"- Multi-platform creators: {cp.get('multi_platform_creators', 'N/A')}\n")
            f.write(f"- Detailed report: `{cp.get('output_dir')}/CROSS_PLATFORM_REPORT.md`\n\n")

        # Trends
        if 'trends' in results:
            tr = results['trends']
            f.write("### Trend analysis\n")
            f.write(f"- Trends detected: {tr.get('trends_detected', 'N/A')}\n")
            f.write(f"- Growing trends: {tr.get('growing_trends', 'N/A')}\n")
            f.write(f"- Detailed report: `{tr.get('output_dir')}/TREND_REPORT.md`\n\n")

        # Semantic
        if 'semantic' in results and not results['semantic'].get('skipped'):
            sem = results['semantic']
            f.write("### Semantic analysis (AI-powered)\n")
            f.write(f"- Videos analyzed: {sem.get('videos_analyzed', 'N/A')}\n")
            f.write(f"- API calls: {sem.get('api_calls', 'N/A')}\n")
            f.write(f"- Detailed results: `{sem.get('output_dir')}`\n\n")

        # Sentiment
        if 'sentiment' in results and not results['sentiment'].get('skipped'):
            sent = results['sentiment']
            f.write("### Sentiment analysis (AI-powered)\n")
            f.write(f"- Videos analyzed: {sent.get('videos_analyzed', 'N/A')}\n")
            f.write(f"- API calls: {sent.get('api_calls', 'N/A')}\n")
            f.write(f"- Detailed results: `{sent.get('output_dir')}`\n\n")

        # Topics
        if 'topics' in results and not results['topics'].get('skipped'):
            top = results['topics']
            f.write("### Topic modeling\n")
            f.write(f"- Topics discovered: {top.get('num_topics', 'N/A')}\n")
            f.write(f"- Videos clustered: {top.get('videos_clustered', 'N/A')}\n")
            f.write(f"- Detailed results: `{top.get('output_dir')}`\n\n")

        f.write("---\n\n")
        f.write("## Next steps\n\n")
        f.write("1. Review individual module reports for detailed findings\n")
        f.write("2. Use exported CSV files in R for advanced statistical analysis\n")
        f.write("3. Generate publication-quality visualizations with ggplot2\n")
        f.write("4. Cross-reference semantic and engagement data for insights\n")

    print(f"\nUnified report saved to {output_path / 'FULL_ANALYSIS_REPORT.md'}")


def main():
    parser = argparse.ArgumentParser(
        description="Run full content analysis pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Full analysis
    python run_full_analysis.py analysis/data --output analysis/results

    # Skip AI (saves API costs)
    python run_full_analysis.py analysis/data --skip-ai

    # Specific modules only
    python run_full_analysis.py analysis/data --modules engagement trends
        """
    )

    parser.add_argument(
        "data_dir",
        help="Directory with consolidated content data (all_posts.csv)"
    )
    parser.add_argument(
        "--output",
        default="analysis/full_analysis_results",
        help="Output directory for results"
    )
    parser.add_argument(
        "--processed-dir",
        help="Directory with processed video results (for AI analysis)"
    )
    parser.add_argument(
        "--skip-ai",
        action="store_true",
        help="Skip AI-powered analyses (semantic, sentiment, topic modeling)"
    )
    parser.add_argument(
        "--modules",
        nargs="+",
        choices=["engagement", "cross_platform", "trends", "semantic", "sentiment", "topics"],
        help="Run only specific modules"
    )
    parser.add_argument(
        "--ai-limit",
        type=int,
        default=0,
        help="Limit number of videos for AI analysis (0=all)"
    )

    args = parser.parse_args()

    if not check_dependencies():
        sys.exit(1)

    # Determine which modules to run
    if args.modules:
        modules = set(args.modules)
    else:
        modules = {"engagement", "cross_platform", "trends"}
        if not args.skip_ai:
            modules.update({"semantic", "sentiment", "topics"})

    # Create output directory
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)

    results = {}

    print("\n" + "="*60)
    print("NJ INFLUENCER CONTENT ANALYSIS")
    print("="*60)
    print(f"Data directory: {args.data_dir}")
    print(f"Output directory: {args.output}")
    print(f"Modules: {', '.join(modules)}")
    print("="*60)

    # Run each module
    if "engagement" in modules:
        try:
            results["engagement"] = run_engagement_analysis(args.data_dir, args.output)
        except Exception as e:
            print(f"Engagement analysis failed: {e}")
            results["engagement"] = {"error": str(e)}

    if "cross_platform" in modules:
        try:
            results["cross_platform"] = run_cross_platform_analysis(args.data_dir, args.output)
        except Exception as e:
            print(f"Cross-platform analysis failed: {e}")
            results["cross_platform"] = {"error": str(e)}

    if "trends" in modules:
        try:
            results["trends"] = run_trend_analysis(args.data_dir, args.output)
        except Exception as e:
            print(f"Trend analysis failed: {e}")
            results["trends"] = {"error": str(e)}

    # AI-powered analyses require processed video directory
    processed_dir = args.processed_dir or "analysis/video_results"

    if "semantic" in modules:
        try:
            results["semantic"] = run_semantic_analysis(
                processed_dir, args.output, args.ai_limit
            )
        except Exception as e:
            print(f"Semantic analysis failed: {e}")
            results["semantic"] = {"error": str(e)}

    if "sentiment" in modules:
        try:
            results["sentiment"] = run_sentiment_analysis(
                processed_dir, args.output, args.ai_limit
            )
        except Exception as e:
            print(f"Sentiment analysis failed: {e}")
            results["sentiment"] = {"error": str(e)}

    if "topics" in modules:
        try:
            results["topics"] = run_topic_modeling(args.data_dir, args.output)
        except Exception as e:
            print(f"Topic modeling failed: {e}")
            results["topics"] = {"error": str(e)}

    # Generate unified report
    generate_unified_report(args.output, results)

    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print(f"Results saved to: {args.output}")
    print(f"Main report: {args.output}/FULL_ANALYSIS_REPORT.md")


if __name__ == "__main__":
    main()
