---
id: jina
name: Jina AI
description: Reader API turns any URL into clean LLM-friendly text. Also provides top-tier embeddings and a Reranker API.
category: search
url: https://jina.ai
pricing: freemium
alternatives: [tavily, firecrawl]
quality_score: 8.5
discovery_context: "Needed to extract article text from news sites for a summarization pipeline"
discovered_by: hermes-content
discovered_at: 2026-04-05
last_verified: 2026-04-24
integration_notes: |
  Reader: GET https://r.jina.ai/https://URL
  Embeddings: https://api.jina.ai/v1/embeddings
  Free: 200K tokens/day for embeddings, 1000 reader calls/month
flags: [has-api, has-free-tier, open-source, supports-streaming]
---

## Overview

Jina AI provides two essential APIs for AI developers: a Reader that extracts clean text from any URL, and embedding models that compete with OpenAI at a fraction of the cost.

## Key Features

- **Reader API**: `GET r.jina.ai/{url}` → returns clean markdown
- **Embeddings**: jina-embeddings-v3 (1024 dimensions, 8192 context)
- **Reranker**: Improve search relevance with cross-encoder reranking
- Open-source embedding models on HuggingFace

## Pricing

Free: 200K tokens/day embeddings, 1000 reader calls/month
Pay-as-you-go: $0.004/1K input tokens for embeddings
