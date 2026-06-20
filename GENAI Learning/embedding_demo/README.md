# Embeddings and Cosine Similarity - Revision Notes

## Objective

The purpose of this project is to understand how semantic search works using embeddings.

Instead of searching documents based on exact keyword matches, we search based on meaning.

---

## Problem Statement

Consider the following document:

* Redis is an in-memory database

Now a user asks:

* Which database stores data in memory?

The query does not contain the exact phrase "in-memory database", but both texts have the same meaning.

Traditional keyword search may struggle with this.

Embeddings solve this problem.

---

# What Are Embeddings?

An embedding is a numerical representation of text.

The embedding model converts text into a vector of numbers.

Example:

Text:

* FastAPI is a Python web framework

Embedding:

* [0.12, -0.45, 0.78, ...]

The numbers themselves are not important to humans.

What matters is that texts with similar meanings generate vectors that are close to each other.

---

# Documents Used

The project contains four documents:

1. FastAPI is a Python web framework
2. Redis is an in-memory database
3. PostgreSQL is a relational database
4. MongoDB is a NoSQL document database

Each document is converted into an embedding vector.

---

# Query Flow

When a user enters a query:

Example:

* Which database stores data in memory?

The system performs the following steps:

1. Convert the query into an embedding.
2. Compare the query embedding against every document embedding.
3. Calculate a similarity score.
4. Return the document with the highest score.

---

# What Is Cosine Similarity?

Cosine similarity is a mathematical technique used to measure how similar two vectors are.

The output ranges from:

* 1.0 → Extremely similar
* 0.8 → Very similar
* 0.5 → Somewhat related
* 0.0 → Unrelated
* -1.0 → Opposite direction

Higher score means higher semantic similarity.

---

# Why Does Cosine Similarity Work?

Cosine similarity compares the direction of vectors rather than their actual values.

Example:

Query:

* Which database stores data in memory?

Document:

* Redis is an in-memory database

Although the wording is different, both sentences describe the same concept.

Because the embedding model understands the meaning, both vectors are placed close together in vector space.

As a result, cosine similarity returns a high score.

---

# Example Queries and Expected Results

## Query 1

Input:

* Which database stores data in memory?

Expected Result:

* Redis is an in-memory database

Reason:

The query is asking about an in-memory database, which is exactly what Redis is.

---

## Query 2

Input:

* Where can I store relational data?

Expected Result:

* PostgreSQL is a relational database

Reason:

The query refers to relational data, which matches PostgreSQL.

---

## Query 3

Input:

* Python API framework

Expected Result:

* FastAPI is a Python web framework

Reason:

The query and document describe the same technology category.

---

## Query 4

Input:

* Document oriented database

Expected Result:

* MongoDB is a NoSQL document database

Reason:

MongoDB is commonly used as a document-oriented database.

---

# Key Learning

This project demonstrates that:

* AI search is based on meaning, not exact keywords.
* Text can be converted into vectors.
* Similar meanings produce similar vectors.
* Cosine similarity helps find the most relevant document.
* This is the foundation of Semantic Search, RAG Systems, AI Assistants, and Vector Databases.

---

# Limitation of Current Approach

The current implementation compares the query against every document.

Example:

100 documents
→ 100 comparisons

1,000 documents
→ 1,000 comparisons

1,000,000 documents
→ 1,000,000 comparisons

As the number of documents increases, search becomes slower and more expensive.

This problem leads to the next topic:

**Vector Databases**, which are designed to perform similarity search efficiently at large scale.
