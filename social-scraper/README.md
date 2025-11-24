# NJ Influencer Social Media Scraper

A Python workflow to scrape social media content from New Jersey-based influencers. Downloads the 50 most recent posts from TikTok, Instagram, and YouTube accounts.

## Setup

### 1. Install Dependencies

```bash
cd social-scraper
pip install -r requirements.txt
```

### 2. Instagram Authentication (Recommended)

Instagram limits access for non-authenticated users. Set environment variables:

```bash
export INSTAGRAM_USERNAME="your_username"
export INSTAGRAM_PASSWORD="your_password"
```

**Note**: Consider using a secondary account for scraping to avoid risking your main account.

## Usage

### Basic Usage - Scrape All Influencers

```bash
python main.py
```

### Test Mode - Scrape First Influencer Only

```bash
python main.py --test
```

### Scrape Specific Platforms

```bash
# TikTok only
python main.py --platforms tiktok

# Instagram and YouTube
python main.py --platforms instagram youtube
```

### Process Specific Range

```bash
# Process influencers 5-10
python main.py --start 5 --end 10
```

## Output Structure

```
output/
├── Garden State/
│   ├── tiktok/
│   │   ├── video_id.mp4
│   │   ├── video_id.info.json
│   │   └── metadata.json
│   ├── instagram/
│   │   ├── 2024-01-15_shortcode/
│   │   └── metadata.json
│   └── youtube/
│       ├── video_id.mp4
│       └── metadata.json
├── Hoboken Girl/
│   └── ...
└── scraping_report.json
```

## Downloaded Content

For each post, the scraper downloads:
- **Media files**: Videos (mp4/webm) and images (jpg/png)
- **Thumbnails**: Preview images
- **Metadata**: JSON files with:
  - Post ID and URL
  - Caption/description
  - Upload date
  - View/like/comment counts
  - Duration (for videos)

## Configuration

Edit `config.py` to customize:
- `MAX_POSTS_PER_ACCOUNT`: Number of posts to download (default: 50)
- `REQUEST_DELAY`: Seconds between requests (default: 2)

## Platform-Specific Notes

### TikTok
- Uses yt-dlp
- May be blocked by TikTok's anti-bot measures
- Best results with VPN or residential IP

### Instagram
- Uses instaloader
- **Highly recommended**: Login to avoid rate limits
- Private profiles require following

### YouTube
- Uses yt-dlp
- Most reliable scraper
- Downloads at 720p max to save space

## Troubleshooting

### "yt-dlp not found"
```bash
pip install yt-dlp
```

### Instagram Rate Limiting
- Add delays between accounts
- Use authenticated session
- Try again after 1-2 hours

### TikTok Blocking
- TikTok aggressively blocks scrapers
- Try using a VPN
- Reduce concurrent requests

## Legal/Ethical Considerations

- This tool is for research and analysis purposes
- Respect platform Terms of Service
- Don't redistribute scraped content without permission
- Be mindful of rate limits to avoid overwhelming servers
- Content remains property of original creators

## Logs

Check `scraper.log` for detailed execution logs and errors.
