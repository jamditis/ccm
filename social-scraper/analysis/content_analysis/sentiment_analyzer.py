#!/usr/bin/env python3
"""
Sentiment and Tone Analysis

Analyzes emotional tone, sentiment, and rhetorical style of content:
- Overall sentiment (positive/negative/neutral)
- Emotional tone dimensions
- Rhetorical techniques
- Persuasion patterns
- Authenticity signals
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import defaultdict
from tqdm import tqdm

# Lazy imports
genai = None
anthropic = None


@dataclass
class SentimentResult:
    """Detailed sentiment and tone analysis."""
    video_id: str
    influencer: str
    platform: str

    # Core sentiment
    sentiment_score: float  # -1 (negative) to +1 (positive)
    sentiment_label: str  # very_negative, negative, neutral, positive, very_positive

    # Emotional dimensions (0-1 scale)
    joy: float
    anger: float
    fear: float
    sadness: float
    surprise: float
    disgust: float
    trust: float
    anticipation: float

    # Dominant emotions
    primary_emotion: str
    secondary_emotion: str

    # Tone characteristics
    formality: str  # casual, conversational, formal, professional
    energy_level: str  # low, moderate, high, very_high
    humor_level: float  # 0-1
    sarcasm_detected: bool

    # Rhetorical style
    rhetorical_mode: str  # informative, persuasive, entertaining, confrontational, inspirational
    persuasion_techniques: List[str]
    call_to_action_strength: str  # none, soft, moderate, strong, urgent

    # Authenticity signals
    authenticity_score: float  # 0-1
    personal_disclosure_level: str  # none, low, medium, high
    vulnerable_moments: bool
    scripted_vs_spontaneous: str  # scripted, semi_scripted, spontaneous

    # Engagement prediction
    controversy_potential: float  # 0-1
    shareability_score: float  # 0-1
    comment_bait_score: float  # 0-1

    # Analysis metadata
    confidence: float
    timestamp: str


SENTIMENT_PROMPT = """You are an expert media psychologist analyzing social media content.
Perform a deep sentiment and tone analysis of this content.

CONTENT:
Platform: {platform}
Influencer: {influencer}
Title: {title}
Transcript: {transcript}
OCR Text: {ocr_text}

Analyze the emotional and rhetorical qualities. Respond with JSON only:

{{
    "sentiment_score": -1.0 to 1.0 (-1=very negative, 0=neutral, 1=very positive),
    "sentiment_label": "very_negative|negative|neutral|positive|very_positive",

    "emotions": {{
        "joy": 0.0 to 1.0,
        "anger": 0.0 to 1.0,
        "fear": 0.0 to 1.0,
        "sadness": 0.0 to 1.0,
        "surprise": 0.0 to 1.0,
        "disgust": 0.0 to 1.0,
        "trust": 0.0 to 1.0,
        "anticipation": 0.0 to 1.0
    }},
    "primary_emotion": "most dominant emotion",
    "secondary_emotion": "second most dominant emotion",

    "formality": "casual|conversational|formal|professional",
    "energy_level": "low|moderate|high|very_high",
    "humor_level": 0.0 to 1.0,
    "sarcasm_detected": true or false,

    "rhetorical_mode": "informative|persuasive|entertaining|confrontational|inspirational",
    "persuasion_techniques": ["technique1", "technique2"],
    "call_to_action_strength": "none|soft|moderate|strong|urgent",

    "authenticity_score": 0.0 to 1.0,
    "personal_disclosure_level": "none|low|medium|high",
    "vulnerable_moments": true or false,
    "scripted_vs_spontaneous": "scripted|semi_scripted|spontaneous",

    "controversy_potential": 0.0 to 1.0,
    "shareability_score": 0.0 to 1.0,
    "comment_bait_score": 0.0 to 1.0,

    "confidence": 0.0 to 1.0
}}

