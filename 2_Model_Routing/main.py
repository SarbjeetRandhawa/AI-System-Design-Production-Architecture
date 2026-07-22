"""
Main Execution Script for Enterprise Model Routing.
Demonstrates various query scenarios (simple, coding, reasoning, vision).
"""

import asyncio
from router_engine import ModelRouterEngine

async def run_demos():
    router = ModelRouterEngine(user_tier="enterprise")
    
    print("=" * 60)
    print("🚀 ENTERPRISE AI MODEL ROUTER DEMONSTRATION")
    print("=" * 60)

    # Test Case 1: Simple Greeting Query with PII
    prompt_1 = "Hello, my email is john.doe@company.com. What is 2 + 2?"
    res_1 = await router.execute_request(prompt_1)
    print("\n[Test 1 - Simple Query + PII]")
    print(f"Model Used: {res_1['model_used']} | Provider: {res_1['provider']}")
    print(f"Latency: {res_1['latency_ms']} ms | Cost: ${res_1['cost_usd']}")
    print(f"Sanitized Prompt: {res_1['prompt_sanitized']}")
    print(f"Output: {res_1['response']}")

    # Test Case 2: Complex Architecture & Coding Request
    prompt_2 = "Refactor this architecture to optimize def search_graph algorithm and memory efficiency."
    res_2 = await router.execute_request(prompt_2)
    print("\n[Test 2 - Coding & Refactoring Task]")
    print(f"Model Used: {res_2['model_used']} | Provider: {res_2['provider']}")
    print(f"Latency: {res_2['latency_ms']} ms | Cost: ${res_2['cost_usd']}")
    print(f"Output: {res_2['response']}")

    # Test Case 3: High Reasoning Math Proof
    prompt_3 = "Provide a formal mathematical proof for graph isomorphism complexity bounds."
    res_3 = await router.execute_request(prompt_3)
    print("\n[Test 3 - Deep Reasoning & Proof Task]")
    print(f"Model Used: {res_3['model_used']} | Provider: {res_3['provider']}")
    print(f"Latency: {res_3['latency_ms']} ms | Cost: ${res_3['cost_usd']}")
    print(f"Output: {res_3['response']}")

    # Test Case 4: Vision Payload
    prompt_4 = "Describe the attached chart."
    res_4 = await router.execute_request(prompt_4, has_image=True)
    print("\n[Test 4 - Vision Multimodal Input]")
    print(f"Model Used: {res_4['model_used']} | Provider: {res_4['provider']}")
    print(f"Latency: {res_4['latency_ms']} ms | Cost: ${res_4['cost_usd']}")
    print(f"Output: {res_4['response']}")

if __name__ == "__main__":
    asyncio.run(run_demos())
