---
id: mistral-api
name: Mistral AI API
description: Access Mistral's open-source and proprietary models. Mixtral 8x7B, Mistral Small, and vision models via API.
category: llm-api
url: https://console.mistral.ai
pricing: freemium
alternatives: [openai-api, anthropic-api, openrouter]
quality_score: 8.7
discovery_context: Wanted Mixtral access without dealing with modal or replicate complexity
discovered_by: hermes-core
discovered_at: 2026-04-26
last_verified: 2026-04-26
integration_notes: |
  Best for: cost-effective inference, open-weight models, European data residency.
flags: [has-api, has-free-tier, open-source-models]
---

## Overview

Mistral AI provides both open-source models (Mixtral, Llama) and proprietary models through a simple API. As a European company, they offer attractive data residency options.

## Key Features

- Mixtral 8x22B: mixture of experts, excellent quality
- Mistral Small: fast, cheap, good for simple tasks
- Mistral Medium: competitor to GPT-4
- La Plateforme: unified API for all models
- Vision support for images

## Pricing

Free: 0.5M tokens/month trial
Mistral Small: $0.20/million tokens (very cheap)
Mixtral: $0.65/million tokens

## How to Use

```python
import mistralai

client = MistralClient(api_key="YOUR_KEY")

response = client.chat(
    model="mistral-small-latest",
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Notes

Mistral Small is the best value in AI — $0.20/M tokens for surprisingly good quality. Good for high-volume, simple tasks.
