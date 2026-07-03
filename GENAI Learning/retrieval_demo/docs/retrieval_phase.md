# Hybrid Retrieval Pipeline Documentation

## Overview

The Retrieval Phase is responsible for finding the most relevant document chunks from the Qdrant vector database for a given user query.

This phase reuses the dense and sparse embedding models from the ingestion pipeline, performs independent dense and sparse retrieval, and combines the ranked results using **Reciprocal Rank Fusion (RRF)**.

Unlike the ingestion pipeline, this phase is completely read-only and focuses on efficient document retrieval.

---

# Objectives

The retrieval pipeline is designed to:

* Generate dense and sparse query embeddings.
* Perform semantic and keyword-based retrieval.
* Combine results using Reciprocal Rank Fusion (RRF).
* Return the most relevant document chunks.
* Keep retrieval independent from the LLM generation phase.

---

# Retrieval Architecture

```text
                         User Query
                              │
                              ▼
                     Retrieval Service
              ┌───────────────┼───────────────┐
              ▼                               ▼
      Dense Embedder                  Sparse Embedder
              │                               │
              ▼                               ▼
      Dense Query Vector             Sparse Query Vector
              │                               │
              ▼                               ▼
         Dense Search                  Sparse Search
              │                               │
              └───────────────┬───────────────┘
                              ▼
                    Reciprocal Rank Fusion
                              │
                              ▼
                 Top-K Retrieved Chunks
```

---

# Folder Structure

```text
project/
│
├── retrieval/
│   ├── models/
│   │   ├── retrieved_chunk.py
│   │   └── search_query.py
│   │
│   └── services/
│       ├── retrieval_service.py
│       └── rrf_service.py
│
├── repositories/
│   ├── interfaces/
│   │   └── search_repository.py
│   │
│   └── qdrant/
│       └── qdrant_search_repository.py
│
├── scripts/
│   └── retrieval_demo.py
```

---

# Component Responsibilities

## SearchQuery

Represents a search request passed to the repository.

Fields:

* Dense query vector
* Sparse query vector
* Top-K
* Score threshold
* Metadata filter

Purpose:

Provides a single request model for all repository search operations.

---

## RetrievedChunk

Represents a retrieved document chunk.

Fields:

* Chunk ID
* Chunk content
* Search score
* RRF score
* Metadata

Purpose:

Acts as the domain model shared across the retrieval pipeline while hiding Qdrant-specific models.

---

## SearchRepository

Defines the contract for all vector database search operations.

Responsibilities:

* Dense Search
* Sparse Search

The interface is independent of any vector database implementation.

---

## QdrantSearchRepository

Concrete implementation of the SearchRepository.

Responsibilities:

* Execute dense vector search.
* Execute sparse vector search.
* Call Qdrant using `query_points()`.
* Map Qdrant `ScoredPoint` objects into `RetrievedChunk`.

This class contains all Qdrant-specific logic.

---

## RetrievalService

Coordinates the entire retrieval workflow.

Responsibilities:

1. Accept user query.
2. Generate dense embedding.
3. Generate sparse embedding.
4. Execute dense retrieval.
5. Execute sparse retrieval.
6. Fuse results using RRF.
7. Return ranked chunks.

Business logic is implemented here rather than inside the repository.

---

## RRFService

Implements Reciprocal Rank Fusion.

Responsibilities:

* Merge dense and sparse rankings.
* Deduplicate retrieved chunks.
* Compute RRF scores.
* Produce the final ranked list.

This service is completely independent of Qdrant.

---

# Retrieval Flow

## Step 1

User submits a query.

Example:

```text
What is OAuth2 authentication?
```

---

## Step 2

Generate dense embedding.

Produces a dense vector used for semantic retrieval.

---

## Step 3

Generate sparse embedding.

Produces a sparse vector used for keyword-based retrieval.

---

## Step 4

Execute dense search.

Qdrant searches the dense vector index and returns the top-K semantically similar chunks.

---

## Step 5

Execute sparse search.

