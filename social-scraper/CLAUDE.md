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

## Current Status (v0.3.0)

### Completed Scraping
- **TikTok:** 1,281 videos from 41 influencers
- **YouTube:** 224 videos from 41 influencers
- **Instagram:** ~1,900 posts from 41 influencers

See `output/SCRAPING_REPORT.md` for detailed batch statistics.

### Completed AI analysis (December 2025)

Full-dataset analysis completed using batch processing across multiple providers:

| Analysis type | Posts analyzed | Coverage |
|---------------|----------------|----------|
| Semantic | 3,650 | 100% |
| Sentiment | 3,244 | 96.4% |

**Provider breakdown (sentiment):**
- Claude batch (Haiku 4.5): 1,470 posts
- Gemini 3 Flash batch: 910 posts
- OpenAI GPT-5: 864 posts

**Merged results saved to:** `analysis/ai_results_merged/`

### News/information findings

| Metric | Count | % of total |
|--------|-------|------------|
| News/opinion/educational content | 608 | 16.7% |
| Informative rhetorical mode | 1,542 | 43.1% |
| High NJ relevance (≥0.7) | 1,788 | 49.0% |
| Core local NJ news | 256 | 7.6% |

Top topics: NJ lifestyle/dining, NJ food, basketball recruiting, local culture, Jersey City lifestyle, high school sports.

See `analysis/news_analysis/` for detailed news-focused analysis.

### Interactive web report (December 2025)

Publication-ready interactive web report created in `reports/njinfluencers-deploy/`:

**Files:**
- `index.html` - Main interactive report with charts, case studies, embeds
- `research-brief.html` - Academic-style research brief
- `videos/` - Self-hosted video files for reliable playback (33 MB total)

**Features:**
- Dark/light mode toggle with persistent preference
- Animated number counters for key statistics
- Interactive Chart.js visualizations (theme-aware)
- Embedded case study videos (TikTok, YouTube, Instagram)
- Copy-to-clipboard buttons for analysis prompts
- Sticky navigation with smooth scrolling
- Mobile responsive design
- CCM brand colors and logo

**Video files for self-hosting** (in `videos/` folder):
- `gardenstate-7507004545118113054.mp4` - Garden State Netflix news
- `hobokengirl-7512539324152286495.mp4` - Hoboken Girl free activities
- `hobokengirl-7570087280501722382.mp4` - Hoboken Girl HS football
- `lynnhazan-7431585165358468394.mp4` - Lynn Hazan restaurant recs
- `newarknjblog-7372020273731652910.mp4` - NewarkNJblog apartment news
- `noregulars-7477360979089591595.mp4` - No Regulars (counter-example)

**Deployment:** Upload `videos/` folder to FTP, then update iframe src attributes to use self-hosted video URLs instead of TikTok embeds (TikTok embeds return 403 errors).

**Correct influencer profile URLs:**
- Hoboken Girl TikTok: `@thehobokengirl`
- Garden State TikTok: `@thegardenstatepodcast`
- NJ Hoop Recruit TikTok: `@njhooprecruit`
- Jersey Sports Zone TikTok: `@jsz_sports`
- Weird NJ YouTube: `@WeirdNJTV`
- Chris Gethard Instagram: `@chrisgeth`
- Joe Bartolozzi YouTube: `@JoeBartolozzi`
- No Regulars TikTok: `@noregulars`

---

## AI-Powered content analysis

This project includes LLM-powered content analysis using multiple AI providers. The analysis focuses on understanding **news and information content** from NJ influencers.

### Supported AI providers

| Provider | Model | Env variable | Speed | Cost |
|----------|-------|-------------|-------|------|
| Claude | claude-sonnet-4-20250514 | `ANTHROPIC_API_KEY` | ~7 sec/post | $$$ |
| Gemini | gemini-3-flash | `GEMINI_API_KEY` | ~3 sec/post | $ |
| OpenAI | gpt-5.1-chat-latest | `OPENAI_API_KEY` | ~4 sec/post | $$ |

### Analysis types

#### 1. Semantic analysis (`analysis/content_analysis/semantic_analyzer.py`)
Extracts structured information about content:
- **main_topic**: Primary subject matter
- **content_type**: news, lifestyle, promotion, entertainment, opinion, educational
- **nj_relevance_score**: 0-1 score for New Jersey focus
- **local_vs_universal**: regional vs universal appeal
- **key_messages**: Core messages/themes
- **target_audience**: Who the content is for
- **entities mentioned**: People, organizations, brands, other creators

#### 2. Sentiment analysis (`analysis/content_analysis/sentiment_analyzer.py`)
Analyzes emotional and rhetorical qualities:
- **sentiment_score**: -1 (negative) to +1 (positive)
- **primary_emotion**: joy, anger, fear, sadness, surprise, disgust, trust, anticipation
- **rhetorical_mode**: informative, persuasive, entertaining, confrontational, inspirational
- **authenticity_score**: 0-1 credibility measure
- **controversy_potential**: 0-1 virality risk

### Running AI analysis

#### Prerequisites
1. Consolidate post data first:
   ```bash
   cd social-scraper
   venv/Scripts/activate
   python analysis/consolidate.py
   ```
   This creates `analysis/data/all_posts.csv` from scraped content.

2. Set API keys in `.env`:
   ```
   ANTHROPIC_API_KEY=your_key
   GEMINI_API_KEY=your_key
   OPENAI_API_KEY=your_key
   ```

