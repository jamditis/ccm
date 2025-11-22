"""
OCR Processing Module

Extracts text from video frames using a cascading approach:
1. Tesseract OCR (fast, free) - first pass
2. Gemini Vision (accurate, paid) - for low-confidence or complex content

Usage:
    from video_processor import process_frames_ocr

    results = process_frames_ocr(
        frame_paths,
        output_dir,
        gemini_api_key="your-key"
    )
"""

import os
import json
import base64
from pathlib import Path
from typing import Optional, List, Dict, Any
from tqdm import tqdm

import pytesseract
from PIL import Image, ImageDraw, ImageFont
import math

# Optional Gemini import
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


def ocr_with_tesseract(
    image_path: str,
    lang: str = "eng",
    config: str = "--psm 6"
) -> Dict[str, Any]:
    """
    Extract text from image using Tesseract OCR.

    Args:
        image_path: Path to image file
        lang: Language code (eng, spa, etc.)
        config: Tesseract configuration

    Returns:
        Dict with text and confidence data
    """
    image = Image.open(image_path)

    # Get detailed data with confidence scores
    data = pytesseract.image_to_data(
        image,
        lang=lang,
        config=config,
        output_type=pytesseract.Output.DICT
    )

    # Extract text and calculate average confidence
    words = []
    confidences = []

    for i, word in enumerate(data["text"]):
        if word.strip():
            conf = int(data["conf"][i])
            if conf > 0:  # -1 means no confidence available
                words.append(word)
                confidences.append(conf)

    text = " ".join(words)
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0

    # Also get bounding boxes for words
    word_boxes = []
    for i, word in enumerate(data["text"]):
        if word.strip() and int(data["conf"][i]) > 0:
            word_boxes.append({
                "text": word,
                "confidence": int(data["conf"][i]),
                "x": data["left"][i],
                "y": data["top"][i],
                "width": data["width"][i],
                "height": data["height"][i]
            })

    return {
        "text": text,
        "word_count": len(words),
        "avg_confidence": round(avg_confidence, 1),
        "word_boxes": word_boxes,
        "engine": "tesseract"
    }


def ocr_with_gemini(
    image_path: str,
    api_key: str,
    model: str = "gemini-2.5-flash",
    prompt: Optional[str] = None
) -> Dict[str, Any]:
    """
    Extract text from image using Gemini Vision.

    Args:
        image_path: Path to image file
        api_key: Gemini API key
        model: Gemini model to use
        prompt: Custom prompt (default: extract all text)

    Returns:
        Dict with extracted text and analysis
    """
    if not GEMINI_AVAILABLE:
        raise ImportError("google-generativeai not installed")

    genai.configure(api_key=api_key)

    # Read and encode image
    with open(image_path, "rb") as f:
        image_data = f.read()

    # Default prompt for text extraction
    if prompt is None:
        prompt = """Extract ALL text visible in this image. Include:
- Main text/titles
- Captions/subtitles
- Any on-screen text overlays
- Brand names/logos with text
- Numbers and statistics shown

Format as plain text, preserving line breaks where logical.
If no text is visible, respond with "NO_TEXT_DETECTED"."""

    # Create model and generate
    model_instance = genai.GenerativeModel(model)

    response = model_instance.generate_content([
        prompt,
        {"mime_type": "image/jpeg", "data": image_data}
    ])

    text = response.text.strip()

    return {
        "text": text if text != "NO_TEXT_DETECTED" else "",
        "word_count": len(text.split()) if text != "NO_TEXT_DETECTED" else 0,
        "engine": "gemini",
        "model": model
    }


