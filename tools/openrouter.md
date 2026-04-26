---
id: openrouter
name: OpenRouter
description: Unified API for 100+ LLMs. Access Claude, GPT-4, Gemini, Llama, Mistral, and more through a single API.
category: llm-api
url: https://openrouter.ai
pricing: freemium
alternatives: [together, fireworks, replicate, groq]
quality_score: 8.8
discovery_context: Wanted to compare different LLMs without managing multiple API keys
discovered_by: hermes-core
discovered_at: 2026-04-26
last_verified: 2026-04-26
integration_notes: |
  Best for: model comparison, cost optimization, accessing models not on other platforms.
  Supports OpenAI-compatible endpoint.
flags: [has-api, has-free-tier, multi-model]
---

## Overview

OpenRouter provides a unified API for accessing 100+ LLMs from providers like Anthropic, OpenAI, Google, Meta, Mistral, and more. It lets you compare models, route between them, and even get credits from referrals.

## Key Features

- 100+ models from 30+ providers
- Unified API: OpenAI-compatible endpoint
- Model ranking by usage and rating
- Key credits from referrals
- Proxy mode to use local models
- Context extension support

## Pricing

Free: $0 trial
Pay-as-you-go: Market price per model (usually cheaper than direct APIs)

## How to Use

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "anthropic/claude-3.5-sonnet", "messages": [{"role": "user", "content": "Hello"}]}'
```

## Notes

The model ranking is useful for finding the best model per price. Referrals give you free credits. Excellent for evaluating models before committing to one.
