# Hybrid Search Project - Phase 1: Ingestion Pipeline

## Overview

The objective of Phase 1 was to build a **production-style Hybrid Search ingestion pipeline** capable of storing both dense and sparse vectors inside Qdrant.

Instead of creating a simple proof-of-concept, the project follows Clean Architecture principles, making every component independently testable and replaceable.

The final pipeline looks like:

```text
Markdown File
      │
      ▼
Markdown Loader
      │
      ▼
Document
      │
      ▼
Recursive Chunker
      │
      ▼
Chunks
      │
      ▼
Dense Embedder
      │
      ▼
Sparse Embedder
      │
      ▼
Point Builder
      │
      ▼
Point Repository
      │
      ▼
Qdrant Hybrid Collection
```

---

# Project Structure

```text
project/
│
├── api/
├── core/
├── exceptions/
├── ingestion/
│   ├── builders/
│   ├── chunkers/
│   ├── embedders/
│   ├── interfaces/
│   ├── loaders/
│   └── services/
│
├── repositories/
│   ├── interfaces/
│   └── qdrant/
│
├── schemas/
├── scripts/
├── tests/
└── requirements.txt
```

---

# End-to-End Flow

```text
Markdown File
        │
        ▼
MarkdownLoader
        │
        ▼
Document
        │
        ▼
RecursiveChunker
        │
        ▼
Chunk[]
        │
        ▼
PointBuilder
    ┌───────┴────────┐
    ▼                ▼
Dense Embedder   Sparse Embedder
    │                │
    └───────┬────────┘
            ▼
      HybridPoint[]
            │
            ▼
QdrantPointRepository
            │
            ▼
Qdrant Hybrid Collection
```

---

# Components

## 1. Configuration (`core/`)

### Purpose

Centralized configuration management using environment variables.

### Configuration Includes

* Qdrant Host
* Qdrant Port
* Collection Name
* Dense Model
* Sparse Model
* Chunk Size
* Chunk Overlap
* Batch Size
* Dense Vector Dimension

### Why?

Avoids hardcoded values and makes switching environments easier.

---

## 2. Dependency Container

### Purpose

Creates all shared dependencies once.

Responsibilities:

* Load configuration
* Create AsyncQdrantClient
* Create repositories
* Create embedders
* Create chunker
* Create loader
* Create ingestion service

### Why Dependency Injection?

Instead of every class creating its own dependencies:

```text
Bad

Repository
      │
Creates Client
```

We used:

```text
Container
      │
Creates Client
      │
Injects
      │
Repository
```

Benefits:

* Easier testing
* Better maintainability
* Loose coupling

---

## 3. Markdown Loader

### Input

```text
README.md
```

### Output

```python
Document
```

Responsibilities:

* Read markdown asynchronously
* Validate file
* Generate document id
* Create Document object

### Why?

Keeps file I/O isolated from business logic.

---

## 4. Recursive Chunker

Input:

```python
Document
```

Output:

```python
list[Chunk]
```

Uses:

* RecursiveCharacterTextSplitter

Configuration:

* chunk_size
* chunk_overlap

Each chunk contains:

* chunk_id
* chunk_index
* document_id
* source
* text
* metadata

### Why Recursive Chunking?

Compared with fixed-size chunking:

* Preserves paragraphs
* Produces more meaningful chunks
* Better retrieval quality

---

## 5. Dense Embedder

Implementation:

Sentence Transformers

Model:

```
all-MiniLM-L6-v2
```

Output:

```python
list[float]
```

Dimension:

```
384
```

### Why this model?

Advantages:

* Fast inference
* Small model
* Excellent semantic performance
* Ideal for RAG applications

### Important Decision

Model loaded once during startup.

Not:

```python
embed()

↓

Load Model

↓

Encode
```

Instead:

```text
Startup

↓

Load Model

↓

Reuse
```

---

## 6. Sparse Embedder

Implementation:

FastEmbed

Model:

```
Qdrant/bm25
```

Output:

```python
indices

values
```

Example:

```python
indices=[4,19,27]

values=[1.3,0.9,2.1]
```

### Why Sparse Embeddings?

Dense embeddings capture meaning.

Sparse embeddings preserve exact keywords.

Together they enable Hybrid Search.

---

## 7. Point Builder

Input:

```python
Chunk
```

Output:

