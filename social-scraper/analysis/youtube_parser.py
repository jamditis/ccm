"""
YouTube Data Parser
Parses yt-dlp JSON metadata from YouTube videos
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


def parse_youtube_post(json_path: str) -> Dict[str, Any]:
    """Parse a single YouTube .info.json file"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract timestamp
    timestamp = data.get('timestamp')
    upload_date = data.get('upload_date', '')

    if timestamp:
        date = datetime.fromtimestamp(timestamp)
    elif upload_date:
        date = datetime.strptime(upload_date, '%Y%m%d')
    else:
        date = None

    return {
        'platform': 'youtube',
        'post_id': data.get('id', ''),
        'username': data.get('uploader', '') or data.get('channel', ''),
        'channel_id': data.get('channel_id', ''),
        'title': data.get('title', ''),
        'description': data.get('description', ''),
        'duration_seconds': data.get('duration', 0),
        'view_count': data.get('view_count', 0),
        'like_count': data.get('like_count', 0),
        'comment_count': data.get('comment_count', 0),
        'timestamp': timestamp,
        'upload_date': date.strftime('%Y-%m-%d') if date else '',
        'url': data.get('webpage_url', ''),
        'thumbnail': data.get('thumbnail', ''),
        'categories': data.get('categories', []),
        'tags': data.get('tags', []),
        'file_path': json_path
    }


def parse_influencer_youtube(influencer_dir: str, influencer_name: str) -> List[Dict[str, Any]]:
    """Parse all YouTube posts for an influencer"""
    youtube_dir = Path(influencer_dir) / 'youtube'
    posts = []

    if not youtube_dir.exists():
        return posts

    for json_file in youtube_dir.glob('*.info.json'):
        try:
            post = parse_youtube_post(str(json_file))
            post['influencer_name'] = influencer_name
            posts.append(post)
        except Exception as e:
            print(f"Error parsing {json_file}: {e}")

    return posts


def parse_all_youtube(output_dir: str) -> List[Dict[str, Any]]:
    """Parse all YouTube data from output directory"""
    output_path = Path(output_dir)
    all_posts = []

    for influencer_dir in output_path.iterdir():
        if influencer_dir.is_dir() and not influencer_dir.name.startswith('.'):
            posts = parse_influencer_youtube(str(influencer_dir), influencer_dir.name)
            all_posts.extend(posts)
            if posts:
                print(f"Parsed {len(posts)} YouTube posts for {influencer_dir.name}")

    return all_posts


def get_youtube_stats(posts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate aggregate statistics for YouTube posts"""
    if not posts:
        return {}

    total_views = sum(p.get('view_count', 0) or 0 for p in posts)
    total_likes = sum(p.get('like_count', 0) or 0 for p in posts)
    total_comments = sum(p.get('comment_count', 0) or 0 for p in posts)
    total_duration = sum(p.get('duration_seconds', 0) or 0 for p in posts)

    return {
        'total_posts': len(posts),
        'total_views': total_views,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_duration_seconds': total_duration,
        'total_duration_hours': total_duration / 3600,
        'avg_views': total_views / len(posts) if posts else 0,
        'avg_likes': total_likes / len(posts) if posts else 0,
        'avg_comments': total_comments / len(posts) if posts else 0,
        'avg_duration': total_duration / len(posts) if posts else 0,
        'engagement_rate': (total_likes + total_comments) / total_views if total_views else 0
    }


if __name__ == '__main__':
    # Test parsing
    output_dir = '../output'
    posts = parse_all_youtube(output_dir)
    print(f"\nTotal YouTube posts parsed: {len(posts)}")

    stats = get_youtube_stats(posts)
    print(f"\nYouTube Statistics:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:,.2f}")
        else:
            print(f"  {key}: {value:,}")
