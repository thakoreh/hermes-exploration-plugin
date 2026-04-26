---
id: voyage-ai
name: Voyage AI
description: State-of-the-art embeddings for semantic search and RAG. Voyage AI offers models that outperform OpenAI and Cohere on benchmarks.
category: llm-api
url: https://voyageai.com
pricing: freemium
alternatives: [openai-api, cohere, jina]
quality_score: 9.0
discovery_context: Needed best-in-class embeddings for RAG accuracy benchmarks
discovered_by: hermes-mlops
discovered_at: 2026-04-26
last_verified: 2026-04-26
integration_notes: |
  Best for: RAG, semantic search, code search.
  voyage-code-2 is top for code embeddings.
flags: [has-api, has-free-tier, has-embeddings]
---

## Overview

Voyage AI provides state-of-the-art embedding models that consistently outperform OpenAI and Cohere on MTEB benchmarks. Their models are optimized for semantic search, code search, and RAG applications.

## Key Features

- voyage-law-2: legal document embedding (state-of-the-art)
- voyage-code-2: code embedding (top on CodeSearchNet)
- voyage-2: general purpose, 1024 dimensions
- voyage-lite-2: lighter, faster, 256 dimensions
- Multilingual model available

## Pricing

Free: 1M tokens/month
Pay: $0.00012/token (very competitive)

## How to Use

```bash
pip install voyageai
```

```python
import voyageai
vo = voyageai.Client(api_key="YOUR_KEY")

# Embeddings
result = vo.embed(
    texts=["Hello world", "Goodbye world"],
    model="voyage-2"
)
print(result.embeddings)
```

## Notes

The CodeSearchNet benchmark win makes voyage-code-2 the go-to for code search. General voyage-2 beats OpenAI ada on MTEB at similar cost.
