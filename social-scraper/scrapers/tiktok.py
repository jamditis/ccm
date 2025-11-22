"""TikTok scraper using yt-dlp."""

import re
import logging
import subprocess
import json
from pathlib import Path
from typing import Optional

from .base import BaseScraper

logger = logging.getLogger(__name__)


class TikTokScraper(BaseScraper):
    """Scraper for TikTok videos using yt-dlp."""

    platform_name = "tiktok"

    def extract_username(self, url: str) -> Optional[str]:
        """Extract TikTok username from URL."""
        # Patterns: https://www.tiktok.com/@username or https://tiktok.com/@username
        patterns = [
            r"tiktok\.com/@([^/?&]+)",
            r"tiktok\.com/([^/@?&]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1).strip()

        return None

    def scrape(self, url: str, influencer_name: str) -> dict:
        """Scrape TikTok videos using yt-dlp."""
        result = {
            "success": False,
            "posts_downloaded": 0,
            "errors": [],
        }

        username = self.extract_username(url)
        if not username:
            result["errors"].append(f"Could not extract username from URL: {url}")
            return result

        output_path = self.get_output_path(influencer_name)

        # Construct the TikTok user URL
        user_url = f"https://www.tiktok.com/@{username}"

        logger.info(f"Scraping TikTok: @{username}")

        try:
            # Use yt-dlp to download videos
            output_template = str(output_path / "%(id)s.%(ext)s")

            cmd = [
                "yt-dlp",
                "--no-warnings",
                "-f", "best",
                "--max-downloads", str(self.max_posts),
                "--write-info-json",
                "--write-thumbnail",
                "--no-overwrites",
                "-o", output_template,
                "--playlist-end", str(self.max_posts),
                "--extractor-args", "tiktok:api_hostname=api22-normal-c-useast2a.tiktokv.com",
                user_url,
            ]

            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600,  # 10 minute timeout
            )

            # Count downloaded files
            video_files = list(output_path.glob("*.mp4")) + list(output_path.glob("*.webm"))
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
                            "description": info.get("description"),
                            "upload_date": info.get("upload_date"),
                            "duration": info.get("duration"),
                            "view_count": info.get("view_count"),
                            "like_count": info.get("like_count"),
                            "comment_count": info.get("comment_count"),
                            "uploader": info.get("uploader"),
                            "uploader_id": info.get("uploader_id"),
                        })
                except Exception as e:
                    logger.warning(f"Error reading metadata file {json_file}: {e}")

            if metadata:
                self.save_metadata(output_path, metadata)

            if process.returncode != 0 and result["posts_downloaded"] == 0:
                error_msg = process.stderr or process.stdout or "Unknown error"
                # Check for common issues
                if "Unable to download" in error_msg or "HTTP Error" in error_msg:
                    result["errors"].append(f"TikTok may be blocking requests. Try again later.")
                else:
                    result["errors"].append(f"yt-dlp error: {error_msg[:500]}")
            else:
                result["success"] = True
                logger.info(f"Downloaded {result['posts_downloaded']} TikTok videos for @{username}")

        except subprocess.TimeoutExpired:
            result["errors"].append("Timeout while downloading TikTok videos")
        except FileNotFoundError:
            result["errors"].append("yt-dlp not found. Please install it: pip install yt-dlp")
        except Exception as e:
            result["errors"].append(f"Error scraping TikTok: {str(e)}")
            logger.exception(f"Error scraping TikTok for {username}")

        return result
