# 🚀 Module 10 – Deployment & AI DevOps ⭐⭐⭐⭐⭐

> Deploying enterprise-grade AI systems requires moving beyond local runtime scripts to containerized, auto-scaled, and highly resilient cloud environments. This module covers containerization, orchestration, serving engines, and continuous integration/deployment (CI/CD) pipelines.

---

## 📦 Part 1 – Infrastructure & Containerization

### Lesson 35. Containerization for AI Services ✅
* **Dockerizing AI Services**
  * Building minimal, multi-stage Docker files for python API gateways, worker pools, and database layers.
  * Optimizing image size (using slim base images and separating build-time dependencies) to decrease cold-start latencies in serverless environments.
  * GPU support configurations: setting up NVIDIA Container Toolkit (`nvidia-docker2`) and passing `--gpus all` flags for model inference containers.
* **Kubernetes Orchestration**
  * Defining Kubernetes manifests for deployment, services, ingress routers, and config maps.
  * Autoscaling on custom metrics: Using KEDA (Kubernetes Event-driven Autoscaling) to scale GPU inference nodes based on queue sizes or token-per-second throughput.
  * Node affinity and tolerations: Routing heavy inference workloads strictly to GPU-enabled node pools while keeping API gateways on standard CPU nodes.

---

## ⚡ Part 2 – Model Serving & CI/CD

### Lesson 36. High-Performance Serving Engines ✅
* **vLLM**
  * Deploying open-source LLMs (e.g., Llama, Mistral) using vLLM for high-throughput serving.
  * Key features: PagedAttention (managing KV cache memory allocation to prevent fragmentation), continuous batching, and speculative decoding.
* **Triton Inference Server**
  * Deploying Triton for multi-framework model execution (PyTorch, TensorRT, ONNX).
  * Key features: Dynamic batching, concurrent model execution, and model pipelining.
* **API Gateways**
  * Setting up AI-aware API gateways (e.g., Kong, Envoy, LiteLLM) to handle request routing, rate limiting, and fallback options.

---

### Lesson 37. CI/CD & Progressive Delivery ✅
* **Continuous Integration (CI)**
  * Automated testing pipelines verifying code linting, unit tests, and integration tests on build steps.
  * Model validation steps: Running regression tests using framework tools (DeepEval, RAGAS) to ensure changes do not degrade factual accuracy.
* **Progressive Delivery**
  * **Blue-Green Deployments**: Swapping production traffic routing from old to new environments instantly once target health checks pass.
  * **Canary Deployments**: Incrementally routing a small fraction of users (1% -> 10% -> 50% -> 100%) to new models or pipeline configurations while monitoring performance metrics.
  * **Shadow Deployments**: Duplicating live request streams to evaluate a new model in the background without affecting production responses.
