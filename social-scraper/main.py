#!/usr/bin/env python3
"""
Main orchestrator for social media scraping workflow.

Reads influencer data from CSV and scrapes their social media accounts.
"""

import csv
import logging
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from tqdm import tqdm

import config
from scrapers import TikTokScraper, InstagramScraper, YouTubeScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(config.BASE_DIR / "scraper.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def load_influencers_from_csv(csv_path: Path) -> list[dict]:
    """Load influencer data from CSV file."""
    influencers = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Skip header rows (first 3 rows are empty or header)
    data_rows = rows[config.CSV_DATA_START_ROW:]

    for row in data_rows:
        # Check if row has enough columns and has a name
        if len(row) <= max(config.CSV_COLUMNS.values()):
            continue

        name = row[config.CSV_COLUMNS["name"]].strip()
        if not name:
            continue

        influencer = {
            "name": name,
            "tiktok_url": row[config.CSV_COLUMNS["tiktok_url"]].strip() if row[config.CSV_COLUMNS["tiktok_url"]] else None,
            "instagram_url": row[config.CSV_COLUMNS["instagram_url"]].strip() if row[config.CSV_COLUMNS["instagram_url"]] else None,
            "youtube_url": row[config.CSV_COLUMNS["youtube_url"]].strip() if row[config.CSV_COLUMNS["youtube_url"]] else None,
        }

        # Only include if at least one URL exists
        if any([influencer["tiktok_url"], influencer["instagram_url"], influencer["youtube_url"]]):
            influencers.append(influencer)

    return influencers


def scrape_influencer(
    influencer: dict,
    tiktok_scraper: TikTokScraper,
    instagram_scraper: InstagramScraper,
    youtube_scraper: YouTubeScraper,
) -> dict:
    """Scrape all available platforms for a single influencer."""
    results = {
        "name": influencer["name"],
        "platforms": {},
    }

    # TikTok
    if influencer["tiktok_url"]:
        logger.info(f"Scraping TikTok for {influencer['name']}")
        result = tiktok_scraper.scrape(influencer["tiktok_url"], influencer["name"])
        results["platforms"]["tiktok"] = result

    # Instagram
    if influencer["instagram_url"]:
        logger.info(f"Scraping Instagram for {influencer['name']}")
        result = instagram_scraper.scrape(influencer["instagram_url"], influencer["name"])
        results["platforms"]["instagram"] = result

    # YouTube
    if influencer["youtube_url"]:
        logger.info(f"Scraping YouTube for {influencer['name']}")
        result = youtube_scraper.scrape(influencer["youtube_url"], influencer["name"])
        results["platforms"]["youtube"] = result

    return results


def generate_report(all_results: list[dict], output_dir: Path) -> None:
    """Generate a summary report of scraping results."""
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_influencers": len(all_results),
        "summary": {
            "tiktok": {"success": 0, "failed": 0, "total_posts": 0},
            "instagram": {"success": 0, "failed": 0, "total_posts": 0},
            "youtube": {"success": 0, "failed": 0, "total_posts": 0},
        },
        "details": all_results,
    }

    for result in all_results:
        for platform, data in result["platforms"].items():
            if data["success"]:
                report["summary"][platform]["success"] += 1
                report["summary"][platform]["total_posts"] += data["posts_downloaded"]
            else:
                report["summary"][platform]["failed"] += 1

    # Save report
    report_path = output_dir / "scraping_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)

    # Print summary
    print("\n" + "=" * 60)
    print("SCRAPING SUMMARY")
    print("=" * 60)
    print(f"Total influencers processed: {report['total_influencers']}")
    print()

    for platform, stats in report["summary"].items():
        print(f"{platform.upper()}:")
        print(f"  Successful: {stats['success']}")
        print(f"  Failed: {stats['failed']}")
        print(f"  Total posts downloaded: {stats['total_posts']}")
        print()

    print(f"Report saved to: {report_path}")
    print("=" * 60)


def main(
    start_index: int = 0,
    end_index: Optional[int] = None,
    platforms: Optional[list[str]] = None,
):
    """
    Main entry point for the scraper.

    Args:
        start_index: Start from this influencer index (0-based)
        end_index: End at this influencer index (exclusive)
        platforms: List of platforms to scrape (tiktok, instagram, youtube)
    """
    print("=" * 60)
    print("NJ INFLUENCER SOCIAL MEDIA SCRAPER")
    print("=" * 60)

    # Check if CSV exists
    if not config.CSV_PATH.exists():
        logger.error(f"CSV file not found: {config.CSV_PATH}")
        sys.exit(1)

    # Create output directory
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load influencers
    influencers = load_influencers_from_csv(config.CSV_PATH)
    logger.info(f"Loaded {len(influencers)} influencers from CSV")

    # Apply index filters
    if end_index:
        influencers = influencers[start_index:end_index]
    else:
        influencers = influencers[start_index:]

    if not influencers:
        logger.warning("No influencers to process")
        return

    print(f"Processing {len(influencers)} influencers...")
    print(f"Output directory: {config.OUTPUT_DIR}")
    print()

    # Initialize scrapers
    tiktok_scraper = TikTokScraper(config.OUTPUT_DIR)
    instagram_scraper = InstagramScraper(config.OUTPUT_DIR)
    youtube_scraper = YouTubeScraper(config.OUTPUT_DIR)

    # Filter platforms if specified
    if platforms:
        platforms = [p.lower() for p in platforms]

    # Scrape each influencer
    all_results = []

    for influencer in tqdm(influencers, desc="Processing influencers"):
        try:
            # Filter URLs based on platform selection
            filtered_influencer = influencer.copy()
            if platforms:
                if "tiktok" not in platforms:
                    filtered_influencer["tiktok_url"] = None
                if "instagram" not in platforms:
                    filtered_influencer["instagram_url"] = None
                if "youtube" not in platforms:
                    filtered_influencer["youtube_url"] = None

            result = scrape_influencer(
                filtered_influencer,
                tiktok_scraper,
                instagram_scraper,
                youtube_scraper,
            )
            all_results.append(result)

        except KeyboardInterrupt:
            logger.info("Interrupted by user")
            break
        except Exception as e:
            logger.error(f"Error processing {influencer['name']}: {e}")
            all_results.append({
                "name": influencer["name"],
                "platforms": {},
                "error": str(e),
            })

    # Generate report
    generate_report(all_results, config.OUTPUT_DIR)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scrape social media content from NJ influencers")
    parser.add_argument(
        "--start",
        type=int,
        default=0,
        help="Start from this influencer index (0-based)",
    )
    parser.add_argument(
        "--end",
        type=int,
        default=None,
        help="End at this influencer index (exclusive)",
    )
    parser.add_argument(
        "--platforms",
        nargs="+",
        choices=["tiktok", "instagram", "youtube"],
        help="Specific platforms to scrape",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test mode: only process first influencer",
    )

    args = parser.parse_args()

    if args.test:
        args.end = 1

    main(
        start_index=args.start,
        end_index=args.end,
        platforms=args.platforms,
    )
