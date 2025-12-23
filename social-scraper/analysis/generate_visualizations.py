#!/usr/bin/env python3
"""
NJ Influencer Content Analysis - Visualization Generator

Generates publication-quality charts from AI analysis results.
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from collections import Counter
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Output directory
OUTPUT_DIR = Path("analysis/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Platform colors
PLATFORM_COLORS = {
    "tiktok": "#00F2EA",
    "youtube": "#FF0000",
    "instagram": "#E4405F"
}


def load_data():
    """Load all analysis data from merged results."""
    # Try merged data first, fall back to original paths

    # Semantic analysis (merged)
    semantic_merged = Path("analysis/ai_results_merged/all_semantic_results.json")
    semantic_orig = Path("analysis/ai_results/semantic/semantic_analysis_summary.csv")
    if semantic_merged.exists():
        semantic_full = json.load(open(semantic_merged))
        # Create DataFrame for compatibility
        semantic = pd.DataFrame(semantic_full)
    elif semantic_orig.exists():
        semantic = pd.read_csv(semantic_orig)
        semantic_full = json.load(open(Path("analysis/ai_results/semantic/semantic_analysis_full.json")))
    else:
        semantic = None
        semantic_full = None

    # Sentiment analysis (merged)
    sentiment_merged = Path("analysis/ai_results_merged/all_sentiment_results.json")
    sentiment_orig = Path("analysis/ai_results/sentiment/sentiment_summary.csv")
    if sentiment_merged.exists():
        sentiment = pd.DataFrame(json.load(open(sentiment_merged)))
    elif sentiment_orig.exists():
        sentiment = pd.read_csv(sentiment_orig)
    else:
        sentiment = None

    # Aggregate stats (merged)
    sentiment_stats_merged = Path("analysis/ai_results_merged/sentiment_aggregate_stats.json")
    sentiment_stats_orig = Path("analysis/ai_results/sentiment/sentiment_aggregate_stats.json")
    if sentiment_stats_merged.exists():
        sentiment_stats = json.load(open(sentiment_stats_merged))
    elif sentiment_stats_orig.exists():
        sentiment_stats = json.load(open(sentiment_stats_orig))
    else:
        sentiment_stats = None

    return semantic, sentiment, semantic_full, sentiment_stats


def format_number(x):
    """Format large numbers for display."""
    if x >= 1e9:
        return f"{x/1e9:.1f}B"
    elif x >= 1e6:
        return f"{x/1e6:.1f}M"
    elif x >= 1e3:
        return f"{x/1e3:.1f}K"
    return str(int(x))


def create_sentiment_distribution(sentiment_stats):
    """Create sentiment distribution pie chart."""
    fig, ax = plt.subplots(figsize=(10, 8))

    dist = sentiment_stats["overall"]["sentiment_distribution"]
    labels = list(dist.keys())
    sizes = list(dist.values())

    colors = ["#2ecc71", "#27ae60", "#95a5a6", "#e74c3c", "#c0392b"]
    color_map = {
        "very_positive": "#2ecc71",
        "positive": "#27ae60",
        "neutral": "#95a5a6",
        "negative": "#e74c3c",
        "very_negative": "#c0392b"
    }
    colors = [color_map.get(l, "#95a5a6") for l in labels]

    wedges, texts, autotexts = ax.pie(
        sizes, labels=None, autopct='%1.1f%%',
        colors=colors, startangle=90,
        pctdistance=0.75
    )

    # Legend with counts
    legend_labels = [f"{l.replace('_', ' ').title()} ({v})" for l, v in zip(labels, sizes)]
    ax.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(1, 0.5))

    ax.set_title(f"Sentiment distribution\n(n={sentiment_stats['overall']['count']} posts)",
                 fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "01_sentiment_distribution.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("  Created: 01_sentiment_distribution.png")


def create_emotion_breakdown(sentiment_stats):
    """Create primary emotions bar chart."""
    fig, ax = plt.subplots(figsize=(12, 6))

    emotions = sentiment_stats["overall"]["primary_emotions"]
    # Sort by count
    emotions = dict(sorted(emotions.items(), key=lambda x: -x[1]))

    colors = {
        "joy": "#f1c40f",
        "anticipation": "#e67e22",
        "trust": "#3498db",
        "surprise": "#9b59b6",
        "sadness": "#34495e",
        "neutral": "#95a5a6",
        "disgust": "#27ae60",
        "fear": "#e74c3c",
        "anger": "#c0392b"
    }

    bars = ax.bar(
        range(len(emotions)),
        list(emotions.values()),
        color=[colors.get(e, "#95a5a6") for e in emotions.keys()]
    )

    ax.set_xticks(range(len(emotions)))
    ax.set_xticklabels([e.title() for e in emotions.keys()], rotation=45, ha='right')
    ax.set_ylabel("Number of posts")
    ax.set_title("Primary emotions detected in content", fontsize=14, fontweight='bold')

    # Add value labels
    for bar, val in zip(bars, emotions.values()):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
                str(val), ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "02_emotion_breakdown.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("  Created: 02_emotion_breakdown.png")


def create_rhetorical_modes(sentiment_stats):
    """Create rhetorical modes visualization."""
    fig, ax = plt.subplots(figsize=(10, 6))

    modes = sentiment_stats["overall"]["rhetorical_modes"]
    modes = dict(sorted(modes.items(), key=lambda x: -x[1]))

    colors = ["#3498db", "#9b59b6", "#e74c3c", "#f39c12", "#1abc9c"]

    bars = ax.barh(range(len(modes)), list(modes.values()), color=colors[:len(modes)])
    ax.set_yticks(range(len(modes)))
    ax.set_yticklabels([m.title() for m in modes.keys()])
    ax.set_xlabel("Number of posts")
    ax.set_title("Rhetorical modes used by influencers", fontsize=14, fontweight='bold')

    # Add value labels
    for bar, val in zip(bars, modes.values()):
        ax.text(bar.get_width() + 3, bar.get_y() + bar.get_height()/2,
                str(val), ha='left', va='center', fontsize=10)

    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "03_rhetorical_modes.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("  Created: 03_rhetorical_modes.png")


def create_influencer_sentiment(sentiment_stats):
    """Create influencer sentiment comparison."""
    fig, ax = plt.subplots(figsize=(14, 8))

    influencers = sentiment_stats["by_influencer"]
    # Sort by sentiment score
    sorted_inf = sorted(influencers.items(), key=lambda x: x[1]["avg_sentiment"], reverse=True)

    names = [x[0] for x in sorted_inf]
    sentiments = [x[1]["avg_sentiment"] for x in sorted_inf]
    authenticity = [x[1]["avg_authenticity"] for x in sorted_inf]

    x = np.arange(len(names))
    width = 0.35

    bars1 = ax.bar(x - width/2, sentiments, width, label='Sentiment', color='#3498db', alpha=0.8)
    bars2 = ax.bar(x + width/2, authenticity, width, label='Authenticity', color='#2ecc71', alpha=0.8)

    ax.set_ylabel('Score')
    ax.set_title('Sentiment vs authenticity by influencer', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
    ax.legend()
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "04_influencer_sentiment.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("  Created: 04_influencer_sentiment.png")


def create_semantic_topics(semantic_full):
    """Create topic distribution from semantic analysis."""
    if not semantic_full:
        return

    # Count main topics
    topic_counts = Counter()
    for item in semantic_full:
        if "main_topic" in item:
            topic_counts[item["main_topic"]] += 1

    if not topic_counts:
        return

    fig, ax = plt.subplots(figsize=(12, 8))

    # Get top 15 topics
    top_topics = topic_counts.most_common(15)
    topics = [t[0] for t in top_topics]
    counts = [t[1] for t in top_topics]

    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(topics)))

    bars = ax.barh(range(len(topics)), counts, color=colors)
    ax.set_yticks(range(len(topics)))
    ax.set_yticklabels(topics)
    ax.set_xlabel("Number of posts")
    ax.set_title("Top 15 content topics", fontsize=14, fontweight='bold')

    # Add value labels
    for bar, val in zip(bars, counts):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                str(val), ha='left', va='center', fontsize=9)

    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "05_content_topics.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("  Created: 05_content_topics.png")


def create_content_types(semantic_full):
    """Create content type distribution."""
    if not semantic_full:
        return

    # Count content types
    type_counts = Counter()
    for item in semantic_full:
        if "content_type" in item:
            type_counts[item["content_type"]] += 1

    if not type_counts:
        return

    fig, ax = plt.subplots(figsize=(10, 8))

    labels = list(type_counts.keys())
    sizes = list(type_counts.values())

    colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))

    wedges, texts, autotexts = ax.pie(
        sizes, labels=None, autopct='%1.1f%%',
        colors=colors, startangle=90,
        pctdistance=0.75
    )

    legend_labels = [f"{l.replace('_', ' ').title()} ({v})" for l, v in zip(labels, sizes)]
    ax.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(1, 0.5))

    ax.set_title(f"Content types distribution\n(n={len(semantic_full)} posts)",
                 fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "06_content_types.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("  Created: 06_content_types.png")


def create_nj_relevance(semantic_full):
    """Create NJ relevance score distribution."""
    if not semantic_full:
        return

    relevance_scores = [item.get("nj_relevance_score", 0) for item in semantic_full
                        if "nj_relevance_score" in item]

    if not relevance_scores:
        return

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Histogram
    ax1.hist(relevance_scores, bins=20, color='#3498db', edgecolor='white', alpha=0.7)
    ax1.set_xlabel("NJ relevance score")
    ax1.set_ylabel("Number of posts")
    ax1.set_title("Distribution of NJ relevance scores", fontsize=12, fontweight='bold')
    ax1.axvline(x=np.mean(relevance_scores), color='red', linestyle='--',
                label=f'Mean: {np.mean(relevance_scores):.2f}')
    ax1.legend()

    # Buckets
    buckets = {"Low (0-0.3)": 0, "Medium (0.3-0.7)": 0, "High (0.7-1.0)": 0}
    for s in relevance_scores:
        if s < 0.3:
            buckets["Low (0-0.3)"] += 1
        elif s < 0.7:
            buckets["Medium (0.3-0.7)"] += 1
        else:
            buckets["High (0.7-1.0)"] += 1

    colors = ['#e74c3c', '#f39c12', '#2ecc71']
    ax2.bar(buckets.keys(), buckets.values(), color=colors)
    ax2.set_ylabel("Number of posts")
    ax2.set_title("NJ relevance categories", fontsize=12, fontweight='bold')

    # Add value labels
    for i, (k, v) in enumerate(buckets.items()):
        ax2.text(i, v + 2, str(v), ha='center', fontsize=11)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "07_nj_relevance.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("  Created: 07_nj_relevance.png")


def create_sentiment_vs_authenticity(sentiment):
    """Create scatter plot of sentiment vs authenticity."""
    if sentiment is None:
        return

    fig, ax = plt.subplots(figsize=(10, 8))

    scatter = ax.scatter(
        sentiment["sentiment_score"],
        sentiment["authenticity_score"],
        c=sentiment["controversy_potential"],
        cmap='RdYlGn_r',
        alpha=0.6,
        s=50
    )

    plt.colorbar(scatter, label='Controversy potential')
    ax.set_xlabel("Sentiment score")
    ax.set_ylabel("Authenticity score")
    ax.set_title("Sentiment vs authenticity\n(color = controversy potential)",
                 fontsize=14, fontweight='bold')
    ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.3)
    ax.axvline(x=0, color='gray', linestyle='--', alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "08_sentiment_authenticity.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("  Created: 08_sentiment_authenticity.png")


def create_energy_formality(sentiment):
    """Create energy level and formality breakdown."""
    if sentiment is None or "energy_level" not in sentiment.columns:
        return

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Energy levels
    energy_counts = sentiment["energy_level"].value_counts()
    colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']
    ax1.bar(energy_counts.index, energy_counts.values, color=colors[:len(energy_counts)])
    ax1.set_xlabel("Energy level")
    ax1.set_ylabel("Count")
    ax1.set_title("Content energy levels", fontsize=12, fontweight='bold')

    # Formality
    formality_counts = sentiment["formality"].value_counts()
    ax2.bar(formality_counts.index, formality_counts.values, color='#9b59b6')
    ax2.set_xlabel("Formality")
    ax2.set_ylabel("Count")
    ax2.set_title("Content formality", fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "09_energy_formality.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("  Created: 09_energy_formality.png")


def create_summary_dashboard(sentiment_stats, semantic_full):
    """Create a summary dashboard."""
    fig = plt.figure(figsize=(16, 12))

    # Create grid
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

    # Title
    total_posts = sentiment_stats['overall']['count']
    fig.suptitle(f"NJ Influencer content analysis summary\n{total_posts:,} posts analyzed",
                 fontsize=16, fontweight='bold', y=0.98)

    # 1. Overall stats (text)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.axis('off')
    overall = sentiment_stats["overall"]
    stats_text = f"""
    Total posts: {overall['count']}

    Avg sentiment: {overall['avg_sentiment']:.2f}

    Top emotion: Joy ({overall['primary_emotions'].get('joy', 0)})

    Top mode: Informative ({overall['rhetorical_modes'].get('informative', 0)})
    """
    ax1.text(0.1, 0.5, stats_text, transform=ax1.transAxes, fontsize=12,
             verticalalignment='center', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
    ax1.set_title("Overview", fontsize=12, fontweight='bold')

    # 2. Sentiment pie
    ax2 = fig.add_subplot(gs[0, 1])
    dist = sentiment_stats["overall"]["sentiment_distribution"]
    color_map = {
        "very_positive": "#2ecc71",
        "positive": "#27ae60",
        "neutral": "#95a5a6",
        "negative": "#e74c3c",
        "very_negative": "#c0392b"
    }
    colors = [color_map.get(l, "#95a5a6") for l in dist.keys()]
    ax2.pie(dist.values(), labels=[l.replace('_', ' ').title() for l in dist.keys()],
            autopct='%1.0f%%', colors=colors, startangle=90)
    ax2.set_title("Sentiment", fontsize=12, fontweight='bold')

    # 3. Emotions bar
    ax3 = fig.add_subplot(gs[0, 2])
    emotions = dict(sorted(sentiment_stats["overall"]["primary_emotions"].items(),
                          key=lambda x: -x[1])[:5])
    ax3.barh(list(emotions.keys()), list(emotions.values()), color='#3498db')
    ax3.set_title("Top emotions", fontsize=12, fontweight='bold')
    ax3.invert_yaxis()

    # 4. Rhetorical modes
    ax4 = fig.add_subplot(gs[1, 0])
    modes = sentiment_stats["overall"]["rhetorical_modes"]
    ax4.bar(list(modes.keys()), list(modes.values()), color='#9b59b6')
    ax4.set_title("Rhetorical modes", fontsize=12, fontweight='bold')
    ax4.tick_params(axis='x', rotation=45)

    # 5. Top influencers by sentiment
    ax5 = fig.add_subplot(gs[1, 1:])
    inf_data = [(name, data["avg_sentiment"]) for name, data in sentiment_stats["by_influencer"].items()]
    inf_data = sorted(inf_data, key=lambda x: x[1], reverse=True)[:10]
    names = [x[0][:20] for x in inf_data]  # Truncate names
    scores = [x[1] for x in inf_data]
    colors = ['#2ecc71' if s > 0 else '#e74c3c' for s in scores]
    ax5.barh(names, scores, color=colors)
    ax5.set_title("Top 10 influencers by sentiment", fontsize=12, fontweight='bold')
    ax5.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    ax5.invert_yaxis()

    # 6. Topics (if available)
    ax6 = fig.add_subplot(gs[2, :])
    if semantic_full:
        topic_counts = Counter()
        for item in semantic_full:
            if "main_topic" in item:
                topic_counts[item["main_topic"]] += 1
        top_topics = topic_counts.most_common(10)
        if top_topics:
            topics = [t[0] for t in top_topics]
            counts = [t[1] for t in top_topics]
            ax6.bar(range(len(topics)), counts, color=plt.cm.viridis(np.linspace(0.2, 0.8, len(topics))))
            ax6.set_xticks(range(len(topics)))
            ax6.set_xticklabels(topics, rotation=45, ha='right')
            ax6.set_title("Top 10 content topics", fontsize=12, fontweight='bold')
        else:
            ax6.text(0.5, 0.5, "No topic data available", ha='center', va='center')
            ax6.axis('off')
    else:
        ax6.text(0.5, 0.5, "No semantic data available", ha='center', va='center')
        ax6.axis('off')

    plt.savefig(OUTPUT_DIR / "00_summary_dashboard.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("  Created: 00_summary_dashboard.png")


def main():
    print("\n=== Generating visualizations ===\n")

    # Load data
    print("Loading data...")
    semantic, sentiment, semantic_full, sentiment_stats = load_data()

    if sentiment_stats is None:
        print("ERROR: Could not load sentiment stats. Check analysis/ai_results/sentiment/")
        return

    print(f"  Sentiment data: {sentiment_stats['overall']['count']} posts")
    print(f"  Semantic data: {len(semantic_full) if semantic_full else 0} posts")

    print("\nGenerating charts...")

    # Generate all visualizations
    create_sentiment_distribution(sentiment_stats)
    create_emotion_breakdown(sentiment_stats)
    create_rhetorical_modes(sentiment_stats)
    create_influencer_sentiment(sentiment_stats)
    create_semantic_topics(semantic_full)
    create_content_types(semantic_full)
    create_nj_relevance(semantic_full)
    create_sentiment_vs_authenticity(sentiment)
    create_energy_formality(sentiment)
    create_summary_dashboard(sentiment_stats, semantic_full)

    print(f"\n=== All visualizations saved to {OUTPUT_DIR} ===\n")


if __name__ == "__main__":
    main()
