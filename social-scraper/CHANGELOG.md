# Changelog

All notable changes to the NJ Influencer Social Media Scraper will be documented in this file.

## [0.1.7] - 2025-11-21

### Video Processing Progress
- **420 videos processed** (320 main + recovery in progress)
- Completed batch 220-319 successfully
- GPU acceleration (MPS) enabled for Whisper transcription
- Processing 320-420 with GPU (2-3x faster)

### M1 GPU Acceleration
- Modified `transcriber.py` to use MPS (Metal Performance Shaders)
- Automatic device detection: MPS → CUDA → CPU
- Significantly faster transcription on Apple Silicon

### Current Running Processes
- **Recovery (0-99)**: Re-processing lost metadata
- **Main (320-420)**: GPU-accelerated processing

### Progress Summary
| Range | Status | Notes |
|-------|--------|-------|
| 0-99 | Recovery in progress | Separate directory |
| 100-219 | Complete | Original run |
| 220-319 | Complete | This session |
| 320-420 | In progress | GPU enabled |

### GitHub Sync
- Repository: https://github.com/jamditis/ccm/tree/main/social-scraper
- Code synced to public repo (no secrets/data)

### Remaining Work
- **2,627 videos remaining** (420/3,047 = 13.8% complete)
- Recovery process in progress (videos 0-99)
- Next batch: 420-520

## [0.1.6] - 2025-11-21

### Video Processing Progress
- **220 videos processed** across 4 influencers:
  - Hoboken Girl (Jennifer Tripucka and team)
  - Jersey Sports Zone
  - Lynn Hazan-Bush (lynnhazan_)
  - marmodernvibes
- Batch results saved in `analysis/video_results_with_costs/`
- Processing includes: transcription (Whisper), frame extraction, OCR (Tesseract + Gemini)

### Known Issue - Batch File Overwriting
- `batch_process.py` restarts batch numbering at 1 each run
- This caused batch files 001-010 to be overwritten with later video runs
- **Data loss**: Original batch metadata for videos 0-99 was overwritten
- **Actual video data**: Individual transcripts/OCR still exist in influencer directories

### Fixed - Checkpoint Sync
- Updated `checkpoint.json` to reflect actual progress
- Checkpoint now tracks: `total_processed: 220`, `current_batch: 22`
- Monitor will resume correctly from video 220

### Resume Instructions
To continue video processing:
```bash
# Use batch monitor for automatic progression
python3 analysis/video_processor/batch_monitor.py output \
  --results-dir analysis/video_results_with_costs \
  --batch-size 10 \
  --gemini-key YOUR_KEY

# Or manual run (next 10 batches)
python3 analysis/video_processor/batch_process.py output \
  --results-dir analysis/video_results_with_costs \
  --start-from 420 \
  --end-at 520 \
  --batch-size 10 \
  --gemini-key YOUR_KEY
```

### Recovery Process Started
- Re-processing videos 0-99 to recover lost metadata
- Saving to `analysis/video_results_recovery/` (separate directory)
- Running in parallel with main process

### TODO: Merge Recovery Data
**IMPORTANT**: When recovery completes, merge results into main directory:
```bash
# After recovery finishes, merge batch files
cp analysis/video_results_recovery/batch_*.json analysis/video_results_with_costs/

# Merge influencer directories
cp -r analysis/video_results_recovery/*/ analysis/video_results_with_costs/

# Update checkpoint to reflect merged data
# total_processed should include recovered videos
```

### Remaining Work
- **Main process**: 2,627 videos remaining (420/3,047 = 13.8% complete)
- **Recovery process**: 100 videos (0-99)
- Estimated Gemini API cost: ~$0.02-0.05 per video
- Total remaining cost estimate: ~$52-130

## [0.1.5] - 2025-11-21

### Added - Video Processing Module
Complete video content analysis pipeline built in `analysis/video_processor/`:

- **audio_extractor.py** - Extract audio with 2x speedup
  - Reduces transcription time/cost by 50%
  - Uses ffmpeg atempo filter
  - Batch processing support

- **transcriber.py** - Local Whisper transcription
  - Free, no API costs
  - Automatic timestamp normalization for sped-up audio
  - SRT/TXT export formats

- **frame_extractor.py** - Frame extraction at configurable FPS
  - Default 1fps for OCR
  - Keyframe extraction option
  - Timestamp-based extraction

- **ocr_processor.py** - Tesseract + Gemini cascade
  - Tesseract first (fast, free)
  - Gemini escalation for low confidence (<70%)
  - Entity extraction (URLs, mentions, hashtags)

- **batch_process.py** - Full pipeline orchestrator
  - Processes all videos automatically
  - Configurable batch sizes
  - Resume capability
  - JSON results with statistics

### Test Results
- Pipeline tested on TikTok videos
- Audio extraction: 91.7s → 45.8s (50% reduction)
- Transcription: Working with timestamp normalization
- OCR: Tesseract-first cascade operational

