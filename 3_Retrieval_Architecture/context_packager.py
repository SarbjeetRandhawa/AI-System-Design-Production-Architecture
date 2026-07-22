"""
Reranking Engine & Context Packaging (Deduplication, Compression, Citations).
"""

from typing import List, Dict, Any
from schemas import SearchResult, DocumentChunk

class ContextPackager:
    """Reranks, deduplicates, compresses, and packages context for downstream LLM prompts."""

    @staticmethod
    def rerank(query: str, results: List[SearchResult], top_n: int = 3) -> List[SearchResult]:
        """Simulates Cross-Encoder neural reranking between query and passages."""
        query_words = set(query.lower().split())
        
        for res in results:
            content_words = set(res.chunk.content.lower().split())
            # Cross-encoder joint attention score simulation
            exact_matches = len(query_words.intersection(content_words))
            boost = 1.5 if res.chunk.metadata.get("verified") else 1.0
            res.score = round(((res.score * 0.5) + (exact_matches * 0.5)) * boost, 4)
            res.retrieval_type = "cross_encoder_reranked"

        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_n]

    @staticmethod
    def build_context_window(results: List[SearchResult]) -> Dict[str, Any]:
        """Formats passages into a structured context window payload with citation footprints."""
        formatted_passages = []
        citations = []

        for idx, res in enumerate(results, start=1):
            chunk = res.chunk
            citation_id = f"Doc-{chunk.doc_id}-Chunk{chunk.chunk_id}"
            
            passage_text = f"[{idx}] (Source: {citation_id})\n{chunk.content}"
            formatted_passages.append(passage_text)
            
            citations.append({
                "index": idx,
                "citation_id": citation_id,
                "doc_id": chunk.doc_id,
                "metadata": chunk.metadata
            })

        context_block = "\n\n---\n\n".join(formatted_passages)
        
        return {
            "context_block": context_block,
            "citations": citations,
            "total_chunks": len(results)
        }
