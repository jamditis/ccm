# Video Processing Pipeline

Process scraped videos through transcription, frame extraction, and OCR. Use when preparing video content for AI analysis.

## You Are

A media engineer at CCM who has processed 1,500+ videos. You know the 4-stage pipeline, Whisper model tradeoffs, and Gemini Vision API integration for OCR.

## 4-Stage Pipeline

```
Video → Audio Extraction → Transcription → Frame Extraction → OCR
         (FFmpeg)          (Whisper)        (FFmpeg)         (Gemini)
```

**Location:** `/social-scraper/analysis/video_processor/`

## Stage 1: Audio Extraction

```python
# audio_extractor.py
import subprocess
from pathlib import Path

def extract_audio(video_path: Path, output_dir: Path, speedup: float = 2.0) -> Path:
    """Extract audio from video with optional speedup."""
    output_path = output_dir / f"{video_path.stem}.wav"

    cmd = [
        'ffmpeg', '-i', str(video_path),
        '-vn',  # No video
        '-acodec', 'pcm_s16le',  # WAV format
        '-ar', '16000',  # 16kHz for Whisper
        '-ac', '1',  # Mono
        '-filter:a', f'atempo={speedup}',  # Speed up
        str(output_path),
        '-y'  # Overwrite
    ]

    subprocess.run(cmd, capture_output=True, check=True)
    return output_path
```

## Stage 2: Transcription (Whisper)

```python
# transcriber.py
import whisper
from pathlib import Path

# Model selection based on needs
WHISPER_MODELS = {
    'tiny': {'speed': 'fastest', 'quality': 'lowest', 'vram': '1GB'},
    'base': {'speed': 'fast', 'quality': 'good', 'vram': '1GB'},
    'small': {'speed': 'medium', 'quality': 'better', 'vram': '2GB'},
    'medium': {'speed': 'slow', 'quality': 'great', 'vram': '5GB'},
    'large': {'speed': 'slowest', 'quality': 'best', 'vram': '10GB'},
}

def transcribe(audio_path: Path, model_name: str = 'base') -> dict:
    """Transcribe audio using Whisper."""
    model = whisper.load_model(model_name)

    result = model.transcribe(
        str(audio_path),
        language='en',
        verbose=False,
    )

    return {
        'text': result['text'],
        'segments': [
            {
                'start': seg['start'],
                'end': seg['end'],
                'text': seg['text'].strip(),
            }
            for seg in result['segments']
        ],
        'language': result['language'],
        'word_count': len(result['text'].split()),
    }

def save_srt(segments: list, output_path: Path):
    """Save transcript as SRT subtitle file."""
    with open(output_path, 'w') as f:
        for i, seg in enumerate(segments, 1):
            start = format_timestamp(seg['start'])
            end = format_timestamp(seg['end'])
            f.write(f"{i}\n{start} --> {end}\n{seg['text']}\n\n")

def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
```

## Stage 3: Frame Extraction

```python
# frame_extractor.py
import subprocess
from pathlib import Path

def extract_frames(video_path: Path, output_dir: Path, fps: float = 1.0) -> list:
    """Extract frames at specified FPS."""
    frames_dir = output_dir / 'frames'
    frames_dir.mkdir(exist_ok=True)

    output_pattern = str(frames_dir / 'frame_%04d.png')

    cmd = [
        'ffmpeg', '-i', str(video_path),
        '-vf', f'fps={fps}',  # Extract at FPS
        '-q:v', '2',  # High quality
        output_pattern,
        '-y'
    ]

    subprocess.run(cmd, capture_output=True, check=True)

    return sorted(frames_dir.glob('frame_*.png'))
```

## Stage 4: OCR (Gemini Vision)

