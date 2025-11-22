"""
Data Consolidation Script
Combines data from all platforms into unified CSV datasets
"""

import json
import csv
import os
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

from tiktok_parser import parse_all_tiktok, get_tiktok_stats
from youtube_parser import parse_all_youtube, get_youtube_stats
from instagram_parser import parse_all_instagram, get_instagram_stats


def consolidate_all_posts(output_dir: str) -> List[Dict[str, Any]]:
    """Consolidate all posts from all platforms into unified format"""
    all_posts = []

    # Parse each platform
    print("Parsing TikTok data...")
    tiktok_posts = parse_all_tiktok(output_dir)
    all_posts.extend(tiktok_posts)

    print("\nParsing YouTube data...")
    youtube_posts = parse_all_youtube(output_dir)
    all_posts.extend(youtube_posts)

    print("\nParsing Instagram data...")
    instagram_posts = parse_all_instagram(output_dir)
    all_posts.extend(instagram_posts)

    return all_posts


def calculate_influencer_metrics(posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Calculate aggregate metrics per influencer across all platforms"""
    from collections import defaultdict

    # Group posts by influencer
    influencer_posts = defaultdict(list)
    for post in posts:
        influencer_posts[post['influencer_name']].append(post)

    metrics = []
    for name, inf_posts in influencer_posts.items():
        # Split by platform
        tiktok = [p for p in inf_posts if p['platform'] == 'tiktok']
        youtube = [p for p in inf_posts if p['platform'] == 'youtube']
        instagram = [p for p in inf_posts if p['platform'] == 'instagram']

        # TikTok metrics
        tiktok_views = sum(p.get('view_count', 0) or 0 for p in tiktok)
        tiktok_likes = sum(p.get('like_count', 0) or 0 for p in tiktok)
        tiktok_comments = sum(p.get('comment_count', 0) or 0 for p in tiktok)
        tiktok_reposts = sum(p.get('repost_count', 0) or 0 for p in tiktok)

        # YouTube metrics
        youtube_views = sum(p.get('view_count', 0) or 0 for p in youtube)
        youtube_likes = sum(p.get('like_count', 0) or 0 for p in youtube)
        youtube_comments = sum(p.get('comment_count', 0) or 0 for p in youtube)

        # Instagram metrics
        instagram_likes = sum(p.get('like_count', 0) or 0 for p in instagram)
        instagram_comments = sum(p.get('comment_count', 0) or 0 for p in instagram)
        instagram_video_views = sum(p.get('video_view_count', 0) or 0 for p in instagram)

        # Combined metrics
        total_views = tiktok_views + youtube_views + instagram_video_views
        total_likes = tiktok_likes + youtube_likes + instagram_likes
        total_comments = tiktok_comments + youtube_comments + instagram_comments
        total_engagement = total_likes + total_comments + tiktok_reposts

        metrics.append({
            'influencer_name': name,
            'total_posts': len(inf_posts),
            'tiktok_posts': len(tiktok),
            'youtube_posts': len(youtube),
            'instagram_posts': len(instagram),
            'total_views': total_views,
            'total_likes': total_likes,
            'total_comments': total_comments,
            'total_engagement': total_engagement,
            'tiktok_views': tiktok_views,
            'tiktok_likes': tiktok_likes,
            'tiktok_comments': tiktok_comments,
            'tiktok_reposts': tiktok_reposts,
            'youtube_views': youtube_views,
            'youtube_likes': youtube_likes,
            'youtube_comments': youtube_comments,
            'instagram_likes': instagram_likes,
            'instagram_comments': instagram_comments,
            'instagram_video_views': instagram_video_views,
            'avg_engagement_per_post': total_engagement / len(inf_posts) if inf_posts else 0,
            'engagement_rate': total_engagement / total_views if total_views else 0
        })

    # Sort by total engagement
    metrics.sort(key=lambda x: x['total_engagement'], reverse=True)
    return metrics


def export_to_csv(data: List[Dict[str, Any]], filepath: str):
    """Export data to CSV file"""
    if not data:
        print(f"No data to export to {filepath}")
        return

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"Exported {len(data)} records to {filepath}")


def export_to_json(data: Any, filepath: str):
    """Export data to JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)
    print(f"Exported to {filepath}")


