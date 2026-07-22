# 🏭 Module 5 – Production RAG ⭐⭐⭐⭐⭐

> **Production RAG (Retrieval-Augmented Generation)** is an enterprise-grade architecture designed to connect Large Language Models dynamically to external company data. Unlike simple prototypes, a production RAG system balances ingestion scalability, low-latency hybrid retrieval, neural reranking, token cost management, robust observability, and continuous evaluation metrics.

---

## 📚 Architectural Pipeline Overview

```
 ┌────────────────┐      ┌────────────────┐      ┌────────────────┐      ┌────────────────┐
 │ 1. Data        │ ───► │ 2. Indexing    │ ───► │ 3. Query       │ ───► │ 4. Retrieval   │
 │    Ingestion   │      │    Pipeline    │      │    Processing  │      │    Layer       │
 └────────────────┘      └────────────────┘      └────────────────┘      └───────┬────────┘
                                                                                 │
 ┌────────────────┐      ┌────────────────┐      ┌────────────────┐              │
 │ 7. Generation  │ ◄─── │ 6. Context     │ ◄─── │ 5. Reranking   │ ◄────────────┘
 │    Layer       │      │    Construction│      │    Stage       │
 └───────┬────────┘      └────────────────┘      └────────────────┘
         │
         ▼
 ┌────────────────┐      ┌────────────────┐
 │ 8. Evaluation  │ &    │ 9. Monitoring  │
 │    Metrics     │      │    System      │
 └────────────────┘      └────────────────┘
```

---

## 🏗️ Part 1 – Data Ingestion & Indexing ⭐⭐⭐⭐⭐

*This is the offline pipeline responsible for preparing enterprise knowledge.*

### Lesson 1. Production RAG Architecture ✅
* **Prototype vs Production RAG**
  * *Prototype RAG*: Simple scripts reading local PDFs using naive fixed-size chunking, single dense vector store (e.g., Chroma/FAISS), cosine distance search, and direct LLM context dumping. Fails on scale, security, and latency.
  * *Production RAG*: Multi-stage distributed pipeline featuring layout-aware document extraction, hybrid search (dense + BM25), neural cross-encoder reranking, RBAC/ACL security metadata, tenant isolation, semantic caching, and full telemetry tracing.
* **Production RAG Components**
  * **Ingestion Layer**: Heterogeneous data connectors (SharePoint, Confluence, S3, SQL).
  * **Transformation & Indexing**: Layout parsing, semantic chunking, embedding generation, vector/lexical index builders.
  * **Query Processing Engine**: Query rewriting, coreference resolution, intent classification, HyDE.
  * **Retrieval & Reranking**: Parallel hybrid search execution and cross-encoder rescoring.
  * **Context Packaging**: Deduplication, token compression, citation attribution.
  * **Generation & Governance**: Model routing, system prompt grounding, token budgeting.
  * **Observability & Evaluation**: RAG Triad evaluation metrics, latency percentiles, and cost monitoring.
* **High-Level Architecture**
  * Asynchronous decoupling of **Offline Data Preparation** (Ingestion $\to$ Indexing) and **Online Query Execution** (Query $\to$ Retrieval $\to$ Generation).
* **Production Request Flow**
  1. Client prompt passes through Security/DLP and Rate Limiting.
  2. Query Engine rewrites intent and extracts metadata filters.
  3. Parallel execution across Dense Vector DB, BM25 Lexical Index, and Knowledge Graph.
  4. Reciprocal Rank Fusion (RRF) merges result sets.
  5. Cross-Encoder reranks top candidates.
  6. Context Packager builds prompt with citations.
  7. Model Router sends prompt to optimal LLM.

---

### Lesson 2. Enterprise Ingestion Pipeline ✅
* **Data Sources**
  * Connecting to disparate enterprise data silos: SharePoint, Confluence, JIRA, Google Drive, Notion, S3 buckets, PostgreSQL/MySQL DBs, REST APIs, Web Crawlers.
* **Validation**
  * Ingestion validation routines verifying file integrity, MIME type detection, byte-stream corruption checks, virus scanning, and character set encoding normalization (`UTF-8`).
* **Transformation**
  * Structural document parsing (PDF, DOCX, PPTX, HTML, Markdown).
  * Converting multi-modal document structures (embedded tables, charts, scanned text) into clean structured text and Markdown tables using specialized engines (LlamaParse, Unstructured, Marker).
