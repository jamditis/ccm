#!/usr/bin/env python3
"""
Semantic Content Analyzer

Deep analysis of content using LLMs to understand:
- Main topics and themes
- Key messages and narratives
- Content format/style classification
- NJ-specific local relevance
- Audience targeting signals
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from tqdm import tqdm

# Lazy imports for API clients
genai = None
anthropic = None


@dataclass
class ContentAnalysis:
    """Structured output from semantic analysis."""
    video_id: str
    influencer: str
    platform: str

    # Core content analysis
    main_topic: str
    subtopics: List[str]
    content_type: str  # educational, entertainment, news, opinion, promotion, etc.
    content_format: str  # talking_head, vlog, tutorial, reaction, skit, etc.

    # NJ relevance
    nj_relevance_score: float  # 0-1 how NJ-specific
    nj_locations_mentioned: List[str]
    nj_issues_mentioned: List[str]
    local_vs_universal: str  # local, regional, national, universal

    # Narrative analysis
    key_messages: List[str]
    call_to_action: Optional[str]
    narrative_frame: str  # how the story is framed
    tone: str  # serious, humorous, informative, provocative, etc.

    # Audience signals
    target_audience: str
    assumed_knowledge: str  # low, medium, high
    engagement_hooks: List[str]  # what techniques used to engage

    # Entities and references
    people_mentioned: List[str]
    organizations_mentioned: List[str]
    brands_mentioned: List[str]
    other_creators_mentioned: List[str]

    # Quality metrics
    production_quality: str  # low, medium, high, professional
    originality_score: float  # 0-1 how original vs derivative

    # Meta
    analysis_confidence: float
    raw_response: str
    timestamp: str


ANALYSIS_PROMPT = """You are an expert media analyst specializing in social media content and local journalism.
Analyze this content from a New Jersey influencer and provide a detailed assessment.

CONTENT TO ANALYZE:
Platform: {platform}
Influencer: {influencer}
Title/Caption: {title}
Description: {description}
Duration: {duration} seconds
Transcript: {transcript}
OCR Text (from video frames): {ocr_text}

Provide your analysis in the following JSON format (respond ONLY with valid JSON):

{{
    "main_topic": "Primary subject matter in 3-5 words",
    "subtopics": ["subtopic1", "subtopic2", "subtopic3"],
    "content_type": "educational|entertainment|news|opinion|promotion|lifestyle|reaction|other",
    "content_format": "talking_head|vlog|tutorial|reaction|skit|interview|montage|news_report|other",

    "nj_relevance_score": 0.0 to 1.0,
    "nj_locations_mentioned": ["location1", "location2"],
    "nj_issues_mentioned": ["issue1", "issue2"],
    "local_vs_universal": "local|regional|national|universal",

    "key_messages": ["message1", "message2", "message3"],
    "call_to_action": "What action is viewer asked to take, or null",
    "narrative_frame": "How the content frames its subject (e.g., 'exposing hidden truth', 'celebrating local culture', 'personal journey')",
    "tone": "serious|humorous|informative|provocative|inspirational|casual|dramatic|satirical",

    "target_audience": "Description of intended audience (e.g., 'NJ residents interested in local politics')",
    "assumed_knowledge": "low|medium|high",
    "engagement_hooks": ["hook1", "hook2"],

    "people_mentioned": ["person1", "person2"],
    "organizations_mentioned": ["org1", "org2"],
    "brands_mentioned": ["brand1", "brand2"],
    "other_creators_mentioned": ["creator1", "creator2"],

    "production_quality": "low|medium|high|professional",
    "originality_score": 0.0 to 1.0,

    "analysis_confidence": 0.0 to 1.0
}}

