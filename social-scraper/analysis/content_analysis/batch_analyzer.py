#!/usr/bin/env python3
"""
Batch Analyzer for Claude API

Uses Anthropic's Message Batches API for 50% cost savings on large-scale analysis.
Processes requests asynchronously - submit all at once, poll for results.

Usage:
    # Semantic analysis with batch mode
    python run_ai_analysis.py --provider claude --batch-mode --output analysis/ai_results_batch

    # Or use directly
    from batch_analyzer import ClaudeBatchAnalyzer
    analyzer = ClaudeBatchAnalyzer()
    results = analyzer.batch_analyze_semantic(content_list, output_dir)
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

import re
from semantic_analyzer import ContentAnalysis, ANALYSIS_PROMPT
from sentiment_analyzer import SentimentResult, SENTIMENT_PROMPT


def extract_json_from_text(text: str) -> str:
    """
    Extract JSON object from text that may have extra content.

    Handles cases where the model adds commentary before/after JSON.
    """
    # Remove markdown code blocks
    if text.startswith("```"):
        lines = text.split("\n")
        # Find the closing ```
        end_idx = len(lines) - 1
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == "```":
                end_idx = i
                break
        text = "\n".join(lines[1:end_idx])

    # Find JSON object boundaries
    start = text.find("{")
    if start == -1:
        return text

    # Count braces to find matching closing brace
    depth = 0
    end = start
    for i, char in enumerate(text[start:], start):
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break

    return text[start:end]


@dataclass
class BatchStatus:
    """Track batch processing status."""
    batch_id: str
    batch_type: str  # "semantic" or "sentiment"
    total_requests: int
    processing: int
    succeeded: int
    errored: int
    canceled: int
    expired: int
    status: str  # "in_progress", "ended", "canceling"
    created_at: str
    results_url: Optional[str] = None


class ClaudeBatchAnalyzer:
    """
    Batch analyzer using Claude's Message Batches API.

    Benefits:
    - 50% cost savings vs real-time API
    - Higher throughput (no rate limiting concerns)
    - Submit up to 100,000 requests per batch

    Trade-offs:
    - Asynchronous (results in <1 hour typically, up to 24h max)
    - No streaming
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-haiku-4-5-20251001"  # Haiku 4.5 for cost efficiency
    ):
        """
        Initialize batch analyzer.

        Args:
            api_key: Anthropic API key (or set ANTHROPIC_API_KEY env var)
            model: Model to use. Default is Haiku 4.5 for cost efficiency.
                   Batch pricing (50% off):
                   - Haiku 4.5: $0.50/MTok input, $2.50/MTok output
                   - Sonnet 4: $1.50/MTok input, $7.50/MTok output
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY required")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model

    def _build_semantic_prompt(self, content: Dict[str, Any]) -> str:
        """Build semantic analysis prompt for a single content item."""
        transcript = (content.get("transcript") or "")[:8000]
        ocr_text = (content.get("ocr_text") or "")[:2000]
        description = (content.get("description") or "")[:2000]

        return ANALYSIS_PROMPT.format(
            platform=content.get("platform", "unknown"),
            influencer=content.get("influencer", "unknown"),
            title=content.get("title") or "(no title)",
            description=description or "(no description)",
            duration=content.get("duration", 0),
            transcript=transcript or "(no transcript available)",
            ocr_text=ocr_text or "(no OCR text)"
        )

    def _build_sentiment_prompt(self, content: Dict[str, Any]) -> str:
        """Build sentiment analysis prompt for a single content item."""
        transcript = (content.get("transcript") or "")[:6000]
        ocr_text = (content.get("ocr_text") or "")[:1500]
        description = content.get("description") or ""

        if not transcript and description:
            transcript = description[:4000]

        return SENTIMENT_PROMPT.format(
            platform=content.get("platform", "unknown"),
            influencer=content.get("influencer", "unknown"),
            title=content.get("title") or "(no title)",
            transcript=transcript or "(no transcript)",
            ocr_text=ocr_text or "(no OCR text)"
        )

    def _validate_and_dedupe_content(
        self,
        content_list: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Validate content list for batch processing.

        - Ensures unique custom_ids (video_ids)
        - Truncates IDs to 64 chars max (API limit)
        - Removes duplicates
        - Warns about potential issues
        """
        seen_ids = set()
        validated = []

        for content in content_list:
            video_id = content.get("video_id", "")

            # Skip empty IDs
            if not video_id:
                print(f"Warning: Skipping content with empty video_id")
                continue

            # Truncate to 64 chars (Anthropic batch API limit)
            if len(video_id) > 64:
                video_id = video_id[:64]
                content = content.copy()
                content["video_id"] = video_id

            # Skip duplicates
            if video_id in seen_ids:
                print(f"Warning: Skipping duplicate video_id: {video_id}")
                continue

            seen_ids.add(video_id)
            validated.append(content)

        if len(validated) != len(content_list):
            print(f"Validated: {len(validated)} unique items (removed {len(content_list) - len(validated)} duplicates/invalid)")

        return validated

    def _chunk_content_list(
        self,
        content_list: List[Dict[str, Any]],
        max_batch_size: int = 50000  # Stay well under 100k limit
    ) -> List[List[Dict[str, Any]]]:
        """
        Split content into manageable batches.

        Batch API limit is 100k requests or 256MB, whichever comes first.
        We use 50k as a safe default.
        """
        if len(content_list) <= max_batch_size:
            return [content_list]

        chunks = []
        for i in range(0, len(content_list), max_batch_size):
            chunks.append(content_list[i:i + max_batch_size])

        print(f"Split into {len(chunks)} batches of ~{max_batch_size} requests each")
        return chunks

    def create_semantic_batch(
        self,
        content_list: List[Dict[str, Any]],
        output_dir: str
    ) -> BatchStatus:
        """
        Create a batch for semantic analysis.

        Returns BatchStatus with batch_id for polling.

        Best practices applied:
        - Unique custom_ids for each request
        - Validates input before submission
        - Checkpointing for resumability
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Check for existing batch checkpoint
        checkpoint_file = output_path / "batch_checkpoint.json"
        if checkpoint_file.exists():
            with open(checkpoint_file) as f:
                checkpoint = json.load(f)
            if checkpoint.get("batch_id") and checkpoint.get("status") != "ended":
                print(f"Resuming existing batch: {checkpoint['batch_id']}")
                return BatchStatus(**checkpoint)

        # Validate and dedupe content
        content_list = self._validate_and_dedupe_content(content_list)

        # Build batch requests
        requests = []
        for content in content_list:
            video_id = content.get("video_id", "")
            prompt = self._build_semantic_prompt(content)

            requests.append(Request(
                custom_id=video_id,
                params=MessageCreateParamsNonStreaming(
                    model=self.model,
                    max_tokens=2048,
                    messages=[{"role": "user", "content": prompt}]
                )
            ))

        print(f"Creating batch with {len(requests)} semantic analysis requests...")

        # Submit batch
        batch = self.client.messages.batches.create(requests=requests)

        status = BatchStatus(
            batch_id=batch.id,
            batch_type="semantic",
            total_requests=len(requests),
            processing=batch.request_counts.processing,
            succeeded=batch.request_counts.succeeded,
            errored=batch.request_counts.errored,
            canceled=batch.request_counts.canceled,
            expired=batch.request_counts.expired,
            status=batch.processing_status,
            created_at=batch.created_at.isoformat() if batch.created_at else datetime.now().isoformat(),
            results_url=batch.results_url
        )

        # Save checkpoint
        self._save_batch_checkpoint(checkpoint_file, status, content_list)

        print(f"Batch created: {batch.id}")
        print(f"Status: {batch.processing_status}")
        print(f"Expected completion: typically <1 hour (max 24h)")

        return status

    def create_sentiment_batch(
        self,
        content_list: List[Dict[str, Any]],
        output_dir: str
    ) -> BatchStatus:
        """
        Create a batch for sentiment analysis.

        Returns BatchStatus with batch_id for polling.

        Best practices applied:
        - Unique custom_ids for each request
        - Validates input before submission
        - Checkpointing for resumability
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Check for existing batch checkpoint
        checkpoint_file = output_path / "sentiment_batch_checkpoint.json"
        if checkpoint_file.exists():
            with open(checkpoint_file) as f:
                checkpoint = json.load(f)
            if checkpoint.get("batch_id") and checkpoint.get("status") != "ended":
                print(f"Resuming existing batch: {checkpoint['batch_id']}")
                return BatchStatus(**checkpoint)

        # Validate and dedupe content
        content_list = self._validate_and_dedupe_content(content_list)

        # Build batch requests
        requests = []
        for content in content_list:
            video_id = content.get("video_id", "")
            prompt = self._build_sentiment_prompt(content)

            requests.append(Request(
                custom_id=video_id,
                params=MessageCreateParamsNonStreaming(
                    model=self.model,
                    max_tokens=4096,  # Increased for complete JSON responses
                    messages=[{"role": "user", "content": prompt}]
                )
            ))

        print(f"Creating batch with {len(requests)} sentiment analysis requests...")

        # Submit batch
        batch = self.client.messages.batches.create(requests=requests)

        status = BatchStatus(
            batch_id=batch.id,
            batch_type="sentiment",
            total_requests=len(requests),
            processing=batch.request_counts.processing,
            succeeded=batch.request_counts.succeeded,
            errored=batch.request_counts.errored,
            canceled=batch.request_counts.canceled,
            expired=batch.request_counts.expired,
            status=batch.processing_status,
            created_at=batch.created_at.isoformat() if batch.created_at else datetime.now().isoformat(),
            results_url=batch.results_url
        )

        # Save checkpoint
        self._save_batch_checkpoint(checkpoint_file, status, content_list)

        print(f"Batch created: {batch.id}")
        print(f"Status: {batch.processing_status}")

        return status

    def poll_batch(
        self,
        batch_id: str,
        poll_interval: int = 60,
        max_wait: int = 86400  # 24 hours
    ) -> BatchStatus:
        """
        Poll batch until completion.

        Args:
            batch_id: The batch ID to poll
            poll_interval: Seconds between polls (default 60)
            max_wait: Maximum seconds to wait (default 24h)

        Returns:
            Final BatchStatus when complete
        """
        start_time = time.time()

        while True:
            batch = self.client.messages.batches.retrieve(batch_id)

            status = BatchStatus(
                batch_id=batch.id,
                batch_type="unknown",  # Will be set from checkpoint
                total_requests=sum([
                    batch.request_counts.processing,
                    batch.request_counts.succeeded,
                    batch.request_counts.errored,
                    batch.request_counts.canceled,
                    batch.request_counts.expired
                ]),
                processing=batch.request_counts.processing,
                succeeded=batch.request_counts.succeeded,
                errored=batch.request_counts.errored,
                canceled=batch.request_counts.canceled,
                expired=batch.request_counts.expired,
                status=batch.processing_status,
                created_at=batch.created_at.isoformat() if batch.created_at else "",
                results_url=batch.results_url
            )

            # Calculate progress
            completed = status.succeeded + status.errored + status.canceled + status.expired
            total = status.total_requests
            pct = (completed / total * 100) if total > 0 else 0

            print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                  f"Batch {batch_id[:20]}... "
                  f"Progress: {completed}/{total} ({pct:.1f}%) "
                  f"Status: {status.status}")

            if status.status == "ended":
                print(f"\nBatch complete!")
                print(f"  Succeeded: {status.succeeded}")
                print(f"  Errored: {status.errored}")
                print(f"  Canceled: {status.canceled}")
                print(f"  Expired: {status.expired}")
                return status

            # Check timeout
            elapsed = time.time() - start_time
            if elapsed > max_wait:
                print(f"Warning: Max wait time ({max_wait}s) exceeded")
                return status

            time.sleep(poll_interval)

    def retrieve_semantic_results(
        self,
        batch_id: str,
        content_list: List[Dict[str, Any]],
        output_dir: str
    ) -> List[ContentAnalysis]:
        """
        Retrieve and process semantic analysis results from a completed batch.
        """
        output_path = Path(output_dir)

        # Build lookup for content metadata
        content_lookup = {c["video_id"]: c for c in content_list}

        results = []
        error_count = 0

        print(f"Retrieving results for batch {batch_id}...")

        for result in self.client.messages.batches.results(batch_id):
            video_id = result.custom_id
            content = content_lookup.get(video_id, {})

            if result.result.type == "succeeded":
                response_text = result.result.message.content[0].text.strip()

                # Handle markdown code blocks
                if response_text.startswith("```"):
                    lines = response_text.split("\n")
                    response_text = "\n".join(lines[1:-1])

                try:
                    data = json.loads(response_text)

                    analysis = ContentAnalysis(
                        video_id=video_id,
                        influencer=content.get("influencer", ""),
                        platform=content.get("platform", ""),
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
                    results.append(analysis)

                except json.JSONDecodeError:
                    error_count += 1
                    results.append(self._create_error_semantic_result(video_id, content, "JSON parse error"))

            elif result.result.type == "errored":
                error_count += 1
                error_msg = str(result.result.error) if hasattr(result.result, 'error') else "Unknown error"
                results.append(self._create_error_semantic_result(video_id, content, error_msg))

            else:
                # canceled or expired
                error_count += 1
                results.append(self._create_error_semantic_result(video_id, content, result.result.type))

        print(f"Retrieved {len(results)} results ({error_count} errors)")

        # Export results
        self._export_semantic_results(results, output_path)

        return results

    def retrieve_sentiment_results(
        self,
        batch_id: str,
        content_list: List[Dict[str, Any]],
        output_dir: str
    ) -> List[SentimentResult]:
        """
        Retrieve and process sentiment analysis results from a completed batch.
        """
        output_path = Path(output_dir)

        # Build lookup for content metadata
        content_lookup = {c["video_id"]: c for c in content_list}

        results = []
        error_count = 0

        print(f"Retrieving sentiment results for batch {batch_id}...")

        for result in self.client.messages.batches.results(batch_id):
            video_id = result.custom_id
            content = content_lookup.get(video_id, {})

            if result.result.type == "succeeded":
                response_text = result.result.message.content[0].text.strip()

                # Extract JSON from response (handles extra commentary)
                response_text = extract_json_from_text(response_text)

                try:
                    data = json.loads(response_text)
                    emotions = data.get("emotions", {})

                    sentiment = SentimentResult(
                        video_id=video_id,
                        influencer=content.get("influencer", ""),
                        platform=content.get("platform", ""),
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
                    results.append(sentiment)

                except json.JSONDecodeError:
                    error_count += 1
                    results.append(self._create_error_sentiment_result(video_id, content, "JSON parse error"))

            elif result.result.type == "errored":
                error_count += 1
                error_msg = str(result.result.error) if hasattr(result.result, 'error') else "Unknown error"
                results.append(self._create_error_sentiment_result(video_id, content, error_msg))

            else:
                error_count += 1
                results.append(self._create_error_sentiment_result(video_id, content, result.result.type))

        print(f"Retrieved {len(results)} sentiment results ({error_count} errors)")

        # Export results
        self._export_sentiment_results(results, output_path)

        return results

    def _create_error_semantic_result(
        self,
        video_id: str,
        content: Dict[str, Any],
        error: str
    ) -> ContentAnalysis:
        """Create an error result for semantic analysis."""
        return ContentAnalysis(
            video_id=video_id,
            influencer=content.get("influencer", ""),
            platform=content.get("platform", ""),
            main_topic="Error",
            subtopics=[],
            content_type="error",
            content_format="error",
            nj_relevance_score=0,
            nj_locations_mentioned=[],
            nj_issues_mentioned=[],
            local_vs_universal="unknown",
            key_messages=[],
            call_to_action=None,
            narrative_frame="Error",
            tone="error",
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
            raw_response=error,
            timestamp=datetime.now().isoformat()
        )

    def _create_error_sentiment_result(
        self,
        video_id: str,
        content: Dict[str, Any],
        error: str
    ) -> SentimentResult:
        """Create an error result for sentiment analysis."""
        return SentimentResult(
            video_id=video_id,
            influencer=content.get("influencer", ""),
            platform=content.get("platform", ""),
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

    def _save_batch_checkpoint(
        self,
        checkpoint_file: Path,
        status: BatchStatus,
        content_list: List[Dict[str, Any]]
    ):
        """Save batch checkpoint for resumability."""
        with open(checkpoint_file, "w") as f:
            json.dump({
                **asdict(status),
                "content_ids": [c["video_id"] for c in content_list],
                "saved_at": datetime.now().isoformat()
            }, f, indent=2)

    def _export_semantic_results(self, results: List[ContentAnalysis], output_path: Path):
        """Export semantic results to JSON and CSV."""
        import csv

        # Full JSON
        json_file = output_path / "semantic_analysis_full.json"
        with open(json_file, "w") as f:
            json.dump([asdict(r) for r in results], f, indent=2)

        # Summary CSV
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

        print(f"Semantic results exported to {output_path}")

    def _export_sentiment_results(self, results: List[SentimentResult], output_path: Path):
        """Export sentiment results to JSON and CSV."""
        import csv

        # Full JSON
        json_file = output_path / "sentiment_analysis_full.json"
        with open(json_file, "w") as f:
            json.dump([asdict(r) for r in results], f, indent=2)

        # Summary CSV
        csv_file = output_path / "sentiment_summary.csv"
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
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

        print(f"Sentiment results exported to {output_path}")

    def run_full_batch_analysis(
        self,
        content_list: List[Dict[str, Any]],
        output_dir: str,
        poll_interval: int = 60
    ) -> Dict[str, Any]:
        """
        Run complete batch analysis (semantic + sentiment).

        This is the main entry point for batch processing.
        Submits both batches, polls for completion, retrieves results.

        Args:
            content_list: List of content dicts to analyze
            output_dir: Output directory for results
            poll_interval: Seconds between status polls

        Returns:
            Dict with semantic_results and sentiment_results
        """
        output_path = Path(output_dir)
        semantic_dir = output_path / "semantic"
        sentiment_dir = output_path / "sentiment"

        print("=" * 60)
        print("CLAUDE BATCH ANALYSIS")
        print(f"Processing {len(content_list)} posts")
        print(f"Cost savings: 50% vs real-time API")
        print("=" * 60)

        # Step 1: Submit semantic batch
        print("\n[1/4] Submitting semantic analysis batch...")
        semantic_status = self.create_semantic_batch(content_list, str(semantic_dir))

        # Step 2: Submit sentiment batch
        print("\n[2/4] Submitting sentiment analysis batch...")
        sentiment_status = self.create_sentiment_batch(content_list, str(sentiment_dir))

        # Step 3: Poll both batches
        print("\n[3/4] Polling for batch completion...")
        print("(Both batches processing in parallel)")

        semantic_done = semantic_status.status == "ended"
        sentiment_done = sentiment_status.status == "ended"

        while not (semantic_done and sentiment_done):
            if not semantic_done:
                semantic_status = self.poll_batch(
                    semantic_status.batch_id,
                    poll_interval=poll_interval,
                    max_wait=poll_interval + 1  # Single poll
                )
                semantic_done = semantic_status.status == "ended"

            if not sentiment_done:
                sentiment_status = self.poll_batch(
                    sentiment_status.batch_id,
                    poll_interval=poll_interval,
                    max_wait=poll_interval + 1
                )
                sentiment_done = sentiment_status.status == "ended"

            if not (semantic_done and sentiment_done):
                time.sleep(poll_interval)

        # Step 4: Retrieve results
        print("\n[4/4] Retrieving results...")

        semantic_results = self.retrieve_semantic_results(
            semantic_status.batch_id,
            content_list,
            str(semantic_dir)
        )

        sentiment_results = self.retrieve_sentiment_results(
            sentiment_status.batch_id,
            content_list,
            str(sentiment_dir)
        )

        print("\n" + "=" * 60)
        print("BATCH ANALYSIS COMPLETE")
        print(f"Semantic: {len(semantic_results)} results")
        print(f"Sentiment: {len(sentiment_results)} results")
        print(f"Results saved to: {output_dir}")
        print("=" * 60)

        return {
            "semantic_results": semantic_results,
            "sentiment_results": sentiment_results,
            "semantic_status": asdict(semantic_status),
            "sentiment_status": asdict(sentiment_status)
        }


def retry_failed_requests(
    batch_id: str,
    content_list: List[Dict[str, Any]],
    output_dir: str,
    batch_type: str = "semantic",
    api_key: Optional[str] = None
) -> Optional[BatchStatus]:
    """
    Retry failed requests from a completed batch.

    Extracts errored/expired requests and creates a new batch for them.

    Args:
        batch_id: Original batch ID
        content_list: Original content list (for rebuilding requests)
        output_dir: Output directory
        batch_type: "semantic" or "sentiment"
        api_key: Anthropic API key

    Returns:
        New BatchStatus if retries needed, None if no failures
    """
    client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    # Get failed request IDs
    failed_ids = []
    for result in client.messages.batches.results(batch_id):
        if result.result.type in ["errored", "expired"]:
            failed_ids.append(result.custom_id)

    if not failed_ids:
        print("No failed requests to retry")
        return None

    print(f"Found {len(failed_ids)} failed requests to retry")

    # Filter content list to just failed items
    content_lookup = {c["video_id"]: c for c in content_list}
    retry_content = [content_lookup[vid] for vid in failed_ids if vid in content_lookup]

    if not retry_content:
        print("Warning: Could not find content for failed IDs")
        return None

    # Create retry batch
    analyzer = ClaudeBatchAnalyzer(api_key=api_key)
    retry_dir = f"{output_dir}_retry"

    if batch_type == "semantic":
        return analyzer.create_semantic_batch(retry_content, retry_dir)
    else:
        return analyzer.create_sentiment_batch(retry_content, retry_dir)


def cancel_batch(batch_id: str, api_key: Optional[str] = None):
    """Cancel a running batch."""
    client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
    result = client.messages.batches.cancel(batch_id)
    print(f"Batch {batch_id} cancellation initiated. Status: {result.processing_status}")
    return result


def list_batches(api_key: Optional[str] = None, limit: int = 20):
    """List recent batches."""
    client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    print(f"Recent batches (limit {limit}):")
    print("-" * 80)

    for batch in client.messages.batches.list(limit=limit):
        succeeded = batch.request_counts.succeeded
        total = sum([
            batch.request_counts.processing,
            batch.request_counts.succeeded,
            batch.request_counts.errored,
            batch.request_counts.canceled,
            batch.request_counts.expired
        ])

        print(f"ID: {batch.id}")
        print(f"  Status: {batch.processing_status}")
        print(f"  Progress: {succeeded}/{total}")
        print(f"  Created: {batch.created_at}")
        print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Claude Batch Analyzer")
    parser.add_argument("action", choices=["analyze", "status", "cancel", "list"],
                        help="Action to perform")
    parser.add_argument("--batch-id", help="Batch ID for status/cancel")
    parser.add_argument("--input", help="Input CSV file for analyze")
    parser.add_argument("--output", default="analysis/ai_results_batch",
                        help="Output directory")
    parser.add_argument("--limit", type=int, default=0, help="Limit posts (0=all)")

    args = parser.parse_args()

    if args.action == "list":
        list_batches()

    elif args.action == "cancel":
        if not args.batch_id:
            print("Error: --batch-id required for cancel")
        else:
            cancel_batch(args.batch_id)

    elif args.action == "status":
        if not args.batch_id:
            print("Error: --batch-id required for status")
        else:
            analyzer = ClaudeBatchAnalyzer()
            status = analyzer.poll_batch(args.batch_id, poll_interval=1, max_wait=5)
            print(f"\nFinal status: {status}")

    elif args.action == "analyze":
        if not args.input:
            print("Error: --input required for analyze")
        else:
            import pandas as pd

            df = pd.read_csv(args.input)
            content_list = df.to_dict('records')

            if args.limit > 0:
                content_list = content_list[:args.limit]

            analyzer = ClaudeBatchAnalyzer()
            results = analyzer.run_full_batch_analysis(content_list, args.output)
            print(f"\nDone! Results in {args.output}")
