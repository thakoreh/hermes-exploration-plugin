---
id: cohere
name: Cohere
description: Enterprise AI platform with command models, embeddings, and Rerank. Known for excellent retrieval and multilingual support.
category: llm-api
url: https://cohere.com
pricing: freemium
alternatives: [openai-api, anthropic-api, voyage-ai]
quality_score: 8.8
discovery_context: Needed embeddings with better multilingual support for international RAG
discovered_by: hermes-mlops
discovered_at: 2026-04-26
last_verified: 2026-04-26
integration_notes: |
  Best for: RAG, embeddings, reranking, multilingual applications.
  Embeddings-v3 supports 100+ languages.
flags: [has-api, has-free-tier, has-embeddings, has-rerank]
---

## Overview

Cohere provides enterprise AI building blocks: command models for generation, embeddings for retrieval, and Rerank for improved search quality. Their embedding models excel at multilingual understanding.

## Key Features

- Command: instruction-following chat model
- Embeddings-v3: 1024/1024 dimensions, 100+ languages
- Rerank-3: improved search result ranking
- Chat API with citations
- Playground and evals dashboard
- Python, Node, Go SDKs

## Pricing

Free tier: trial credits
Command: $0.15/million input tokens
Embeddings: $0.05/million tokens
Rerank: $0.05/1000 calls

## How to Use

```bash
pip install cohere
```

```python
import cohere
co = cohere.Client("YOUR_KEY")

# Embeddings
embeddings = co.embed(
    texts=["Hello world"],
    model="embed-english-v3.0"
).embeddings

# Rerank
results = co.rerank(
    query="What is AI?",
    documents=["Doc 1", "Doc 2"],
    model="rerank-english-v3.0"
)
```

## Notes

Rerank is underrated for improving search quality. Combined with embeddings, it forms a powerful retrieval pipeline.
