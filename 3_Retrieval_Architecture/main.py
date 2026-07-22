"""
Main Execution Script for Production Retrieval Architecture Pipeline.
Executes Query Processing -> Hybrid Retrieval (BM25 + Vector + RRF) -> Reranking -> Context Packaging.
"""

from schemas import DocumentChunk
from query_processor import QueryProcessor
from hybrid_retriever import HybridRetriever
from context_packager import ContextPackager

def run_retrieval_pipeline_demo():
    print("=" * 65)
    print("🚀 ENTERPRISE RETRIEVAL ARCHITECTURE PIPELINE DEMO")
    print("=" * 65)

    # 1. Sample Corpus Setup
    corpus = [
        DocumentChunk(
            chunk_id="c1", 
            doc_id="doc_101", 
            content="AcmeCorp 2023 Retrieval Architecture leverages dense vector embeddings and BM25 hybrid search.", 
            metadata={"year": 2023, "tenant": "AcmeCorp", "verified": True}
        ),
        DocumentChunk(
            chunk_id="c2", 
            doc_id="doc_102", 
            content="RAG pipelines require reciprocal rank fusion RRF to merge sparse lexical and dense semantic results.", 
            metadata={"year": 2024, "tenant": "AcmeCorp", "verified": True}
        ),
        DocumentChunk(
            chunk_id="c3", 
            doc_id="doc_103", 
            content="Model routing and vector similarity search reduce costs across large language model enterprise deployments.", 
            metadata={"year": 2023, "tenant": "Globex", "verified": False}
        ),
        DocumentChunk(
            chunk_id="c4", 
            doc_id="doc_104", 
            content="Cross-encoder reranking algorithms evaluate query and document pairs jointly to improve Precision@K.", 
            metadata={"year": 2024, "tenant": "AcmeCorp", "verified": True}
        ),
    ]

    # 2. Raw Query Entry
    raw_query = "Explain AcmeCorp 2023 retrieval architecture vector similarity search"
    print(f"\n[Step 1 - Raw User Query]: '{raw_query}'")

    # 3. Query Processing & Filter Extraction
    clean_q, filters = QueryProcessor.extract_metadata_filters(raw_query)
    expanded_queries = QueryProcessor.expand_query(clean_q)
    print(f"\n[Step 2 - Query Processing]")
    print(f"Cleaned Query  : '{clean_q}'")
    print(f"Extracted Filters: {filters}")
    print(f"Expanded Queries : {expanded_queries}")

    # 4. Hybrid Search (Vector + BM25 + RRF)
    retriever = HybridRetriever(corpus)
    hybrid_candidates = retriever.search(clean_q, top_k=4)
    print(f"\n[Step 3 - Hybrid Search Execution (BM25 + Vector + RRF)]")
    for res in hybrid_candidates:
        print(f" -> Chunk ID: {res.chunk.chunk_id} | RRF Score: {res.score} | Content: {res.chunk.content[:60]}...")

    # 5. Reranking Stage
    reranked_results = ContextPackager.rerank(clean_q, hybrid_candidates, top_n=2)
    print(f"\n[Step 4 - Cross-Encoder Reranking Stage]")
    for res in reranked_results:
        print(f" -> Chunk ID: {res.chunk.chunk_id} | Rerank Score: {res.score} | Content: {res.chunk.content[:60]}...")

    # 6. Context Window Packaging & Citation Building
    context_payload = ContextPackager.build_context_window(reranked_results)
    print(f"\n[Step 5 - Context Window Assembly & Citations]")
    print("Generated Context Block for LLM Prompt:\n")
    print(context_payload["context_block"])
    print("\nCitation References:", context_payload["citations"])

if __name__ == "__main__":
    run_retrieval_pipeline_demo()
