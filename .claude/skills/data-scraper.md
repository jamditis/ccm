# Data Scraper Extender

---
description: Add new platform scrapers or extend existing ones following the BaseScraper pattern
activation_triggers:
  - "add scraper"
  - "scrape platform"
  - "extend scraper"
  - "new platform"
related_skills:
  - research-pipeline
  - video-processor
---

## When to Use

- Adding support for a new social media platform
- Extending existing TikTok/Instagram/YouTube scrapers
- Need rate limiting, checkpointing, and error recovery

## When NOT to Use

- Processing already-scraped content (use video-processor or content-analyzer)
- Running the existing pipeline (use research-pipeline)
- Building web tools (use journalism-tool-builder)

## You Are

A Python developer at CCM who built scrapers for TikTok, Instagram, and YouTube. You know the BaseScraper pattern, rate limit handling, and how to structure output for downstream analysis.

## Base Scraper Pattern

Inherit from BaseScraper in `/social-scraper/scrapers/base.py`:

```python
from abc import ABC, abstractmethod
from pathlib import Path
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
```

## New Scraper Template

```python
import re
import asyncio
from pathlib import Path
from .base import BaseScraper

class NewPlatformScraper(BaseScraper):
    PLATFORM = "newplatform"
    URL_PATTERN = re.compile(r'https?://(?:www\.)?newplatform\.com/(@[\w]+)')

    def __init__(self, output_dir: Path):
        super().__init__(output_dir)
        self.rate_limit_delay = 2.0
        self.max_retries = 3

    def validate_url(self, url: str) -> bool:
        return bool(self.URL_PATTERN.match(url))

    async def scrape(self, url: str, output_dir: Path) -> dict:
        if not self.validate_url(url):
            raise ValueError(f"Invalid URL: {url}")

        match = self.URL_PATTERN.match(url)
        username = match.group(1)

        platform_dir = output_dir / self.PLATFORM
        platform_dir.mkdir(parents=True, exist_ok=True)

        for attempt in range(self.max_retries):
            try:
                result = await self._fetch_content(username, platform_dir)
                await asyncio.sleep(self.rate_limit_delay)
                return result
            except RateLimitError:
                wait = 2 ** attempt * 5
                self.logger.warning(f"Rate limited, waiting {wait}s")
                await asyncio.sleep(wait)
            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt == self.max_retries - 1:
                    raise

        return {'status': 'failed', 'url': url}
```

## Output Metadata Format

Standardized across all platforms:

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
  "hashtags": ["#topic1", "#topic2"]
}
```

## Rate Limit Handling

```python
class RateLimitError(Exception):
    pass

async def handle_response(response):
    if response.status == 429:
        retry_after = int(response.headers.get('Retry-After', 60))
        raise RateLimitError(f"Retry after {retry_after}s")
    return response
```

## yt-dlp Integration

For video platforms:

```python
import yt_dlp

def download_video(url: str, output_path: Path) -> dict:
    ydl_opts = {
        'format': 'best[height<=720]',
        'outtmpl': str(output_path / '%(id)s.%(ext)s'),
        'writeinfojson': True,
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return {
            'post_id': info['id'],
            'title': info.get('title'),
            'view_count': info.get('view_count'),
            'duration_seconds': info.get('duration'),
        }
```

## Checkpointing

```python
def save_checkpoint(completed_ids: set, path: Path):
    with open(path, 'w') as f:
        json.dump({
            'completed_ids': list(completed_ids),
            'timestamp': datetime.now().isoformat()
        }, f)

def load_checkpoint(path: Path) -> set:
    if path.exists():
        with open(path) as f:
            return set(json.load(f).get('completed_ids', []))
    return set()
```

## Scraping Report

Track results in `scraping_report.json`:

```python
def update_report(path: Path, url: str, result: dict):
    report = json.loads(path.read_text()) if path.exists() else {
        'started_at': datetime.now().isoformat(),
        'total': 0, 'successful': 0, 'failed': 0,
        'results': []
    }

    report['total'] += 1
    report['successful' if result.get('status') == 'success' else 'failed'] += 1
    report['results'].append(result)
    path.write_text(json.dumps(report, indent=2))
```

## File Structure

```
/social-scraper/
├── scrapers/
│   ├── __init__.py
│   ├── base.py          # BaseScraper ABC
│   ├── tiktok.py
│   ├── instagram.py
│   ├── youtube.py
│   └── newplatform.py   # Your new scraper
├── main.py
├── config.py
└── requirements.txt
```

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Skip URL validation | Waste API calls | Validate pattern first |
| Ignore rate limits | Get blocked | Implement exponential backoff |
| No checkpointing | Lose progress | Save every 10 items |
| Inconsistent metadata | Breaks downstream | Match standard format |
| Download max quality | Storage bloat | Cap at 720p |
| Catch all exceptions silently | Hide bugs | Log and re-raise |

## Output

Create at: `/social-scraper/scrapers/[platform].py`
Output data to: `/output/{influencer}/{platform}/`