def create_frame_grid(
    frame_paths: List[str],
    grid_size: int = 4,
    thumb_size: tuple = (400, 400),
    label_height: int = 30
) -> Image.Image:
    """
    Create a grid image from multiple frames.

    Args:
        frame_paths: List of frame image paths
        grid_size: Number of frames per row/column (e.g., 4 = 4x4 grid)
        thumb_size: Size of each thumbnail
        label_height: Height of label area above each thumbnail

    Returns:
        PIL Image with grid of frames
    """
    n_frames = len(frame_paths)
    cols = min(grid_size, n_frames)
    rows = math.ceil(n_frames / cols)

    cell_width = thumb_size[0]
    cell_height = thumb_size[1] + label_height

    grid_width = cols * cell_width
    grid_height = rows * cell_height

    # Create grid image
    grid = Image.new('RGB', (grid_width, grid_height), color='white')
    draw = ImageDraw.Draw(grid)

    for i, frame_path in enumerate(frame_paths):
        row = i // cols
        col = i % cols

        x = col * cell_width
        y = row * cell_height

        # Draw label
        label = f"Frame {i + 1}"
        draw.rectangle([x, y, x + cell_width, y + label_height], fill='black')
        draw.text((x + 10, y + 5), label, fill='white')

        # Load and resize frame
        try:
            img = Image.open(frame_path)
            img.thumbnail(thumb_size, Image.Resampling.LANCZOS)

            # Center the thumbnail
            img_x = x + (cell_width - img.width) // 2
            img_y = y + label_height + (thumb_size[1] - img.height) // 2

            grid.paste(img, (img_x, img_y))
        except Exception as e:
            # Draw error placeholder
            draw.text((x + 10, y + label_height + 10), f"Error: {str(e)[:20]}", fill='red')

    return grid


def ocr_grid_with_gemini(
    frame_paths: List[str],
    api_key: str,
    model: str = "gemini-2.5-flash",
    grid_size: int = 4
) -> Dict[str, Any]:
    """
    Process multiple frames as a grid with Gemini.

    Args:
        frame_paths: List of frame image paths
        api_key: Gemini API key
        model: Gemini model to use
        grid_size: Frames per row/column in grid

    Returns:
        Dict with text extracted from each frame
    """
    if not GEMINI_AVAILABLE:
        raise ImportError("google-generativeai not installed")

    genai.configure(api_key=api_key)

    # Create grid image
    grid = create_frame_grid(frame_paths, grid_size)

    # Save to bytes
    import io
    img_bytes = io.BytesIO()
    grid.save(img_bytes, format='JPEG', quality=85)
    img_data = img_bytes.getvalue()

    # Prompt for grid analysis
    prompt = f"""This image contains a grid of {len(frame_paths)} video frames, labeled Frame 1 through Frame {len(frame_paths)}.

For EACH frame, extract ALL visible text including:
- Main text/titles
- Captions/subtitles
- On-screen text overlays
- Brand names/logos
- Numbers and statistics

Format your response as:
FRAME 1:
[text from frame 1]

FRAME 2:
[text from frame 2]

... and so on for all {len(frame_paths)} frames.

If a frame has no visible text, write "NO_TEXT" for that frame."""

    # Generate
    model_instance = genai.GenerativeModel(model)
    response = model_instance.generate_content([
        prompt,
        {"mime_type": "image/jpeg", "data": img_data}
    ])

    # Parse response
    response_text = response.text.strip()
    frame_texts = {}

    # Parse each frame's text
    import re
    pattern = r'FRAME\s*(\d+):\s*\n?(.*?)(?=FRAME\s*\d+:|$)'
    matches = re.findall(pattern, response_text, re.DOTALL | re.IGNORECASE)

    for match in matches:
        frame_num = int(match[0])
        text = match[1].strip()
        if text.upper() == "NO_TEXT":
            text = ""
        frame_texts[frame_num] = text

    return {
        "frame_texts": frame_texts,
        "raw_response": response_text,
        "frame_count": len(frame_paths),
        "engine": "gemini_grid",
        "model": model
    }


def should_escalate_to_gemini(
    tesseract_result: Dict[str, Any],
    confidence_threshold: float = 70.0,
    min_words: int = 3
) -> bool:
    """
    Determine if Gemini should be used for better results.

    Args:
        tesseract_result: Result from Tesseract OCR
        confidence_threshold: Escalate if below this confidence
        min_words: Escalate if fewer words detected

    Returns:
        True if Gemini should be used
    """
    # Low confidence
    if tesseract_result["avg_confidence"] < confidence_threshold:
        return True

    # Very few words (might be missing text)
    if tesseract_result["word_count"] < min_words:
        return True

    # Check for signs of complex content
    # (This could be expanded with image analysis)

    return False