```python
HybridPoint
```

Responsibilities:

* Generate dense embeddings
* Generate sparse embeddings
* Build payload
* Create domain model

### Important Design Decision

Dense and sparse embeddings are generated concurrently using:

```python
asyncio.gather()
```

instead of sequential execution.

---

## 8. Batch Embedding

Instead of

```text
100 chunks

↓

100 Dense Calls
```

we used

```text
100 Chunks

↓

embed_batch()

↓

1 Dense Call
```

Same for sparse embeddings.

Benefits:

* Faster inference
* Lower overhead
* Better CPU utilization

---

## 9. Point Repository

Responsibilities:

* Convert HybridPoint
* Build PointStruct
* Create SparseVector
* Upload batches

Uses:

```python
client.upsert()
```

Batch Upload:

```
100 points
```

(configurable)

---

## 10. Collection Repository

Responsibilities:

* Verify connection
* Check collection existence
* Create collection
* Delete collection

Collection schema:

```text
Collection

├── Dense Vector

│      384 dimensions

│      Cosine Similarity

│

└── Sparse Vector
```

Collection creation is **idempotent**.

Running the ingestion pipeline multiple times does not recreate the collection.

---

## 11. Ingestion Service

Acts as the orchestration layer.

Responsibilities:

```text
Load File

↓

Chunk

↓

Generate Embeddings

↓

Create Points

↓

Upload
```

Notice:

It contains **no embedding logic** and **no Qdrant logic**.

It only coordinates components.

---

# Qdrant Design

Each point stores:

```text
Point

│

├── Dense Vector

├── Sparse Vector

└── Payload
```

Dense and sparse vectors are stored in the **same point**.

### Why?

Advantages:

* No duplicated payload
* Lower storage requirements
* Easier retrieval
* Better consistency
* Single point id

Instead of

```text
Dense Point

Sparse Point
```

we use

```text
One Point

↓

Dense

+

Sparse
```

---

# Important Architectural Decisions

## Clean Architecture

Separated into:

* Loader
* Chunker
* Embedder
* Builder
* Repository
* Service

Each class has one responsibility.

---

## Repository Pattern

Repositories hide Qdrant implementation details.

Service layer never communicates directly with Qdrant.

---

## Dependency Injection

All dependencies are created once inside the container.

Benefits:

* Easier testing
* Loose coupling
* Shared instances

---

## Batch Processing

Instead of loading every chunk into memory at once:

```text
1000 Chunks

↓

100

↓

Upload

↓

Next 100
```

Memory usage remains nearly constant.

---

## Async First

Used:

* Async Qdrant Client
* aiofiles
* asyncio.gather()
* asyncio.to_thread()

This keeps the application scalable while integrating synchronous ML libraries.

---

# Technologies Used

* Python 3.12+
* Qdrant
* Sentence Transformers
* FastEmbed
* LangChain Text Splitters
* Pydantic
* aiofiles
* Loguru
* Docker

---

# What We Learned

* Clean Architecture for AI systems
* Repository Pattern
* Dependency Injection
* Async programming
* Hybrid Search ingestion
* Dense embeddings
* Sparse embeddings
* Batch embedding
* Batch upload
* Qdrant named vectors
* Payload design
* Production folder structure

---

# Production Improvements Applied

* Batch embedding
* Batch upload
* Idempotent collection creation
* Dependency Injection
* Environment-based configuration
* Custom exceptions
* Structured logging
* Interface-based design
* Async-first architecture

---

# Final Result

Successfully built a complete Hybrid Search ingestion pipeline capable of:

* Reading Markdown files
* Splitting documents into chunks
* Generating dense embeddings
* Generating sparse embeddings
* Creating hybrid Qdrant points
* Uploading points in batches
* Storing dense and sparse vectors inside the same Qdrant point

The pipeline processed the sample markdown document, generated **24 chunks**, and successfully uploaded them into the Qdrant Hybrid Collection.

---

# Next Phase

Phase 2 will focus on **Hybrid Retrieval**, where we will implement:

```text
User Query
      │
      ▼
Dense Query Embedding
      │
      ▼
Sparse Query Embedding
      │
      ▼
Dense Search
      +
Sparse Search
      │
      ▼
Reciprocal Rank Fusion (RRF)
      │
      ▼
Top-K Hybrid Results
```
