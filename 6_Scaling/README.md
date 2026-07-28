# ⚖️ Module 6 – Scaling & High Availability ⭐⭐⭐⭐⭐

> Scaling RAG architectures for production requires decoupling compute from state, designing stateless microservices, deploying robust queue and job orchestration pipelines, implementing high availability failovers, and managing multi-tier caching layers to maintain sub-100ms response times at scale.

---

## 🏗️ Part 1 – Scaling & Infrastructure

### Lesson 21. Scaling RAG ✅
* **21.1 Horizontal Scaling**
  * **Why Horizontal Scaling**: Decoupling compute from state allows individual microservices (API gateways, query processors, embedding models, vector nodes) to scale horizontally, preventing monolithic resource starvation.
  * **Kubernetes HPA**: Scaling replica pods dynamically based on CPU/Memory thresholds or custom metrics like concurrent query throughput and request queues.
  * **API Gateway Scaling**: Scaling edge nodes to run rate-limiting checks, TLS termination, and request routing across auto-scaling clusters.
  * **LLM Service Scaling**: Deploying model execution instances (vLLM, Triton Inference Server) on dynamically allocated GPU node pools.
  * **Vector DB Scaling**: Spreading indexes across distributed query nodes and index workers to handle concurrent semantic lookups.
  * **Autoscaling Metrics**: Tuning HPA configurations to trigger scaling on custom Prometheus metrics (e.g., token count per second, embedding service queue depth).
  * **Load Balancing**: Distributing incoming network traffic evenly to active pod replicas to maintain low latency.
* **21.2 Stateless AI Services**
  * **Stateless Microservices**: Ensuring query processing, context construction, and model routing components hold no local memory states, making them highly resilient and horizontally scalable.
  * **Session Storage**: Offloading active user context, conversation histories, and agent variables to externalized, distributed memory buffers.
  * **Redis**: Fast, in-memory key-value cache used for quick retrieval of active sliding window conversation memory.
  * **DynamoDB**: Scalable NoSQL store for persisting long-term multi-session chat histories and user preferences.
  * **Chat History Storage**: Storing raw multi-turn conversation traces separately from live execution buffers to limit token usage.
  * **Conversation State**: Maintaining state checkpoint variables for multi-step agent graphs outside of the core microservice pods.
  * **Authentication Tokens**: Enforcing stateless authorization validation via JWT signature verification at the gateway level.
* **21.3 Distributed Retrieval**
  * **Index Sharding**: Partitioning massive vector database collections and inverted indices across multiple physical compute nodes to enable parallel index searching.
  * **Distributed ANN**: Executing parallel approximate nearest neighbor graph traversals across index shards concurrently.
  * **Distributed BM25**: Merging exact term frequency matching from decoupled inverted index clusters.
  * **Query Fan-Out**: Broadcasting search query payloads to all distributed sharded nodes in parallel.
  * **Query Aggregation**: Merging returned candidate lists from all sharded nodes in a central coordinator node.
  * **Cross-Shard Ranking**: Normalizing and re-scoring candidate lists returned from disparate sharded partitions.
  * **Distributed Metadata Filtering**: Executing metadata validation dynamically at individual shard levels before merging lists.
* **21.4 Worker Pools**
  * **Background Workers**: Decoupling slow, intensive processing jobs from the user request loop using asynchronous background worker processes.
  * **Celery**: Python-based distributed task queue used for managing document parsing and ingestion runs.
  * **Ray**: Compute framework for parallelizing heavy mathematical workflows, such as batch embedding calculation and validation.
  * **Temporal**: Durable execution framework for orchestrating long-running, multi-step document ETL state machines.
  * **Parallel Ingestion**: Fan-out worker pools reading, parsing, and cleaning multiple source documents concurrently.
  * **Embedding Workers**: Asynchronous worker pools calling embedding APIs in batches to maximize throughput.
  * **OCR Workers**: GPU-accelerated workers handling visual layout analysis and text extraction.
  * **Evaluation Workers**: Background pools running unit tests, hallucination checkers, and RAGAS evaluations.
* **21.5 Load Balancing**
  * **API Load Balancing**: Gateway routers distributing query payloads dynamically to stateless processing containers.
  * **Vector DB Load Balancing**: Internal load balancers distributing read traffic across multiple read-replicas of vector database clusters.
  * **LLM Load Balancing**: Distributing inference tokens across multiple active GPU clusters or hosting API endpoints.
  * **Sticky Sessions**: Routing requests from a specific user session to the same container only when regional caching yields latency benefits.
  * **Health Checks**: Continuous monitoring of container endpoints to evict unhealthy nodes instantly.

---

### Lesson 22. High Availability ✅
* **22.1 Failover**
  * **LLM Failover**: Automatically rerouting inference queries to secondary model API endpoints (e.g., Azure OpenAI fallback for OpenAI) upon receiving rate limits ($429$) or server outages ($5\text{xx}$).
  * **Vector DB Failover**: Swapping cluster endpoint aliases automatically from primary to secondary vector nodes during network split-brain events.
  * **Regional Failover**: Setting up active-passive geo-redundancy to route traffic to secondary AWS regions during major cloud infrastructure failures.
  * **Automatic Failback**: Resuming traffic to primary endpoints once automated health checkers confirm recovery.
