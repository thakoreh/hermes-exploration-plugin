---
id: deepseek-coder
name: DeepSeek Coder
description: Open-source code generation model. Fine-tuned for code tasks, rivals GPT-4 on benchmarks.
category: coding
url: https://deepseek.com
pricing: free
alternatives: [gpt-4o, claude-3.5-sonnet, code-llama]
quality_score: 9.0
discovery_context: Needed open-source code model that rivals GPT-4 for cost-sensitive projects
discovered_by: hermes-core
discovered_at: 2026-04-26
last_verified: 2026-04-26
flags: [open-source, has-code-specialization]
---

## Overview

DeepSeek Coder is an open-source code model that rivals GPT-4 on code generation benchmarks. Trained on 2T tokens including 80+ languages of code, it excels at generation, completion, and debugging.

## Key Features

- Available in 1B to 33B parameter sizes
- Trained on 80+ programming languages
- 128K context window
- State-of-the-art on HumanEval, MBPP
- Available via Together AI, Fireworks

## How to Access

Via API: Together AI (deepseek-coder-33b-instruct)
Via open weights: Ollama, LM Studio

## Notes

DeepSeek Coder 33B is the sweet spot — better than CodeLlama on benchmarks, cheaper than GPT-4 via API. Excellent for production code generation.
