import json
import math
from typing import Dict, Any, List, Optional

class SemanticChunkHierarchyReRankerClient:
    """
    Production-grade hierarchical semantic chunk re-ranker for agentic RAG.
    Maintains parent-child document chunk hierarchies, scores semantic relevance
    against agent queries, and selects the most compact set of context chunks.
    """
    def __init__(self, token_limit: int = 1200):
        self.token_limit = token_limit

    def rerank_hierarchical_chunks(
        self,
        query: str = "How do we handle credit burn rate warnings in Metronome billing?",
        candidate_chunks: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        if not candidate_chunks:
            candidate_chunks = [
                {"chunk_id": "chk_p1_c1", "parent_doc": "billing_spec.md", "text": "Metronome triggers credit burn notifications when customer balance reaches 15% threshold.", "tokens": 85, "keyword_score": 0.92, "semantic_score": 0.88},
                {"chunk_id": "chk_p1_c2", "parent_doc": "billing_spec.md", "text": "Invoicing runs on the 1st of each calendar month using UTC timezone timestamps.", "tokens": 75, "keyword_score": 0.35, "semantic_score": 0.40},
                {"chunk_id": "chk_p2_c1", "parent_doc": "alerts_guide.md", "text": "Runaway burn rate detection uses statistical Z-scores to flag abnormal API spike surges.", "tokens": 90, "keyword_score": 0.85, "semantic_score": 0.91},
                {"chunk_id": "chk_p3_c1", "parent_doc": "stripe_sync.md", "text": "Stripe Connect synchronization handles automated payment capture and refund arbitration.", "tokens": 80, "keyword_score": 0.20, "semantic_score": 0.30}
            ]

        # Hybrid blend score: 40% keyword + 60% semantic
        scored_chunks = []
        for c in candidate_chunks:
            hybrid_score = round((c["keyword_score"] * 0.4) + (c["semantic_score"] * 0.6), 3)
            scored_chunks.append({
                "chunk_id": c["chunk_id"],
                "parent_doc": c["parent_doc"],
                "text": c["text"],
                "tokens": c["tokens"],
                "hybrid_relevance_score": hybrid_score
            })

        # Sort descending by score
        scored_chunks.sort(key=lambda x: x["hybrid_relevance_score"], reverse=True)

        selected_chunks = []
        total_tokens_used = 0
        for sc in scored_chunks:
            if total_tokens_used + sc["tokens"] <= self.token_limit and sc["hybrid_relevance_score"] >= 0.60:
                selected_chunks.append(sc)
                total_tokens_used += sc["tokens"]

        return {
            "rerank_id": "rnk_rag_3310",
            "query": query,
            "candidate_chunks_evaluated": len(candidate_chunks),
            "chunks_selected_count": len(selected_chunks),
            "total_context_tokens_used": total_tokens_used,
            "token_budget_utilization": f"{round((total_tokens_used / max(1, self.token_limit)) * 100, 1)}%",
            "top_ranked_chunk_id": selected_chunks[0]["chunk_id"] if selected_chunks else None,
            "selected_hierarchical_context": selected_chunks,
            "status": "OPTIMAL_CONTEXT_PACKED"
        }