def process_frame_ocr(
    frame_path: str,
    gemini_api_key: Optional[str] = None,
    confidence_threshold: float = 70.0,
    always_use_gemini: bool = False
) -> Dict[str, Any]:
    """
    Process single frame with OCR cascade.

    Args:
        frame_path: Path to frame image
        gemini_api_key: API key for Gemini (None to skip)
        confidence_threshold: Threshold for Gemini escalation
        always_use_gemini: Skip Tesseract, use Gemini directly

    Returns:
        OCR result dict
    """
    result = {
        "frame_path": frame_path,
        "tesseract_result": None,
        "gemini_result": None,
        "final_text": "",
        "engine_used": "none"
    }

    if not always_use_gemini:
        # First pass: Tesseract
        try:
            tesseract_result = ocr_with_tesseract(frame_path)
            result["tesseract_result"] = tesseract_result

            # Check if we should escalate
            use_gemini = should_escalate_to_gemini(
                tesseract_result,
                confidence_threshold
            )

            if not use_gemini or not gemini_api_key:
                result["final_text"] = tesseract_result["text"]
                result["engine_used"] = "tesseract"
                return result

        except Exception as e:
            result["tesseract_error"] = str(e)
            use_gemini = True

    # Second pass: Gemini (if needed and available)
    if gemini_api_key and (always_use_gemini or use_gemini):
        try:
            gemini_result = ocr_with_gemini(frame_path, gemini_api_key)
            result["gemini_result"] = gemini_result
            result["final_text"] = gemini_result["text"]
            result["engine_used"] = "gemini"
        except Exception as e:
            result["gemini_error"] = str(e)
            # Fall back to Tesseract if Gemini fails
            if result["tesseract_result"]:
                result["final_text"] = result["tesseract_result"]["text"]
                result["engine_used"] = "tesseract_fallback"

    return result


def compute_text_similarity(text1: str, text2: str) -> float:
    """
    Compute similarity between two text strings.

    Returns value between 0.0 (completely different) and 1.0 (identical).
    """
    if not text1 and not text2:
        return 1.0
    if not text1 or not text2:
        return 0.0

    # Normalize texts
    t1 = set(text1.lower().split())
    t2 = set(text2.lower().split())

    if not t1 and not t2:
        return 1.0
    if not t1 or not t2:
        return 0.0

    # Jaccard similarity
    intersection = len(t1 & t2)
    union = len(t1 | t2)

    return intersection / union if union > 0 else 0.0


