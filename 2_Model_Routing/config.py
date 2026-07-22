"""
Model Registry & Data Schemas for Model Routing.
Defines model metadata, pricing structures, context window limits, and capability flags.
"""

from dataclasses import dataclass
from typing import Dict

@dataclass
class ModelConfig:
    name: str
    provider: str
    cost_per_1k_input: float
    cost_per_1k_output: float
    max_context: int
    supports_vision: bool
    supports_tools: bool
    latency_p50_ms: int

# Enterprise Model Registry
MODEL_REGISTRY: Dict[str, ModelConfig] = {
    "llama-3-8b": ModelConfig(
        name="llama-3-8b",
        provider="groq",
        cost_per_1k_input=0.0001,
        cost_per_1k_output=0.0002,
        max_context=8192,
        supports_vision=False,
        supports_tools=False,
        latency_p50_ms=120
    ),
    "gpt-4o-mini": ModelConfig(
        name="gpt-4o-mini",
        provider="openai",
        cost_per_1k_input=0.00015,
        cost_per_1k_output=0.0006,
        max_context=128000,
        supports_vision=True,
        supports_tools=True,
        latency_p50_ms=350
    ),
    "gpt-4o": ModelConfig(
        name="gpt-4o",
        provider="openai",
        cost_per_1k_input=0.0025,
        cost_per_1k_output=0.010,
        max_context=128000,
        supports_vision=True,
        supports_tools=True,
        latency_p50_ms=600
    ),
    "claude-3-5-sonnet": ModelConfig(
        name="claude-3-5-sonnet",
        provider="anthropic",
        cost_per_1k_input=0.003,
        cost_per_1k_output=0.015,
        max_context=200000,
        supports_vision=True,
        supports_tools=True,
        latency_p50_ms=750
    ),
    "o1-preview": ModelConfig(
        name="o1-preview",
        provider="openai",
        cost_per_1k_input=0.015,
        cost_per_1k_output=0.060,
        max_context=128000,
        supports_vision=False,
        supports_tools=False,
        latency_p50_ms=2500
    ),
}