Focus especially on:
1. How this content relates to New Jersey specifically
2. What narrative techniques the creator uses
3. Who the content is designed to reach
4. What the creator wants the audience to do/think/feel"""


class SemanticAnalyzer:
    """Deep semantic analysis of video content using Claude or Gemini."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        provider: str = "claude",  # "claude" or "gemini"
        model: Optional[str] = None
    ):
        self.provider = provider.lower()
        self.total_api_calls = 0

        if self.provider == "claude":
            global anthropic
            import anthropic as anthropic_module
            anthropic = anthropic_module

            self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
            if not self.api_key:
                raise ValueError("Anthropic API key required")

            self.client = anthropic.Anthropic(api_key=self.api_key)
            self.model_name = model or "claude-sonnet-4-20250514"

        elif self.provider == "gemini":
            from google import genai as genai_client
            from google.genai import types as genai_types

            self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
            if not self.api_key:
                raise ValueError("Gemini API key required")

            self.gemini_client = genai_client.Client(api_key=self.api_key)
            self.gemini_model = model or "gemini-3-flash-preview"
            # Use low thinking for faster responses
            self.gemini_config = genai_types.GenerateContentConfig(
                thinking_config=genai_types.ThinkingConfig(thinking_level="low")
            )

        elif self.provider == "openai":
            global openai
            import openai as openai_module
            openai = openai_module

            self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OpenAI API key required")

            self.client = openai.OpenAI(api_key=self.api_key)
            self.model_name = model or "gpt-5.1-chat-latest"

        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def analyze_content(
        self,
        video_id: str,
        influencer: str,
        platform: str,
        title: str = "",
        description: str = "",
        duration: int = 0,
        transcript: str = "",
        ocr_text: str = ""
    ) -> ContentAnalysis:
        """
        Perform deep semantic analysis on a single piece of content.
        """
        # Truncate long texts to stay within token limits
        transcript = transcript[:8000] if transcript else ""
        ocr_text = ocr_text[:2000] if ocr_text else ""
        description = description[:2000] if description else ""

        prompt = ANALYSIS_PROMPT.format(
            platform=platform,
            influencer=influencer,
            title=title or "(no title)",
            description=description or "(no description)",
            duration=duration,
            transcript=transcript or "(no transcript available)",
            ocr_text=ocr_text or "(no OCR text)"
        )

        try:
            # Call appropriate API
            if self.provider == "claude":
                message = self.client.messages.create(
                    model=self.model_name,
                    max_tokens=2048,
                    messages=[{"role": "user", "content": prompt}]
                )
                response_text = message.content[0].text.strip()
            elif self.provider == "gemini":
                response = self.gemini_client.models.generate_content(
                    model=self.gemini_model,
                    contents=prompt,
                    config=self.gemini_config
                )
                response_text = response.text.strip()
            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    max_completion_tokens=2048,
                    messages=[{"role": "user", "content": prompt}]
                )
                response_text = response.choices[0].message.content.strip()

            self.total_api_calls += 1

            # Handle markdown code blocks
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                response_text = "\n".join(lines[1:-1])

            data = json.loads(response_text)

            return ContentAnalysis(
                video_id=video_id,
                influencer=influencer,
                platform=platform,
                main_topic=data.get("main_topic", "Unknown"),
                subtopics=data.get("subtopics", []),
                content_type=data.get("content_type", "other"),
                content_format=data.get("content_format", "other"),
                nj_relevance_score=float(data.get("nj_relevance_score", 0)),
                nj_locations_mentioned=data.get("nj_locations_mentioned", []),
                nj_issues_mentioned=data.get("nj_issues_mentioned", []),
                local_vs_universal=data.get("local_vs_universal", "universal"),
                key_messages=data.get("key_messages", []),
                call_to_action=data.get("call_to_action"),
                narrative_frame=data.get("narrative_frame", "Unknown"),
                tone=data.get("tone", "Unknown"),
                target_audience=data.get("target_audience", "General"),
                assumed_knowledge=data.get("assumed_knowledge", "low"),
                engagement_hooks=data.get("engagement_hooks", []),
                people_mentioned=data.get("people_mentioned", []),
                organizations_mentioned=data.get("organizations_mentioned", []),
                brands_mentioned=data.get("brands_mentioned", []),
                other_creators_mentioned=data.get("other_creators_mentioned", []),
                production_quality=data.get("production_quality", "medium"),
                originality_score=float(data.get("originality_score", 0.5)),
                analysis_confidence=float(data.get("analysis_confidence", 0.5)),
                raw_response=response_text,
                timestamp=datetime.now().isoformat()
            )

        except json.JSONDecodeError as e:
            # Return partial analysis on JSON parse error
            return ContentAnalysis(
                video_id=video_id,
                influencer=influencer,
                platform=platform,
                main_topic="Parse Error",
                subtopics=[],
                content_type="other",
                content_format="other",
                nj_relevance_score=0,
                nj_locations_mentioned=[],
                nj_issues_mentioned=[],
                local_vs_universal="unknown",
                key_messages=[],
                call_to_action=None,
                narrative_frame="Unknown",
                tone="Unknown",
                target_audience="Unknown",
                assumed_knowledge="unknown",
                engagement_hooks=[],
                people_mentioned=[],
                organizations_mentioned=[],
                brands_mentioned=[],
                other_creators_mentioned=[],
                production_quality="unknown",
                originality_score=0,
                analysis_confidence=0,
                raw_response=str(e),
                timestamp=datetime.now().isoformat()
            )

    def batch_analyze(
        self,
        content_list: List[Dict[str, Any]],
        output_dir: str,
        checkpoint_every: int = 10
    ) -> List[ContentAnalysis]:
        """
        Analyze multiple pieces of content with checkpointing.

        content_list: List of dicts with keys:
            - video_id, influencer, platform, title, description,
            - duration, transcript, ocr_text
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Load existing checkpoint
        checkpoint_file = output_path / "analysis_checkpoint.json"
        completed_ids = set()
        results = []

        if checkpoint_file.exists():
            with open(checkpoint_file, "r") as f:
                checkpoint = json.load(f)
                completed_ids = set(checkpoint.get("completed_ids", []))
                results = [ContentAnalysis(**r) for r in checkpoint.get("results", [])]
                print(f"Resuming from checkpoint: {len(completed_ids)} already analyzed")

        # Filter to unprocessed content
        to_process = [c for c in content_list if c["video_id"] not in completed_ids]
        print(f"Processing {len(to_process)} of {len(content_list)} items")

        for i, content in enumerate(tqdm(to_process, desc="Semantic Analysis")):
            analysis = self.analyze_content(**content)
            results.append(analysis)
            completed_ids.add(content["video_id"])

            # Checkpoint
            if (i + 1) % checkpoint_every == 0:
                self._save_checkpoint(checkpoint_file, completed_ids, results)

        # Final save
        self._save_checkpoint(checkpoint_file, completed_ids, results)

        # Export full results
        self._export_results(results, output_path)

        return results

    def _save_checkpoint(
        self,
        checkpoint_file: Path,
        completed_ids: set,
        results: List[ContentAnalysis]
    ):
        """Save checkpoint for resumable processing."""
        with open(checkpoint_file, "w") as f:
            json.dump({
                "completed_ids": list(completed_ids),
                "results": [asdict(r) for r in results],
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)

    def _export_results(self, results: List[ContentAnalysis], output_path: Path):
        """Export results to JSON and CSV."""
        # Full JSON export
        json_file = output_path / "semantic_analysis_full.json"
        with open(json_file, "w") as f:
            json.dump([asdict(r) for r in results], f, indent=2)

        # Summary CSV for analysis
        import csv
        csv_file = output_path / "semantic_analysis_summary.csv"

        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "video_id", "influencer", "platform",
                "main_topic", "content_type", "content_format",
                "nj_relevance_score", "local_vs_universal",
                "tone", "target_audience",
                "production_quality", "originality_score",
                "analysis_confidence"
            ])
            writer.writeheader()
            for r in results:
                writer.writerow({
                    "video_id": r.video_id,
                    "influencer": r.influencer,
                    "platform": r.platform,
                    "main_topic": r.main_topic,
                    "content_type": r.content_type,
                    "content_format": r.content_format,
                    "nj_relevance_score": r.nj_relevance_score,
                    "local_vs_universal": r.local_vs_universal,
                    "tone": r.tone,
                    "target_audience": r.target_audience,
                    "production_quality": r.production_quality,
                    "originality_score": r.originality_score,
                    "analysis_confidence": r.analysis_confidence
                })

        print(f"\nResults exported to:")
        print(f"  JSON: {json_file}")
        print(f"  CSV: {csv_file}")
        print(f"  Total API calls: {self.total_api_calls}")


def load_processed_content(results_dir: str) -> List[Dict[str, Any]]:
    """
    Load previously processed video results for semantic analysis.

    Combines metadata + transcripts + OCR from batch processing.
    """
    results_path = Path(results_dir)
    content_list = []

    # Load all batch results
    for batch_file in results_path.glob("batch_*_results.json"):
        with open(batch_file, "r") as f:
            batch_results = json.load(f)

        for result in batch_results:
            if result.get("status") in ["success", "partial"]:
                # Get transcript text
                transcript = ""
                if result.get("transcript"):
                    transcript = result["transcript"].get("text", "")

                # Get OCR text
                ocr_text = ""
                if result.get("ocr"):
                    ocr_text = result["ocr"].get("unique_text", "")

                content_list.append({
                    "video_id": result.get("video_name", ""),
                    "influencer": result.get("influencer", ""),
                    "platform": _detect_platform(result.get("video_path", "")),
                    "title": "",  # Need to load from original metadata
                    "description": "",
                    "duration": 0,
                    "transcript": transcript,
                    "ocr_text": ocr_text
                })

    return content_list


def _detect_platform(path: str) -> str:
    """Detect platform from file path."""
    path_lower = path.lower()
    if "tiktok" in path_lower:
        return "tiktok"
    elif "youtube" in path_lower:
        return "youtube"
    elif "instagram" in path_lower:
        return "instagram"
    return "unknown"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run semantic analysis on processed videos")
    parser.add_argument("results_dir", help="Directory with batch processing results")
    parser.add_argument("--output", default="analysis/semantic_results", help="Output directory")
    parser.add_argument("--limit", type=int, default=0, help="Limit number to analyze (0=all)")

    args = parser.parse_args()

    # Load processed content
    content = load_processed_content(args.results_dir)
    print(f"Found {len(content)} processed videos")

    if args.limit > 0:
        content = content[:args.limit]
        print(f"Limited to {args.limit} videos")

    # Run analysis
    analyzer = SemanticAnalyzer()
    results = analyzer.batch_analyze(content, args.output)

    print(f"\nAnalysis complete: {len(results)} videos analyzed")
