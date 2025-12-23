#!/usr/bin/env python3
"""
Topic Modeling and Clustering

Discovers emergent themes and topics across the corpus using:
- Text embeddings (OpenAI or local)
- Clustering algorithms (K-means, HDBSCAN)
- Topic labeling with LLMs
- Visualization of topic clusters
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import defaultdict
import numpy as np
from tqdm import tqdm


@dataclass
class TopicCluster:
    """A discovered topic cluster."""
    cluster_id: int
    label: str
    description: str
    keywords: List[str]
    size: int
    video_ids: List[str]
    representative_examples: List[str]
    avg_engagement: float
    platforms: Dict[str, int]
    influencers: Dict[str, int]


@dataclass
class TopicModelResult:
    """Full topic modeling results."""
    num_topics: int
    clusters: List[TopicCluster]
    video_assignments: Dict[str, int]  # video_id -> cluster_id
    coherence_score: float
    timestamp: str


class TopicModeler:
    """
    Discover topics across content corpus using embeddings and clustering.
    """

    def __init__(
        self,
        embedding_model: str = "text-embedding-3-small",
        openai_api_key: Optional[str] = None,
        gemini_api_key: Optional[str] = None
    ):
        self.openai_key = openai_api_key or os.environ.get("OPENAI_API_KEY")
        self.gemini_key = gemini_api_key or os.environ.get("GEMINI_API_KEY")
        self.embedding_model = embedding_model

        # Lazy load heavy dependencies
        self._openai_client = None
        self._gemini_model = None

    @property
    def openai_client(self):
        if self._openai_client is None:
            from openai import OpenAI
            self._openai_client = OpenAI(api_key=self.openai_key)
        return self._openai_client

    @property
    def gemini_model(self):
        if self._gemini_model is None:
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_key)
            self._gemini_model = genai.GenerativeModel("gemini-1.5-flash")
        return self._gemini_model

    def get_embeddings(
        self,
        texts: List[str],
        batch_size: int = 100
    ) -> np.ndarray:
        """
        Get embeddings for a list of texts using OpenAI.
        """
        embeddings = []

        for i in tqdm(range(0, len(texts), batch_size), desc="Getting embeddings"):
            batch = texts[i:i + batch_size]
            # Truncate long texts
            batch = [t[:8000] if t else "" for t in batch]

            response = self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=batch
            )

            for item in response.data:
                embeddings.append(item.embedding)

        return np.array(embeddings)

    def cluster_embeddings(
        self,
        embeddings: np.ndarray,
        method: str = "hdbscan",
        n_clusters: Optional[int] = None,
        min_cluster_size: int = 5
    ) -> Tuple[np.ndarray, int]:
        """
        Cluster embeddings using specified method.

        Returns: (cluster_labels, num_clusters)
        """
        # Dimensionality reduction first
        from sklearn.decomposition import PCA

        # Reduce to 50 dimensions for clustering
        n_components = min(50, embeddings.shape[1], embeddings.shape[0] - 1)
        pca = PCA(n_components=n_components)
        reduced = pca.fit_transform(embeddings)

        if method == "hdbscan":
            try:
                import hdbscan
                clusterer = hdbscan.HDBSCAN(
                    min_cluster_size=min_cluster_size,
                    min_samples=3,
                    metric='euclidean'
                )
                labels = clusterer.fit_predict(reduced)
            except ImportError:
                print("HDBSCAN not available, falling back to KMeans")
                method = "kmeans"

        if method == "kmeans":
            from sklearn.cluster import KMeans

            if n_clusters is None:
                # Use elbow method to find optimal k
                n_clusters = self._find_optimal_k(reduced)

            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            labels = kmeans.fit_predict(reduced)

        num_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        return labels, num_clusters

    def _find_optimal_k(self, data: np.ndarray, max_k: int = 20) -> int:
        """Find optimal number of clusters using elbow method."""
        from sklearn.cluster import KMeans

        max_k = min(max_k, len(data) - 1)
        inertias = []

        for k in range(2, max_k + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(data)
            inertias.append(kmeans.inertia_)

        # Find elbow point using second derivative
        if len(inertias) < 3:
            return 5

        diffs = np.diff(inertias)
        diffs2 = np.diff(diffs)
        elbow = np.argmax(diffs2) + 2

        return max(5, min(elbow, 15))  # Keep between 5 and 15 clusters

    def label_clusters(
        self,
        clusters: Dict[int, List[Dict[str, Any]]]
    ) -> Dict[int, Dict[str, Any]]:
        """
        Use LLM to generate descriptive labels for each cluster.
        """
        labeled = {}

        for cluster_id, items in tqdm(clusters.items(), desc="Labeling clusters"):
            if cluster_id == -1:
                # Noise cluster
                labeled[cluster_id] = {
                    "label": "Uncategorized",
                    "description": "Content that doesn't fit into main clusters",
                    "keywords": []
                }
                continue

            # Sample up to 10 items from cluster
            sample = items[:10] if len(items) <= 10 else np.random.choice(
                items, 10, replace=False
            ).tolist()

            # Build prompt
            content_summaries = []
            for item in sample:
                summary = f"- {item.get('title', 'Untitled')}: {item.get('transcript', '')[:200]}"
                content_summaries.append(summary)

            prompt = f"""Analyze these {len(items)} pieces of content from NJ influencers and identify their common theme.

