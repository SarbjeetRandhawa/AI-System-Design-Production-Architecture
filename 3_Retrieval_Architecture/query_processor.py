"""
Query Processing Unit: Query Rewriting, Expansion, and Metadata Extraction.
"""

import re
from typing import Dict, Any, List, Tuple

class QueryProcessor:
    """Refines input queries for optimal lexical and vector retrieval."""

    @staticmethod
    def extract_metadata_filters(query: str) -> Tuple[str, Dict[str, Any]]:
        filters = {}

        # Extract year constraint
        year_match = re.search(r'\b(20\d{2})\b', query)
        if year_match:
            filters["year"] = int(year_match.group(1))

        # Extract entity tag
        if "acme" in query.lower():
            filters["tenant"] = "AcmeCorp"
        elif "globex" in query.lower():
            filters["tenant"] = "Globex"

        # Clean query text
        clean_query = re.sub(r'\b(20\d{2})\b', '', query, flags=re.IGNORECASE).strip()
        return clean_query, filters

    @staticmethod
    def expand_query(query: str) -> List[str]:
        """Generates query variations for expansion / multi-query search."""
        variations = [query]
        lower_q = query.lower()

        if "rag" in lower_q or "retrieval" in lower_q:
            variations.append(query + " vector similarity search chunking")
        if "architecture" in lower_q or "system" in lower_q:
            variations.append(query + " infrastructure pipeline components")

        return list(set(variations))
