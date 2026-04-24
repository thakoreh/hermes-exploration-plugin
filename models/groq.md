---
id: groq
name: Groq
description: Fastest LLM inference API available. Sub-second first-token latency for Llama 3, Mixtral, and Gemma models on custom LPU hardware.
category: llm-provider
url: https://console.groq.com
pricing: freemium
alternatives: [openrouter, together]
quality_score: 9.2
discovery_context: "Building a real-time chat app and needed latency lower than OpenAI or Anthropic"
discovered_by: hermes-core
discovered_at: 2026-04-08
last_verified: 2026-04-24
integration_notes: |
  OpenAI-compatible API — swap base_url to api.groq.com
  Models: llama-3-70b, llama-3-8b, mixtral-8x7b, gemma-7b
  Best for: latency-critical applications, real-time chat
  Free: 30 requests/min, 14,400 requests/day
flags: [has-api, has-free-tier, supports-streaming, supports-function-calling]
---

## Overview

Groq's LPU (Language Processing Unit) delivers the fastest LLM inference in the industry. First-token latency under 1 second for 70B models. Great for real-time applications where speed matters more than absolute throughput.

## Key Features

- Fastest inference: sub-second first-token on Llama 3 70B
- OpenAI-compatible API — easy migration
- Streaming support
- Function calling and JSON mode
- Context windows up to 128K tokens

## Pricing

Free tier: 30 requests/minute, 14,400 requests/day
Paid: pay-per-token, competitive pricing
No subscriptions
