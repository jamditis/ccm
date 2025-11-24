# NJ Influencer Social Media Scraper

## IMPORTANT: Before Starting Any Task
**Check `SESSION_REPORT_2025-11-21.md` first** for:
- Resume instructions and commands
- Running process IDs to check
- Exact progress state when stopped

**Then check `CHANGELOG.md`** to understand:
- Current progress and what's been completed
- Any running processes or pending tasks
- Known issues and their resolutions
- TODO items that need attention (e.g., merging recovery data)

This ensures continuity and prevents duplicating work or wasting API costs.

## GitHub Workflow

When updating `CHANGELOG.md`:
1. Stage your changes: `git add CHANGELOG.md`
2. Also stage any other changed code files
3. Commit and create a PR with the changes

This keeps the repository in sync with local progress.

---

## Project Overview
A Python workflow to scrape social media content from New Jersey-based influencers for research and analysis. Downloads up to 50 most recent posts from TikTok, Instagram, and YouTube accounts.

## Architecture

### Core Components
- `main.py` - Main orchestrator that reads CSV and coordinates scraping
- `config.py` - Configuration settings and environment variables
- `scrapers/` - Platform-specific scraper implementations
  - `base.py` - Abstract base class with shared functionality
  - `tiktok.py` - TikTok scraper using yt-dlp
  - `instagram.py` - Instagram scraper using instaloader
  - `youtube.py` - YouTube scraper using yt-dlp

### Data Flow
1. Read influencer URLs from CSV file
2. For each influencer, scrape TikTok → Instagram → YouTube
3. Download media files (videos, images) and metadata (JSON)
4. Save to organized output directory structure
5. Generate summary report

## Key Dependencies
- `yt-dlp` - TikTok and YouTube video downloading
- `instaloader` - Instagram content and metadata
- `python-dotenv` - Environment variable loading
- `tqdm` - Progress bars

## Configuration

### Environment Variables (.env)
```
INSTAGRAM_UN=your_username
INSTAGRAM_PW=your_password
```

### Settings (config.py)
- `MAX_POSTS_PER_ACCOUNT` - Posts to download per platform (default: 50)
- `REQUEST_DELAY` - Seconds between requests (default: 2)

## Usage

### Basic Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Test with first influencer
python3 main.py --test

# Run specific batch
python3 main.py --start 0 --end 5

# Specific platforms only
python3 main.py --platforms tiktok youtube
```

### Instagram Authentication (Required for best results)
```bash
# For accounts with 2FA
instaloader -l YOUR_USERNAME
# Enter password and 2FA code when prompted
# Session saves to ~/.config/instaloader/
```

## Output Structure
```
output/
├── Influencer Name/
│   ├── tiktok/
│   │   ├── video_id.mp4
│   │   ├── video_id.info.json
│   │   └── metadata.json
│   ├── instagram/
│   │   └── ...
│   └── youtube/
│       └── ...
└── scraping_report.json
```

## Known Issues & Limitations

### Instagram
- Requires authentication for reliable scraping
- Rate limited without login (403 errors)
- 2FA accounts need manual session setup via CLI

### TikTok
- May be blocked by anti-bot measures
- Works best with VPN or residential IP
- Some videos may be region-locked

### YouTube
- Most reliable platform
- Prefers 720p to save space, falls back to best available for higher-res-only videos
- Long videos significantly increase download time (can take 5-10+ minutes per account)
- Downloads include video, thumbnail, description, and metadata JSON

## Development Notes

### Adding New Platforms
1. Create new scraper in `scrapers/` inheriting from `BaseScraper`
2. Implement `extract_username()` and `scrape()` methods
3. Register in `scrapers/__init__.py`
4. Add URL column mapping in `config.py`

### Testing Changes
Always test with `--test` flag first to verify changes work on single influencer before running full batch.

## CSV Format
The input CSV should have columns:
- Column 0: Influencer name
- Column 9: TikTok URL
- Column 10: Instagram URL
- Column 11: YouTube URL

Data starts at row 4 (after header rows).

## Current Status (v0.1.2)

### Completed Scraping
- **TikTok:** 1,281 videos from 39 influencers
- **YouTube:** 224 videos from 39 influencers
- **Instagram:** ~250 posts from 5 influencers (in progress)

### Instagram Progress
- Batch 1 (0-10): 5/10 complete, paused at Joe Bartolozzi
- Batches 2-4 (10-39): Not started

See `output/SCRAPING_REPORT.md` for detailed batch statistics.

### Video Processing - Parallel Batches

Can run **up to 5 batch processes in parallel** without hitting API rate limits:

```bash
# Example: 5 parallel processes
python3 analysis/video_processor/batch_process.py output \
  --results-dir analysis/video_results_with_costs \
  --start-from 1320 --end-at 1520 \
  --batch-size 10 \
  --gemini-key "YOUR_GEMINI_KEY" \
  --openai-key "YOUR_OPENAI_KEY"

# Repeat with different ranges: 1520-1720, 1720-1920, 1920-2120, etc.
```

**Rate limit considerations:**
- OpenAI Whisper: ~50 requests/min
- Gemini: 15 RPM (free tier), higher on paid
- 5 processes = ~15-25 API calls/min (safe)

### Instagram Re-scraping

Now that Instagram authentication is configured, run:

```bash
# Re-scrape all influencers for Instagram only
python3 main.py --platforms instagram

# Or run in batches
python3 main.py --start 0 --end 10 --platforms instagram
python3 main.py --start 10 --end 20 --platforms instagram
python3 main.py --start 20 --end 30 --platforms instagram
python3 main.py --start 30 --end 39 --platforms instagram
```

**Important:** Instagram scraping is slower due to rate limiting. Expect ~2-5 minutes per account with proper delays to avoid blocks.
