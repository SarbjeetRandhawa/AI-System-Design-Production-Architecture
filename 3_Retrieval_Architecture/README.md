# 🔍 Module 3 – Retrieval Architecture ⭐⭐⭐⭐⭐

> **Retrieval Architecture** is the foundational subsystem of modern Enterprise AI and Retrieval-Augmented Generation (RAG) systems. It governs how structured and unstructured data is discovered, processed, indexed, searched, and constructed into optimal context for Large Language Model (LLM) processing.

---

## 📚 What You'll Learn

```
             ┌─────────────────────────────────────────────────────────┐
             │               Retrieval Architecture                    │
             └────────────────────────────┬────────────────────────────┘
                                          │
       ┌───────────────────┬──────────────┴───────┬───────────────────┐
       ▼                   ▼                      ▼                   ▼
┌──────────────┐   ┌──────────────┐       ┌──────────────┐    ┌──────────────┐
│  Part 1:     │   │  Part 2:     │       │  Part 3:     │    │  Part 4:     │
│ Fundamentals │   │ Query Proc.  │       │ Strategies   │    │ Context Const│
└──────────────┘   └──────────────┘       └──────────────┘    └──────────────┘
       │                   │                      │                   │
       └───────────────────┼──────────────────────┴───────────────────┘
                           ▼
             ┌────────────────────────────┐
             │      Part 5: Production    │
             ├────────────────────────────┤
             │      Part 6: Enterprise    │
             └────────────────────────────┘
```

---

## 🏛️ Part 1 — Retrieval Architecture Fundamentals

* **What is Retrieval Architecture?**
  * Retrieval Architecture is the end-to-end software architecture and data pipeline framework designed to fetch relevant external facts and context to augment language models. It forms the core of Retrieval-Augmented Generation (RAG).
  * Rather than relying solely on parametric knowledge embedded inside model weights, retrieval architecture provides non-parametric memory by connecting LLMs dynamically to vector databases, relational storage, full-text search indexes, and graph stores.
* **Why Retrieval Needs an Architecture**
  * **The Limits of Naive Similarity Search**: Vanilla Top-$K$ vector similarity search using cosine distance often fails in real-world applications due to keyword mismatches, embedding space noise, and semantic hallucination.
  * **The Trade-off Spectrum**: Retrieval systems must balance **Recall** (finding all relevant documents), **Precision** (ensuring retrieved documents contain minimal noise), **Latency** (delivering context in sub-100ms), and **Cost/Memory**.
  * **Enterprise Requirements**: Production deployment requires strict tenant data isolation, security access checks, metadata filtering, and high availability, which simple DB queries cannot supply.
* **Components of a Retrieval Layer**
  * **Ingestion & Indexing Pipeline**: Handles document extraction, chunking (fixed-size, semantic, sliding window), embedding calculation via dense bi-encoders, and index creation (HNSW, IVF-PQ, BM25 inversion).
  * **Query Processing & Transformation Unit**: Normalizes natural language queries, classifies search intent, extracts entity metadata, and expands queries into multi-vector search payloads.
  * **Multi-Modal Retrieval Engine**: Executes search operations across heterogeneous backends including dense vector databases (Pinecone, Qdrant, Milvus, pgvector), sparse lexical search engines (Elasticsearch, OpenSearch), and Graph DBs (Neo4j).
  * **Reranking & Selection Stage**: Uses compute-heavy cross-encoders or learning-to-rank algorithms to evaluate query-document relevance scores with high precision.
  * **Context Packaging & Synthesis Layer**: Formats, deduplicates, compresses, and orders chunks while building source attribution citations.
* **Request Lifecycle in Retrieval**
  1. **Ingest & Parse**: Query arrives from user interface with session metadata and authorization credentials.
  2. **Query Refinement**: The query is analyzed, rewritten, expanded, and converted into dense embeddings and sparse token vectors.
  3. **Parallel Execution**: Parallel asynchronous execution against multiple indexes (e.g., dense vector search + BM25 keyword search + metadata pre-filters).
  4. **Merge & Rescore**: Candidate result sets are aggregated, normalized (e.g., using Reciprocal Rank Fusion), and passed through a Neural Reranker.
  5. **Context Window Optimization**: Top-ranked passages undergo context compression and deduplication, and are assembled into a structured prompt with citations before being delivered to the LLM.

---

## 🧠 Part 2 — Query Processing

* **Query Understanding**
  * Raw user queries are frequently informal, incomplete, or syntactically messy. Query understanding analyzes syntactic structure, identifies entity types (people, products, dates), and models semantic relationships within the query.
  * Ensures the system understands *what* the user is asking before searching the underlying corpora.
* **Query Classification**
  * Routes queries into specific pipeline branches based on intent types:
    * **Factual / QA**: Short, direct answers requiring high-precision document lookup.
    * **Analytical / Summarization**: Broad queries requiring high-recall multi-document aggregation.
    * **Transactional / Action**: Requests targeting API calls, database updates, or function invocations.
    * **Navigational**: Seeking specific documents or explicit section titles.