Qdrant searches the sparse vector index and returns the top-K keyword-relevant chunks.

---

## Step 6

Apply Reciprocal Rank Fusion (RRF).

The dense and sparse rankings are merged using their ranking positions instead of raw similarity scores.

---

## Step 7

Return the final ranked chunks.

These chunks become the context for the next phase of the RAG pipeline.

---

# Why Use Manual RRF?

Instead of relying on Qdrant's built-in FusionQuery, this project implements RRF manually.

Reasons:

* Better understanding of the algorithm.
* Easier debugging.
* Database-independent implementation.
* Greater flexibility for future ranking strategies.
* Valuable for interview preparation.

Future versions of the project may replace manual RRF with server-side fusion for improved performance.

---

# Why Dense and Sparse Retrieval?

Dense retrieval:

* Captures semantic meaning.
* Handles synonyms and paraphrases.
* Best for natural language questions.

Sparse retrieval:

* Preserves exact keywords.
* Performs well for technical documentation.
* Useful for API names, version numbers, identifiers, and code.

Hybrid retrieval combines the strengths of both approaches.

---

# Why Use Reciprocal Rank Fusion?

Dense and sparse retrieval produce scores on different scales.

Example:

Dense Search:

```text
0.92
0.88
0.81
```

Sparse Search:

```text
12.5
8.7
5.4
```

These scores cannot be directly compared.

RRF ignores raw similarity scores and instead combines ranking positions, resulting in a more robust and consistent final ranking.

---

# Design Decisions

## Async-First Design

Embedding generation and retrieval are executed concurrently using `asyncio.gather()` to reduce overall latency.

---

## Repository Pattern

The Retrieval Service depends on the SearchRepository abstraction rather than Qdrant directly.

Benefits:

* Easier testing.
* Better maintainability.
* Supports future database replacement.

---

## Dependency Injection

All dependencies are injected into the Retrieval Service.

Benefits:

* Loose coupling.
* Improved testability.
* Clear separation of responsibilities.

---

## Domain Models

Qdrant-specific models remain inside the repository layer.

The rest of the application works only with `RetrievedChunk`.

---

# Logging Strategy

Loguru is used throughout the retrieval pipeline.

Important log points include:

* Retrieval started.
* Dense search started and completed.
* Sparse search started and completed.
* Number of retrieved chunks.
* RRF completed.
* Exceptions and failures.

---

# Error Handling

The repository catches infrastructure-specific exceptions and raises application-level exceptions.

Benefits:

* Prevents leaking Qdrant implementation details.
* Keeps business logic independent of infrastructure.
* Provides consistent error handling.

---

# Performance Considerations

Current implementation:

* Dense retrieval
* Sparse retrieval
* Manual RRF

Performance optimizations:

* Asynchronous execution.
* Parallel embedding generation.
* Parallel search execution.
* `with_vectors=False` to reduce response size.
* Top-K retrieval to minimize data transfer.

---

# Future Improvements

Potential enhancements include:

* Server-side FusionQuery using Qdrant.
* Metadata filtering.
* Query rewriting.
* Query expansion.
* Re-ranking using Cross Encoders.
* Parent document retrieval.
* Context compression.
* Retrieval evaluation metrics.
* Caching frequently executed queries.

---

# Lessons Learned

During the implementation of the retrieval pipeline:

* Dense and sparse embeddings complement each other.
* Repository Pattern simplifies infrastructure changes.
* RRF provides a reliable hybrid ranking mechanism.
* Async execution significantly reduces retrieval latency.
* Separating retrieval from generation leads to a cleaner RAG architecture.

---

# Completion Checklist

* ✅ Retrieval architecture designed.
* ✅ SearchRepository interface created.
* ✅ QdrantSearchRepository implemented.
* ✅ Dense search implemented.
* ✅ Sparse search implemented.
* ✅ Manual Reciprocal Rank Fusion implemented.
* ✅ RetrievalService implemented.
* ✅ End-to-end retrieval pipeline verified.
* ✅ Hybrid retrieval demo completed.

---