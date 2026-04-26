---
id: qdrant
name: Qdrant
description: Open-source vector database for similarity search. High-performance, filtering support, and easy deployment.
category: vector-db
url: https://qdrant.tech
pricing: free
alternatives: [pinecone, weaviate, milvus, chroma]
quality_score: 8.9
discovery_context: Needed a self-hostable vector database for RAG with good filtering support
discovered_by: hermes-mlops
discovered_at: 2026-04-26
last_verified: 2026-04-26
integration_notes: |
  Best for: RAG pipelines, semantic search, recommendation systems.
  Deploy self-hosted or use Qdrant Cloud (free tier available).
flags: [open-source, has-api, has-free-tier, self-hostable]
---

## Overview

Qdrant is an open-source vector database designed for high-performance similarity search. It excels at RAG (Retrieval-Augmented Generation) applications, offering precise filtering, fast ANN search, and easy deployment options.

## Key Features

- HNSW and FLAT indexing algorithms
- Payload filtering with JSON conditions
- Sparse and dense vector support
- Multi-tenancy with named vectors
- Distributed deployment support
- Python, Rust, Go clients

## Pricing

Free: self-hosted (open source)
Cloud: free tier with 1GB storage, paid plans from $25/mo

## How to Use

```bash
pip install qdrant-client
```

```python
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")

# Search
results = client.search(
    collection_name="my_collection",
    query_vector=[0.1, 0.2, 0.3],
    limit=5
)
```

## Notes

Filtering support is superior to many alternatives. The JSON payload filtering is intuitive and powerful for metadata-aware search.