def process_frames_ocr(
    frame_paths: List[str],
    output_dir: str,
    gemini_api_key: Optional[str] = None,
    confidence_threshold: float = 70.0,
    dedup_similarity_threshold: float = 0.85
) -> List[Dict[str, Any]]:
    """
    Process multiple frames with OCR cascade and deduplication.

    First runs Tesseract on all frames to identify duplicates,
    then only sends unique/low-confidence frames to Gemini.

    Args:
        frame_paths: List of frame image paths
        output_dir: Directory for output files
        gemini_api_key: API key for Gemini
        confidence_threshold: Threshold for Gemini escalation
        dedup_similarity_threshold: Skip Gemini if text similarity > this

    Returns:
        List of OCR results (includes cost_summary)
    """
    # Cost tracking for Gemini 2.5 Flash
    # Pricing estimates (as of Nov 2024):
    # - Input: ~$0.075/1M tokens, images ~5K-10K tokens per grid
    # - Output: ~$0.30/1M tokens, ~500-1K tokens per response
    # Estimated cost per grid: ~$0.001-0.002
    ESTIMATED_COST_PER_GRID = 0.0015  # $0.0015 per 16-frame grid
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Phase 1: Run Tesseract on ALL frames first
    print("  Phase 1: Tesseract OCR on all frames...")
    tesseract_results = []
    for frame_path in tqdm(frame_paths, desc="Tesseract pass"):
        try:
            tess_result = ocr_with_tesseract(frame_path)
            tesseract_results.append({
                "frame_path": frame_path,
                "tesseract_result": tess_result,
                "text": tess_result["text"],
                "confidence": tess_result["avg_confidence"]
            })
        except Exception as e:
            tesseract_results.append({
                "frame_path": frame_path,
                "tesseract_result": None,
                "text": "",
                "confidence": 0,
                "error": str(e)
            })

    # Phase 2: Identify unique frames (not duplicates of previous)
    unique_indices = []
    prev_text = ""

    for i, result in enumerate(tesseract_results):
        current_text = result["text"]
        similarity = compute_text_similarity(prev_text, current_text)

        # Mark as unique if text is different enough from previous
        if similarity < dedup_similarity_threshold:
            unique_indices.append(i)
            prev_text = current_text

    duplicates_skipped = len(tesseract_results) - len(unique_indices)
    print(f"  Identified {len(unique_indices)} unique frames ({duplicates_skipped} duplicates skipped)")

    # Phase 3: Process unique frames with Gemini escalation
    results = []
    gemini_calls = 0
    tesseract_only = 0

    for i, tess_data in enumerate(tesseract_results):
        frame_path = tess_data["frame_path"]

        result = {
            "frame_path": frame_path,
            "tesseract_result": tess_data["tesseract_result"],
            "gemini_result": None,
            "final_text": tess_data["text"],
            "engine_used": "tesseract",
            "is_duplicate": i not in unique_indices
        }

        # Skip Gemini for duplicates
        if i not in unique_indices:
            result["engine_used"] = "tesseract_dedup"
            tesseract_only += 1
            results.append(result)
            continue

        # Check if we should escalate to Gemini
        needs_gemini = False
        if tess_data["tesseract_result"]:
            needs_gemini = should_escalate_to_gemini(
                tess_data["tesseract_result"],
                confidence_threshold
            )
        else:
            needs_gemini = True  # Tesseract failed

        if needs_gemini:
            result["needs_gemini"] = True
        else:
            tesseract_only += 1

        results.append(result)

    # Phase 4: Batch process frames needing Gemini using grid
    frames_needing_gemini = [
        (i, r) for i, r in enumerate(results)
        if r.get("needs_gemini") and not r.get("is_duplicate")
    ]

    if frames_needing_gemini and gemini_api_key:
        print(f"  Phase 4: Processing {len(frames_needing_gemini)} frames with Gemini (batched)...")

        # Process in batches of 16 (4x4 grid)
        batch_size = 16
        for batch_start in range(0, len(frames_needing_gemini), batch_size):
            batch = frames_needing_gemini[batch_start:batch_start + batch_size]
            batch_paths = [results[idx]["frame_path"] for idx, _ in batch]

            try:
                grid_result = ocr_grid_with_gemini(batch_paths, gemini_api_key)
                gemini_calls += 1  # Count as 1 API call for the grid

                # Update results with Gemini text
                for j, (idx, _) in enumerate(batch):
                    frame_num = j + 1
                    if frame_num in grid_result["frame_texts"]:
                        gemini_text = grid_result["frame_texts"][frame_num]
                        results[idx]["gemini_result"] = {"text": gemini_text}
                        results[idx]["final_text"] = gemini_text
                        results[idx]["engine_used"] = "gemini_grid"
                    else:
                        results[idx]["engine_used"] = "tesseract_fallback"

            except Exception as e:
                # Fallback to tesseract for failed batch
                for idx, _ in batch:
                    results[idx]["gemini_error"] = str(e)
                    results[idx]["engine_used"] = "tesseract_fallback"
    else:
        # Mark remaining as tesseract only
        for i, r in enumerate(results):
            if r.get("needs_gemini") and not r.get("is_duplicate"):
                results[i]["engine_used"] = "tesseract_fallback"
                tesseract_only += 1

    # Calculate costs
    estimated_cost = gemini_calls * ESTIMATED_COST_PER_GRID
    frames_processed_by_gemini = min(len(frames_needing_gemini), gemini_calls * 16) if frames_needing_gemini else 0

    # Create cost summary
    cost_summary = {
        "total_frames": len(frame_paths),
        "unique_frames": len(unique_indices),
        "duplicates_skipped": duplicates_skipped,
        "tesseract_only": tesseract_only,
        "gemini_api_calls": gemini_calls,
        "frames_sent_to_gemini": frames_processed_by_gemini,
        "estimated_cost_usd": round(estimated_cost, 4),
        "cost_per_frame_usd": round(estimated_cost / len(frame_paths), 6) if len(frame_paths) > 0 else 0,
        "cost_efficiency_pct": round((len(frame_paths) - frames_processed_by_gemini) / len(frame_paths) * 100, 1) if len(frame_paths) > 0 else 100
    }

    # Save results with cost summary
    results_with_costs = {
        "frames": results,
        "cost_summary": cost_summary
    }

    results_path = output_dir / "ocr_results.json"
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results_with_costs, f, indent=2, ensure_ascii=False)

    # Summary
    print(f"\nProcessed {len(frame_paths)} frames")
    print(f"  Unique frames: {len(unique_indices)}")
    print(f"  Duplicates skipped: {duplicates_skipped}")
    print(f"  Tesseract only: {tesseract_only}")
    print(f"  Gemini API calls: {gemini_calls}")
    print(f"  Frames sent to Gemini: {frames_processed_by_gemini}")
    print(f"  Estimated cost: ${estimated_cost:.4f}")
    if len(frame_paths) > 0:
        print(f"  Cost efficiency: {cost_summary['cost_efficiency_pct']:.1f}% free")

    # Aggregate all text
    all_text = "\n".join([
        r["final_text"] for r in results if r["final_text"]
    ])

    all_text_path = output_dir / "all_ocr_text.txt"
    with open(all_text_path, "w", encoding="utf-8") as f:
        f.write(all_text)

    return results