* **Query Rewriting**
  * Conversational turns often contain ambiguous references (e.g., *"What was its revenue in Q3?"* where *"its"* refers to a previous turn).
  * **Coreference Resolution**: Replaces pronouns and context-dependent terms with explicit entities derived from conversation history.
  * **Sub-query Generation**: Decomposes complex multi-part questions into discrete, atomic sub-queries that can be retrieved independently.
* **Query Expansion**
  * Addresses the vocabulary mismatch problem (when the user's search words differ from the document text).
  * **Synonym & Phrase Expansion**: Augments queries with domain-specific jargon, abbreviations, and related terms.
  * **Hypothetical Document Embeddings (HyDE)**: Uses an LLM to generate a hypothetical answer snippet, which is then embedded to find real documents with similar semantic vector profiles.
* **Intent Detection**
  * Determines whether a query requires live web search, enterprise knowledge lookup, relational SQL queries, or internal knowledge generation.
  * Configures downstream parameters such as distance threshold, target index, and maximum candidates ($K$).
* **Metadata Extraction**
  * Converts implicit natural language constraints into explicit database filtering payloads.
  * *Example*: *"Show me Q3 financial reports for Acme Corp after 2023"* $\rightarrow$ Extracted Filters: `{"entity": "Acme Corp", "doc_type": "financial_report", "quarter": "Q3", "year": {"$gt": 2023}}`.

---

## 🏹 Part 3 — Retrieval Strategies

* **Lexical Search**
  * Uses inverted index data structures to match exact token occurrences.
  * **BM25 (Best Matching 25)**: Evaluates term frequency (TF), inverse document frequency (IDF), and document length normalization. Outstanding for searching proper nouns, product SKUs, code identifiers, and rare technical jargon.
* **Semantic Search**
  * Translates text into continuous vector representations via dense embedding models (e.g., `text-embedding-3-large`, `bge-large-en`).
  * Calculates spatial proximity using vector distance metrics (Cosine Similarity, Dot Product, Euclidean Distance). Captures semantic intent regardless of exact wording.
* **Hybrid Search**
  * Combines the high precision of lexical matching with the high semantic recall of dense vector search.
  * **Score Normalization**: Scales disparate score distributions (BM25 arbitrary scores vs cosine 0-1 values).
  * **Reciprocal Rank Fusion (RRF)**: Merges ranked lists using position rank values:
    $$RRF\_Score(d \in D) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
    where $r_m(d)$ is document $d$'s rank in retrieval method $m$, and $k$ is a constant (typically 60).
* **Graph Retrieval**
  * Uses Knowledge Graphs to capture structured relationships between entities ($Node \xrightarrow{Edge} Node$).
  * **GraphRAG**: Combines vector search with graph traversal. Solves global summarization and complex multi-entity reasoning queries by extracting subgraphs and community summaries.
* **Multi-stage Retrieval**
  * Employs a funnel architecture:
    * **Stage 1 (Coarse Retrieval)**: Fast, lightweight search over millions of items returning $K=100-500$ candidates (e.g., ANN vector search / BM25).
    * **Stage 2 (Fine Reranking)**: Heavy cross-encoder scoring over the top candidates to produce $K=5-15$ final passages.
* **Parent-Child Retrieval**
  * Decouples the **embedding text chunk** from the **context window payload**.
  * Documents are split into small leaf chunks (e.g., 100 tokens) for precise vector matching. When a leaf chunk matches, its larger parent container (e.g., 1000 tokens or full section) is returned to the LLM for rich context.
* **Metadata Filtering**
  * **Pre-filtering**: Filters vector index space prior to distance calculation (high accuracy, requires filtered indexing/HNSW support).
  * **Post-filtering**: Executes vector distance search first, then drops non-matching candidates (can result in fewer than $K$ final items if filters are restrictive).
* **Multi-hop Retrieval**
  * Designed for iterative reasoning tasks where answering a prompt requires chaining multiple factual steps.
  * The results of Hop 1 are evaluated and synthesized into a follow-up query to drive Hop 2 retrieval, collecting evidence across interconnected documents.

---

## 📦 Part 4 — Context Construction

* **Candidate Selection**
  * Merges candidate pools from multiple retrieval algorithms, removes invalid records, and applies dynamic score thresholds to prune low-relevance passages.
* **Reranking**
  * **Bi-Encoders vs Cross-Encoders**: Bi-encoders embed query and document separately (fast, scalable). Cross-encoders pass query and document jointly into self-attention layers ($[CLS] + Query + [SEP] + Document$), capturing complex term interactions at higher computational cost.
  * Models like Cohere Rerank or BGE-Reranker re-order candidate lists to maximize relevance density.
* **Context Compression**
  * Eliminates non-essential tokens from retrieved passages to streamline prompt length.
  * **Sentence Extraction**: Uses lightweight classifiers or LLMs to remove filler sentences and retain only key factual statements.
  * **Selective Context / LLMLingua**: Uses small language models to measure token perplexity and compress prompts by dropping predictable tokens without losing semantic meaning.
* **Deduplication**
  * Prevents wasting context window capacity on repetitive passages across multiple ingested sources.
  * **Exact Hashing**: MD5 / SHA-256 for identical strings.
  * **Near-Duplicate Detection**: MinHash, Locality-Sensitive Hashing (LSH), or high cosine similarity clustering ($> 0.95$) to drop redundant content.
* **Context Window Management**
  * **"Lost in the Middle" Mitigation**: Research shows LLMs attend most effectively to the start and end of prompt contexts. Context managers place the highest-scoring passages at the very top and bottom of the context block, placing lower-priority passages in the center.
  * **Token Allocation**: Dynamically balances token budgets between system prompts, retrieved context, conversation history, and user input.
* **Citation Building**
  * Maintains end-to-end metadata lineage for every chunk in the prompt.
  * Instructs the LLM to output inline footnotes (e.g., `[Doc 2, Page 14]`) linking directly back to verified document URIs and exact text spans for auditability.

---

## ⚙️ Part 5 — Production Retrieval

* **Caching**
  * **Exact Match Cache**: Key-value lookup (Redis) using SHA-256 hashes of input queries to instantly return historical context payloads.
  * **Semantic Cache**: Measures vector distance between incoming query and cached historical queries (e.g., GPTCache). If distance $< \epsilon$, serves cached retrieval results, saving database lookups and latency.
* **Retrieval Monitoring**
  * **Offline Metrics**:
    * **Precision@K**: Fraction of top-$K$ retrieved items that are relevant.
    * **Recall@K**: Fraction of all relevant items retrieved in top-$K$.
    * **MRR (Mean Reciprocal Rank)**: Evaluates position of the first relevant result.
    * **NDCG (Normalized Discounted Cumulative Gain)**: Measures ranking quality with position-based decay.
  * **Online Metrics**: Retrieval latency (p50, p95, p99), embedding generation latency, cache hit ratios, and user conversion/thumbs feedback.
* **Index Updates**
  * Managing index rebuilds and updates without impacting read traffic.
  * **Blue/Green Index Deployment**: Builds new vector/BM25 indexes in shadow environments before swapping read aliases seamlessly.
  * **Write-Ahead Logging (WAL)**: Buffers real-time updates in memory before flushing to persistent disk indexes.
* **Incremental Indexing**
  * Continuous data ingestion using event-driven architectures (Kafka, Debezium CDC). Updates, inserts, or deletes individual vector embeddings and inverted index entries in near real-time as source files change.
* **Failure Handling**
  * **Graceful Degradation**: Fallback paths when vector databases experience latency spikes or downtime (e.g., vector search timeout $\rightarrow$ fallback to BM25 keyword search $\rightarrow$ fallback to parametric LLM knowledge).
  * **Circuit Breakers & Retries**: Prevents cascading failures across retrieval microservices.
* **Multi-tenant Retrieval**
  * **Data Isolation**: Enforces tenant-level data segregation to prevent cross-tenant data leaks.
  * **Partition Strategies**: Soft multi-tenancy (metadata filtering per tenant ID in a shared index) vs Hard multi-tenancy (dedicated vector collections or separate database instances per tenant).

---

## 🏢 Part 6 — Enterprise Retrieval

* **Enterprise Knowledge Bases**
  * Ingesting heterogeneous corporate data silos (Confluence, SharePoint, JIRA, Google Drive, Salesforce, S3, SQL DBs).
  * Requires robust document parsers (handling PDFs, complex tables, slides, embedded images) and metadata normalization.
* **Distributed Retrieval**
  * Partitioning and scaling retrieval infrastructure across massive datasets.
  * **Sharding**: Distributing vector collections across nodes by document ID or tenant ID.
  * **ANN Algorithms at Scale**: Hierarchical Navigable Small World (HNSW) graphs, Inverted File with Product Quantization (IVF-PQ) for RAM reduction, and GPU-accelerated vector search (FAISS, cuVS).
* **Retrieval Security**
  * **Access Control Enforcement**: Integrating Access Control Lists (ACLs), Role-Based Access Control (RBAC), and Attribute-Based Access Control (ABAC).
  * **Document-Level Security (DLS)**: Truncating retrieval result sets dynamically based on user security tokens extracted from identity providers (e.g., OAuth/Okta tokens mapped to document permission vectors).
* **Hybrid Enterprise Search**
  * Unifying legacy enterprise search systems (OpenSearch, Elasticsearch, Solr) with next-generation neural vector engines via middleware API gateways.
* **Cross-Repository Retrieval**
  * Search federation across multiple distinct search engines simultaneously.
  * Merges disparate schemas, normalizes heterogeneous relevance scores, and presents a single unified context payload to the model interface.
