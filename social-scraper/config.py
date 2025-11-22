"""Configuration settings for social media scraper."""

import os
from pathlib import Path

# Load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Paths
BASE_DIR = Path(__file__).parent
CSV_PATH = BASE_DIR / "_Mapping NJ Influencer Journalism  - Original List.csv"
OUTPUT_DIR = BASE_DIR / "output"

# Scraping settings
MAX_POSTS_PER_ACCOUNT = 50
REQUEST_DELAY = 2  # seconds between requests

# Instagram settings (requires login for full functionality)
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_UN", "")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PW", "")

# Column indices in CSV (0-indexed)
CSV_COLUMNS = {
    "name": 0,
    "tiktok_url": 9,
    "instagram_url": 10,
    "youtube_url": 11,
}

# CSV starts at row 4 (0-indexed: row 3)
CSV_DATA_START_ROW = 3