def main():
    """Main consolidation workflow"""
    output_dir = '../output'
    analysis_output = Path(__file__).parent / 'data'
    analysis_output.mkdir(exist_ok=True)

    # Consolidate all posts
    print("=" * 60)
    print("CONSOLIDATING ALL PLATFORM DATA")
    print("=" * 60)

    all_posts = consolidate_all_posts(output_dir)
    print(f"\nTotal posts consolidated: {len(all_posts)}")

    # Calculate per-influencer metrics
    print("\n" + "=" * 60)
    print("CALCULATING INFLUENCER METRICS")
    print("=" * 60)

    influencer_metrics = calculate_influencer_metrics(all_posts)

    # Get platform-specific stats
    tiktok_posts = [p for p in all_posts if p['platform'] == 'tiktok']
    youtube_posts = [p for p in all_posts if p['platform'] == 'youtube']
    instagram_posts = [p for p in all_posts if p['platform'] == 'instagram']

    tiktok_stats = get_tiktok_stats(tiktok_posts)
    youtube_stats = get_youtube_stats(youtube_posts)
    instagram_stats = get_instagram_stats(instagram_posts)

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"\nTikTok: {len(tiktok_posts)} posts")
    print(f"  Total views: {tiktok_stats.get('total_views', 0):,}")
    print(f"  Total likes: {tiktok_stats.get('total_likes', 0):,}")

    print(f"\nYouTube: {len(youtube_posts)} posts")
    print(f"  Total views: {youtube_stats.get('total_views', 0):,}")
    print(f"  Total likes: {youtube_stats.get('total_likes', 0):,}")

    print(f"\nInstagram: {len(instagram_posts)} posts")
    print(f"  Total likes: {instagram_stats.get('total_likes', 0):,}")
    print(f"  Total comments: {instagram_stats.get('total_comments', 0):,}")

    # Top influencers by engagement
    print("\n" + "=" * 60)
    print("TOP 10 INFLUENCERS BY TOTAL ENGAGEMENT")
    print("=" * 60)
    for i, inf in enumerate(influencer_metrics[:10], 1):
        print(f"{i}. {inf['influencer_name']}")
        print(f"   Posts: {inf['total_posts']} | Engagement: {inf['total_engagement']:,}")

    # Export data
    print("\n" + "=" * 60)
    print("EXPORTING DATA")
    print("=" * 60)

    # All posts CSV
    export_to_csv(all_posts, str(analysis_output / 'all_posts.csv'))

    # Influencer metrics CSV
    export_to_csv(influencer_metrics, str(analysis_output / 'influencer_metrics.csv'))

    # Platform-specific CSVs
    export_to_csv(tiktok_posts, str(analysis_output / 'tiktok_posts.csv'))
    export_to_csv(youtube_posts, str(analysis_output / 'youtube_posts.csv'))
    export_to_csv(instagram_posts, str(analysis_output / 'instagram_posts.csv'))

    # Summary JSON
    summary = {
        'generated_at': datetime.now().isoformat(),
        'total_posts': len(all_posts),
        'total_influencers': len(influencer_metrics),
        'tiktok': tiktok_stats,
        'youtube': youtube_stats,
        'instagram': instagram_stats,
        'top_10_by_engagement': [
            {'name': inf['influencer_name'], 'engagement': inf['total_engagement']}
            for inf in influencer_metrics[:10]
        ]
    }
    export_to_json(summary, str(analysis_output / 'summary.json'))

    print("\nConsolidation complete!")
    return all_posts, influencer_metrics


if __name__ == '__main__':
    main()
