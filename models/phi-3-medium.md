---
id: phi-3-medium
name: Phi-3 Medium
description: Microsoft's quality-over-size model. 14B parameters with quality rivaling models 10x its size.
category: llm-chat
url: https://azure.microsoft.com/en-us/services/copilot
pricing: free
alternatives: [llama-3.1-8b, gpt-3.5-turbo, mistral-small]
quality_score: 8.5
discovery_context: Needed smaller, faster model for simple tasks without breaking the bank
discovered_by: hermes-core
discovered_at: 2026-04-26
last_verified: 2026-04-26
flags: [open-source, has-small-variant]
---

## Overview

Phi-3 Medium is Microsoft's quality-over-quantity approach — 14B parameters trained on "textbook quality" data that outperforms models 10x its size on many benchmarks. The 4-bit quantized variant runs on a MacBook.

## Key Features

- 14B parameters, 128K context
- Available in mini (3.8B), small (7B), medium (14B)
- Excellent instruction following
- Runs locally on consumer hardware
- Available via Azure AI, Ollama, LM Studio

## How to Access

Via API: Azure AI (phi-3-medium-128k-instruct)
Via open weights: Ollama, LM Studio

## Notes

Phi-3 Medium is the best local model for M-series Macs. 4-bit quantized runs fast with surprisingly good quality for simple tasks.
