"""
Rule-Based, Cost-Aware, and Complexity-Based Model Selection Classifier.
Determines optimal candidate model chains for incoming requests.
"""

from typing import List
from config import MODEL_REGISTRY

class QueryClassifier:
    """Analyzes prompt length, complexity, and capability requirements."""
    
    @staticmethod
    def estimate_tokens(text: str) -> int:
        return max(1, len(text) // 4)

    @classmethod
    def classify_complexity(cls, prompt: str) -> str:
        reasoning_keywords = ["proof", "algorithm", "architecture", "refactor", "optimize", "math", "derive"]
        code_keywords = ["def ", "class ", "import ", "function", "select * from", "public static void"]
        
        lower_p = prompt.lower()
        if any(kw in lower_p for kw in reasoning_keywords):
            return "high_reasoning"
        if any(kw in lower_p for kw in code_keywords):
            return "coding"
        if len(prompt) < 100:
            return "simple"
        return "medium"

    @classmethod
    def select_models(cls, prompt: str, has_image: bool = False, requires_tools: bool = False) -> List[str]:
        tokens = cls.estimate_tokens(prompt)
        complexity = cls.classify_complexity(prompt)

        # 1. Vision Capability Check
        if has_image:
            return ["gpt-4o-mini", "gpt-4o", "claude-3-5-sonnet"]

        # 2. Simple & Cheap Routing
        if complexity == "simple" and tokens < 500:
            return ["llama-3-8b", "gpt-4o-mini", "gpt-4o"]

        # 3. High Reasoning Routing
        if complexity == "high_reasoning":
            return ["o1-preview", "claude-3-5-sonnet", "gpt-4o"]

        # 4. Coding Workflows
        if complexity == "coding":
            return ["claude-3-5-sonnet", "gpt-4o", "gpt-4o-mini"]

        # Default fallback cascade
        return ["gpt-4o-mini", "gpt-4o", "claude-3-5-sonnet"]
