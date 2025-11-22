"""Instagram scraper using instaloader."""

import re
import logging
from pathlib import Path
from typing import Optional

import instaloader
from instaloader import Profile, Post
from instaloader.exceptions import (
    ProfileNotExistsException,
    PrivateProfileNotFollowedException,
    LoginRequiredException,
    ConnectionException,
)

import config
from .base import BaseScraper

logger = logging.getLogger(__name__)


class InstagramScraper(BaseScraper):
    """Scraper for Instagram posts using instaloader."""

    platform_name = "instagram"

    def __init__(self, output_dir: Path):
        super().__init__(output_dir)
        self.loader = instaloader.Instaloader(
            download_videos=True,
            download_video_thumbnails=True,
            download_geotags=False,
            download_comments=False,
            save_metadata=True,
            compress_json=False,
            post_metadata_txt_pattern="",
            max_connection_attempts=3,
        )

        # Try to load existing session first
        if config.INSTAGRAM_USERNAME:
            try:
                self.loader.load_session_from_file(config.INSTAGRAM_USERNAME)
                logger.info(f"Loaded Instagram session for {config.INSTAGRAM_USERNAME}")
                return
            except FileNotFoundError:
                logger.info("No saved session found, attempting login...")
            except Exception as e:
                logger.warning(f"Could not load session: {e}")

        # Try to login if credentials are provided
        if config.INSTAGRAM_USERNAME and config.INSTAGRAM_PASSWORD:
            try:
                self.loader.login(config.INSTAGRAM_USERNAME, config.INSTAGRAM_PASSWORD)
                # Save session for future use
                self.loader.save_session_to_file()
                logger.info("Successfully logged into Instagram and saved session")
            except Exception as e:
                logger.warning(f"Could not login to Instagram: {e}")
                if "two-factor" in str(e).lower():
                    logger.warning("2FA required. Run: instaloader -l YOUR_USERNAME")
                    logger.warning("This will prompt for 2FA code and save the session.")
                logger.warning("Continuing without login - some features may be limited")

    def extract_username(self, url: str) -> Optional[str]:
        """Extract Instagram username from URL."""
        # Patterns for Instagram URLs
        patterns = [
            r"instagram\.com/([^/?&]+)",
            r"instagram\.com/p/[^/]+/",  # Post URL
        ]

        # Skip posts, we want profile URLs
        if "/p/" in url or "/reel/" in url:
            return None

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                username = match.group(1).strip()
                # Filter out non-username paths
                if username not in ["p", "reel", "stories", "explore", "accounts"]:
                    return username

        return None

    def scrape(self, url: str, influencer_name: str) -> dict:
        """Scrape Instagram posts using instaloader."""
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

        logger.info(f"Scraping Instagram: @{username}")

        try:
            # Get profile
            profile = Profile.from_username(self.loader.context, username)

            if profile.is_private and not profile.followed_by_viewer:
                result["errors"].append(f"Profile @{username} is private")
                return result

            # Download posts
            posts_downloaded = 0
            metadata = []

            for post in profile.get_posts():
                if posts_downloaded >= self.max_posts:
                    break

                try:
                    # Download the post
                    self.loader.download_post(post, target=output_path)
                    posts_downloaded += 1

                    # Collect metadata
                    post_metadata = {
                        "shortcode": post.shortcode,
                        "url": f"https://www.instagram.com/p/{post.shortcode}/",
                        "typename": post.typename,
                        "date": post.date_utc.isoformat(),
                        "caption": post.caption if post.caption else "",
                        "likes": post.likes,
                        "comments": post.comments,
                        "is_video": post.is_video,
                        "video_view_count": post.video_view_count if post.is_video else None,
                    }
                    metadata.append(post_metadata)

                    self.rate_limit()

                except Exception as e:
                    logger.warning(f"Error downloading post {post.shortcode}: {e}")
                    continue

            result["posts_downloaded"] = posts_downloaded

            if metadata:
                self.save_metadata(output_path, metadata)

            if posts_downloaded > 0:
                result["success"] = True
                logger.info(f"Downloaded {posts_downloaded} Instagram posts for @{username}")
            else:
                result["errors"].append(f"No posts downloaded for @{username}")

        except ProfileNotExistsException:
            result["errors"].append(f"Profile @{username} does not exist")
        except PrivateProfileNotFollowedException:
            result["errors"].append(f"Profile @{username} is private and not followed")
        except LoginRequiredException:
            result["errors"].append("Login required. Set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD env vars")
        except ConnectionException as e:
            result["errors"].append(f"Connection error: {str(e)}. Instagram may be rate limiting.")
        except Exception as e:
            result["errors"].append(f"Error scraping Instagram: {str(e)}")
            logger.exception(f"Error scraping Instagram for {username}")

        return result
