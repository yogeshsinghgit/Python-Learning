# Production-Ready PDF RAG – Ingestion Module

## Overview

This module implements a **production-ready document ingestion pipeline** for a PDF-based Retrieval-Augmented Generation (RAG) system.

Unlike tutorial implementations that directly split PDF text and generate embeddings, this architecture is designed around **clean architecture**, **domain-driven models**, and **replaceable components**, allowing the ingestion pipeline to evolve without affecting downstream retrieval or generation.

---

# Architecture

```text
                           PDF
                            │
                            ▼
                 DocumentLoader (Unstructured)
                            │
                            ▼
                     Document Domain Model
                            │
                            ▼
                DocumentPreprocessor
                            │
                            ▼
              SemanticElementChunker
                            │
                            ▼
                TokenAwareChunker
                            │
                            ▼
                   TokenSplitter
                            │
                            ▼
                    ChunkMapper
                            │
                            ▼
                         Chunk[]
                            │
                            ▼
                  ChunkEnricher
                            │
                            ▼
                VectorDocumentBuilder
                            │
                            ▼
                    VectorDocument[]
                            │
                            ▼
                 PineconeRepository
                            │
                            ▼
                    Pinecone Vector DB
```

---

# High-Level Pipeline

```text
PDF
 │
 ▼
Document Loader
 │
 ▼
Document Preprocessing
 │
 ▼
Semantic Chunking
 │
 ▼
Token-aware Splitting
 │
 ▼
Chunk Enrichment
 │
 ▼
Dense + Sparse Embeddings
 │
 ▼
VectorDocument Creation
 │
 ▼
Batch Upsert
 │
 ▼
Pinecone
```

---

# Project Structure

```text
app/

├── core/
│   ├── config.py
│   ├── logging.py
│   ├── constants.py
│   └── exceptions.py
│
├── infrastructure/
│
│   ├── vector_db/
│   │
│   ├── embeddings/
│   │
│   └── ...
│
├── rag_services/
│
│   └── ingestion/
│
│       ├── chunkers/
│       ├── enrichers/
│       ├── interfaces/
│       ├── loaders/
│       ├── mappers/
│       ├── models/
│       ├── pipeline/
│       ├── preprocessors/
│       ├── splitters/
│       └── tokenizers/
│
└── schemas/
```

---

# Production Features Implemented

## 1. Parser Abstraction

Implemented:

* `DocumentLoader` interface
* `UnstructuredDocumentLoader`

The application never depends directly on Unstructured classes.

Benefits:

* Parser can be replaced with:

  * Docling
  * LlamaParse
  * OCR pipeline
  * Custom parser

without changing the rest of the application.

---

## 2. Domain Models

Implemented:

* Document
* DocumentMetadata
* DocumentElement
* DocumentElementType

The ingestion pipeline operates only on domain models.

No third-party SDK objects propagate beyond the loader.

---

## 3. Strongly Typed Document Metadata

Captured metadata includes:

* filename
* parser
* parser_version (future-ready)
* mime_type
* page_count
* checksum
* file_size
* languages
* ingested_at
* extra_metadata

This supports:

* document tracking
* observability
* deduplication
* future audit requirements

---

## 4. SHA-256 Checksum

Each document is assigned a checksum during ingestion.

Production use cases:

* duplicate detection
* incremental ingestion
* version comparison
* cache lookup

---

## 5. Document Preprocessing

Implemented as a dedicated stage.

Responsibilities:

* whitespace normalization
* newline normalization
* remove empty elements
* preserve semantic structure

The loader preserves the original document while preprocessing prepares it for chunking.

---

## 6. Semantic Chunking

Implemented:

* `SemanticElementChunker`

Instead of splitting raw text, chunk boundaries are determined using semantic document elements.

Examples:

* Title
* NarrativeText
* Table
* ListItem
* Header
* Footer
* Image

Advantages:

* preserves document hierarchy
* improves retrieval quality
* avoids arbitrary character-based splits

---

## 7. Token-Aware Chunking

Implemented:

* `TokenAwareChunker`

Responsibilities:

