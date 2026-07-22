"""
Document Chunking and Indexing Data Structures.
Defines schemas for Document Chunks, Vector Search Results, and BM25 Tokens.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

@dataclass
class DocumentChunk:
    chunk_id: str
    doc_id: str
    content: str
    parent_content: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SearchResult:
    chunk: DocumentChunk
    score: float
    retrieval_type: str  # 'vector', 'bm25', 'hybrid', or 'reranked'
