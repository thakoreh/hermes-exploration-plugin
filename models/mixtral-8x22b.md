---
id: mixtral-8x22b
name: Mixtral 8x22B
description: Mixture-of-experts model from Mistral. 39B active parameters, expert routing for efficient inference.
category: llm-chat
url: https://mistral.ai
pricing: free
alternatives: [llama-3.1-70b, gpt-4o, claude-3.5-sonnet]
quality_score: 8.9
discovery_context: Wanted mixture-of-experts efficiency — high quality with lower active parameter count
discovered_by: hermes-core
discovered_at: 2026-04-26
last_verified: 2026-04-26
flags: [open-source, mixture-of-experts]
---

## Overview

Mixtral 8x22B uses mixture-of-experts architecture where only 39B parameters are active per token. This means GPT-3.5-class cost with near GPT-4 quality. Excellent for tasks requiring breadth of knowledge.

## Key Features

- 8 experts, 39B active parameters per token
- 65B total parameters
- 64K context window
- Excellent code generation
- Available via Mistral La Plateforme, Groq, Fireworks

## How to Access

Via API: Mistral La Plateforme, Groq (fastest), Fireworks
Via open weights: Ollama, LM Studio

## Notes

The MoE architecture means fast inference despite the large total size. Groq's implementation is particularly impressive for speed.
