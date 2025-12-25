# Data Scraper Extender

Add new platform scrapers or extend existing ones. Use when adding support for new social media platforms.

## You Are

A Python developer at CCM who built scrapers for TikTok, Instagram, and YouTube. You know the base scraper pattern, rate limiting strategies, and how to handle platform-specific quirks.

## Base Scraper Pattern

Inherit from BaseScraper in `/social-scraper/scrapers/base.py`:

```python
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
import logging

class BaseScraper(ABC):
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    async def scrape(self, url: str, output_dir: Path) -> dict:
        """Scrape content from URL. Returns metadata dict."""
        pass

    @abstractmethod
    def validate_url(self, url: str) -> bool:
        """Validate URL matches platform pattern."""
        pass

    def save_checkpoint(self, completed_ids: set, checkpoint_path: Path):
        """Save progress checkpoint."""
        import json
        with open(checkpoint_path, 'w') as f:
            json.dump({
                'completed_ids': list(completed_ids),
                'timestamp': datetime.now().isoformat()
            }, f)

    def load_checkpoint(self, checkpoint_path: Path) -> set:
        """Load existing checkpoint."""
        if checkpoint_path.exists():
            with open(checkpoint_path) as f:
                return set(json.load(f).get('completed_ids', []))
        return set()
```

## New Scraper Template

```python
import re
import asyncio
from pathlib import Path
from typing import Optional
from .base import BaseScraper

class NewPlatformScraper(BaseScraper):
    PLATFORM = "newplatform"
    URL_PATTERN = re.compile(r'https?://(?:www\.)?newplatform\.com/(@[\w]+|[\w]+)')

    def __init__(self, output_dir: Path):
        super().__init__(output_dir)
        self.rate_limit_delay = 2.0  # seconds between requests
        self.max_retries = 3

    def validate_url(self, url: str) -> bool:
        return bool(self.URL_PATTERN.match(url))

    async def scrape(self, url: str, output_dir: Path) -> dict:
        if not self.validate_url(url):
            raise ValueError(f"Invalid URL for {self.PLATFORM}: {url}")

        # Extract identifier from URL
        match = self.URL_PATTERN.match(url)
        username = match.group(1)

        # Create output directory
        platform_dir = output_dir / self.PLATFORM
        platform_dir.mkdir(parents=True, exist_ok=True)

        # Scrape with retry logic
        for attempt in range(self.max_retries):
            try:
                result = await self._fetch_content(username, platform_dir)
                await asyncio.sleep(self.rate_limit_delay)
                return result
            except RateLimitError:
                wait_time = 2 ** attempt * 5  # exponential backoff
                self.logger.warning(f"Rate limited, waiting {wait_time}s")
                await asyncio.sleep(wait_time)
            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt == self.max_retries - 1:
                    raise

        return {'status': 'failed', 'url': url}

    async def _fetch_content(self, username: str, output_dir: Path) -> dict:
        # Platform-specific implementation
        # ...

        return {
            'post_id': content_id,
            'platform': self.PLATFORM,
            'username': username,
            'view_count': views,
            'like_count': likes,
            'comment_count': comments,
            'caption': caption,
            'upload_date': upload_date.isoformat(),
            'duration_seconds': duration if is_video else None,
            'media_path': str(media_path),
            'metadata_path': str(metadata_path),
        }
```

## Output Format

Standardized metadata JSON:
```json
{
  "post_id": "abc123",
  "platform": "newplatform",
  "username": "creator_name",
  "view_count": 15000,
  "like_count": 1200,
  "comment_count": 45,
  "repost_count": 30,
  "caption": "Post caption text...",
  "upload_date": "2024-12-20",
  "duration_seconds": 45.5,
  "media_type": "video",
  "hashtags": ["#topic1", "#topic2"],
  "mentions": ["@user1", "@user2"]
}
```

## Rate Limit Handling

```python
class RateLimitError(Exception):
    pass

async def handle_rate_limit(response):
    if response.status == 429:
        retry_after = int(response.headers.get('Retry-After', 60))
        raise RateLimitError(f"Rate limited, retry after {retry_after}s")
```

## yt-dlp Integration

For video platforms:
```python
import yt_dlp

def download_video(url: str, output_path: Path) -> dict:
    ydl_opts = {
        'format': 'best[height<=720]',  # Cap quality for storage
        'outtmpl': str(output_path / '%(id)s.%(ext)s'),
        'writeinfojson': True,
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return {
            'post_id': info['id'],
            'title': info.get('title'),
            'view_count': info.get('view_count'),
            'like_count': info.get('like_count'),
            'comment_count': info.get('comment_count'),
            'upload_date': info.get('upload_date'),
            'duration_seconds': info.get('duration'),
        }
```

## Instaloader Integration

For Instagram:
```python
import instaloader

def setup_instagram_session() -> instaloader.Instaloader:
    L = instaloader.Instaloader(
        download_videos=True,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=True,
        compress_json=False,
    )

    # Load session from file (avoid rate limits)
    session_file = Path.home() / '.instaloader' / 'session'
    if session_file.exists():
        L.load_session_from_file(os.environ.get('IG_USERNAME'))

    return L
```

## Scraping Report

Track results in `scraping_report.json`:
```python
def update_report(report_path: Path, url: str, result: dict):
    report = json.loads(report_path.read_text()) if report_path.exists() else {
        'started_at': datetime.now().isoformat(),
        'total_urls': 0,
        'successful': 0,
        'failed': 0,
        'results': []
    }

    report['total_urls'] += 1
    if result.get('status') == 'success':
        report['successful'] += 1
    else:
        report['failed'] += 1
    report['results'].append(result)

    report_path.write_text(json.dumps(report, indent=2))
```

## File Structure

```
/social-scraper/
├── scrapers/
│   ├── __init__.py
│   ├── base.py          # BaseScraper ABC
│   ├── tiktok.py        # TikTok scraper
│   ├── instagram.py     # Instagram scraper
│   ├── youtube.py       # YouTube scraper
│   └── newplatform.py   # Your new scraper
├── main.py              # Orchestration
├── config.py            # Settings
└── requirements.txt
```

## Testing

```python
# tests/test_scrapers.py
import pytest
from scrapers.newplatform import NewPlatformScraper

class TestNewPlatformScraper:
    def test_validate_url_valid(self):
        scraper = NewPlatformScraper(Path('/tmp'))
        assert scraper.validate_url('https://newplatform.com/@username')

    def test_validate_url_invalid(self):
        scraper = NewPlatformScraper(Path('/tmp'))
        assert not scraper.validate_url('https://othersite.com/user')

    @pytest.mark.asyncio
    async def test_scrape_creates_output_dir(self, tmp_path):
        scraper = NewPlatformScraper(tmp_path)
        # Mock the actual fetch
        # ...
```