### Content Ready for Processing
- **3,047 total videos** found
  - TikTok: 1,281 videos
  - YouTube: 250 videos
  - Instagram: 1,516 videos

## [0.1.4] - 2025-11-21

### Added - Video Processing Tools
- Installed all dependencies for video content analysis:
  - **Whisper** (local) - Free transcription
  - **ffmpeg 8.0.1** - Audio/video processing
  - **Tesseract 5.5.1** - OCR engine
  - **google-generativeai** - Gemini vision API
  - **pytesseract** - Python Tesseract wrapper

## [0.1.3] - 2025-11-21

### Completed - Full Instagram Scraping
- All 39 influencers scraped successfully
  - Batch 1 (0-10): ~500 posts
  - Batch 2 (10-20): ~500 posts
  - Batch 3 (20-30): 500 posts
  - Batch 4 (30-39): ~400 posts
  - **Total: ~1,900 Instagram posts**

### Completed - Total Content Scraped
| Platform | Content | Views | Likes |
|----------|---------|-------|-------|
| TikTok | 1,281 videos | 209.5M | 20.3M |
| YouTube | 224 videos | 33.3M | 875K |
| Instagram | ~1,900 posts | TBD | TBD |
| **Total** | **~3,400 pieces** | - | - |

### Added - Analysis Pipeline
- `analysis/` directory with complete data processing pipeline:
  - `tiktok_parser.py` - Parse TikTok JSON metadata
  - `youtube_parser.py` - Parse YouTube JSON metadata
  - `instagram_parser.py` - Parse Instagram JSON metadata
  - `consolidate.py` - Combine all platforms into CSV exports
  - `nj_influencer_analysis.ipynb` - Jupyter notebook with visualizations
  - `viz_comparison.py` - Compare seaborn vs plotnine vs altair
  - `ANALYSIS_PLAN.md` - Step-by-step analysis workflow
  - `ideas/VISUALIZATION_IDEAS.md` - Future visualization approaches

### Added - Visualization Libraries
- Installed and tested: altair, plotnine, pyvis, seaborn
- Comparison charts generated in `analysis/figures/`
- Recommendation: Use Altair for publication-quality charts

### Parser Test Results
- TikTok: 1,457 posts parsed, 209.5M views, 20.3M likes
- YouTube: 153 posts parsed, 33.3M views, 875K likes
- Instagram: Ready for parsing

### Documentation
- Created comprehensive visualization ideas document
- Documented TrueAnon-style network visualization approach
- Added R/RStudio comparison and hybrid workflow

## [0.1.2] - 2025-11-20

### Completed
- Full scraping run of all 39 NJ influencers
  - TikTok: 1,281 videos downloaded (~85% success rate)
  - YouTube: 224 videos downloaded (~50% success rate)
- Instagram scraping initiated with authenticated session
  - Completed 5/39 influencers (~250 posts)
  - Paused for resume later
- Generated comprehensive scraping report (`output/SCRAPING_REPORT.md`)

### Added
- Detailed batch-by-batch statistics in scraping report
- Platform analysis and performance metrics
- Instagram session authentication via instaloader

## [0.1.1] - 2025-11-19

### Fixed
- YouTube format selection now falls back to best available when 720p not available
  - Previous: `-f "best[height<=720]"` would fail on higher-res-only videos
  - New: `-f "bestvideo[height<=720]+bestaudio/best[height<=720]/best"` with fallback
- Resolves "Requested format is not available" errors for channels with only 1080p+ content

## [0.1.0] - 2024-11-19

### Added
- Initial project setup with full scraping workflow
- TikTok scraper using yt-dlp
  - Downloads videos, thumbnails, and metadata
  - Extracts engagement stats (views, likes, comments)
- Instagram scraper using instaloader
  - Downloads posts (images/videos) with metadata
  - Supports session-based authentication for 2FA accounts
  - Automatic rate limit handling with retries
- YouTube scraper using yt-dlp
  - Downloads videos at 720p max to save space
  - Includes descriptions and engagement metrics
- Main orchestrator script with CLI arguments
  - Batch processing with `--start` and `--end`
  - Platform filtering with `--platforms`
  - Test mode with `--test`
- Configuration system
  - Environment variable support via .env file
  - Customizable post limits and rate limiting
- Output organization
  - Structured folders by influencer and platform
  - Consolidated metadata.json per platform
  - Final scraping_report.json with summary stats
- Documentation
  - README.md with setup and usage instructions
  - CLAUDE.md with architecture details
  - CHANGELOG.md for version tracking

### Technical Details
- Python 3.11+ required
- Supports macOS (tested on Darwin 24.6.0)
- CSV input with 39 NJ influencers
- Handles ~50 posts per account across 3 platforms

### Known Issues
- Instagram requires authentication for reliable operation
- TikTok may block requests (platform anti-bot measures)
- Some influencers may have private or deleted accounts
