"""
Frame Extraction Module

Extracts frames from videos at regular intervals for OCR processing.
Uses ffmpeg for efficient frame extraction.

Usage:
    from video_processor import extract_frames

    # Extract 1 frame per second
    frames = extract_frames("video.mp4", "frames_dir/", fps=1)
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from tqdm import tqdm


def extract_frames(
    video_path: str,
    output_dir: str,
    fps: float = 1.0,
    quality: int = 2,
    max_frames: Optional[int] = None
) -> Dict[str, Any]:
    """
    Extract frames from video at specified frame rate.

    Args:
        video_path: Path to input video
        output_dir: Directory for extracted frames
        fps: Frames per second to extract (1.0 = 1 frame/sec)
        quality: JPEG quality (1-31, lower is better)
        max_frames: Maximum frames to extract (None for all)

    Returns:
        Dict with extraction results
    """
    video_path = Path(video_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get video info
    probe_cmd = [
        "ffprobe",
        "-v", "quiet",
        "-show_entries", "format=duration:stream=width,height,r_frame_rate",
        "-of", "json",
        str(video_path)
    ]

    probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
    video_info = {"duration": 0, "width": 0, "height": 0, "fps": 0}

    if probe_result.returncode == 0:
        try:
            data = json.loads(probe_result.stdout)
            video_info["duration"] = float(data.get("format", {}).get("duration", 0))

            if data.get("streams"):
                stream = data["streams"][0]
                video_info["width"] = stream.get("width", 0)
                video_info["height"] = stream.get("height", 0)

                # Parse frame rate (e.g., "30/1" or "29.97")
                fps_str = stream.get("r_frame_rate", "0/1")
                if "/" in fps_str:
                    num, den = fps_str.split("/")
                    video_info["fps"] = float(num) / float(den) if float(den) > 0 else 0
                else:
                    video_info["fps"] = float(fps_str)
        except (json.JSONDecodeError, ValueError, KeyError):
            pass

    # Calculate expected frames
    expected_frames = int(video_info["duration"] * fps)
    if max_frames and expected_frames > max_frames:
        expected_frames = max_frames

    # Output pattern
    output_pattern = output_dir / f"{video_path.stem}_frame_%04d.jpg"

    # Build ffmpeg command
    cmd = [
        "ffmpeg",
        "-i", str(video_path),
        "-vf", f"fps={fps}",
        "-qscale:v", str(quality),
        "-y"
    ]

    if max_frames:
        cmd.extend(["-frames:v", str(max_frames)])

    cmd.append(str(output_pattern))

    # Run extraction
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg error: {result.stderr}")

    # Count extracted frames
    frames = sorted(output_dir.glob(f"{video_path.stem}_frame_*.jpg"))

    return {
        "video_path": str(video_path),
        "output_dir": str(output_dir),
        "frame_count": len(frames),
        "frames": [str(f) for f in frames],
        "fps_extracted": fps,
        "video_duration": video_info["duration"],
        "video_fps": video_info["fps"],
        "resolution": f"{video_info['width']}x{video_info['height']}"
    }


def extract_keyframes(
    video_path: str,
    output_dir: str,
    quality: int = 2
) -> Dict[str, Any]:
    """
    Extract only keyframes (I-frames) from video.

    Keyframes are typically scene changes, making them
    good candidates for OCR without redundancy.

    Args:
        video_path: Path to input video
        output_dir: Directory for extracted frames
        quality: JPEG quality

    Returns:
        Dict with extraction results
    """
    video_path = Path(video_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_pattern = output_dir / f"{video_path.stem}_keyframe_%04d.jpg"

    cmd = [
        "ffmpeg",
        "-i", str(video_path),
        "-vf", "select='eq(pict_type,I)'",
        "-vsync", "vfr",
        "-qscale:v", str(quality),
        "-y",
        str(output_pattern)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg error: {result.stderr}")

    frames = sorted(output_dir.glob(f"{video_path.stem}_keyframe_*.jpg"))

    return {
        "video_path": str(video_path),
        "output_dir": str(output_dir),
        "frame_count": len(frames),
        "frames": [str(f) for f in frames],
        "extraction_type": "keyframes"
    }


def extract_frames_at_timestamps(
    video_path: str,
    timestamps: List[float],
    output_dir: str,
    quality: int = 2
) -> Dict[str, Any]:
    """
    Extract frames at specific timestamps.

    Useful for extracting frames at transcript segment boundaries.

    Args:
        video_path: Path to input video
        timestamps: List of times in seconds
        output_dir: Directory for extracted frames
        quality: JPEG quality

    Returns:
        Dict with extraction results
    """
    video_path = Path(video_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    frames = []

    for i, ts in enumerate(timestamps):
        output_path = output_dir / f"{video_path.stem}_ts{ts:.1f}s_{i:04d}.jpg"

        cmd = [
            "ffmpeg",
            "-ss", str(ts),
            "-i", str(video_path),
            "-vframes", "1",
            "-qscale:v", str(quality),
            "-y",
            str(output_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0 and output_path.exists():
            frames.append({
                "path": str(output_path),
                "timestamp": ts
            })

    return {
        "video_path": str(video_path),
        "output_dir": str(output_dir),
        "frame_count": len(frames),
        "frames": frames,
        "extraction_type": "timestamps"
    }


def batch_extract_frames(
    video_paths: List[str],
    output_base_dir: str,
    fps: float = 1.0,
    quality: int = 2
) -> List[Dict[str, Any]]:
    """
    Extract frames from multiple videos.

    Args:
        video_paths: List of video file paths
        output_base_dir: Base directory for all outputs
        fps: Frames per second
        quality: JPEG quality

    Returns:
        List of extraction results
    """
    results = []
    output_base = Path(output_base_dir)

    for video_path in tqdm(video_paths, desc="Extracting frames"):
        video_name = Path(video_path).stem
        output_dir = output_base / video_name

        try:
            result = extract_frames(video_path, str(output_dir), fps, quality)
            result["status"] = "success"
        except Exception as e:
            result = {
                "video_path": video_path,
                "status": "error",
                "error": str(e)
            }

        results.append(result)

    # Summary
    successful = sum(1 for r in results if r.get("status") == "success")
    total_frames = sum(r.get("frame_count", 0) for r in results)

    print(f"\nExtracted frames from {successful}/{len(video_paths)} videos")
    print(f"Total frames: {total_frames}")

    return results


def cleanup_frames(output_dir: str, keep_every_n: int = 1) -> int:
    """
    Clean up extracted frames, optionally keeping only every Nth frame.

    Useful for reducing storage after processing.

    Args:
        output_dir: Directory containing frames
        keep_every_n: Keep every Nth frame (1 = keep all)

    Returns:
        Number of frames deleted
    """
    output_dir = Path(output_dir)
    frames = sorted(output_dir.glob("*.jpg"))

    deleted = 0
    for i, frame in enumerate(frames):
        if keep_every_n > 1 and i % keep_every_n != 0:
            frame.unlink()
            deleted += 1

    return deleted


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python frame_extractor.py <video_path> [fps] [output_dir]")
        print("Example: python frame_extractor.py video.mp4 1.0 frames/")
        sys.exit(1)

    video_path = sys.argv[1]
    fps = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    output_dir = sys.argv[3] if len(sys.argv) > 3 else f"{Path(video_path).stem}_frames"

    print(f"Extracting frames from: {video_path}")
    print(f"FPS: {fps}")
    print(f"Output: {output_dir}")

    result = extract_frames(video_path, output_dir, fps)

    print(f"\nExtracted {result['frame_count']} frames")
    print(f"Video duration: {result['video_duration']:.1f}s")
    print(f"Resolution: {result['resolution']}")
