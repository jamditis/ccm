"""
Video Processing Module for NJ Influencer Analysis

Extracts transcripts and visual content from scraped videos using:
- ffmpeg for audio extraction and speedup
- Whisper for transcription
- Tesseract + Gemini for OCR

Cost optimizations:
- 2x audio speedup reduces transcription time by 50%
- Tesseract-first cascade minimizes expensive LLM calls
"""

from .audio_extractor import (
    extract_audio,
    extract_and_speedup,
    process_video_batch,
    find_videos_in_directory
)

from .transcriber import (
    transcribe_audio,
    normalize_timestamps,
    transcribe_with_speedup,
    batch_transcribe,
    export_to_srt
)

from .frame_extractor import (
    extract_frames,
    extract_keyframes,
    batch_extract_frames
)

from .ocr_processor import (
    ocr_with_tesseract,
    ocr_with_gemini,
    create_frame_grid,
    ocr_grid_with_gemini,
    process_frame_ocr,
    process_frames_ocr,
    deduplicate_text,
    extract_entities
)

__all__ = [
    # Audio
    'extract_audio',
    'extract_and_speedup',
    'process_video_batch',
    'find_videos_in_directory',
    # Transcription
    'transcribe_audio',
    'normalize_timestamps',
    'transcribe_with_speedup',
    'batch_transcribe',
    'export_to_srt',
    # Frames
    'extract_frames',
    'extract_keyframes',
    'batch_extract_frames',
    # OCR
    'ocr_with_tesseract',
    'ocr_with_gemini',
    'create_frame_grid',
    'ocr_grid_with_gemini',
    'process_frame_ocr',
    'process_frames_ocr',
    'deduplicate_text',
    'extract_entities'
]
