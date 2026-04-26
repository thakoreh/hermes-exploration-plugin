---
id: openai-api
name: OpenAI API
description: Access GPT-4o, o1, o3, and o3-mini via OpenAI's API. The gold standard for LLM API access with function calling, vision, streaming, and the Assistants API.
category: llm-api
url: https://platform.openai.com
pricing: pay-per-use
alternatives:
  - anthropic-api
  - google-ai-api
  - openrouter
quality_score: 9.5
discovery_context: Primary LLM API for production applications requiring GPT-4o or o1/o3 reasoning models
discovered_by: hermes-core
discovered_at: 2026-04-25
last_verified: 2026-04-25
flags:
  - has-api
  - has-free-tier
  - supports-streaming
  - supports-function-calling
  - supports-vision
  - supports-json-mode
API: https://api.openai.com/v1/chat/completions
Free: $5 credit for new accounts, no ongoing free tier
Pricing: $2.50-$15/M input tokens, $10-$60/M output tokens (varies by model)
---

# OpenAI API

The OpenAI API provides access to the most widely-used LLMs: GPT-4o (fast, multimodal), o1 (reasoning), o3 (advanced reasoning), and o3-mini (efficient reasoning). Industry standard for production LLM applications.

## Key Models

| Model | Context | Key Strength | Price |
|-------|---------|--------------|-------|
| gpt-4o | 128K | Fast, multimodal, function calling | Mid |
| gpt-4o-mini | 128K | Cheaper, nearly as capable | Low |
| o1 | 200K | Reasoning, math, coding | High |
| o3 | 200K | Advanced reasoning | Very High |
| o3-mini | 200K | Efficient reasoning | Medium |

## Core Capabilities

- **Function calling** — structured output, tool use
- **Vision** — image input (screenshots, charts, photos)
- **Streaming** — real-time token streaming
- **Assistants API** — persistent threads, code interpreter, file search
- **JSON mode** — guaranteed valid JSON output
- **Vision** — image understanding at human level

## Python SDK

```bash
pip install openai
```

```python
from openai import OpenAI
client = OpenAI(api_key="sk-...")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}],
    temperature=0.7,
    max_tokens=500
)
print(response.choices[0].message.content)
```

## Use Cases

- Chatbots and virtual assistants
- Content generation (blog, marketing, docs)
- Code generation and review
- Data extraction and transformation
- Reasoning and analysis tasks
