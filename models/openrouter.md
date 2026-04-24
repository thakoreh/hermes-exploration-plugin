---
id: openrouter
name: OpenRouter
description: Unified API gateway for 100+ LLM models from Anthropic, OpenAI, Meta, Mistral, and dozens of others. Single API key, single endpoint.
category: llm-provider
url: https://openrouter.ai
pricing: freemium
alternatives: [apiogether, go字, nat.dev]
quality_score: 9.0
discovery_context: "Looking for a way to compare multiple LLM responses without managing multiple API keys"
discovered_by: hermes-core
discovered_at: 2026-04-20
last_verified: 2026-04-24
integration_notes: |
  Standard OpenAI-compatible API. Swap endpoint from openai.com to openrouter.ai.
  Models: claude-3.5-sonnet, gpt-4-turbo, gemini-pro-1.5, llama-3-70b, mixtral-8x7b.
  Supports streaming, function calling, vision.
  Use case: fast model comparison, cost arbitrage across providers.
flags: [has-api, open-source, has-free-tier, supports-streaming, supports-function-calling, supports-vision]
---

## Overview

OpenRouter is an API aggregator that provides unified access to 100+ models from different providers through a single OpenAI-compatible API. You pay per token at each provider's rates + a small markup.

## Key Features

- Single API key for 100+ models
- OpenAI-compatible endpoint (swap `base_url`)
- Model ranking by traffic, price, context window
-生成synthetic rankings and usage stats per model
- Supports all major model features: vision, function calling, streaming

## Pricing

Free tier: $5 free credits for new accounts
Models: $0.50-$15/M tokens depending on model
No subscription required, pay-as-you-go
