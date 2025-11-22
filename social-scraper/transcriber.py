"""
Transcription Module

Uses OpenAI Whisper (local) to transcribe audio files.
Includes timestamp normalization for sped-up audio.

Usage:
    from video_processor import transcribe_with_speedup

    # Transcribe with automatic timestamp correction
    result = transcribe_with_speedup(
        audio_path="audio_2x.mp3",
        speed_factor=2.0,
        model="medium"
    )
"""

import os
import json
import whisper
import torch
from pathlib import Path
from typing import Optional, List, Dict, Any
from tqdm import tqdm


# Global model cache
_model_cache = {}


def get_device():
    """Get the best available device for Whisper (MPS for M1, CUDA, or CPU)."""
    if torch.backends.mps.is_available():
        return "mps"
    elif torch.cuda.is_available():
        return "cuda"
    return "cpu"


def load_model(model_name: str = "medium") -> whisper.Whisper:
    """
    Load Whisper model with caching.

    Args:
        model_name: Model size (tiny, base, small, medium, large)

    Returns:
        Loaded Whisper model
    """
    if model_name not in _model_cache:
        device = get_device()
        print(f"Loading Whisper model: {model_name} on {device}")
        _model_cache[model_name] = whisper.load_model(model_name, device=device)
    return _model_cache[model_name]


def transcribe_audio(
    audio_path: str,
    model: str = "medium",
    language: Optional[str] = "en",
    task: str = "transcribe"
) -> Dict[str, Any]:
    """
    Transcribe audio file using Whisper.

    Args:
        audio_path: Path to audio file
        model: Whisper model size
        language: Language code (None for auto-detect)
        task: "transcribe" or "translate"

    Returns:
        Dict with:
            - text: Full transcript
            - segments: List of segments with timestamps
            - language: Detected language
    """
    whisper_model = load_model(model)

    result = whisper_model.transcribe(
        audio_path,
        language=language,
        task=task,
        verbose=False
    )

    return {
        "text": result["text"],
        "segments": result["segments"],
        "language": result["language"]
    }


def normalize_timestamps(
    segments: List[Dict[str, Any]],
    speed_factor: float
) -> List[Dict[str, Any]]:
    """
    Normalize timestamps from sped-up audio back to original timing.

    Formula: original_time = transcribed_time * speed_factor

    Args:
        segments: List of transcript segments with start/end times
        speed_factor: The speedup that was applied to audio

    Returns:
        Segments with corrected timestamps
    """
    normalized = []

    for segment in segments:
        normalized_segment = segment.copy()
        normalized_segment["start"] = segment["start"] * speed_factor
        normalized_segment["end"] = segment["end"] * speed_factor

        # Also update word-level timestamps if present
        if "words" in segment:
            normalized_segment["words"] = []
            for word in segment["words"]:
                normalized_word = word.copy()
                normalized_word["start"] = word["start"] * speed_factor
                normalized_word["end"] = word["end"] * speed_factor
                normalized_segment["words"].append(normalized_word)

        normalized.append(normalized_segment)

    return normalized


