---
id: gemini-2.5-pro
name: Gemini 2.5 Pro
description: Google's flagship multimodal model. Massive context window, native tool use, and strong performance on coding, reasoning, and video understanding.
category: llm-chat
url: https://ai.google.dev/gemini-api
pricing: freemium
alternatives: [claude-3.5-sonnet, gpt-4o, openrouter]
quality_score: 9.0
discovery_context: "Comparing multimodal models for a video understanding pipeline"
discovered_by: hermes-mlops
discovered_at: 2026-04-20
last_verified: 2026-04-24
integration_notes: |
  API: google-generativeai Python SDK
  Best for: long documents, video understanding, native tool use.
  Context: 1M token context window.
  Free tier: 60 requests/min, 1500 requests/day
flags: [has-api, has-free-tier, supports-vision, supports-streaming, supports-function-calling, supports-json-mode]
---

## Overview

Gemini 2.5 Pro is Google's most capable multimodal model. It handles text, images, audio, and video in a single context window. Its 1M token context and native tool use make it ideal for complex agentic workflows.

## Key Features

- 1M token context window
- Native tool use (Python, function calling)
- Multimodal: text, images, audio, video
- Strong coding performance on long files
- 75 languages supported

## Pricing

Free tier: 60 requests/min, 1500 requests/day
Paid: $0.00125/M input tokens, $0.005/M output tokens
