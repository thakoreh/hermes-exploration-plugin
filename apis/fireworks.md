---
id: fireworks
name: Fireworks AI
description: Fast inference for open-source AI models. Llama 3.1, Mixtral, and custom fine-tuned models with 99.9% uptime SLA.
category: ai-api
url: https://fireworks.ai
pricing: freemium
alternatives: [together, replicate, groq, openrouter]
quality_score: 8.8
discovery_context: Needed production-grade inference with SLA guarantees for enterprise RAG
discovered_by: hermes-mlops
discovered_at: 2026-04-26
last_verified: 2026-04-26
integration_notes: |
  Best for: production inference, custom fine-tuned models, structured output.
  Function calling and JSON mode support.
flags: [has-api, has-free-tier, has-sla]
---

## Overview

Fireworks AI provides fast, production-grade inference for open-source models with a 99.9% uptime SLA. They specialize in serving fine-tuned models and offer excellent support for structured outputs.

## Key Features

- Llama 3.1, Mixtral, DeepSeek models
- Function calling / tool use
- Structured JSON output
- 99.9% uptime SLA on Pro
- Fine-tuning service
- Batch inference API

## Pricing

Free: $1 free credits
Pay-per-token: Competitive (Llama 3.1 70B ~$0.65/million)

## How to Use

```python
import fireworks.client as fw

fw.api_key = "YOUR_KEY"

response = fw.ChatCompletion.create(
    model="accounts/fireworks/models/llama-v3p1-70b-instruct",
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Notes

The SLA and structured output support make this a good choice for enterprise. Fine-tuning service is excellent for domain adaptation.
