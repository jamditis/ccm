#!/usr/bin/env python3
"""
Trend Detection and Temporal Analysis

Identifies trends, patterns, and temporal dynamics:
- Trending topics over time
- Content velocity and momentum
- Seasonal patterns
- Emerging topics
- Influencer response to trends
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict
import statistics
import pandas as pd
import numpy as np


@dataclass
class TrendSignal:
    """A detected trend signal."""
    trend_id: str
    name: str
    description: str

    # Temporal characteristics
    first_seen: str
    peak_date: str
    current_status: str  # emerging, growing, peak, declining, stable

    # Strength metrics
    momentum_score: float  # Rate of growth
    volume: int  # Total posts
    total_views: int
    engagement_rate: float

    # Participation
    influencers_participating: List[str]
    platforms_active: List[str]

    # Related keywords
    keywords: List[str]
    hashtags: List[str]


@dataclass
class TemporalPattern:
    """Temporal posting pattern."""
    pattern_type: str  # daily, weekly, monthly, seasonal
    description: str

    # Best times
    best_day: str
    best_hour: Optional[int]
    worst_day: str

    # Volume patterns
    weekday_vs_weekend: float  # Ratio
    peak_periods: List[str]
    low_periods: List[str]


class TrendDetector:
    """Detect trends and temporal patterns in content."""

    def __init__(self):
        self.trends: List[TrendSignal] = []
        self.temporal_patterns: Dict[str, TemporalPattern] = {}

    def load_data(self, data_dir: str) -> pd.DataFrame:
        """Load post data with timestamps."""
        data_path = Path(data_dir)

        for path in [data_path / "all_posts.csv", data_path / "data" / "all_posts.csv"]:
            if path.exists():
                df = pd.read_csv(path)
                # Parse dates
                df['upload_date'] = pd.to_datetime(df['upload_date'], errors='coerce')
                return df

        raise FileNotFoundError(f"Could not find all_posts.csv")

    def detect_temporal_patterns(
        self,
        df: pd.DataFrame
    ) -> Dict[str, TemporalPattern]:
        """Analyze posting patterns over time."""
        patterns = {}

        # Filter to valid dates
        df_valid = df[df['upload_date'].notna()].copy()

        if len(df_valid) == 0:
            print("Warning: No valid dates found")
            return patterns

        # Extract time components
        df_valid['day_of_week'] = df_valid['upload_date'].dt.day_name()
        df_valid['month'] = df_valid['upload_date'].dt.month_name()
        df_valid['hour'] = df_valid['upload_date'].dt.hour
        df_valid['is_weekend'] = df_valid['upload_date'].dt.dayofweek >= 5

        # Daily patterns
        daily_counts = df_valid.groupby('day_of_week').size()
        daily_views = df_valid.groupby('day_of_week')['view_count'].sum()

        if len(daily_counts) > 0:
            best_day = daily_views.idxmax() if len(daily_views) > 0 else "Unknown"
            worst_day = daily_views.idxmin() if len(daily_views) > 0 else "Unknown"

            weekday_count = df_valid[~df_valid['is_weekend']].shape[0]
            weekend_count = df_valid[df_valid['is_weekend']].shape[0]
            weekday_ratio = weekday_count / weekend_count if weekend_count > 0 else 1

            patterns['daily'] = TemporalPattern(
                pattern_type='daily',
                description=f"Best performance on {best_day}",
                best_day=best_day,
                best_hour=None,
                worst_day=worst_day,
                weekday_vs_weekend=round(weekday_ratio, 2),
                peak_periods=[best_day],
                low_periods=[worst_day]
            )

        # Monthly patterns
        monthly_counts = df_valid.groupby('month').size()
        monthly_views = df_valid.groupby('month')['view_count'].sum()

        if len(monthly_counts) > 0:
            peak_month = monthly_views.idxmax() if len(monthly_views) > 0 else "Unknown"
            low_month = monthly_views.idxmin() if len(monthly_views) > 0 else "Unknown"

            patterns['monthly'] = TemporalPattern(
                pattern_type='monthly',
                description=f"Peak activity in {peak_month}",
                best_day=peak_month,
                best_hour=None,
                worst_day=low_month,
                weekday_vs_weekend=0,
                peak_periods=[peak_month],
                low_periods=[low_month]
            )

        # Overall temporal analysis
        date_range = (df_valid['upload_date'].max() - df_valid['upload_date'].min()).days
        avg_posts_per_day = len(df_valid) / max(date_range, 1)

        patterns['overall'] = TemporalPattern(
            pattern_type='overall',
            description=f"Averaging {avg_posts_per_day:.1f} posts/day over {date_range} days",
            best_day=patterns.get('daily', TemporalPattern('', '', '', None, '', 0, [], [])).best_day,
            best_hour=None,
            worst_day=patterns.get('daily', TemporalPattern('', '', '', None, '', 0, [], [])).worst_day,
            weekday_vs_weekend=patterns.get('daily', TemporalPattern('', '', '', None, '', 0, [], [])).weekday_vs_weekend,
            peak_periods=[],
            low_periods=[]
        )

        self.temporal_patterns = patterns
        return patterns

    def detect_content_trends(
        self,
        df: pd.DataFrame,
        time_window_days: int = 30,
        min_posts: int = 5
    ) -> List[TrendSignal]:
        """Detect trending topics based on keyword frequency and engagement."""
        df_valid = df[df['upload_date'].notna()].copy()

        if len(df_valid) == 0:
            return []

        # Extract keywords from titles/descriptions
        keyword_posts = defaultdict(list)

        for _, row in df_valid.iterrows():
            text = str(row.get('title', '')) + ' ' + str(row.get('description', ''))
            text = text.lower()

            # Extract hashtags
            import re
            hashtags = re.findall(r'#(\w+)', text)

            # Extract significant words (simple approach)
            words = re.findall(r'\b[a-z]{4,}\b', text)

            # Common stop words to filter
            stop_words = {
                'this', 'that', 'with', 'from', 'have', 'been', 'were', 'what',
                'when', 'where', 'which', 'while', 'about', 'could', 'would',
                'should', 'there', 'their', 'these', 'those', 'your', 'just',
                'only', 'more', 'some', 'them', 'than', 'into', 'like', 'make',
                'made', 'does', 'dont', 'will', 'also', 'very', 'know', 'come'
            }

            keywords = [w for w in words if w not in stop_words]

            for kw in set(hashtags + keywords):
                keyword_posts[kw].append({
                    'date': row['upload_date'],
                    'views': row.get('view_count', 0),
                    'engagement': row.get('like_count', 0) + row.get('comment_count', 0),
                    'influencer': row.get('influencer_name', ''),
                    'platform': row.get('platform', '')
                })

        # Analyze each keyword for trend signals
        trends = []
        now = df_valid['upload_date'].max()

        for keyword, posts in keyword_posts.items():
            if len(posts) < min_posts:
                continue

            # Calculate trend metrics
            dates = [p['date'] for p in posts]
            views = [p.get('views', 0) or 0 for p in posts]
            engagement = [p.get('engagement', 0) or 0 for p in posts]

            first_seen = min(dates)
            last_seen = max(dates)

            # Recent activity
            recent_cutoff = now - pd.Timedelta(days=time_window_days)
            recent_posts = [p for p in posts if p['date'] >= recent_cutoff]

            if len(recent_posts) == 0:
                continue

            # Calculate momentum (posts in recent window vs older)
            older_posts = [p for p in posts if p['date'] < recent_cutoff]
            if len(older_posts) > 0:
                momentum = len(recent_posts) / len(older_posts)
            else:
                momentum = len(recent_posts)  # All posts are recent = high momentum

            # Determine status
            recent_ratio = len(recent_posts) / len(posts)
            if recent_ratio > 0.7 and momentum > 1.5:
                status = "growing"
            elif recent_ratio > 0.8:
                status = "peak"
            elif recent_ratio < 0.3:
                status = "declining"
            elif momentum > 1:
                status = "emerging"
            else:
                status = "stable"

            # Get participating influencers and platforms
            influencers = list(set(p['influencer'] for p in posts))
            platforms = list(set(p['platform'] for p in posts))

            total_views = sum(v for v in views if v)
            total_engagement = sum(e for e in engagement if e)
            engagement_rate = total_engagement / total_views if total_views > 0 else 0

            # Find peak date (most views)
            peak_idx = views.index(max(views)) if views else 0
            peak_date = dates[peak_idx] if dates else first_seen

            trends.append(TrendSignal(
                trend_id=f"trend_{keyword}",
                name=keyword,
                description=f"Topic appearing in {len(posts)} posts",
                first_seen=str(first_seen.date()) if hasattr(first_seen, 'date') else str(first_seen),
                peak_date=str(peak_date.date()) if hasattr(peak_date, 'date') else str(peak_date),
                current_status=status,
                momentum_score=round(momentum, 2),
                volume=len(posts),
                total_views=int(total_views),
                engagement_rate=round(engagement_rate, 4),
                influencers_participating=influencers[:10],
                platforms_active=platforms,
                keywords=[keyword],
                hashtags=[]
            ))

        # Sort by momentum and volume
        trends.sort(key=lambda x: (x.momentum_score * x.volume), reverse=True)

        self.trends = trends[:100]  # Top 100 trends
        return self.trends

    def analyze_influencer_trend_response(
        self,
        df: pd.DataFrame,
        trends: List[TrendSignal]
    ) -> Dict[str, Dict[str, Any]]:
        """Analyze how each influencer responds to trends."""
        response_patterns = {}

        trend_keywords = {t.name for t in trends[:50]}

        for influencer in df['influencer_name'].unique():
            inf_df = df[df['influencer_name'] == influencer]

            # Count trend participation
            trend_count = 0
            early_adopter_count = 0

            for _, row in inf_df.iterrows():
                text = str(row.get('title', '')) + ' ' + str(row.get('description', ''))
                text = text.lower()

                for trend in trends[:50]:
                    if trend.name in text:
                        trend_count += 1
                        # Check if early adopter
                        post_date = row.get('upload_date')
                        if pd.notna(post_date):
                            first_seen = pd.to_datetime(trend.first_seen)
                            if hasattr(post_date, 'date') and (post_date - first_seen).days < 7:
                                early_adopter_count += 1
                        break

            response_patterns[influencer] = {
                'total_posts': len(inf_df),
                'trend_aligned_posts': trend_count,
                'trend_alignment_rate': trend_count / len(inf_df) if len(inf_df) > 0 else 0,
                'early_adopter_count': early_adopter_count,
                'is_trend_setter': early_adopter_count > 3
            }

        return response_patterns

    def generate_report(self, output_dir: str):
        """Generate trend analysis report."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Export trends
        with open(output_path / "detected_trends.json", "w") as f:
            json.dump([asdict(t) for t in self.trends], f, indent=2)

        # Export temporal patterns
        patterns_export = {k: asdict(v) for k, v in self.temporal_patterns.items()}
        with open(output_path / "temporal_patterns.json", "w") as f:
            json.dump(patterns_export, f, indent=2)

        # Markdown report
        self._generate_markdown_report(output_path)

        # CSV for R
        self._export_csv(output_path)

        print(f"\nTrend analysis saved to {output_path}")

    def _generate_markdown_report(self, output_path: Path):
        """Generate markdown trend report."""
        with open(output_path / "TREND_REPORT.md", "w") as f:
            f.write("# Trend analysis report\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")

            # Temporal patterns
            f.write("## Temporal patterns\n\n")
            for name, pattern in self.temporal_patterns.items():
                f.write(f"### {name.title()}\n")
                f.write(f"- {pattern.description}\n")
                if pattern.best_day:
                    f.write(f"- Best day: {pattern.best_day}\n")
                if pattern.worst_day:
                    f.write(f"- Worst day: {pattern.worst_day}\n")
                if pattern.weekday_vs_weekend:
                    f.write(f"- Weekday/weekend ratio: {pattern.weekday_vs_weekend}\n")
                f.write("\n")

            # Top trends
            f.write("## Top trending topics\n\n")
            f.write("### Currently growing\n")
            growing = [t for t in self.trends if t.current_status == "growing"][:15]
            for t in growing:
                f.write(f"- **{t.name}** (momentum: {t.momentum_score}, volume: {t.volume})\n")
                f.write(f"  - Views: {t.total_views:,}, Engagement: {t.engagement_rate:.4f}\n")
                f.write(f"  - Influencers: {len(t.influencers_participating)}\n")

            f.write("\n### Emerging topics\n")
            emerging = [t for t in self.trends if t.current_status == "emerging"][:15]
            for t in emerging:
                f.write(f"- **{t.name}** (momentum: {t.momentum_score})\n")

            f.write("\n### Peak topics\n")
            peak = [t for t in self.trends if t.current_status == "peak"][:10]
            for t in peak:
                f.write(f"- **{t.name}** ({t.volume} posts, {t.total_views:,} views)\n")

            f.write("\n## High-volume topics\n\n")
            by_volume = sorted(self.trends, key=lambda x: x.volume, reverse=True)[:20]
            for t in by_volume:
                f.write(f"- **{t.name}**: {t.volume} posts, {t.total_views:,} views\n")

    def _export_csv(self, output_path: Path):
        """Export CSV for R analysis."""
        import csv

        with open(output_path / "trends_data.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "trend_id", "name", "status", "momentum_score",
                "volume", "total_views", "engagement_rate",
                "influencer_count", "platform_count", "first_seen", "peak_date"
            ])
            writer.writeheader()

            for t in self.trends:
                writer.writerow({
                    "trend_id": t.trend_id,
                    "name": t.name,
                    "status": t.current_status,
                    "momentum_score": t.momentum_score,
                    "volume": t.volume,
                    "total_views": t.total_views,
                    "engagement_rate": t.engagement_rate,
                    "influencer_count": len(t.influencers_participating),
                    "platform_count": len(t.platforms_active),
                    "first_seen": t.first_seen,
                    "peak_date": t.peak_date
                })


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Detect trends and temporal patterns")
    parser.add_argument("data_dir", help="Directory with consolidated post data")
    parser.add_argument("--output", default="analysis/trend_results")
    parser.add_argument("--window", type=int, default=30, help="Time window in days for trend detection")

    args = parser.parse_args()

    detector = TrendDetector()

    df = detector.load_data(args.data_dir)
    print(f"Loaded {len(df)} posts")

    patterns = detector.detect_temporal_patterns(df)
    print(f"Detected {len(patterns)} temporal patterns")

    trends = detector.detect_content_trends(df, time_window_days=args.window)
    print(f"Detected {len(trends)} trends")

    detector.generate_report(args.output)


if __name__ == "__main__":
    main()
