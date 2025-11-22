"""
Audio Extraction Module

Extracts audio from video files and applies 2x speedup for cost-efficient transcription.
Uses ffmpeg for all audio processing.

Usage:
    from video_processor import extract_and_speedup

    # Single video
    output_path = extract_and_speedup("video.mp4", "output_dir/")

    # Batch processing
    results = process_video_batch(video_paths, output_dir)
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from tqdm import tqdm


def extract_audio(
    video_path: str,
    output_path: Optional[str] = None,
    audio_format: str = "mp3",
    sample_rate: int = 16000
) -> str:
    """
    Extract audio from video file.

    Args:
        video_path: Path to input video file
        output_path: Path for output audio (default: same dir as video)
        audio_format: Output format (mp3, wav, etc.)
        sample_rate: Audio sample rate in Hz (16000 for Whisper)

    Returns:
        Path to extracted audio file
    """
    video_path = Path(video_path)

    if output_path is None:
        output_path = video_path.with_suffix(f".{audio_format}")
    else:
        output_path = Path(output_path)

    # ffmpeg command to extract audio
    cmd = [
        "ffmpeg",
        "-i", str(video_path),
        "-vn",  # No video
        "-acodec", "libmp3lame" if audio_format == "mp3" else "pcm_s16le",
        "-ar", str(sample_rate),  # Sample rate
        "-ac", "1",  # Mono
        "-y",  # Overwrite
        str(output_path)
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg error: {result.stderr}")

    return str(output_path)


def extract_and_speedup(
    video_path: str,
    output_dir: Optional[str] = None,
    speed_factor: float = 2.0,
    audio_format: str = "mp3",
    sample_rate: int = 16000
) -> Dict[str, Any]:
    """
    Extract audio from video and apply speedup for cost-efficient transcription.

    The speedup reduces audio duration, cutting transcription costs proportionally.
    Timestamps will need to be normalized after transcription.

    Args:
        video_path: Path to input video file
        output_dir: Directory for output files (default: same as video)
        speed_factor: Speedup multiplier (2.0 = 50% cost reduction)
        audio_format: Output format
        sample_rate: Audio sample rate

    Returns:
        Dict with:
            - original_path: Path to original video
            - audio_path: Path to sped-up audio
            - speed_factor: Applied speedup
            - original_duration: Duration before speedup
            - processed_duration: Duration after speedup
    """
    video_path = Path(video_path)

    if output_dir is None:
        output_dir = video_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    # Output filename with speed indicator
    output_name = f"{video_path.stem}_audio_{speed_factor}x.{audio_format}"
    output_path = output_dir / output_name

    # Get original duration
    probe_cmd = [
        "ffprobe",
        "-v", "quiet",
        "-show_entries", "format=duration",
        "-of", "json",
        str(video_path)
    ]

    probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)

    original_duration = 0.0
    if probe_result.returncode == 0:
        try:
            probe_data = json.loads(probe_result.stdout)
            original_duration = float(probe_data.get("format", {}).get("duration", 0))
        except (json.JSONDecodeError, ValueError):
            pass

    # ffmpeg command with atempo filter for speedup
    # atempo only supports 0.5-2.0, so chain multiple for higher speeds
    atempo_filters = []
    remaining_speed = speed_factor

    while remaining_speed > 2.0:
        atempo_filters.append("atempo=2.0")
        remaining_speed /= 2.0

    if remaining_speed > 0.5:
        atempo_filters.append(f"atempo={remaining_speed}")

    filter_chain = ",".join(atempo_filters) if atempo_filters else "atempo=1.0"

    cmd = [
        "ffmpeg",
        "-i", str(video_path),
        "-vn",  # No video
        "-filter:a", filter_chain,
        "-acodec", "libmp3lame" if audio_format == "mp3" else "pcm_s16le",
        "-ar", str(sample_rate),
        "-ac", "1",  # Mono
        "-y",  # Overwrite
        str(output_path)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg error: {result.stderr}")

    # Calculate processed duration
    processed_duration = original_duration / speed_factor if original_duration > 0 else 0

    return {
        "original_path": str(video_path),
        "audio_path": str(output_path),
        "speed_factor": speed_factor,
        "original_duration": original_duration,
        "processed_duration": processed_duration,
        "cost_reduction": f"{(1 - 1/speed_factor) * 100:.0f}%"
    }


def process_video_batch(
    video_paths: List[str],
    output_dir: str,
    speed_factor: float = 2.0,
    audio_format: str = "mp3"
) -> List[Dict[str, Any]]:
    """
    Process multiple videos, extracting and speeding up audio.

    Args:
        video_paths: List of video file paths
        output_dir: Directory for all output files
        speed_factor: Speedup multiplier
        audio_format: Output audio format

    Returns:
        List of result dicts for each video
    """
    results = []
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for video_path in tqdm(video_paths, desc="Extracting audio"):
        try:
            result = extract_and_speedup(
                video_path,
                output_dir,
                speed_factor,
                audio_format
            )
            result["status"] = "success"
        except Exception as e:
            result = {
                "original_path": video_path,
                "status": "error",
                "error": str(e)
            }

        results.append(result)

    # Summary
    successful = sum(1 for r in results if r.get("status") == "success")
    total_original = sum(r.get("original_duration", 0) for r in results if r.get("status") == "success")
    total_processed = sum(r.get("processed_duration", 0) for r in results if r.get("status") == "success")

    print(f"\nProcessed {successful}/{len(video_paths)} videos")
    print(f"Total original duration: {total_original/3600:.1f} hours")
    print(f"Total processed duration: {total_processed/3600:.1f} hours")
    print(f"Time saved: {(total_original - total_processed)/3600:.1f} hours")

    return results


def find_videos_in_directory(
    directory: str,
    extensions: List[str] = [".mp4", ".mov", ".avi", ".mkv", ".webm"]
) -> List[str]:
    """
    Recursively find all video files in a directory.

    Args:
        directory: Root directory to search
        extensions: Video file extensions to include

    Returns:
        List of video file paths
    """
    directory = Path(directory)
    videos = []

    for ext in extensions:
        videos.extend(directory.rglob(f"*{ext}"))

    return [str(v) for v in sorted(videos)]


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) < 2:
        print("Usage: python audio_extractor.py <video_path_or_directory>")
        sys.exit(1)

    input_path = sys.argv[1]

    if os.path.isdir(input_path):
        videos = find_videos_in_directory(input_path)
        print(f"Found {len(videos)} videos")

        if videos:
            output_dir = os.path.join(input_path, "extracted_audio")
            results = process_video_batch(videos, output_dir)

            # Save results
            results_path = os.path.join(output_dir, "extraction_results.json")
            with open(results_path, "w") as f:
                json.dump(results, f, indent=2)
            print(f"Results saved to {results_path}")
    else:
        result = extract_and_speedup(input_path)
        print(json.dumps(result, indent=2))