def deduplicate_text(results: List[Dict[str, Any]]) -> str:
    """
    Deduplicate extracted text across frames.

    Since consecutive frames often have the same text,
    this removes duplicates while preserving unique content.

    Args:
        results: List of OCR results

    Returns:
        Deduplicated text
    """
    seen = set()
    unique_texts = []

    for result in results:
        text = result.get("final_text", "").strip()
        if text and text not in seen:
            seen.add(text)
            unique_texts.append(text)

    return "\n---\n".join(unique_texts)


def extract_entities(ocr_text: str) -> Dict[str, List[str]]:
    """
    Extract common entities from OCR text.

    Looks for patterns like:
    - URLs
    - @mentions
    - #hashtags
    - Numbers/statistics

    Args:
        ocr_text: Combined OCR text

    Returns:
        Dict of entity types to lists of matches
    """
    import re

    entities = {
        "urls": [],
        "mentions": [],
        "hashtags": [],
        "numbers": [],
        "emails": []
    }

    # URLs
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    entities["urls"] = list(set(re.findall(url_pattern, ocr_text)))

    # @mentions
    mention_pattern = r'@[\w.]+'
    entities["mentions"] = list(set(re.findall(mention_pattern, ocr_text)))

    # #hashtags
    hashtag_pattern = r'#\w+'
    entities["hashtags"] = list(set(re.findall(hashtag_pattern, ocr_text)))

    # Numbers with context (prices, stats, etc.)
    number_pattern = r'\$?[\d,]+\.?\d*[%KMB]?'
    numbers = re.findall(number_pattern, ocr_text)
    entities["numbers"] = [n for n in set(numbers) if len(n) > 1]

    # Emails
    email_pattern = r'[\w.+-]+@[\w-]+\.[\w.-]+'
    entities["emails"] = list(set(re.findall(email_pattern, ocr_text)))

    return entities


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python ocr_processor.py <image_path> [gemini_api_key]")
        sys.exit(1)

    image_path = sys.argv[1]
    api_key = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"Processing: {image_path}")

    result = process_frame_ocr(image_path, api_key)

    print(f"\nEngine used: {result['engine_used']}")

    if result["tesseract_result"]:
        print(f"Tesseract confidence: {result['tesseract_result']['avg_confidence']}%")
        print(f"Tesseract words: {result['tesseract_result']['word_count']}")

    print(f"\nExtracted text:")
    print(result["final_text"] or "(no text detected)")
