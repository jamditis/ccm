#!/usr/bin/env python3
"""
Batch Processing Monitor

Monitors video processing batches and automatically progresses to next batch.
Handles checkpointing for resilience against interruptions.

Usage:
    python batch_monitor.py output/ --gemini-key YOUR_KEY

Features:
- Automatic progression when error rate < 10%
- Error logging for re-runs
- Checkpoint saving for resume capability
- Periodic status updates
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Configuration
MAX_ERROR_RATE = 0.10  # 10% error threshold
CHECK_INTERVAL = 30    # Seconds between checks
BATCH_SIZE = 50        # Videos per batch


def load_checkpoint(checkpoint_path: str) -> Dict[str, Any]:
    """Load checkpoint from file."""
    if os.path.exists(checkpoint_path):
        with open(checkpoint_path, 'r') as f:
            return json.load(f)
    return {
        "current_batch": 0,
        "total_processed": 0,
        "total_errors": 0,
        "batches_completed": [],
        "error_log": [],
        "started_at": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat()
    }


def save_checkpoint(checkpoint: Dict[str, Any], checkpoint_path: str):
    """Save checkpoint to file."""
    checkpoint["last_updated"] = datetime.now().isoformat()
    with open(checkpoint_path, 'w') as f:
        json.dump(checkpoint, f, indent=2)


def check_batch_results(results_dir: str, batch_num: int) -> Dict[str, Any]:
    """Check results of a completed batch."""
    results_path = Path(results_dir)
    batch_file = results_path / f"batch_{batch_num:03d}_results.json"

    if not batch_file.exists():
        return {"status": "not_found"}

    with open(batch_file, 'r') as f:
        results = json.load(f)

    total = len(results)
    successful = sum(1 for r in results if r.get("status") == "success")
    partial = sum(1 for r in results if r.get("status") == "partial")
    failed = sum(1 for r in results if r.get("status") == "failed")

    error_rate = failed / total if total > 0 else 0

    # Collect error details
    errors = []
    for r in results:
        if r.get("status") == "failed" or r.get("errors"):
            errors.append({
                "video": r.get("video_path", "unknown"),
                "influencer": r.get("influencer", "unknown"),
                "errors": r.get("errors", [r.get("error", "Unknown error")])
            })

    return {
        "status": "completed",
        "total": total,
        "successful": successful,
        "partial": partial,
        "failed": failed,
        "error_rate": error_rate,
        "errors": errors
    }


def run_batch(
    output_dir: str,
    results_dir: str,
    start_from: int,
    batch_size: int,
    platform: str,
    whisper_model: str,
    gemini_key: Optional[str]
) -> subprocess.Popen:
    """Start a batch processing run."""
    cmd = [
        "python3",
        "analysis/video_processor/batch_process.py",
        output_dir,
        "--results-dir", results_dir,
        "--batch-size", str(batch_size),
        "--start-from", str(start_from),
        "--whisper-model", whisper_model
    ]

    if platform:
        cmd.extend(["--platform", platform])

    if gemini_key:
        cmd.extend(["--gemini-key", gemini_key])

    # Run in background
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    return process


def monitor_and_progress(
    output_dir: str,
    results_dir: str = "analysis/video_results",
    platform: Optional[str] = None,
    batch_size: int = BATCH_SIZE,
    whisper_model: str = "medium",
    gemini_key: Optional[str] = None,
    max_error_rate: float = MAX_ERROR_RATE,
    check_interval: int = CHECK_INTERVAL
):
    """
    Main monitoring loop.

    Monitors batch processing and automatically progresses to next batch.
    """
    results_path = Path(results_dir)
    results_path.mkdir(parents=True, exist_ok=True)

    checkpoint_path = str(results_path / "checkpoint.json")
    error_log_path = str(results_path / "error_log.json")

    # Load checkpoint
    checkpoint = load_checkpoint(checkpoint_path)

    print("="*60)
    print("BATCH PROCESSING MONITOR")
    print("="*60)
    print(f"Output dir: {output_dir}")
    print(f"Results dir: {results_dir}")
    print(f"Platform: {platform or 'all'}")
    print(f"Batch size: {batch_size}")
    print(f"Max error rate: {max_error_rate*100}%")
    print(f"Check interval: {check_interval}s")
    print()

    # Count total videos
    from batch_process import find_platform_videos
    videos = find_platform_videos(output_dir, platform)
    total_videos = sum(len(v) for v in videos.values())

    print(f"Total videos to process: {total_videos}")
    print(f"Resuming from video: {checkpoint['total_processed']}")
    print("="*60)

    current_process = None
    batch_num = checkpoint["current_batch"]

    try:
        while checkpoint["total_processed"] < total_videos:
            batch_num += 1
            start_from = checkpoint["total_processed"]

            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Starting batch {batch_num}")
            print(f"  Videos {start_from + 1} to {min(start_from + batch_size, total_videos)}")

            # Update checkpoint
            checkpoint["current_batch"] = batch_num
            save_checkpoint(checkpoint, checkpoint_path)

            # Start batch
            current_process = run_batch(
                output_dir,
                results_dir,
                start_from,
                batch_size,
                platform,
                whisper_model,
                gemini_key
            )

            # Monitor until complete
            while current_process.poll() is None:
                time.sleep(check_interval)

                # Print status
                print(f"  [{datetime.now().strftime('%H:%M:%S')}] Batch {batch_num} running...")

            # Batch completed - check results
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Batch {batch_num} finished")

            batch_results = check_batch_results(results_dir, batch_num)

            if batch_results["status"] == "completed":
                print(f"  Results: {batch_results['successful']} success, "
                      f"{batch_results['partial']} partial, "
                      f"{batch_results['failed']} failed")
                print(f"  Error rate: {batch_results['error_rate']*100:.1f}%")

                # Update checkpoint
                checkpoint["total_processed"] += batch_results["total"]
                checkpoint["total_errors"] += batch_results["failed"]
                checkpoint["batches_completed"].append({
                    "batch": batch_num,
                    "total": batch_results["total"],
                    "successful": batch_results["successful"],
                    "failed": batch_results["failed"],
                    "error_rate": batch_results["error_rate"]
                })

                # Log errors
                if batch_results["errors"]:
                    checkpoint["error_log"].extend(batch_results["errors"])

                    # Save error log separately
                    with open(error_log_path, 'w') as f:
                        json.dump(checkpoint["error_log"], f, indent=2)

                    print(f"  Logged {len(batch_results['errors'])} errors for re-run")

                save_checkpoint(checkpoint, checkpoint_path)

                # Check error rate
                if batch_results["error_rate"] > max_error_rate:
                    print(f"\n⚠️  High error rate ({batch_results['error_rate']*100:.1f}% > {max_error_rate*100}%)")
                    print("  Continuing to next batch (errors logged for re-run)")
                else:
                    print(f"  ✓ Error rate acceptable, continuing...")
            else:
                print(f"  ⚠️  Could not find batch results")

            # Progress summary
            progress = checkpoint["total_processed"] / total_videos * 100
            print(f"\n  Overall progress: {checkpoint['total_processed']}/{total_videos} ({progress:.1f}%)")

        # All batches complete
        print("\n" + "="*60)
        print("PROCESSING COMPLETE")
        print("="*60)
        print(f"Total processed: {checkpoint['total_processed']}")
        print(f"Total errors: {checkpoint['total_errors']}")
        print(f"Overall error rate: {checkpoint['total_errors']/checkpoint['total_processed']*100:.1f}%")

        if checkpoint["error_log"]:
            print(f"\nErrors logged to: {error_log_path}")
            print("Run with --retry-errors to reprocess failed videos")

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        print(f"Progress saved to: {checkpoint_path}")
        print(f"Resume with same command to continue from video {checkpoint['total_processed']}")

        if current_process:
            current_process.terminate()

    finally:
        save_checkpoint(checkpoint, checkpoint_path)

    return checkpoint


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Monitor and automatically progress through video processing batches"
    )
    parser.add_argument(
        "output_dir",
        help="Directory containing scraped videos"
    )
    parser.add_argument(
        "--results-dir",
        default="analysis/video_results",
        help="Directory for processing results"
    )
    parser.add_argument(
        "--platform",
        choices=["tiktok", "youtube", "instagram"],
        help="Process only specific platform"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=BATCH_SIZE,
        help="Videos per batch"
    )
    parser.add_argument(
        "--whisper-model",
        default="medium",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size"
    )
    parser.add_argument(
        "--gemini-key",
        help="Gemini API key"
    )
    parser.add_argument(
        "--max-error-rate",
        type=float,
        default=MAX_ERROR_RATE,
        help="Maximum acceptable error rate (0-1)"
    )
    parser.add_argument(
        "--check-interval",
        type=int,
        default=CHECK_INTERVAL,
        help="Seconds between status checks"
    )

    args = parser.parse_args()

    gemini_key = args.gemini_key or os.environ.get("GEMINI_API_KEY")

    monitor_and_progress(
        args.output_dir,
        args.results_dir,
        args.platform,
        args.batch_size,
        args.whisper_model,
        gemini_key,
        args.max_error_rate,
        args.check_interval
    )


if __name__ == "__main__":
    main()
