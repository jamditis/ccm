#!/usr/bin/env python3
"""
Cross-Platform Content Analysis

Analyzes how influencers adapt content across platforms:
- Content repurposing patterns
- Platform-specific strategies
- Audience segmentation by platform
- Performance comparison across platforms
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import defaultdict
import statistics
import pandas as pd


@dataclass
class CrossPlatformProfile:
    """Cross-platform presence for an influencer."""
    influencer: str
    platforms: List[str]
    primary_platform: str
    platform_balance: str  # single_platform, balanced, platform_dominant

    # Per-platform metrics
    platform_posts: Dict[str, int]
    platform_views: Dict[str, int]
    platform_engagement: Dict[str, float]

    # Cross-platform patterns
    content_consistency: float  # 0-1 how similar content is across platforms
    posting_frequency_ratio: Dict[str, float]  # relative to most active platform
    performance_ratio: Dict[str, float]  # views relative to best platform

    # Strategy indicators
    repurposing_detected: bool
    platform_exclusive_content: Dict[str, float]  # % content unique to platform
    cross_promotion_score: float  # 0-1


@dataclass
class PlatformComparison:
    """Comparison metrics between platforms."""
    platforms_compared: List[str]
    total_content: Dict[str, int]
    total_views: Dict[str, int]
    avg_engagement_rate: Dict[str, float]

    # Content characteristics by platform
    avg_duration: Dict[str, float]
    content_types: Dict[str, Dict[str, int]]  # platform -> {type: count}

    # Performance patterns
    best_performing_platform: str
    highest_engagement_platform: str
    most_active_platform: str

    # Influencer distribution
    platform_specialists: Dict[str, List[str]]  # platform -> influencers who focus there
    multi_platform_creators: List[str]


class CrossPlatformAnalyzer:
    """Analyze cross-platform content strategies."""

    def __init__(self):
        self.influencer_profiles: Dict[str, CrossPlatformProfile] = {}
        self.platform_comparison: Optional[PlatformComparison] = None

    def load_data(self, data_dir: str) -> pd.DataFrame:
        """Load consolidated post data."""
        data_path = Path(data_dir)

        for path in [data_path / "all_posts.csv", data_path / "data" / "all_posts.csv"]:
            if path.exists():
                return pd.read_csv(path)

        raise FileNotFoundError(f"Could not find all_posts.csv")

    def analyze_influencer_cross_platform(
        self,
        df: pd.DataFrame
    ) -> Dict[str, CrossPlatformProfile]:
        """Analyze each influencer's cross-platform presence."""
        profiles = {}

        for influencer in df['influencer_name'].unique():
            inf_df = df[df['influencer_name'] == influencer]

            platforms = list(inf_df['platform'].unique())
            platform_posts = inf_df.groupby('platform').size().to_dict()
            platform_views = inf_df.groupby('platform')['view_count'].sum().to_dict()

            # Calculate engagement by platform
            platform_engagement = {}
            for platform in platforms:
                plat_df = inf_df[inf_df['platform'] == platform]
                views = plat_df['view_count'].sum()
                likes = plat_df['like_count'].sum()
                comments = plat_df['comment_count'].sum()
                if views > 0:
                    platform_engagement[platform] = (likes + comments) / views
                else:
                    platform_engagement[platform] = 0

            # Determine primary platform
            primary = max(platform_views.keys(), key=lambda x: platform_views.get(x, 0))

            # Platform balance
            if len(platforms) == 1:
                balance = "single_platform"
            else:
                max_posts = max(platform_posts.values())
                min_posts = min(platform_posts.values())
                if max_posts > 0 and min_posts / max_posts > 0.5:
                    balance = "balanced"
                else:
                    balance = "platform_dominant"

            # Posting frequency ratio
            max_posts = max(platform_posts.values()) if platform_posts else 1
            freq_ratio = {p: c / max_posts for p, c in platform_posts.items()}

            # Performance ratio
            max_views = max(platform_views.values()) if platform_views else 1
            perf_ratio = {p: v / max_views if max_views > 0 else 0 for p, v in platform_views.items()}

            # Content consistency (placeholder - would need semantic analysis)
            content_consistency = 0.5  # Default

            # Cross-promotion detection (look for mentions in captions)
            cross_promo = 0.0
            captions = inf_df['title'].fillna('') + ' ' + inf_df.get('description', pd.Series([''] * len(inf_df))).fillna('')
            promo_keywords = ['youtube', 'tiktok', 'instagram', 'subscribe', 'follow', 'link in bio']
            for caption in captions:
                if any(kw in str(caption).lower() for kw in promo_keywords):
                    cross_promo += 1
            cross_promo = min(1.0, cross_promo / len(captions)) if len(captions) > 0 else 0

            profiles[influencer] = CrossPlatformProfile(
                influencer=influencer,
                platforms=platforms,
                primary_platform=primary,
                platform_balance=balance,
                platform_posts=platform_posts,
                platform_views={k: int(v) for k, v in platform_views.items()},
                platform_engagement=platform_engagement,
                content_consistency=content_consistency,
                posting_frequency_ratio=freq_ratio,
                performance_ratio=perf_ratio,
                repurposing_detected=len(platforms) > 1 and balance == "balanced",
                platform_exclusive_content={p: 1.0 for p in platforms},  # Placeholder
                cross_promotion_score=cross_promo
            )

        self.influencer_profiles = profiles
        return profiles

    def compare_platforms(self, df: pd.DataFrame) -> PlatformComparison:
        """Compare content and performance across platforms."""
        platforms = list(df['platform'].unique())

        # Basic counts
        total_content = df.groupby('platform').size().to_dict()
        total_views = df.groupby('platform')['view_count'].sum().to_dict()

        # Engagement rates
        avg_engagement = {}
        for platform in platforms:
            plat_df = df[df['platform'] == platform]
            views = plat_df['view_count'].sum()
            likes = plat_df['like_count'].sum()
            comments = plat_df['comment_count'].sum()
            avg_engagement[platform] = (likes + comments) / views if views > 0 else 0

        # Average duration
        avg_duration = {}
        for platform in platforms:
            plat_df = df[df['platform'] == platform]
            durations = plat_df['duration_seconds'].dropna()
            avg_duration[platform] = durations.mean() if len(durations) > 0 else 0

        # Content types (if available)
        content_types = {p: {} for p in platforms}

        # Best performing
        best_performing = max(total_views.keys(), key=lambda x: total_views.get(x, 0))
        highest_engagement = max(avg_engagement.keys(), key=lambda x: avg_engagement.get(x, 0))
        most_active = max(total_content.keys(), key=lambda x: total_content.get(x, 0))

        # Identify platform specialists
        specialists = {p: [] for p in platforms}
        multi_platform = []

        for influencer, profile in self.influencer_profiles.items():
            if profile.platform_balance == "single_platform":
                specialists[profile.primary_platform].append(influencer)
            elif profile.platform_balance == "platform_dominant":
                specialists[profile.primary_platform].append(influencer)
            else:
                multi_platform.append(influencer)

        comparison = PlatformComparison(
            platforms_compared=platforms,
            total_content=total_content,
            total_views={k: int(v) for k, v in total_views.items()},
            avg_engagement_rate=avg_engagement,
            avg_duration=avg_duration,
            content_types=content_types,
            best_performing_platform=best_performing,
            highest_engagement_platform=highest_engagement,
            most_active_platform=most_active,
            platform_specialists=specialists,
            multi_platform_creators=multi_platform
        )

        self.platform_comparison = comparison
        return comparison

    def generate_report(self, output_dir: str):
        """Generate cross-platform analysis report."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Export profiles
        profiles_export = {k: asdict(v) for k, v in self.influencer_profiles.items()}
        with open(output_path / "cross_platform_profiles.json", "w") as f:
            json.dump(profiles_export, f, indent=2)

        # Export comparison
        if self.platform_comparison:
            with open(output_path / "platform_comparison.json", "w") as f:
                json.dump(asdict(self.platform_comparison), f, indent=2)

        # Generate markdown report
        self._generate_markdown_report(output_path)

        # CSV for R
        self._export_csv(output_path)

        print(f"\nCross-platform analysis saved to {output_path}")

    def _generate_markdown_report(self, output_path: Path):
        """Generate readable markdown report."""
        with open(output_path / "CROSS_PLATFORM_REPORT.md", "w") as f:
            f.write("# Cross-platform analysis report\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")

            if self.platform_comparison:
                comp = self.platform_comparison

                f.write("## Platform overview\n\n")
                f.write("| Platform | Content | Views | Engagement Rate |\n")
                f.write("|----------|---------|-------|----------------|\n")
                for p in comp.platforms_compared:
                    f.write(f"| {p} | {comp.total_content.get(p, 0):,} | ")
                    f.write(f"{comp.total_views.get(p, 0):,} | ")
                    f.write(f"{comp.avg_engagement_rate.get(p, 0):.4f} |\n")

                f.write(f"\n**Best performing platform:** {comp.best_performing_platform}\n")
                f.write(f"**Highest engagement:** {comp.highest_engagement_platform}\n")
                f.write(f"**Most active:** {comp.most_active_platform}\n\n")

                f.write("## Platform specialists\n\n")
                for platform, specialists in comp.platform_specialists.items():
                    f.write(f"### {platform.title()} specialists ({len(specialists)})\n")
                    for inf in specialists[:10]:
                        f.write(f"- {inf}\n")
                    f.write("\n")

                f.write(f"### Multi-platform creators ({len(comp.multi_platform_creators)})\n")
                for inf in comp.multi_platform_creators[:15]:
                    profile = self.influencer_profiles.get(inf)
                    if profile:
                        plats = ", ".join(profile.platforms)
                        f.write(f"- {inf} ({plats})\n")

            f.write("\n## Influencer cross-platform strategies\n\n")

            # Sort by total views
            sorted_inf = sorted(
                self.influencer_profiles.items(),
                key=lambda x: sum(x[1].platform_views.values()),
                reverse=True
            )

            for inf, profile in sorted_inf[:20]:
                f.write(f"### {inf}\n")
                f.write(f"- Platforms: {', '.join(profile.platforms)}\n")
                f.write(f"- Primary: {profile.primary_platform}\n")
                f.write(f"- Balance: {profile.platform_balance}\n")
                f.write(f"- Cross-promotion score: {profile.cross_promotion_score:.2f}\n\n")

    def _export_csv(self, output_path: Path):
        """Export CSV for R analysis."""
        import csv

        with open(output_path / "cross_platform_data.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "influencer", "platforms_count", "primary_platform",
                "platform_balance", "tiktok_posts", "youtube_posts", "instagram_posts",
                "tiktok_views", "youtube_views", "instagram_views",
                "cross_promotion_score", "repurposing_detected"
            ])
            writer.writeheader()

            for inf, profile in self.influencer_profiles.items():
                writer.writerow({
                    "influencer": inf,
                    "platforms_count": len(profile.platforms),
                    "primary_platform": profile.primary_platform,
                    "platform_balance": profile.platform_balance,
                    "tiktok_posts": profile.platform_posts.get("tiktok", 0),
                    "youtube_posts": profile.platform_posts.get("youtube", 0),
                    "instagram_posts": profile.platform_posts.get("instagram", 0),
                    "tiktok_views": profile.platform_views.get("tiktok", 0),
                    "youtube_views": profile.platform_views.get("youtube", 0),
                    "instagram_views": profile.platform_views.get("instagram", 0),
                    "cross_promotion_score": profile.cross_promotion_score,
                    "repurposing_detected": profile.repurposing_detected
                })


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Cross-platform content analysis")
    parser.add_argument("data_dir", help="Directory with consolidated post data")
    parser.add_argument("--output", default="analysis/cross_platform_results")

    args = parser.parse_args()

    analyzer = CrossPlatformAnalyzer()

    df = analyzer.load_data(args.data_dir)
    print(f"Loaded {len(df)} posts")

    profiles = analyzer.analyze_influencer_cross_platform(df)
    print(f"Analyzed {len(profiles)} influencers")

    comparison = analyzer.compare_platforms(df)
    print(f"Compared {len(comparison.platforms_compared)} platforms")

    analyzer.generate_report(args.output)


if __name__ == "__main__":
    main()