def transcribe_with_speedup(
    audio_path: str,
    speed_factor: float = 2.0,
    model: str = "medium",
    language: Optional[str] = "en",
    output_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Transcribe sped-up audio and normalize timestamps.

    This is the main function for cost-optimized transcription:
    1. Transcribe the sped-up audio
    2. Normalize timestamps back to original video timing
    3. Optionally save results

    Args:
        audio_path: Path to sped-up audio file
        speed_factor: The speedup factor applied to the audio
        model: Whisper model size
        language: Language code
        output_path: Optional path to save JSON results

    Returns:
        Dict with:
            - text: Full transcript
            - segments: Timestamp-corrected segments
            - language: Detected language
            - speed_factor: Applied normalization factor
            - audio_path: Source audio file
    """
    # Transcribe
    result = transcribe_audio(audio_path, model, language)

    # Normalize timestamps
    result["segments"] = normalize_timestamps(result["segments"], speed_factor)
    result["speed_factor"] = speed_factor
    result["audio_path"] = audio_path

    # Save if output path provided
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

    return result


def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def export_to_srt(
    segments: List[Dict[str, Any]],
    output_path: str
) -> str:
    """
    Export segments to SRT subtitle format.

    Args:
        segments: List of transcript segments
        output_path: Path for SRT file

    Returns:
        Path to created SRT file
    """
    with open(output_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, 1):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()

            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")

    return output_path


def export_to_txt(
    result: Dict[str, Any],
    output_path: str,
    include_timestamps: bool = True
) -> str:
    """
    Export transcript to plain text.

    Args:
        result: Transcription result dict
        output_path: Path for text file
        include_timestamps: Whether to include segment timestamps

    Returns:
        Path to created text file
    """
    with open(output_path, "w", encoding="utf-8") as f:
        if include_timestamps:
            for segment in result["segments"]:
                start = segment["start"]
                text = segment["text"].strip()
                f.write(f"[{start:.1f}s] {text}\n")
        else:
            f.write(result["text"])

    return output_path


def batch_transcribe(
    audio_files: List[Dict[str, Any]],
    output_dir: str,
    model: str = "medium",
    language: Optional[str] = "en"
) -> List[Dict[str, Any]]:
    """
    Batch transcribe multiple audio files.

    Args:
        audio_files: List of dicts with 'audio_path' and 'speed_factor'
        output_dir: Directory for transcript outputs
        model: Whisper model size
        language: Language code

    Returns:
        List of transcription results
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    results = []

    # Load model once
    load_model(model)

    for audio_info in tqdm(audio_files, desc="Transcribing"):
        audio_path = audio_info["audio_path"]
        speed_factor = audio_info.get("speed_factor", 1.0)

        try:
            # Generate output filename
            audio_name = Path(audio_path).stem
            output_path = output_dir / f"{audio_name}_transcript.json"

            result = transcribe_with_speedup(
                audio_path,
                speed_factor,
                model,
                language,
                str(output_path)
            )

            # Also export SRT
            srt_path = output_dir / f"{audio_name}.srt"
            export_to_srt(result["segments"], str(srt_path))

            result["status"] = "success"
            result["output_path"] = str(output_path)
            result["srt_path"] = str(srt_path)

        except Exception as e:
            result = {
                "audio_path": audio_path,
                "status": "error",
                "error": str(e)
            }

        results.append(result)

    # Summary
    successful = sum(1 for r in results if r.get("status") == "success")
    print(f"\nTranscribed {successful}/{len(audio_files)} files")

    return results


def get_transcript_stats(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate statistics from a transcription result.

    Args:
        result: Transcription result dict

    Returns:
        Stats dict with word count, duration, speaking rate, etc.
    """
    segments = result.get("segments", [])

    if not segments:
        return {}

    total_words = sum(len(s["text"].split()) for s in segments)
    total_duration = segments[-1]["end"] - segments[0]["start"]
    speaking_rate = total_words / (total_duration / 60) if total_duration > 0 else 0

    return {
        "word_count": total_words,
        "segment_count": len(segments),
        "duration_seconds": total_duration,
        "speaking_rate_wpm": round(speaking_rate, 1),
        "language": result.get("language", "unknown")
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python transcriber.py <audio_path> [speed_factor] [model]")
        print("Example: python transcriber.py audio_2x.mp3 2.0 medium")
        sys.exit(1)

    audio_path = sys.argv[1]
    speed_factor = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    model = sys.argv[3] if len(sys.argv) > 3 else "medium"

    print(f"Transcribing: {audio_path}")
    print(f"Speed factor: {speed_factor}x")
    print(f"Model: {model}")

    result = transcribe_with_speedup(audio_path, speed_factor, model)

    # Save outputs
    base_name = Path(audio_path).stem
    output_dir = Path(audio_path).parent

    json_path = output_dir / f"{base_name}_transcript.json"
    srt_path = output_dir / f"{base_name}.srt"
    txt_path = output_dir / f"{base_name}_transcript.txt"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    export_to_srt(result["segments"], str(srt_path))
    export_to_txt(result, str(txt_path))

    # Print stats
    stats = get_transcript_stats(result)
    print(f"\nTranscription complete:")
    print(f"  Words: {stats.get('word_count', 0)}")
    print(f"  Duration: {stats.get('duration_seconds', 0):.1f}s")
    print(f"  Speaking rate: {stats.get('speaking_rate_wpm', 0)} WPM")
    print(f"\nOutputs:")
    print(f"  JSON: {json_path}")
    print(f"  SRT: {srt_path}")
    print(f"  TXT: {txt_path}")
