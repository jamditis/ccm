#!/usr/bin/env python3
"""
Batch Video Processing Script

Processes all scraped videos through the full pipeline:
1. Audio extraction with 2x speedup
2. Transcription with Whisper
3. Frame extraction
4. OCR with Tesseract/Gemini cascade

Usage:
    # Process all videos
    python batch_process.py /path/to/output --gemini-key YOUR_KEY

    # Process specific platform
    python batch_process.py /path/to/output --platform tiktok

    # Process in smaller batches
    python batch_process.py /path/to/output --batch-size 50

    # Skip transcription (frames/OCR only)
    python batch_process.py /path/to/output --skip-transcription
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from tqdm import tqdm

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from video_processor.audio_extractor import extract_and_speedup, find_videos_in_directory
from video_processor.transcriber import transcribe_with_speedup, export_to_srt, get_transcript_stats
from video_processor.frame_extractor import extract_frames
from video_processor.ocr_processor import process_frames_ocr, deduplicate_text, extract_entities


def find_platform_videos(
    output_dir: str,
    platform: Optional[str] = None
) -> Dict[str, List[str]]:
    """
    Find all videos organized by influencer and platform.

    Returns:
        Dict mapping influencer names to list of video paths
    """
    output_path = Path(output_dir)
    videos_by_influencer = {}

    for influencer_dir in output_path.iterdir():
        if not influencer_dir.is_dir():
            continue

        influencer_name = influencer_dir.name
        videos = []

        # Check each platform
        platforms = [platform] if platform else ['tiktok', 'youtube', 'instagram']

        for plat in platforms:
            plat_dir = influencer_dir / plat
            if plat_dir.exists():
                for video in plat_dir.glob("*.mp4"):
                    videos.append(str(video))

        if videos:
            videos_by_influencer[influencer_name] = sorted(videos)

    return videos_by_influencer


def process_single_video(
    video_path: str,
    output_base: str,
    whisper_model: str = "medium",
    speed_factor: float = 2.0,
    fps: float = 1.0,
    gemini_api_key: Optional[str] = None,
    skip_transcription: bool = False,
    skip_ocr: bool = False
) -> Dict[str, Any]:
    """
    Process a single video through the full pipeline.
    """
    video_path = Path(video_path)
    video_name = video_path.stem

    # Create output directory for this video
    output_dir = Path(output_base) / video_name
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "video_path": str(video_path),
        "video_name": video_name,
        "output_dir": str(output_dir),
        "timestamp": datetime.now().isoformat(),
        "status": "success",
        "errors": []
    }

    # 1. Audio extraction with speedup
    try:
        audio_result = extract_and_speedup(
            str(video_path),
            str(output_dir),
            speed_factor
        )
        result["audio"] = audio_result
    except Exception as e:
        result["errors"].append(f"Audio extraction: {str(e)}")
        result["audio"] = None

    # 2. Transcription
    if not skip_transcription and result.get("audio"):
        try:
            transcript = transcribe_with_speedup(
                result["audio"]["audio_path"],
                speed_factor,
                whisper_model
            )

            # Save transcript
            transcript_path = output_dir / f"{video_name}_transcript.json"
            with open(transcript_path, "w", encoding="utf-8") as f:
                json.dump(transcript, f, indent=2, ensure_ascii=False)

            # Export SRT
            srt_path = output_dir / f"{video_name}.srt"
            export_to_srt(transcript["segments"], str(srt_path))

            # Get stats
            stats = get_transcript_stats(transcript)

            result["transcript"] = {
                "path": str(transcript_path),
                "srt_path": str(srt_path),
                "text": transcript["text"],
                "stats": stats
            }
        except Exception as e:
            result["errors"].append(f"Transcription: {str(e)}")
            result["transcript"] = None

    # 3. Frame extraction
    if not skip_ocr:
        try:
            frames_dir = output_dir / "frames"
            frames_result = extract_frames(
                str(video_path),
                str(frames_dir),
                fps
            )
            result["frames"] = {
                "count": frames_result["frame_count"],
                "dir": str(frames_dir)
            }

            # 4. OCR processing
            if frames_result["frames"]:
                ocr_results = process_frames_ocr(
                    frames_result["frames"],
                    str(output_dir / "ocr"),
                    gemini_api_key
                )

                # Deduplicate and extract entities
                all_text = deduplicate_text(ocr_results)
                entities = extract_entities(all_text)

                # Extract cost data if available
                cost_summary = {}
                if isinstance(ocr_results, dict) and "cost_summary" in ocr_results:
                    cost_summary = ocr_results["cost_summary"]
                    ocr_results = ocr_results.get("frames", ocr_results)

                result["ocr"] = {
                    "frame_count": len(ocr_results) if isinstance(ocr_results, list) else 0,
                    "unique_text": all_text[:1000] + "..." if len(all_text) > 1000 else all_text,
                    "entities": entities,
                    "gemini_calls": cost_summary.get("gemini_api_calls", 0),
                    "estimated_cost": cost_summary.get("estimated_cost_usd", 0)
                }
        except Exception as e:
            result["errors"].append(f"Frame/OCR: {str(e)}")
            result["frames"] = None
            result["ocr"] = None

    if result["errors"]:
        result["status"] = "partial" if any([
            result.get("audio"),
            result.get("transcript"),
            result.get("ocr")
        ]) else "failed"

    return result


def batch_process(
    output_dir: str,
    results_dir: str,
    platform: Optional[str] = None,
    batch_size: int = 100,
    whisper_model: str = "medium",
    speed_factor: float = 2.0,
    fps: float = 1.0,
    gemini_api_key: Optional[str] = None,
    skip_transcription: bool = False,
    skip_ocr: bool = False,
    start_from: int = 0,
    end_at: int = 0
) -> Dict[str, Any]:
    """
    Process all videos in batches.
    """
    # Find all videos
    videos_by_influencer = find_platform_videos(output_dir, platform)

    # Flatten to list
    all_videos = []
    for influencer, videos in videos_by_influencer.items():
        for video in videos:
            all_videos.append({
                "influencer": influencer,
                "path": video
            })

    total_videos = len(all_videos)
    print(f"Found {total_videos} videos from {len(videos_by_influencer)} influencers")

    if start_from > 0 or end_at > 0:
        end_idx = end_at if end_at > 0 else len(all_videos)
        all_videos = all_videos[start_from:end_idx]
        print(f"Processing videos {start_from} to {end_idx} ({len(all_videos)} videos)")

    # Create results directory
    results_path = Path(results_dir)
    results_path.mkdir(parents=True, exist_ok=True)

    # Process in batches
    all_results = []
    batch_num = 0

    # Cumulative cost tracking
    total_gemini_calls = 0
    total_estimated_cost = 0.0

    for i in range(0, len(all_videos), batch_size):
        batch = all_videos[i:i + batch_size]
        batch_num += 1

        print(f"\n{'='*60}")
        print(f"Processing batch {batch_num} ({i+1}-{min(i+batch_size, len(all_videos))} of {len(all_videos)})")
        print(f"{'='*60}")

        batch_results = []
        batch_gemini_calls = 0
        batch_cost = 0.0

        for video_info in tqdm(batch, desc=f"Batch {batch_num}"):
            video_path = video_info["path"]
            influencer = video_info["influencer"]

            # Output directory for this video
            video_output = results_path / influencer

            try:
                result = process_single_video(
                    video_path,
                    str(video_output),
                    whisper_model,
                    speed_factor,
                    fps,
                    gemini_api_key,
                    skip_transcription,
                    skip_ocr
                )
                result["influencer"] = influencer
                batch_results.append(result)
            except Exception as e:
                batch_results.append({
                    "video_path": video_path,
                    "influencer": influencer,
                    "status": "failed",
                    "error": str(e)
                })

        all_results.extend(batch_results)

        # Extract cost data from results
        for r in batch_results:
            if r.get("ocr") and isinstance(r["ocr"], dict):
                # Cost is stored per video in OCR results
                video_cost = r["ocr"].get("estimated_cost", 0)
                video_calls = r["ocr"].get("gemini_calls", 0)
                batch_cost += video_cost
                batch_gemini_calls += video_calls

        # Update totals
        total_gemini_calls += batch_gemini_calls
        total_estimated_cost += batch_cost

        # Save batch results
        batch_file = results_path / f"batch_{batch_num:03d}_results.json"
        with open(batch_file, "w", encoding="utf-8") as f:
            json.dump(batch_results, f, indent=2, ensure_ascii=False)

        # Print batch summary
        successful = sum(1 for r in batch_results if r.get("status") == "success")
        partial = sum(1 for r in batch_results if r.get("status") == "partial")
        failed = sum(1 for r in batch_results if r.get("status") == "failed")

        print(f"\nBatch {batch_num} complete: {successful} success, {partial} partial, {failed} failed")
        print(f"  Batch cost: ${batch_cost:.4f} ({batch_gemini_calls} Gemini calls)")
        print(f"  Running total: ${total_estimated_cost:.4f} ({total_gemini_calls} Gemini calls)")

    # Save final summary
    summary = {
        "total_videos": total_videos,
        "processed": len(all_results),
        "successful": sum(1 for r in all_results if r.get("status") == "success"),
        "partial": sum(1 for r in all_results if r.get("status") == "partial"),
        "failed": sum(1 for r in all_results if r.get("status") == "failed"),
        "timestamp": datetime.now().isoformat(),
        "cost_summary": {
            "total_gemini_calls": total_gemini_calls,
            "total_estimated_cost_usd": round(total_estimated_cost, 4),
            "cost_per_video_usd": round(total_estimated_cost / len(all_results), 4) if all_results else 0
        },
        "config": {
            "whisper_model": whisper_model,
            "speed_factor": speed_factor,
            "fps": fps,
            "platform": platform,
            "skip_transcription": skip_transcription,
            "skip_ocr": skip_ocr
        }
    }

    summary_file = results_path / "processing_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"\n{'='*60}")
    print("PROCESSING COMPLETE")
    print(f"{'='*60}")
    print(f"Total: {summary['total_videos']}")
    print(f"Successful: {summary['successful']}")
    print(f"Partial: {summary['partial']}")
    print(f"Failed: {summary['failed']}")
    print(f"\nCOST SUMMARY:")
    print(f"  Total Gemini API calls: {total_gemini_calls}")
    print(f"  Total estimated cost: ${total_estimated_cost:.4f}")
    print(f"  Cost per video: ${summary['cost_summary']['cost_per_video_usd']:.4f}")
    print(f"\nResults saved to: {results_path}")

    return summary


def main():
    parser = argparse.ArgumentParser(
        description="Batch process videos for transcription and OCR"
    )
    parser.add_argument(
        "output_dir",
        help="Directory containing scraped videos (e.g., output/)"
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
        default=100,
        help="Number of videos per batch"
    )
    parser.add_argument(
        "--whisper-model",
        default="medium",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size"
    )
    parser.add_argument(
        "--speed-factor",
        type=float,
        default=2.0,
        help="Audio speedup factor"
    )
    parser.add_argument(
        "--fps",
        type=float,
        default=1.0,
        help="Frames per second to extract"
    )
    parser.add_argument(
        "--gemini-key",
        help="Gemini API key for OCR fallback"
    )
    parser.add_argument(
        "--skip-transcription",
        action="store_true",
        help="Skip audio transcription"
    )
    parser.add_argument(
        "--skip-ocr",
        action="store_true",
        help="Skip frame extraction and OCR"
    )
    parser.add_argument(
        "--start-from",
        type=int,
        default=0,
        help="Start from video N (for resuming)"
    )
    parser.add_argument(
        "--end-at",
        type=int,
        default=0,
        help="End at video N (exclusive, 0 = process all)"
    )

    args = parser.parse_args()

    # Check for Gemini key in environment if not provided
    gemini_key = args.gemini_key or os.environ.get("GEMINI_API_KEY")

    batch_process(
        args.output_dir,
        args.results_dir,
        args.platform,
        args.batch_size,
        args.whisper_model,
        args.speed_factor,
        args.fps,
        gemini_key,
        args.skip_transcription,
        args.skip_ocr,
        args.start_from,
        args.end_at
    )


if __name__ == "__main__":
    main()
