#!/usr/bin/env python3
"""
Engagement Pattern Analyzer

Analyzes what drives engagement across the corpus:
- Engagement rate calculations
- Performance predictors
- Viral content characteristics
- Optimal posting patterns
- Content-engagement correlations
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import defaultdict
import statistics
import pandas as pd
import numpy as np


@dataclass
class EngagementProfile:
    """Engagement metrics for a piece of content."""
    video_id: str
    influencer: str
    platform: str

    # Raw metrics
    view_count: int
    like_count: int
    comment_count: int
    share_count: int
    duration_seconds: int

    # Calculated rates
    engagement_rate: float  # (likes + comments + shares) / views
    like_rate: float
    comment_rate: float
    share_rate: float

    # Relative performance
    z_score: float  # Performance vs influencer average
    platform_percentile: float  # Performance vs platform
    viral_score: float  # How viral relative to typical content

    # Timing
    upload_date: str
    day_of_week: str
    hour_of_day: Optional[int]


@dataclass
class InfluencerEngagementSummary:
    """Aggregate engagement profile for an influencer."""
    influencer: str
    total_posts: int
    total_views: int
    total_engagement: int

    avg_engagement_rate: float
    median_engagement_rate: float
    engagement_rate_std: float

    best_performing_content: List[str]
    worst_performing_content: List[str]

    platform_performance: Dict[str, Dict[str, float]]
    optimal_posting_times: Dict[str, int]
    content_length_sweet_spot: Tuple[int, int]


class EngagementAnalyzer:
    """Analyze engagement patterns across content."""

    def __init__(self):
        self.profiles: List[EngagementProfile] = []
        self.influencer_summaries: Dict[str, InfluencerEngagementSummary] = {}

    def load_data(self, data_dir: str) -> pd.DataFrame:
        """Load consolidated post data."""
        data_path = Path(data_dir)

        # Try different possible locations
        csv_paths = [
            data_path / "all_posts.csv",
            data_path / "data" / "all_posts.csv",
        ]

        for path in csv_paths:
            if path.exists():
                df = pd.read_csv(path)
                print(f"Loaded {len(df)} posts from {path}")
                return df

        raise FileNotFoundError(f"Could not find all_posts.csv in {data_dir}")

    def calculate_engagement_profiles(
        self,
        df: pd.DataFrame
    ) -> List[EngagementProfile]:
        """Calculate engagement metrics for all content."""
        profiles = []

        # Calculate platform-level statistics for percentiles
        platform_stats = {}
        for platform in df['platform'].unique():
            platform_df = df[df['platform'] == platform]
            views = platform_df['view_count'].dropna()
            if len(views) > 0:
                platform_stats[platform] = {
                    'mean_views': views.mean(),
                    'std_views': views.std() or 1,
                    'percentiles': np.percentile(views, [25, 50, 75, 90, 95, 99])
                }

        # Calculate influencer-level stats
        influencer_stats = {}
        for influencer in df['influencer_name'].unique():
            inf_df = df[df['influencer_name'] == influencer]
            views = inf_df['view_count'].dropna()
            if len(views) > 0:
                influencer_stats[influencer] = {
                    'mean_views': views.mean(),
                    'std_views': views.std() or 1
                }

        for _, row in df.iterrows():
            view_count = int(row.get('view_count', 0) if pd.notna(row.get('view_count')) else 0)
            like_count = int(row.get('like_count', 0) if pd.notna(row.get('like_count')) else 0)
            comment_count = int(row.get('comment_count', 0) if pd.notna(row.get('comment_count')) else 0)
            share_count = int(row.get('repost_count', 0) if pd.notna(row.get('repost_count')) else (row.get('share_count', 0) if pd.notna(row.get('share_count')) else 0))
            duration = int(row.get('duration_seconds', 0) if pd.notna(row.get('duration_seconds')) else 0)

            # Calculate rates
            total_engagement = like_count + comment_count + share_count
            engagement_rate = total_engagement / view_count if view_count > 0 else 0
            like_rate = like_count / view_count if view_count > 0 else 0
            comment_rate = comment_count / view_count if view_count > 0 else 0
            share_rate = share_count / view_count if view_count > 0 else 0

            # Z-score vs influencer average
            influencer = row.get('influencer_name', '')
            inf_stat = influencer_stats.get(influencer, {'mean_views': 1, 'std_views': 1})
            z_score = (view_count - inf_stat['mean_views']) / inf_stat['std_views'] if inf_stat['std_views'] > 0 else 0

            # Platform percentile
            platform = row.get('platform', 'unknown')
            plat_stat = platform_stats.get(platform, {'percentiles': [0]*6})
            percentiles = plat_stat['percentiles']

            if view_count >= percentiles[5]:  # 99th
                platform_percentile = 99
            elif view_count >= percentiles[4]:  # 95th
                platform_percentile = 95
            elif view_count >= percentiles[3]:  # 90th
                platform_percentile = 90
            elif view_count >= percentiles[2]:  # 75th
                platform_percentile = 75
            elif view_count >= percentiles[1]:  # 50th
                platform_percentile = 50
            else:
                platform_percentile = 25

            # Viral score (simplified)
            viral_score = min(1.0, z_score / 3) if z_score > 0 else 0

            # Parse date
            upload_date = str(row.get('upload_date', ''))
            day_of_week = "unknown"
            hour = None

            if upload_date and upload_date != 'nan':
                try:
                    dt = pd.to_datetime(upload_date)
                    day_of_week = dt.day_name()
                    hour = dt.hour if hasattr(dt, 'hour') else None
                except Exception:
                    pass

            profiles.append(EngagementProfile(
                video_id=str(row.get('post_id', '')),
                influencer=influencer,
                platform=platform,
                view_count=view_count,
                like_count=like_count,
                comment_count=comment_count,
                share_count=share_count,
                duration_seconds=duration,
                engagement_rate=round(engagement_rate, 6),
                like_rate=round(like_rate, 6),
                comment_rate=round(comment_rate, 6),
                share_rate=round(share_rate, 6),
                z_score=round(z_score, 3),
                platform_percentile=platform_percentile,
                viral_score=round(viral_score, 3),
                upload_date=upload_date,
                day_of_week=day_of_week,
                hour_of_day=hour
            ))

        self.profiles = profiles
        return profiles

    def analyze_influencer_patterns(
        self,
        profiles: List[EngagementProfile]
    ) -> Dict[str, InfluencerEngagementSummary]:
        """Aggregate engagement patterns by influencer."""
        by_influencer = defaultdict(list)
        for p in profiles:
            by_influencer[p.influencer].append(p)

        summaries = {}

        for influencer, items in by_influencer.items():
            views = [p.view_count for p in items]
            engagement_rates = [p.engagement_rate for p in items if p.engagement_rate > 0]

            # Best and worst performing
            sorted_items = sorted(items, key=lambda x: x.view_count, reverse=True)
            best = [p.video_id for p in sorted_items[:5]]
            worst = [p.video_id for p in sorted_items[-5:]]

            # Platform breakdown
            platform_perf = defaultdict(lambda: {'posts': 0, 'views': 0, 'engagement': 0})
            for p in items:
                platform_perf[p.platform]['posts'] += 1
                platform_perf[p.platform]['views'] += p.view_count
                platform_perf[p.platform]['engagement'] += p.like_count + p.comment_count

            # Optimal posting times
            day_counts = defaultdict(int)
            day_views = defaultdict(int)
            for p in items:
                if p.day_of_week != "unknown":
                    day_counts[p.day_of_week] += 1
                    day_views[p.day_of_week] += p.view_count

            optimal_times = {
                day: day_views[day] / day_counts[day]
                for day in day_counts
                if day_counts[day] > 0
            }

            # Content length sweet spot
            duration_views = [(p.duration_seconds, p.view_count) for p in items if p.duration_seconds > 0]
            if duration_views:
                # Sort by views, get top 20%
                sorted_dv = sorted(duration_views, key=lambda x: x[1], reverse=True)
                top_20 = sorted_dv[:max(1, len(sorted_dv) // 5)]
                durations = [d for d, v in top_20]
                sweet_spot = (min(durations), max(durations)) if durations else (0, 0)
            else:
                sweet_spot = (0, 0)

            summaries[influencer] = InfluencerEngagementSummary(
                influencer=influencer,
                total_posts=len(items),
                total_views=sum(views),
                total_engagement=sum(p.like_count + p.comment_count + p.share_count for p in items),
                avg_engagement_rate=statistics.mean(engagement_rates) if engagement_rates else 0,
                median_engagement_rate=statistics.median(engagement_rates) if engagement_rates else 0,
                engagement_rate_std=statistics.stdev(engagement_rates) if len(engagement_rates) > 1 else 0,
                best_performing_content=best,
                worst_performing_content=worst,
                platform_performance=dict(platform_perf),
                optimal_posting_times=optimal_times,
                content_length_sweet_spot=sweet_spot
            )

        self.influencer_summaries = summaries
        return summaries

    def find_viral_patterns(
        self,
        profiles: List[EngagementProfile],
        threshold_percentile: float = 95
    ) -> Dict[str, Any]:
        """Identify patterns in viral/high-performing content."""
        # Get viral threshold
        views = [p.view_count for p in profiles if p.view_count > 0]
        threshold = np.percentile(views, threshold_percentile) if views else 0

        viral = [p for p in profiles if p.view_count >= threshold]
        non_viral = [p for p in profiles if p.view_count < threshold]

        patterns = {
            "viral_count": len(viral),
            "threshold_views": int(threshold),
            "viral_by_platform": defaultdict(int),
            "viral_by_influencer": defaultdict(int),
            "viral_by_day": defaultdict(int),
            "viral_avg_duration": 0,
            "non_viral_avg_duration": 0,
            "viral_avg_engagement_rate": 0,
            "non_viral_avg_engagement_rate": 0,
            "top_viral_content": []
        }

        for p in viral:
            patterns["viral_by_platform"][p.platform] += 1
            patterns["viral_by_influencer"][p.influencer] += 1
            patterns["viral_by_day"][p.day_of_week] += 1

        if viral:
            patterns["viral_avg_duration"] = statistics.mean([p.duration_seconds for p in viral if p.duration_seconds > 0] or [0])
            patterns["viral_avg_engagement_rate"] = statistics.mean([p.engagement_rate for p in viral])

            # Top viral content
            sorted_viral = sorted(viral, key=lambda x: x.view_count, reverse=True)
            patterns["top_viral_content"] = [
                {
                    "video_id": p.video_id,
                    "influencer": p.influencer,
                    "platform": p.platform,
                    "views": p.view_count,
                    "engagement_rate": p.engagement_rate
                }
                for p in sorted_viral[:20]
            ]

        if non_viral:
            patterns["non_viral_avg_duration"] = statistics.mean([p.duration_seconds for p in non_viral if p.duration_seconds > 0] or [0])
            patterns["non_viral_avg_engagement_rate"] = statistics.mean([p.engagement_rate for p in non_viral])

        return patterns

    def generate_report(self, output_dir: str):
        """Generate full engagement analysis report."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Export profiles
        with open(output_path / "engagement_profiles.json", "w") as f:
            json.dump([asdict(p) for p in self.profiles], f, indent=2)

        # Export influencer summaries
        summaries_export = {}
        for name, summary in self.influencer_summaries.items():
            summaries_export[name] = asdict(summary)

        with open(output_path / "influencer_engagement_summaries.json", "w") as f:
            json.dump(summaries_export, f, indent=2)

        # Find viral patterns
        viral_patterns = self.find_viral_patterns(self.profiles)
        with open(output_path / "viral_patterns.json", "w") as f:
            json.dump(viral_patterns, f, indent=2, default=str)

        # Generate markdown report
        self._generate_markdown_report(output_path, viral_patterns)

        # Export CSV for R analysis
        self._export_for_r(output_path)

        print(f"\nEngagement analysis saved to {output_path}")

    def _generate_markdown_report(self, output_path: Path, viral_patterns: Dict):
        """Generate human-readable markdown report."""
        with open(output_path / "ENGAGEMENT_REPORT.md", "w") as f:
            f.write("# Engagement analysis report\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")

            f.write("## Overview\n\n")
            f.write(f"- Total content analyzed: {len(self.profiles)}\n")
            f.write(f"- Total influencers: {len(self.influencer_summaries)}\n")
            f.write(f"- Viral threshold (95th percentile): {viral_patterns['threshold_views']:,} views\n")
            f.write(f"- Viral content count: {viral_patterns['viral_count']}\n\n")

            f.write("## Viral content patterns\n\n")
            f.write("### By platform\n")
            for plat, count in sorted(viral_patterns['viral_by_platform'].items(), key=lambda x: -x[1]):
                f.write(f"- {plat}: {count}\n")

            f.write("\n### By influencer (top 10)\n")
            top_viral_inf = sorted(viral_patterns['viral_by_influencer'].items(), key=lambda x: -x[1])[:10]
            for inf, count in top_viral_inf:
                f.write(f"- {inf}: {count} viral posts\n")

            f.write("\n### Viral vs non-viral characteristics\n")
            f.write(f"- Avg viral duration: {viral_patterns['viral_avg_duration']:.0f}s\n")
            f.write(f"- Avg non-viral duration: {viral_patterns['non_viral_avg_duration']:.0f}s\n")
            f.write(f"- Avg viral engagement rate: {viral_patterns['viral_avg_engagement_rate']:.4f}\n")
            f.write(f"- Avg non-viral engagement rate: {viral_patterns['non_viral_avg_engagement_rate']:.4f}\n")

            f.write("\n## Top performing content\n\n")
            for i, content in enumerate(viral_patterns['top_viral_content'][:10], 1):
                f.write(f"{i}. **{content['influencer']}** ({content['platform']})\n")
                f.write(f"   - Views: {content['views']:,}\n")
                f.write(f"   - Engagement rate: {content['engagement_rate']:.4f}\n\n")

            f.write("\n## Influencer rankings\n\n")
            f.write("### By total views\n")
            sorted_inf = sorted(
                self.influencer_summaries.items(),
                key=lambda x: x[1].total_views,
                reverse=True
            )[:15]

            for i, (name, summary) in enumerate(sorted_inf, 1):
                f.write(f"{i}. **{name}**: {summary.total_views:,} views ({summary.total_posts} posts)\n")

            f.write("\n### By engagement rate\n")
            sorted_by_er = sorted(
                self.influencer_summaries.items(),
                key=lambda x: x[1].avg_engagement_rate,
                reverse=True
            )[:15]

            for i, (name, summary) in enumerate(sorted_by_er, 1):
                f.write(f"{i}. **{name}**: {summary.avg_engagement_rate:.4f} avg engagement rate\n")

    def _export_for_r(self, output_path: Path):
        """Export CSV files formatted for R analysis."""
        # Main profiles CSV
        import csv

        with open(output_path / "engagement_data.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "video_id", "influencer", "platform",
                "view_count", "like_count", "comment_count", "share_count",
                "duration_seconds", "engagement_rate", "like_rate",
                "comment_rate", "z_score", "platform_percentile",
                "viral_score", "day_of_week", "hour_of_day"
            ])
            writer.writeheader()
            for p in self.profiles:
                writer.writerow({
                    "video_id": p.video_id,
                    "influencer": p.influencer,
                    "platform": p.platform,
                    "view_count": p.view_count,
                    "like_count": p.like_count,
                    "comment_count": p.comment_count,
                    "share_count": p.share_count,
                    "duration_seconds": p.duration_seconds,
                    "engagement_rate": p.engagement_rate,
                    "like_rate": p.like_rate,
                    "comment_rate": p.comment_rate,
                    "z_score": p.z_score,
                    "platform_percentile": p.platform_percentile,
                    "viral_score": p.viral_score,
                    "day_of_week": p.day_of_week,
                    "hour_of_day": p.hour_of_day or ""
                })


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Analyze engagement patterns")
    parser.add_argument("data_dir", help="Directory with consolidated post data")
    parser.add_argument("--output", default="analysis/engagement_results")

    args = parser.parse_args()

    analyzer = EngagementAnalyzer()

    # Load data
    df = analyzer.load_data(args.data_dir)

    # Calculate profiles
    profiles = analyzer.calculate_engagement_profiles(df)
    print(f"Calculated {len(profiles)} engagement profiles")

    # Analyze influencer patterns
    summaries = analyzer.analyze_influencer_patterns(profiles)
    print(f"Analyzed {len(summaries)} influencers")

    # Generate report
    analyzer.generate_report(args.output)


if __name__ == "__main__":
    main()