* wraps another chunker
* counts tokens
* validates token limits
* delegates oversized chunks to a splitter

The chunker itself contains no splitting logic.

---

## 8. Token Splitter

Implemented:

* `BaseSplitter`
* `TokenSplitter`

Algorithm:

* fixed token window
* configurable overlap
* preserves metadata
* creates new chunks through `ChunkMapper`

Advantages:

* reusable
* configurable
* independent of chunking strategy

---

## 9. Chunk Mapping

Implemented:

* `ChunkMapper`

Responsibilities:

* build chunks from document elements
* build chunks from existing chunks after splitting

Benefits:

* centralized chunk construction
* consistent metadata
* reusable across chunking strategies

---

## 10. Chunk Enrichment

Implemented:

* `ChunkEnricher`
* `DefaultChunkEnricher`

Each chunk contains:

* original `text`
* `indexed_text`

The embedding pipeline uses:

```python
chunk.indexed_text or chunk.text
```

This allows future retrieval improvements without modifying the original chunk.

Future enrichers:

* Contextual Retrieval
* Summary generation
* Keyword enrichment
* HyDE
* Multi-vector retrieval

---

## 11. Tokenization Abstraction

Implemented:

* `TokenCounter`
* `TiktokenTokenCounter`

The ingestion pipeline is not coupled to any tokenizer implementation.

Future implementations can be added without changing the pipeline.

---

## 12. Vector Document Builder

Implemented:

* `VectorDocumentBuilder`

Responsibilities:

* generate dense embeddings
* generate sparse embeddings
* run embedding generation concurrently
* create `VectorDocument`
* return domain models only

The rest of the application never interacts with embedding SDKs directly.

---

## 13. Repository Pattern

Implemented:

* `VectorRepository`
* `PineconeRepository`

Features:

* batch upsert
* fetch
* query
* delete
* delete all
* create index
* describe index
* list indexes

Repository returns domain models rather than Pinecone SDK objects.

---

## 14. Batch Processing

Vector documents are persisted using batch upsert.

Benefits:

* lower network overhead
* improved throughput
* production scalability

---

## 15. Async-First Design

The ingestion pipeline is fully asynchronous.

Heavy synchronous operations (such as document parsing) are executed using background threads to avoid blocking the event loop.

---

## 16. Clean Architecture

Responsibilities are clearly separated.

```text
Loader
    │
    ▼
Preprocessor
    │
    ▼
Chunker
    │
    ▼
Splitter
    │
    ▼
Mapper
    │
    ▼
Enricher
    │
    ▼
Vector Builder
    │
    ▼
Repository
```

Every component has a single responsibility.

---

## 17. Dependency Injection

The ingestion pipeline depends on abstractions rather than implementations.

Example:

* DocumentLoader
* Chunker
* ChunkEnricher
* TokenCounter
* VectorRepository

This enables easy testing and replacement of implementations.

---

## 18. Production Logging

Every stage logs:

* document loading
* preprocessing
* chunk generation
* token splitting
* embedding generation
* vector persistence

Structured logging enables easier debugging and observability.

---

# Current Ingestion Pipeline

```text
PDF
 │
 ▼
UnstructuredDocumentLoader
 │
 ▼
Document
 │
 ▼
DocumentPreprocessor
 │
 ▼
SemanticElementChunker
 │
 ▼
TokenAwareChunker
 │
 ▼
TokenSplitter
 │
 ▼
ChunkMapper
 │
 ▼
Chunk[]
 │
 ▼
ChunkEnricher
 │
 ▼
Chunk(indexed_text)
 │
 ▼
VectorDocumentBuilder
 │
 ▼
VectorDocument[]
 │
 ▼
PineconeRepository
 │
 ▼
Pinecone Index
```

---

# Next Module

The ingestion layer is now functionally complete.

The next major module is the **Retrieval Pipeline**, which will include:

* Query preprocessing
* Query embeddings
* Hybrid retrieval
* Reciprocal Rank Fusion (RRF)
* Metadata filtering
* Reranking
* Context building
* Prompt assembly
* LLM response generation
* Streaming responses