Consider:
- Word choice, phrasing, and emphasis
- Speaking patterns and cadence (if transcript shows this)
- Use of emotional appeals vs logical arguments
- Authenticity vs performative elements
- What reactions this content is designed to provoke"""


class SentimentAnalyzer:
    """Deep sentiment and tone analysis using Claude or Gemini."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        provider: str = "claude",
        model: Optional[str] = None
    ):
        self.provider = provider.lower()
        self.api_calls = 0

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
            global genai
            import google.generativeai as genai_module
            genai = genai_module

            self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
            if not self.api_key:
                raise ValueError("Gemini API key required")

            from google import genai as genai_client
            from google.genai import types as genai_types

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

    def analyze(
        self,
        video_id: str,
        influencer: str,
        platform: str,
        title: str = "",
        transcript: str = "",
        ocr_text: str = "",
        description: str = "",
        duration: int = 0,
        **kwargs  # Accept any extra parameters
    ) -> SentimentResult:
        """Analyze sentiment and tone of content."""
        # Truncate for token limits
        transcript = transcript[:6000] if transcript else ""
        ocr_text = ocr_text[:1500] if ocr_text else ""
        # Combine title and description if no transcript
        if not transcript and description:
            transcript = description[:4000]

        prompt = SENTIMENT_PROMPT.format(
            platform=platform,
            influencer=influencer,
            title=title or "(no title)",
            transcript=transcript or "(no transcript)",
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
                text = message.content[0].text.strip()
            elif self.provider == "gemini":
                response = self.gemini_client.models.generate_content(
                    model=self.gemini_model,
                    contents=prompt,
                    config=self.gemini_config
                )
                text = response.text.strip()
            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    max_completion_tokens=2048,
                    messages=[{"role": "user", "content": prompt}]
                )
                text = response.choices[0].message.content.strip()

            self.api_calls += 1

            if text.startswith("```"):
                lines = text.split("\n")
                text = "\n".join(lines[1:-1])

            data = json.loads(text)
            emotions = data.get("emotions", {})

            return SentimentResult(
                video_id=video_id,
                influencer=influencer,
                platform=platform,
                sentiment_score=float(data.get("sentiment_score", 0)),
                sentiment_label=data.get("sentiment_label", "neutral"),
                joy=float(emotions.get("joy", 0)),
                anger=float(emotions.get("anger", 0)),
                fear=float(emotions.get("fear", 0)),
                sadness=float(emotions.get("sadness", 0)),
                surprise=float(emotions.get("surprise", 0)),
                disgust=float(emotions.get("disgust", 0)),
                trust=float(emotions.get("trust", 0)),
                anticipation=float(emotions.get("anticipation", 0)),
                primary_emotion=data.get("primary_emotion", "neutral"),
                secondary_emotion=data.get("secondary_emotion", "neutral"),
                formality=data.get("formality", "casual"),
                energy_level=data.get("energy_level", "moderate"),
                humor_level=float(data.get("humor_level", 0)),
                sarcasm_detected=data.get("sarcasm_detected", False),
                rhetorical_mode=data.get("rhetorical_mode", "informative"),
                persuasion_techniques=data.get("persuasion_techniques", []),
                call_to_action_strength=data.get("call_to_action_strength", "none"),
                authenticity_score=float(data.get("authenticity_score", 0.5)),
                personal_disclosure_level=data.get("personal_disclosure_level", "low"),
                vulnerable_moments=data.get("vulnerable_moments", False),
                scripted_vs_spontaneous=data.get("scripted_vs_spontaneous", "semi_scripted"),
                controversy_potential=float(data.get("controversy_potential", 0)),
                shareability_score=float(data.get("shareability_score", 0.5)),
                comment_bait_score=float(data.get("comment_bait_score", 0)),
                confidence=float(data.get("confidence", 0.5)),
                timestamp=datetime.now().isoformat()
            )

        except Exception as e:
            return SentimentResult(
                video_id=video_id,
                influencer=influencer,
                platform=platform,
                sentiment_score=0,
                sentiment_label="error",
                joy=0, anger=0, fear=0, sadness=0,
                surprise=0, disgust=0, trust=0, anticipation=0,
                primary_emotion="error",
                secondary_emotion="error",
                formality="unknown",
                energy_level="unknown",
                humor_level=0,
                sarcasm_detected=False,
                rhetorical_mode="unknown",
                persuasion_techniques=[],
                call_to_action_strength="unknown",
                authenticity_score=0,
                personal_disclosure_level="unknown",
                vulnerable_moments=False,
                scripted_vs_spontaneous="unknown",
                controversy_potential=0,
                shareability_score=0,
                comment_bait_score=0,
                confidence=0,
                timestamp=datetime.now().isoformat()
            )

    def batch_analyze(
        self,
        content_list: List[Dict[str, Any]],
        output_dir: str,
        checkpoint_every: int = 10
    ) -> List[SentimentResult]:
        """Batch analyze with checkpointing."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        checkpoint_file = output_path / "sentiment_checkpoint.json"
        completed_ids = set()
        results = []

        if checkpoint_file.exists():
            with open(checkpoint_file) as f:
                checkpoint = json.load(f)
                completed_ids = set(checkpoint.get("completed_ids", []))
                results = [SentimentResult(**r) for r in checkpoint.get("results", [])]
                print(f"Resuming: {len(completed_ids)} already analyzed")

        to_process = [c for c in content_list if c["video_id"] not in completed_ids]
        print(f"Processing {len(to_process)} of {len(content_list)} items")

        for i, content in enumerate(tqdm(to_process, desc="Sentiment Analysis")):
            result = self.analyze(**content)
            results.append(result)
            completed_ids.add(content["video_id"])

            if (i + 1) % checkpoint_every == 0:
                self._save_checkpoint(checkpoint_file, completed_ids, results)

        self._save_checkpoint(checkpoint_file, completed_ids, results)
        self._export_results(results, output_path)

        return results

    def _save_checkpoint(self, path: Path, completed: set, results: List[SentimentResult]):
        with open(path, "w") as f:
            json.dump({
                "completed_ids": list(completed),
                "results": [asdict(r) for r in results],
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)

    def _export_results(self, results: List[SentimentResult], output_path: Path):
        """Export results to JSON and CSV."""
        # Full JSON
        with open(output_path / "sentiment_analysis_full.json", "w") as f:
            json.dump([asdict(r) for r in results], f, indent=2)

        # CSV summary
        import csv
        with open(output_path / "sentiment_summary.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "video_id", "influencer", "platform",
                "sentiment_score", "sentiment_label",
                "primary_emotion", "secondary_emotion",
                "formality", "energy_level", "humor_level",
                "rhetorical_mode", "authenticity_score",
                "controversy_potential", "shareability_score",
                "confidence"
            ])
            writer.writeheader()
            for r in results:
                writer.writerow({
                    "video_id": r.video_id,
                    "influencer": r.influencer,
                    "platform": r.platform,
                    "sentiment_score": r.sentiment_score,
                    "sentiment_label": r.sentiment_label,
                    "primary_emotion": r.primary_emotion,
                    "secondary_emotion": r.secondary_emotion,
                    "formality": r.formality,
                    "energy_level": r.energy_level,
                    "humor_level": r.humor_level,
                    "rhetorical_mode": r.rhetorical_mode,
                    "authenticity_score": r.authenticity_score,
                    "controversy_potential": r.controversy_potential,
                    "shareability_score": r.shareability_score,
                    "confidence": r.confidence
                })

        # Aggregate stats
        self._generate_aggregate_stats(results, output_path)

        print(f"\nResults exported to {output_path}")
        print(f"Total API calls: {self.api_calls}")

    def _generate_aggregate_stats(self, results: List[SentimentResult], output_path: Path):
        """Generate aggregate sentiment statistics."""
        from collections import defaultdict
        import statistics

        # By platform
        by_platform = defaultdict(list)
        by_influencer = defaultdict(list)

        for r in results:
            by_platform[r.platform].append(r)
            by_influencer[r.influencer].append(r)

        stats = {
            "overall": {
                "count": len(results),
                "avg_sentiment": statistics.mean([r.sentiment_score for r in results]) if results else 0,
                "sentiment_distribution": self._count_labels(results),
                "primary_emotions": self._count_field(results, "primary_emotion"),
                "rhetorical_modes": self._count_field(results, "rhetorical_mode")
            },
            "by_platform": {},
            "by_influencer": {}
        }

        for platform, items in by_platform.items():
            stats["by_platform"][platform] = {
                "count": len(items),
                "avg_sentiment": statistics.mean([r.sentiment_score for r in items]),
                "avg_authenticity": statistics.mean([r.authenticity_score for r in items]),
                "avg_controversy": statistics.mean([r.controversy_potential for r in items])
            }

        for influencer, items in by_influencer.items():
            stats["by_influencer"][influencer] = {
                "count": len(items),
                "avg_sentiment": statistics.mean([r.sentiment_score for r in items]),
                "avg_authenticity": statistics.mean([r.authenticity_score for r in items]),
                "primary_emotions": self._count_field(items, "primary_emotion")
            }

        with open(output_path / "sentiment_aggregate_stats.json", "w") as f:
            json.dump(stats, f, indent=2)

    def _count_labels(self, results: List[SentimentResult]) -> Dict[str, int]:
        counts = defaultdict(int)
        for r in results:
            counts[r.sentiment_label] += 1
        return dict(counts)

    def _count_field(self, results: List[SentimentResult], field: str) -> Dict[str, int]:
        counts = defaultdict(int)
        for r in results:
            counts[getattr(r, field, "unknown")] += 1
        return dict(sorted(counts.items(), key=lambda x: -x[1])[:10])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sentiment and tone analysis")
    parser.add_argument("results_dir", help="Directory with processed video results")
    parser.add_argument("--output", default="analysis/sentiment_results")
    parser.add_argument("--limit", type=int, default=0)

    args = parser.parse_args()

    # Would load content from processed results
    # For now, placeholder
    print("Run with processed video content for analysis")