Sample content from this cluster:
{chr(10).join(content_summaries)}

Respond with JSON only:
{{
    "label": "Short topic label (2-4 words)",
    "description": "One sentence describing this topic cluster",
    "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
}}"""

            try:
                response = self.gemini_model.generate_content(prompt)
                text = response.text.strip()

                # Handle code blocks
                if text.startswith("```"):
                    lines = text.split("\n")
                    text = "\n".join(lines[1:-1])

                data = json.loads(text)
                labeled[cluster_id] = data

            except Exception as e:
                labeled[cluster_id] = {
                    "label": f"Cluster {cluster_id}",
                    "description": f"Error labeling: {str(e)}",
                    "keywords": []
                }

        return labeled

    def build_topic_model(
        self,
        content_list: List[Dict[str, Any]],
        output_dir: str,
        method: str = "hdbscan",
        n_clusters: Optional[int] = None
    ) -> TopicModelResult:
        """
        Full topic modeling pipeline.

        content_list: List of dicts with:
            - video_id, influencer, platform, title, transcript
            - view_count, like_count (optional, for engagement)
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        print(f"Building topic model for {len(content_list)} items...")

        # Create text for embedding (combine title + transcript)
        texts = []
        for item in content_list:
            text = f"{item.get('title', '')} {item.get('transcript', '')}"
            texts.append(text.strip())

        # Get embeddings
        embeddings = self.get_embeddings(texts)

        # Save embeddings for reuse
        np.save(output_path / "embeddings.npy", embeddings)

        # Cluster
        labels, num_clusters = self.cluster_embeddings(
            embeddings, method, n_clusters
        )

        print(f"Found {num_clusters} topic clusters")

        # Group content by cluster
        clusters_content = defaultdict(list)
        video_assignments = {}

        for i, (item, label) in enumerate(zip(content_list, labels)):
            clusters_content[int(label)].append(item)
            video_assignments[item["video_id"]] = int(label)

        # Label clusters with LLM
        cluster_labels = self.label_clusters(clusters_content)

        # Build final cluster objects
        topic_clusters = []

        for cluster_id, items in clusters_content.items():
            label_info = cluster_labels.get(cluster_id, {})

            # Calculate cluster statistics
            platforms = defaultdict(int)
            influencers = defaultdict(int)
            total_engagement = 0

            for item in items:
                platforms[item.get("platform", "unknown")] += 1
                influencers[item.get("influencer", "unknown")] += 1
                total_engagement += item.get("like_count", 0) + item.get("comment_count", 0)

            avg_engagement = total_engagement / len(items) if items else 0

            # Get representative examples
            examples = [item.get("title", "Untitled") for item in items[:5]]

            topic_clusters.append(TopicCluster(
                cluster_id=cluster_id,
                label=label_info.get("label", f"Cluster {cluster_id}"),
                description=label_info.get("description", ""),
                keywords=label_info.get("keywords", []),
                size=len(items),
                video_ids=[item["video_id"] for item in items],
                representative_examples=examples,
                avg_engagement=avg_engagement,
                platforms=dict(platforms),
                influencers=dict(influencers)
            ))

        # Sort by size
        topic_clusters.sort(key=lambda x: x.size, reverse=True)

        result = TopicModelResult(
            num_topics=num_clusters,
            clusters=topic_clusters,
            video_assignments=video_assignments,
            coherence_score=0.0,  # TODO: Calculate coherence
            timestamp=datetime.now().isoformat()
        )

        # Export results
        self._export_results(result, output_path)

        return result

    def _export_results(self, result: TopicModelResult, output_path: Path):
        """Export topic model results."""
        # Full JSON
        with open(output_path / "topic_model_full.json", "w") as f:
            json.dump({
                "num_topics": result.num_topics,
                "clusters": [asdict(c) for c in result.clusters],
                "coherence_score": result.coherence_score,
                "timestamp": result.timestamp
            }, f, indent=2)

        # Video assignments
        with open(output_path / "video_topic_assignments.json", "w") as f:
            json.dump(result.video_assignments, f, indent=2)

        # Topic summary for quick reference
        with open(output_path / "topic_summary.md", "w") as f:
            f.write("# Topic Model Summary\n\n")
            f.write(f"Generated: {result.timestamp}\n")
            f.write(f"Number of topics: {result.num_topics}\n\n")

            for cluster in result.clusters:
                f.write(f"## {cluster.label}\n")
                f.write(f"- **Size:** {cluster.size} videos\n")
                f.write(f"- **Description:** {cluster.description}\n")
                f.write(f"- **Keywords:** {', '.join(cluster.keywords)}\n")
                f.write(f"- **Avg engagement:** {cluster.avg_engagement:.0f}\n")
                f.write(f"- **Platforms:** {cluster.platforms}\n")
                f.write(f"- **Top influencers:** {dict(list(cluster.influencers.items())[:5])}\n")
                f.write(f"- **Examples:** {cluster.representative_examples[:3]}\n\n")

        print(f"\nResults saved to {output_path}")

    def visualize_clusters(
        self,
        embeddings: np.ndarray,
        labels: np.ndarray,
        cluster_labels: Dict[int, str],
        output_path: str
    ):
        """Create 2D visualization of topic clusters using UMAP."""
        try:
            import umap
            import matplotlib.pyplot as plt
        except ImportError:
            print("UMAP or matplotlib not available, skipping visualization")
            return

        # Reduce to 2D
        reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=42)
        embedding_2d = reducer.fit_transform(embeddings)

        # Plot
        plt.figure(figsize=(14, 10))

        # Get unique labels
        unique_labels = set(labels)
        colors = plt.cm.tab20(np.linspace(0, 1, len(unique_labels)))

        for i, label in enumerate(unique_labels):
            mask = labels == label
            cluster_name = cluster_labels.get(label, f"Cluster {label}")

            plt.scatter(
                embedding_2d[mask, 0],
                embedding_2d[mask, 1],
                c=[colors[i]],
                label=f"{cluster_name} ({mask.sum()})",
                alpha=0.7,
                s=50
            )

        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.title("NJ Influencer Content Topic Clusters")
        plt.xlabel("UMAP-1")
        plt.ylabel("UMAP-2")
        plt.tight_layout()

        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"Visualization saved to {output_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build topic model from content")
    parser.add_argument("data_dir", help="Directory with consolidated content data")
    parser.add_argument("--output", default="analysis/topic_model_results")
    parser.add_argument("--method", choices=["kmeans", "hdbscan"], default="hdbscan")
    parser.add_argument("--n-clusters", type=int, help="Number of clusters (kmeans only)")

    args = parser.parse_args()

    # Load content data
    import pandas as pd

    all_posts = pd.read_csv(Path(args.data_dir) / "all_posts.csv")

    content_list = []
    for _, row in all_posts.iterrows():
        content_list.append({
            "video_id": str(row.get("post_id", "")),
            "influencer": row.get("influencer_name", ""),
            "platform": row.get("platform", ""),
            "title": row.get("title", "") or row.get("caption", ""),
            "transcript": "",  # Would need to load from processed results
            "view_count": row.get("view_count", 0),
            "like_count": row.get("like_count", 0),
            "comment_count": row.get("comment_count", 0)
        })

    print(f"Loaded {len(content_list)} items")

    modeler = TopicModeler()
    result = modeler.build_topic_model(
        content_list,
        args.output,
        method=args.method,
        n_clusters=args.n_clusters
    )

    print(f"\nDiscovered {result.num_topics} topics")