```python
# ocr_processor.py
import google.generativeai as genai
from pathlib import Path
import base64

def process_frame_ocr(frame_path: Path, model_name: str = 'gemini-2.0-flash') -> dict:
    """Extract text from frame using Gemini Vision."""
    model = genai.GenerativeModel(model_name)

    with open(frame_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode()

    response = model.generate_content([
        {
            'mime_type': 'image/png',
            'data': image_data,
        },
        """Extract ALL visible text from this image.
        Include: captions, overlays, usernames, hashtags, on-screen text.
        Return as JSON: {"text": [...], "entities": {"people": [], "organizations": [], "locations": []}}"""
    ])

    return {
        'frame': frame_path.name,
        'ocr_result': response.text,
        'model': model_name,
    }

def deduplicate_ocr(ocr_results: list) -> dict:
    """Remove duplicate text across frames."""
    seen_text = set()
    unique_texts = []

    for result in ocr_results:
        texts = result.get('text', [])
        for text in texts:
            normalized = text.strip().lower()
            if normalized not in seen_text:
                seen_text.add(normalized)
                unique_texts.append(text)

    return {'unique_texts': unique_texts, 'total_frames': len(ocr_results)}
```

## Batch Processing

```python
# batch_process.py
from pathlib import Path
import json

def process_batch(
    videos: list,
    output_dir: Path,
    whisper_model: str = 'base',
    fps: float = 1.0,
    batch_size: int = 100,
):
    """Process videos in batches with checkpointing."""
    results_dir = output_dir / 'video_results'
    results_dir.mkdir(exist_ok=True)

    checkpoint_path = results_dir / 'checkpoint.json'
    completed = load_checkpoint(checkpoint_path)

    cost_tracker = {'gemini_calls': 0, 'estimated_usd': 0.0}

    for i, video_path in enumerate(videos):
        video_id = video_path.stem
        if video_id in completed:
            continue

        try:
            # Stage 1: Audio
            audio_path = extract_audio(video_path, results_dir)

            # Stage 2: Transcription
            transcript = transcribe(audio_path, whisper_model)

            # Stage 3: Frames
            frames = extract_frames(video_path, results_dir / video_id, fps)

            # Stage 4: OCR (track costs)
            ocr_results = []
            for frame in frames:
                ocr = process_frame_ocr(frame)
                ocr_results.append(ocr)
                cost_tracker['gemini_calls'] += 1
                cost_tracker['estimated_usd'] += 0.0001  # ~$0.0001/call

            # Save results
            result = {
                'video_id': video_id,
                'transcript': transcript,
                'ocr': deduplicate_ocr(ocr_results),
            }

            with open(results_dir / f'{video_id}_result.json', 'w') as f:
                json.dump(result, f, indent=2)

            completed.add(video_id)

            # Checkpoint every 10 videos
            if len(completed) % 10 == 0:
                save_checkpoint(checkpoint_path, completed)

        except Exception as e:
            logger.error(f"Failed {video_id}: {e}")
            continue

    # Final summary
    save_summary(results_dir, len(completed), cost_tracker)
```

## Model Selection Guide

| Use Case | Whisper Model | Why |
|----------|--------------|-----|
| Development/testing | tiny | Fastest, test pipeline |
| Short content (<60s) | base | Good quality, fast |
| Standard content | small | Production quality |
| Long-form/podcasts | medium | Best for long content |
| Poor audio/accents | large | Maximum accuracy |

## Output Structure

```
video_results/
├── checkpoint.json
├── processing_summary.json
├── video_001/
│   ├── video_001_transcript.json
│   ├── video_001.srt
│   ├── frames/
│   │   ├── frame_0001.png
│   │   ├── frame_0002.png
│   │   └── ...
│   └── ocr/
│       └── ocr_results.json
└── video_002/
    └── ...
```

## Cost Estimation

| Stage | Tool | Cost |
|-------|------|------|
| Audio extraction | FFmpeg | Free |
| Transcription | Whisper (local) | Free (GPU time) |
| Transcription | OpenAI Whisper API | $0.006/min |
| Frame extraction | FFmpeg | Free |
| OCR | Gemini 2.0 Flash | ~$0.0001/image |

**Typical 30s video:** ~30 frames × $0.0001 = $0.003 OCR cost
