---
id: together
name: Together AI
description: Dedicated GPU infrastructure for open-source AI models. Llama 3, Phi-3, DeepSeek, FLUX, and more with fast inference.
category: ai-api
url: https://together.ai
pricing: freemium
alternatives: [replicate, fireworks, groq, openrouter]
quality_score: 8.9
discovery_context: Needed fast inference for open-source LLMs at competitive pricing
discovered_by: hermes-mlops
discovered_at: 2026-04-26
last_verified: 2026-04-26
integration_notes: |
  Best for: fast open-source model inference, fine-tuning, prompt playground.
  Models are hosted on NVIDIA H100s for speed.
flags: [has-api, has-free-tier, has-fine-tuning]
---

## Overview

Together AI provides dedicated GPU infrastructure specifically optimized for open-source AI models. With partnerships with Meta, Intel, and others, they offer some of the fastest and cheapest inference for models like Llama 3, Phi-3, and DeepSeek.

## Key Features

- Llama 3, Phi-3, DeepSeek, FLUX, and more
- Fine-tuning on custom datasets
- Prompt playground
- Streaming API
- Chat completion and instruct models
- NVIDIA H100/H200 GPUs

## Pricing

Free: $5 free credits
Pay-per-token: Very competitive (Llama 3 70B at ~$0.65/million tokens)

## How to Use

```bash
pip install together
```

```python
import together
together.api_key = "YOUR_KEY"

response = together.chat.completions.create(
    model="meta-llama/Llama-3-70b-chat",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

## Notes

Fine-tuning support is excellent and reasonably priced. Good choice for both inference and custom model training.