#### Single provider analysis
```bash
# Run with Claude (default)
python run_ai_analysis.py --limit 500 --provider claude --output analysis/ai_results

# Run with Gemini 3 Flash (faster, cheaper)
python run_ai_analysis.py --limit 500 --provider gemini --output analysis/ai_results_gemini

# Run with GPT-5.1 Instant
python run_ai_analysis.py --limit 500 --provider openai --output analysis/ai_results_openai
```

#### Parallel multi-provider analysis
For faster processing of large datasets, run multiple providers in parallel:
```bash
# Run full analysis with all available providers
python run_parallel_analysis.py
```

Each provider writes to its own output directory, then results are merged.

#### Analysis parameters
- `--limit`: Number of posts to analyze (0 = all)
- `--provider`: claude, gemini, or openai
- `--output`: Output directory for results
- `--semantic-only`: Only run semantic analysis
- `--sentiment-only`: Only run sentiment analysis
- `--batch-mode`: Use Claude Batch API for 50% cost savings (async)

### Batch mode (50% cost savings)

All three providers offer batch APIs with 50% discounts for async processing:

| Provider | Batch API | Discount | Turnaround | Docs |
|----------|-----------|----------|------------|------|
| Claude | Message Batches API | 50% off | <1 hour typically | [docs](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing) |
| OpenAI | Batch API | 50% off | <24 hours | [docs](https://platform.openai.com/docs/api-reference/batch) |
| Gemini | Batch Mode | 50% off | <24 hours | [docs](https://ai.google.dev/gemini-api/docs/batch-api) |

#### Using Claude batch mode (implemented)
```bash
# Submit all posts as a batch - 50% cheaper, uses Haiku 4.5
python run_ai_analysis.py --batch-mode --limit 0 --output analysis/ai_results_batch

# Or use the batch analyzer directly
python -m analysis.content_analysis.batch_analyzer analyze --input analysis/data/all_posts.csv

# List recent batches
python -m analysis.content_analysis.batch_analyzer list

# Check batch status
python -m analysis.content_analysis.batch_analyzer status --batch-id msgbatch_xxx
```

Batch mode benefits:
- **50% cost savings** on all API calls
- **Higher throughput** - no rate limiting concerns
- **Uses Haiku 4.5** by default for maximum cost efficiency
- **Automatic retry** logic for failed requests
- **Checkpointing** via batch_id for resumability

Best practices (per Anthropic docs):
- Unique `custom_id` for each request (we use video_id)
- Batches auto-validated before submission
- Results available for 29 days after creation
- Max 100k requests or 256MB per batch

### Checkpointing and resumption

The analysis system uses automatic checkpointing:
- Progress saved every 10 posts to `*_checkpoint.json`
- Safe to interrupt and resume - no duplicate API calls
- Checkpoints contain completed IDs and full results

To resume interrupted analysis:
```bash
# Just run the same command again - it auto-resumes from checkpoint
python run_ai_analysis.py --limit 1000 --provider claude --output analysis/ai_results
```

### Output files

```
analysis/ai_results_merged/           # Final merged results
├── all_semantic_results.json         # All 3,364 semantic analyses
├── all_sentiment_results.json        # All 3,244 sentiment analyses
└── sentiment_aggregate_stats.json    # Aggregate statistics

analysis/figures/                     # Visualizations
├── 00_summary_dashboard.png
├── 01_sentiment_distribution.png
├── 02_emotion_breakdown.png
├── 03_rhetorical_modes.png
├── 04_influencer_sentiment.png
├── 05_content_topics.png
├── 06_content_types.png
├── 07_nj_relevance.png
├── 08_sentiment_authenticity.png
└── 09_energy_formality.png

analysis/news_analysis/               # News-focused analysis
├── news_content_filtered.csv         # Filtered news content
└── news_analysis_summary.json        # Summary statistics
```

### Generating visualizations

After AI analysis completes:
```bash
python analysis/generate_visualizations.py
```

Creates publication-quality charts in `analysis/figures/`:
- Sentiment distribution pie chart
- Emotion breakdown bar chart
- Rhetorical modes visualization
- Influencer sentiment comparison
- Content topics analysis
- NJ relevance score distribution
- Summary dashboard

### News/information content focus

The primary research goal is understanding how NJ influencers deliver news and information. Key filters:

```python
# Filter to news/information content
news_content = df[df['content_type'].isin(['news', 'opinion', 'educational'])]
news_content = df[df['rhetorical_mode'] == 'informative']

# Filter to NJ-focused content
local_content = df[df['nj_relevance_score'] >= 0.7]
```

### Cost estimates (December 2025)

#### Real-time API pricing
| Posts | Claude Sonnet | Gemini 3 Flash | GPT-5.1 Instant |
|-------|---------------|----------------|-----------------|
| 500 | ~$5-8 | ~$0.50 | ~$2-3 |
| 3,364 (full) | ~$35-50 | ~$3-5 | ~$15-20 |

#### Batch API pricing (50% off)
| Posts | Claude Haiku 4.5 (batch) | Gemini (batch) | OpenAI (batch) |
|-------|--------------------------|----------------|----------------|
| 3,364 (full) | ~$2-4 | ~$1.50-2.50 | ~$7-10 |

**Recommendation**: For large analyses, use batch mode with Claude Haiku 4.5 for best cost efficiency.

Using parallel providers can reduce wall-clock time by 60-70%.
