"""
Asynchronous Router Engine with Fallback & Telemetry.
Executes candidate model cascades with failover handling.
"""

import time
import asyncio
from typing import Dict, Any, List
from config import MODEL_REGISTRY, ModelConfig
from security import SecurityDLP
from classifier import QueryClassifier

class ModelRouterEngine:
    def __init__(self, user_tier: str = "standard"):
        self.user_tier = user_tier

    async def execute_request(
        self, 
        prompt: str, 
        has_image: bool = False, 
        requires_tools: bool = False
    ) -> Dict[str, Any]:
        
        # 1. Sanitize input prompt
        sanitized_prompt = SecurityDLP.sanitize(prompt)
        
        # 2. Determine model candidates
        candidate_models = QueryClassifier.select_models(
            sanitized_prompt, 
            has_image=has_image, 
            requires_tools=requires_tools
        )
        
        last_error: Exception = None

        # 3. Cascading execution loop with fallback
        for model_name in candidate_models:
            model_cfg: ModelConfig = MODEL_REGISTRY[model_name]
            try:
                start_time = time.time()
                
                # Simulate async LLM Provider API call latency
                await asyncio.sleep(model_cfg.latency_p50_ms / 1000.0)

                input_tokens = QueryClassifier.estimate_tokens(sanitized_prompt)
                output_tokens = 120
                
                # Calculate cost USD
                cost = ((input_tokens / 1000.0) * model_cfg.cost_per_1k_input) + \
                       ((output_tokens / 1000.0) * model_cfg.cost_per_1k_output)

                return {
                    "status": "success",
                    "model_used": model_name,
                    "provider": model_cfg.provider,
                    "latency_ms": round((time.time() - start_time) * 1000, 2),
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "cost_usd": round(cost, 6),
                    "prompt_sanitized": sanitized_prompt,
                    "response": f"[Response from {model_name}] for prompt: '{sanitized_prompt[:40]}...'"
                }
            except Exception as err:
                last_error = err
                # Log warning and attempt fallback model
                continue

        return {"status": "error", "message": str(last_error)}