* **Metadata Extraction**
  * Automated extraction of document headers, creation dates, author identities, section titles, document URIs, and department classification tags during ingestion.
* **Document Storage**
  * Persisting raw source documents and parsed JSON artifacts into durable blob storage (S3, Azure Blob, GCS) with hash key indexing (`SHA-256`) for auditability.

---

### Lesson 3. Indexing Pipeline ✅
* **Cleaning**
  * Stripping HTML boilerplate, fixing character encoding glitches, removing non-printable control characters, and stripping repetitive header/footer artifacts.
* **Chunking**
  * **Fixed-Size Chunking**: Token slicing with fixed character overlap (e.g., 512 tokens with 50-token overlap).
  * **Semantic Boundary Chunking**: Splitting text dynamically at natural section headers (`#`, `##`), paragraph breaks, or semantic embedding transitions.
  * **Parent-Child Chunking**: Generating small leaf chunks (100 tokens) for precise vector matching while keeping parent chunks (1000 tokens) linked for LLM context injection.
* **Metadata Assignment**
  * Binding extracted metadata attributes (`doc_id`, `chunk_id`, `created_at`, `security_acl`, `page_number`) directly to chunk schema payloads.
* **Embeddings**
  * Passing normalized text chunks through dense bi-encoder embedding models (`text-embedding-3-large`, `bge-large-en-v1.5`) to generate dense floating-point vector representations.
* **Multiple Indexes**
  * Writing output payloads to dual index structures:
    * **Dense Vector Index**: HNSW / IVF-PQ graphs in vector databases (Pinecone, Qdrant, Milvus, pgvector).
    * **Sparse Inverted Index**: BM25 keyword indexes in search engines (Elasticsearch, OpenSearch).

---

### Lesson 4. Incremental Indexing ✅
* **Change Detection**
  * Continuous data tracking using Change Data Capture (CDC) triggers, database transaction logs (Debezium), or webhooks to detect `INSERT`, `UPDATE`, and `DELETE` events at source repositories.
* **Chunk-Level Updates**
  * Comparing new document content hashes against historical chunk hashes to re-chunk and re-embed *only* changed sections, avoiding full document re-indexing overhead.
* **Version Synchronization**
  * Syncing state across source storage, vector database partitions, and BM25 inverted indexes in near real-time via event streaming (Kafka, RabbitMQ).
* **Delete Handling**
  * Hard and soft delete propagation. Deleting source documents instantly purges all associated chunk IDs across vector DB collections and inverted term indexes to prevent stale retrieval.

---

### Lesson 5. Document Versioning
* **Version IDs**
  * Assigning immutable semantic version identifiers (`v1.0`, `v1.1`, Git commit hashes, or timestamp hashes) to every ingested document.
* **Active vs Archived Versions**
  * Maintaining active state flags in vector metadata. Queries default to searching active indices while preserving archived historical document vectors for time-travel queries.
* **Rollback**
  * Instant rollback mechanisms allowing administrators to revert the active retrieval index to a previous document version snapshot by updating database alias pointers.
* **Audit Trail**
  * Immutable logging of all document ingestion events, version transitions, index modifications, and administrative deletions for compliance and security auditing.
* **Version-Aware Retrieval**
  * Enabling queries to pass target time bounds or version tags (`version: "2023-Q3"`) as metadata pre-filters during vector and keyword search.

---

### Lesson 6. Metadata Strategy
* **Metadata Design**
  * Establishing a standardized metadata schema across all enterprise data sources to enable unified filtering and search federation.
* **Required Metadata**
  * Baseline fields enforced on every ingested chunk: `chunk_id`, `doc_id`, `source_url`, `created_at`, `updated_at`, `tenant_id`, `checksum`.
* **Filtering**
  * Pre-filtering vector search space using structured tags (`{"year": {"$gte": 2023}, "category": "finance"}`) to reduce ANN search latency and eliminate irrelevant candidate domains.
* **Security Metadata**
  * Storing Access Control Lists (ACLs), user permission groups, and security classification levels (`public`, `internal`, `confidential`, `restricted`) within vector metadata.
* **Hierarchical Metadata**
  * Modeling parent-child document relationships (`organization -> department -> project -> document -> section -> chunk`) inside chunk metadata for contextual scoping.
* **Best Practices**
  * Standardizing key names, normalizing data types, keeping metadata payloads lightweight to save memory, and maintaining indexed metadata fields in HNSW vector nodes.
