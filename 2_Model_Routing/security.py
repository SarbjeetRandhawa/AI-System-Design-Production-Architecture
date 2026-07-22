"""
Data Loss Prevention (DLP) & Security Module for Model Router.
Sanitizes prompts before sending payload to cloud LLM providers.
"""

import re

class SecurityDLP:
    """Data Loss Prevention: Redacts sensitive PII and confidential keys."""
    
    @staticmethod
    def sanitize(prompt: str) -> str:
        # Redact emails
        prompt = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[REDACTED_EMAIL]', prompt)
        
        # Redact credit card numbers
        prompt = re.sub(r'\b(?:\d[ -]*?){13,16}\b', '[REDACTED_CARD]', prompt)
        
        # Redact API keys / Tokens (sk-..., bearer tokens)
        prompt = re.sub(r'sk-[a-zA-Z0-9]{32,}', '[REDACTED_API_KEY]', prompt)
        
        return prompt
