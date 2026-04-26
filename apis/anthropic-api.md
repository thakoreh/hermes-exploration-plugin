---
id: anthropic-api
name: Anthropic API
description: Access Claude 3.5 Sonnet, 3.7, and Opus via the Claude API. Known for long context, instruction following, and safe, helpful outputs.
category: llm-api
url: https://console.anthropic.com
pricing: pay-per-use
alternatives:
  - openai-api
  - google-ai-api
  - openrouter
quality_score: 9.4
discovery_context: Claude 3.7 Sonnet for coding agents — best context quality and instruction following in class
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
API: https://api.anthropic.com/v1/messages
Free: Limited free tier for new accounts
Pricing: $3-$18/M input tokens, $15-$75/M output tokens (varies by model)
---

# Anthropic API

The Anthropic API provides access to Claude models — Claude 3.5 Sonnet (fast, best value), Claude 3.7 Sonnet (extended thinking), and Claude 3 Opus (most capable). Known for nuanced, careful reasoning and strong instruction following.

## Key Models

| Model | Context | Key Strength | Price |
|-------|---------|--------------|-------|
| claude-3.5-sonnet | 200K | Coding, analysis, speed | Mid |
| claude-3.7-sonnet | 200K | Extended thinking, complex reasoning | Mid-High |
| claude-3-opus | 200K | Most capable, complex tasks | High |

## Core Capabilities

- **Extended thinking** (3.7): Claude reasons internally before responding
- **Function calling** — structured tool use, parallel calls
- **Vision** — image input at high accuracy
- **Streaming** — real-time token streaming
- **JSON mode** — guaranteed valid JSON output
- **Prompt caching** — cache repeated context to reduce costs

## Python SDK

```bash
pip install anthropic
```

```python
from anthropic import Anthropic
client = Anthropic(api_key="sk-...")

response = client.messages.create(
    model="claude-3-7-sonnet-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.content[0].text)
```

## Extended Thinking

Claude 3.7 Sonnet supports extended thinking — enable with:
```python
thinking={"type": "enabled", "budget_tokens": 10000}
```

Claude internally reasons before giving the final answer. Dramatically improves reasoning tasks.

## Use Cases

- Complex coding tasks and code review
- Long document analysis (100K+ token docs)
- Multi-step reasoning and planning
- Thoughtful writing and editing
- Agentic workflows (computer use coming)
