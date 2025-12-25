# Video Processing Pipeline

---
description: Process scraped videos through transcription, frame extraction, and OCR
activation_triggers:
  - "transcribe video"
  - "extract text from video"
  - "process video"
  - "OCR video"
  - "whisper transcription"
related_skills:
  - data-scraper
  - content-analyzer
  - research-pipeline
---

## When to Use

- Processing scraped videos before AI analysis
- Need transcripts for content analysis
- Extracting on-screen text (captions, graphics)
- Preparing video content for semantic analysis

## When NOT to Use

- Scraping videos (use data-scraper first)
- Analyzing transcripts (use content-analyzer after)
- Creating reports (use report-generator)

## You Are

A media engineer at CCM who has processed 1,500+ videos. You know the 4-stage pipeline, Whisper model tradeoffs, and when Gemini OCR is worth the cost.

## The 4-Stage Pipeline

```
Video → Audio → Transcript → Frames → OCR Text
        Stage 1   Stage 2     Stage 3   Stage 4
```

| Stage | Tool | Output | Cost |
|-------|------|--------|------|
| Audio extraction | FFmpeg | WAV file | Free |
| Transcription | Whisper | JSON + SRT | Free (local) |
| Frame extraction | FFmpeg | PNG images | Free |
| OCR | Gemini Vision | Text JSON | ~$0.0001/image |

## Stage 1: Audio Extraction

```python
import subprocess
from pathlib import Path

def extract_audio(video_path: Path, output_dir: Path, speedup: float = 2.0) -> Path:
    output_path = output_dir / f"{video_path.stem}.wav"

    cmd = [
        'ffmpeg', '-i', str(video_path),
        '-vn',                    # No video
        '-acodec', 'pcm_s16le',   # WAV format
        '-ar', '16000',           # 16kHz for Whisper
        '-ac', '1',               # Mono
        '-filter:a', f'atempo={speedup}',
        str(output_path), '-y'
    ]

    subprocess.run(cmd, capture_output=True, check=True)
    return output_path
```

## Stage 2: Transcription

```python
import whisper

def transcribe(audio_path: Path, model_name: str = 'base') -> dict:
    model = whisper.load_model(model_name)
    result = model.transcribe(str(audio_path), language='en')

    return {
        'text': result['text'],
        'segments': [
            {'start': s['start'], 'end': s['end'], 'text': s['text'].strip()}
            for s in result['segments']
        ],
        'word_count': len(result['text'].split()),
    }
```

**Whisper Model Selection:**

| Model | Speed | Quality | VRAM | Use For |
|-------|-------|---------|------|---------|
| tiny | Fastest | Low | 1GB | Testing pipeline |
| base | Fast | Good | 1GB | **Default** |
| small | Medium | Better | 2GB | Production |
| large | Slow | Best | 10GB | Poor audio |

## Stage 3: Frame Extraction

```python
def extract_frames(video_path: Path, output_dir: Path, fps: float = 1.0) -> list:
    frames_dir = output_dir / 'frames'
    frames_dir.mkdir(exist_ok=True)

    cmd = [
        'ffmpeg', '-i', str(video_path),
        '-vf', f'fps={fps}',
        '-q:v', '2',
        str(frames_dir / 'frame_%04d.png'), '-y'
    ]

    subprocess.run(cmd, capture_output=True, check=True)
    return sorted(frames_dir.glob('frame_*.png'))
```

**FPS Guidelines:**
- 1.0 FPS: Standard (30s video = 30 frames = $0.003 OCR)
- 0.5 FPS: Budget-conscious
- 2.0 FPS: Fast-changing content

## Stage 4: OCR (Gemini Vision)

```python
import google.generativeai as genai
import base64

def process_frame_ocr(frame_path: Path) -> dict:
    model = genai.GenerativeModel('gemini-2.0-flash')

    with open(frame_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode()

    response = model.generate_content([
        {'mime_type': 'image/png', 'data': image_data},
        """Extract ALL visible text: captions, overlays, usernames, hashtags.
        Return JSON: {"texts": [...], "entities": {"people": [], "orgs": []}}"""
    ])

    return {'frame': frame_path.name, 'ocr': response.text}
```

## Batch Processing

```python
def process_batch(videos: list, output_dir: Path, batch_size: int = 100):
    checkpoint_path = output_dir / 'checkpoint.json'
    completed = load_checkpoint(checkpoint_path)
    cost_tracker = {'gemini_calls': 0, 'cost_usd': 0.0}

    for video_path in videos:
        video_id = video_path.stem
        if video_id in completed:
            continue

        try:
            video_dir = output_dir / video_id
            video_dir.mkdir(exist_ok=True)

            # Run pipeline
            audio = extract_audio(video_path, video_dir)
            transcript = transcribe(audio, 'base')
            frames = extract_frames(video_path, video_dir, fps=1.0)

            # OCR (track costs)
            ocr_results = []
            for frame in frames:
                ocr = process_frame_ocr(frame)
                ocr_results.append(ocr)
                cost_tracker['gemini_calls'] += 1
                cost_tracker['cost_usd'] += 0.0001

            # Save
            save_results(video_dir, transcript, ocr_results)
            completed.add(video_id)

            if len(completed) % 10 == 0:
                save_checkpoint(checkpoint_path, completed)

        except Exception as e:
            logger.error(f"Failed {video_id}: {e}")
            continue

    return cost_tracker
```

## Output Structure

```
video_results/
├── checkpoint.json
├── processing_summary.json
└── video_123/
    ├── video_123_transcript.json
    ├── video_123.srt
    ├── frames/
    │   ├── frame_0001.png
    │   └── frame_0002.png
    └── ocr_results.json
```

## Cost Estimation

| Content | Frames | OCR Cost |
|---------|--------|----------|
| 30s video @ 1 FPS | 30 | $0.003 |
| 60s video @ 1 FPS | 60 | $0.006 |
| 1000 videos avg 45s | ~45,000 | ~$4.50 |

**NJ Influencer project**: ~$3 total for video OCR.

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Skip audio speedup | Slower transcription | Use 2x speedup |
| Use large Whisper model | Slow, high VRAM | Start with base |
| Extract at high FPS | Expensive OCR | 1 FPS is enough |
| OCR every frame | Redundant text | Deduplicate results |
| Skip checkpointing | Lose progress on failure | Save every 10 |

## Output

Save to: `/social-scraper/analysis/video_results/`
