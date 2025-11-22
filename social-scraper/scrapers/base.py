"""Base scraper class with common functionality."""

import json
import time
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

import config

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Base class for all social media scrapers."""

    platform_name: str = "base"

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.max_posts = config.MAX_POSTS_PER_ACCOUNT
        self.delay = config.REQUEST_DELAY

    def get_output_path(self, influencer_name: str) -> Path:
        """Get the output directory for an influencer's content."""
        # Sanitize the influencer name for filesystem
        safe_name = "".join(c if c.isalnum() or c in " -_" else "_" for c in influencer_name)
        safe_name = safe_name.strip()[:100]  # Limit length

        path = self.output_dir / safe_name / self.platform_name
        path.mkdir(parents=True, exist_ok=True)
        return path

    def save_metadata(self, output_path: Path, metadata: dict) -> None:
        """Save metadata to a JSON file."""
        metadata_file = output_path / "metadata.json"

        # Load existing metadata if it exists
        existing = []
        if metadata_file.exists():
            try:
                with open(metadata_file, "r", encoding="utf-8") as f:
                    existing = json.load(f)
                    if not isinstance(existing, list):
                        existing = [existing]
            except json.JSONDecodeError:
                existing = []

        # Append new metadata
        if isinstance(metadata, list):
            existing.extend(metadata)
        else:
            existing.append(metadata)

        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, default=str, ensure_ascii=False)

    def rate_limit(self) -> None:
        """Apply rate limiting delay."""
        time.sleep(self.delay)

    @abstractmethod
    def extract_username(self, url: str) -> Optional[str]:
        """Extract username from URL."""
        pass

    @abstractmethod
    def scrape(self, url: str, influencer_name: str) -> dict:
        """
        Scrape content from the given URL.

        Returns:
            dict with keys:
                - success: bool
                - posts_downloaded: int
                - errors: list of error messages
        """
        pass