* **22.2 Backup Retrieval**
  * **BM25 Fallback**: Gracefully falling back to a local BM25 keyword search index if the vector database cluster fails.
  * **Cached Context Fallback**: Serving context from Redis semantic caches for common user queries if the entire retrieval subsystem times out.
  * **Secondary Vector DB**: Maintaining a synchronized backup vector database from a different cloud provider.
  * **Offline Retrieval**: Serving cached baseline corporate documents when all external search networks are unreachable.
* **22.3 Replica Vector Databases**
  * **Read Replicas**: Deploying read-only vector DB nodes to offload search traffic from the primary write-intensive index node.
  * **Multi-AZ Deployment**: Distributing database nodes across multiple Availability Zones to ensure index survival during localized data center outages.
  * **Read/Write Separation**: Routing index update transactions strictly to master nodes while fanning out queries across replica pools.
  * **Replica Synchronization**: Real-time sync protocols ensuring replica nodes maintain parity with the master index changes.
* **22.4 Disaster Recovery**
  * **Snapshots**: Triggering automated daily vector database snapshots and metadata backup dumps.
  * **Backup Strategy**: Retaining encrypted index backups in durable, geographically redundant storage pools.
  * **Restore Procedures**: Verified playbooks for rebuilding HNSW graphs from raw source document hashes during catastrophic crashes.
  * **RPO**: Recover Point Objective defining maximum acceptable data latency gap during restores.
  * **RTO**: Recovery Time Objective defining target recovery time limits for service restorations.
  * **Geo-Redundancy**: Copying snapshot backups automatically to isolated geographical zones.
* **22.5 Circuit Breakers**
  * **Open State**: Short-circuiting outgoing requests to failing downstream LLM or vector systems to prevent thread blocking and cascading failures.
  * **Closed State**: Normal operational state where requests flow unimpeded to backend engines.
  * **Half-Open State**: Permitting a minor percentage of probe requests to pass to verify if a failing backend endpoint has recovered.
  * **Failure Thresholds**: Configuring breaker activation based on consecutive error counts or elevated timeout percentages.
  * **Timeout Handling**: Setting strict client connection timeouts on external API loops.
  * **Preventing Cascading Failures**: Decoupling dependencies so that a failure in the evaluation worker pool never brings down the core chat gateway.

---

### Lesson 23. Queue Architecture ✅
* **23.1 Async Ingestion**
  * **Kafka**: Distributed event stream framework handling high-throughput ingestion updates from corporate repositories.
  * **RabbitMQ**: AMQP-based message broker managing document processing routing and parsing tasks.
  * **AWS SQS**: Managed queue service handling transient ingestion payloads with zero infrastructure overhead.
  * **Event Queues**: Decoupling source webhooks from the indexing pipeline to prevent ingestion spikes from overwhelming resources.
* **23.2 Background Workers**
  * **Parsing**: Workers running OCR and layout analysis algorithms in the background.
  * **OCR**: GPU workers converting scanned images and tables to Markdown.
  * **Embedding**: Workers calculating dense vector representations in batches.
  * **Metadata Extraction**: Workers extracting entity properties and security ACL schemas.
  * **Index Updates**: Background workers committing generated chunk vectors to indexes.
* **23.3 Job Queues**
  * **Priority Queues**: Routing critical real-time document additions (e.g., system updates) ahead of bulk batch indexing runs.
  * **Retry Queues**: Storing failed ingestion jobs for automatic retry processing.
  * **Dead Letter Queue (DLQ)**: Isolating persistently failing document files for manual inspection without halting the queue.
  * **Scheduling**: Scheduling crawling and synchronization runs during off-peak traffic hours.
  * **Exponential Backoff**: Implementing randomized exponential backoffs to query APIs without triggers.
* **23.4 Event-Driven Processing**
  * **CDC**: Real-time Change Data Capture triggering immediate re-indexing when source relational database rows change.
  * **Webhooks**: Source repository webhook triggers initiating ingestion on document creation.
  * **File Events**: OS file system listeners triggering document processing on local directory changes.
  * **Auto-Indexing**: Automating the entire ingestion loop from file creation to vector database entry.
  * **Incremental Indexing**: Running delta updates to modify only changed chunks.
* **23.5 Workflow Orchestration**
  * **Temporal**: Durable execution engine guaranteeing workflows run to completion even during server crashes.
  * **Airflow**: Managing complex batch ETL DAGs for monthly corporate database synchronizations.
  * **Dagster**: Asset-based data orchestrator managing data pipelines with strong type validations.
  * **LangGraph Workflows**: Orchestrating agent graphs with clear state checkpointer boundaries.
  * **Durable Execution**: Storing step-by-step progress state markers to allow ingestion resumes from the last failure checkpoint.

---

### Lesson 24. Caching Strategy ✅
* **24.1 Vector Cache**
  * Caching nearest-neighbor vector query results to eliminate repeated ANN graph traversals for identical search queries.
* **24.2 Retrieval Cache**
  * Caching fully constructed context payloads for recurring search queries in Redis to bypass vector index lookups.
* **24.3 Response Cache**
  * Key-value stores serving completed LLM outputs instantly for identical recurring prompts.
* **24.4 Metadata Cache**
  * Fast storage of tenant security group ACL tables to accelerate pre-filtering checks during retrieval.
* **24.5 Context Cache**
  * Caching assembled prompt structures (system prompt + history + top retrieved chunks) before generation.
* **24.6 Embedding Cache**
  * Caching text-to-vector outputs of frequent search strings to avoid embedding model invocation.
* **24.7 LLM KV Cache**
  * Caching Key-Value attention states of prompt prefixes at the LLM provider side to reduce TTFT latencies and costs.
