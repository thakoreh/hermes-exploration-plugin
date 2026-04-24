---
id: tavily
name: Tavily AI
description: Search API specifically designed for AI agents. Returns clean, relevant results without the SEO noise that clogs up AI responses.
category: search
url: https://tavily.com
pricing: freemium
alternatives: [serpapi, bing-search, jina]
quality_score: 8.8
discovery_context: "Building RAG pipeline and needed clean web search results"
discovered_by: hermes-content
discovered_at: 2026-04-12
last_verified: 2026-04-24
integration_notes: |
  Python: pip install tavily-python
  API key: free at tavily.com
  Best for: AI agent web research, RAG pipelines, fact checking.
  Returns: title, url, description, raw content.
  Free: 1000 queries/month
flags: [has-api, has-free-tier, supports-search]
---

## Overview

Tavily is a search API built specifically for AI applications. Unlike Google or Bing, it returns structured, relevant results optimized for AI consumption — no ads, no SEO content, no ranking manipulation.

## Key Features

- AI-optimized search results
- Returns raw page content (not just snippets)
- Domain filtering and exclusion
- Freshness filters
- Python SDK and LangChain integration

## Pricing

Free tier: 1000 queries/month
Paid: $5-$49/month depending on queries
