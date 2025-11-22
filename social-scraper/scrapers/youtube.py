"""YouTube scraper using yt-dlp."""

import re
import logging
import subprocess
import json
from pathlib import Path
from typing import Optional

from .base import BaseScraper

logger = logging.getLogger(__name__)


class YouTubeScraper(BaseScraper):
    """Scraper for YouTube videos using yt-dlp."""

    platform_name = "youtube"

    def extract_username(self, url: str) -> Optional[str]:
        """Extract and normalize YouTube channel URL."""
        # Various YouTube URL patterns
        patterns = [
            # Channel URLs
            (r"youtube\.com/channel/([^/?&]+)", "channel"),
            (r"youtube\.com/c/([^/?&]+)", "c"),
            (r"youtube\.com/@([^/?&]+)", "handle"),
            (r"youtube\.com/user/([^/?&]+)", "user"),
            # Direct channel path
            (r"youtube\.com/([^/?&]+)", "direct"),
        ]

        for pattern, url_type in patterns:
            match = re.search(pattern, url)
            if match:
                identifier = match.group(1).strip()
                # Skip non-channel paths
                if identifier in ["watch", "playlist", "feed", "results", "shorts"]:
                    continue

                # Construct proper URL
                if url_type == "channel":
                    return f"https://www.youtube.com/channel/{identifier}/videos"
                elif url_type == "handle":
                    return f"https://www.youtube.com/@{identifier}/videos"
                elif url_type == "c":
                    return f"https://www.youtube.com/c/{identifier}/videos"
                elif url_type == "user":
                    return f"https://www.youtube.com/user/{identifier}/videos"
                else:
                    return f"https://www.youtube.com/{identifier}/videos"

        return None

    def scrape(self, url: str, influencer_name: str) -> dict:
        """Scrape YouTube videos using yt-dlp."""
        result = {
            "success": False,
            "posts_downloaded": 0,
            "errors": [],
        }

        channel_url = self.extract_username(url)
        if not channel_url:
            result["errors"].append(f"Could not extract channel from URL: {url}")
            return result

        output_path = self.get_output_path(influencer_name)

        logger.info(f"Scraping YouTube: {channel_url}")

        try:
            # Use yt-dlp to download videos
            output_template = str(output_path / "%(id)s.%(ext)s")

            cmd = [
                "yt-dlp",
                "--no-warnings",
                "-f", "bestvideo[height<=720]+bestaudio/best[height<=720]/best",  # Prefer 720p, fallback to best
                "--max-downloads", str(self.max_posts),
                "--write-info-json",
                "--write-thumbnail",
                "--write-description",
                "--no-overwrites",
                "-o", output_template,
                "--playlist-end", str(self.max_posts),
                "--sleep-interval", "1",
                "--max-sleep-interval", "3",
                channel_url,
            ]

            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=1800,  # 30 minute timeout for YouTube
            )

            # Count downloaded files
            video_files = (
                list(output_path.glob("*.mp4"))
                + list(output_path.glob("*.webm"))
                + list(output_path.glob("*.mkv"))
            )
            result["posts_downloaded"] = len(video_files)

            # Collect metadata from info.json files
            metadata = []
            for json_file in output_path.glob("*.info.json"):
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        info = json.load(f)
                        metadata.append({
                            "id": info.get("id"),
                            "title": info.get("title"),
                            "description": info.get("description", "")[:1000],  # Truncate long descriptions
                            "upload_date": info.get("upload_date"),
                            "duration": info.get("duration"),
                            "view_count": info.get("view_count"),
                            "like_count": info.get("like_count"),
                            "comment_count": info.get("comment_count"),
                            "channel": info.get("channel"),
                            "channel_id": info.get("channel_id"),
                            "channel_url": info.get("channel_url"),
                        })
                except Exception as e:
                    logger.warning(f"Error reading metadata file {json_file}: {e}")

            if metadata:
                self.save_metadata(output_path, metadata)

            if process.returncode != 0 and result["posts_downloaded"] == 0:
                error_msg = process.stderr or process.stdout or "Unknown error"
                if "Video unavailable" in error_msg:
                    result["errors"].append("Channel has no available videos")
                elif "HTTP Error 429" in error_msg:
                    result["errors"].append("YouTube rate limiting. Try again later.")
                else:
                    result["errors"].append(f"yt-dlp error: {error_msg[:500]}")
            else:
                result["success"] = True
                logger.info(f"Downloaded {result['posts_downloaded']} YouTube videos")

        except subprocess.TimeoutExpired:
            result["errors"].append("Timeout while downloading YouTube videos")
        except FileNotFoundError:
            result["errors"].append("yt-dlp not found. Please install it: pip install yt-dlp")
        except Exception as e:
            result["errors"].append(f"Error scraping YouTube: {str(e)}")
            logger.exception(f"Error scraping YouTube")

        return result
