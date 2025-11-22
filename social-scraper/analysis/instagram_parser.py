"""
Instagram Data Parser
Parses instaloader JSON metadata from Instagram posts
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


def parse_instagram_post(json_path: str) -> Dict[str, Any]:
    """Parse a single Instagram JSON file from instaloader"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Instaloader wraps data in 'node' key
    node = data.get('node', data)

    # Extract timestamp
    timestamp = node.get('taken_at_timestamp') or node.get('date')
    if timestamp:
        date = datetime.fromtimestamp(timestamp)
    else:
        date = None

    # Get caption text
    caption = ''
    if 'edge_media_to_caption' in node:
        edges = node['edge_media_to_caption'].get('edges', [])
        if edges:
            caption = edges[0].get('node', {}).get('text', '')
    elif 'caption' in node:
        caption = node.get('caption', '')

    # Get like count
    like_count = 0
    if 'edge_media_preview_like' in node:
        like_count = node['edge_media_preview_like'].get('count', 0)
    elif 'likes' in node:
        like_count = node.get('likes', {}).get('count', 0) if isinstance(node.get('likes'), dict) else node.get('likes', 0)

    # Get comment count
    comment_count = node.get('comments', 0)
    if isinstance(comment_count, dict):
        comment_count = comment_count.get('count', 0)

    # Determine media type
    typename = node.get('__typename', '')
    is_video = node.get('is_video', False) or typename == 'GraphVideo'
    media_type = 'video' if is_video else 'image'
    if typename == 'GraphSidecar':
        media_type = 'carousel'

    # Get video view count if available
    video_view_count = node.get('video_view_count', 0) if is_video else 0

    return {
        'platform': 'instagram',
        'post_id': node.get('id', '') or node.get('shortcode', ''),
        'shortcode': node.get('shortcode', ''),
        'username': node.get('owner', {}).get('username', ''),
        'caption': caption,
        'like_count': like_count,
        'comment_count': comment_count,
        'video_view_count': video_view_count,
        'media_type': media_type,
        'is_video': is_video,
        'timestamp': timestamp,
        'upload_date': date.strftime('%Y-%m-%d') if date else '',
        'url': f"https://www.instagram.com/p/{node.get('shortcode', '')}/",
        'thumbnail': node.get('display_url', ''),
        'file_path': json_path
    }


def parse_influencer_instagram(influencer_dir: str, influencer_name: str) -> List[Dict[str, Any]]:
    """Parse all Instagram posts for an influencer"""
    instagram_dir = Path(influencer_dir) / 'instagram'
    posts = []

    if not instagram_dir.exists():
        return posts

    # Skip metadata.json, only process post JSON files
    for json_file in instagram_dir.glob('*.json'):
        if json_file.name == 'metadata.json':
            continue
        try:
            post = parse_instagram_post(str(json_file))
            post['influencer_name'] = influencer_name
            posts.append(post)
        except Exception as e:
            print(f"Error parsing {json_file}: {e}")

    return posts


def parse_all_instagram(output_dir: str) -> List[Dict[str, Any]]:
    """Parse all Instagram data from output directory"""
    output_path = Path(output_dir)
    all_posts = []

    for influencer_dir in output_path.iterdir():
        if influencer_dir.is_dir() and not influencer_dir.name.startswith('.'):
            posts = parse_influencer_instagram(str(influencer_dir), influencer_dir.name)
            all_posts.extend(posts)
            if posts:
                print(f"Parsed {len(posts)} Instagram posts for {influencer_dir.name}")

    return all_posts


def get_instagram_stats(posts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate aggregate statistics for Instagram posts"""
    if not posts:
        return {}

    total_likes = sum(p.get('like_count', 0) or 0 for p in posts)
    total_comments = sum(p.get('comment_count', 0) or 0 for p in posts)
    total_video_views = sum(p.get('video_view_count', 0) or 0 for p in posts)

    videos = [p for p in posts if p.get('is_video')]
    images = [p for p in posts if not p.get('is_video') and p.get('media_type') != 'carousel']
    carousels = [p for p in posts if p.get('media_type') == 'carousel']

    return {
        'total_posts': len(posts),
        'total_videos': len(videos),
        'total_images': len(images),
        'total_carousels': len(carousels),
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_video_views': total_video_views,
        'avg_likes': total_likes / len(posts) if posts else 0,
        'avg_comments': total_comments / len(posts) if posts else 0,
        'engagement_rate': (total_likes + total_comments) / len(posts) if posts else 0
    }


if __name__ == '__main__':
    # Test parsing
    output_dir = '../output'
    posts = parse_all_instagram(output_dir)
    print(f"\nTotal Instagram posts parsed: {len(posts)}")

    stats = get_instagram_stats(posts)
    print(f"\nInstagram Statistics:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:,.2f}")
        else:
            print(f"  {key}: {value:,}")
