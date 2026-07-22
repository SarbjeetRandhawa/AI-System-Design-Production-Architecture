"""
Hybrid Retriever combining Dense Vector Search and BM25 Lexical Search with Reciprocal Rank Fusion (RRF).
"""

import math
from typing import List, Dict
from schemas import DocumentChunk, SearchResult

class HybridRetriever:
    """In-memory hybrid retriever supporting BM25 + Vector Similarity Search."""

    def __init__(self, corpus: List[DocumentChunk]):
        self.corpus = corpus

    def _simulated_vector_search(self, query: str, top_k: int) -> List[SearchResult]:
        """Simulates dense vector search scoring based on term overlap & length."""
        query_words = set(query.lower().split())
        results = []
        for chunk in self.corpus:
            chunk_words = set(chunk.content.lower().split())
            overlap = len(query_words.intersection(chunk_words))
            # Mock cosine vector score
            score = round(overlap / (len(query_words) + 1.5), 4)
            if score > 0:
                results.append(SearchResult(chunk=chunk, score=score, retrieval_type="vector"))
        
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]

    def _bm25_search(self, query: str, top_k: int) -> List[SearchResult]:
        """Simulates BM25 keyword score matching."""
        query_terms = query.lower().split()
        results = []
        for chunk in self.corpus:
            score = 0.0
            content_lower = chunk.content.lower()
            for term in query_terms:
                tf = content_lower.count(term)
                if tf > 0:
                    # BM25-like term weighting formula simulation
                    score += (tf * 1.5) / (tf + 0.5)
            if score > 0:
                results.append(SearchResult(chunk=chunk, score=round(score, 4), retrieval_type="bm25"))
        
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]

    def reciprocal_rank_fusion(
        self, 
        vector_results: List[SearchResult], 
        bm25_results: List[SearchResult], 
        k: int = 60,
        top_n: int = 5
    ) -> List[SearchResult]:
        """Combines ranked candidate lists using RRF equation."""
        rrf_scores: Dict[str, float] = {}
        chunk_map: Dict[str, DocumentChunk] = {}

        for rank, res in enumerate(vector_results, start=1):
            cid = res.chunk.chunk_id
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (k + rank))
            chunk_map[cid] = res.chunk

        for rank, res in enumerate(bm25_results, start=1):
            cid = res.chunk.chunk_id
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (k + rank))
            chunk_map[cid] = res.chunk

        hybrid_results = [
            SearchResult(chunk=chunk_map[cid], score=round(score, 6), retrieval_type="hybrid_rrf")
            for cid, score in rrf_scores.items()
        ]
        hybrid_results.sort(key=lambda x: x.score, reverse=True)
        return hybrid_results[:top_n]

    def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        vec_res = self._simulated_vector_search(query, top_k=top_k * 2)
        bm25_res = self._bm25_search(query, top_k=top_k * 2)
        return self.reciprocal_rank_fusion(vec_res, bm25_res, top_n=top_k)
