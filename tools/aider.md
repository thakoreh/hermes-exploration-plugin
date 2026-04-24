---
id: aider
name: Aider
description: Terminal-based AI coding assistant. Edit code directly in your local repo with git diff awareness. Works with any LLM that supports function calling.
category: ai-coding
url: https://aider.chat
pricing: free
alternatives: [claude-code, cursor, windsurf, github-copilot]
quality_score: 8.3
discovery_context: "Looking for a CLI-based coding agent that works with local git repos"
discovered_by: hermes-core
discovered_at: 2026-04-15
last_verified: 2026-04-24
integration_notes: |
  Install: pip install aider-chat
  Works with: Claude 3.5/3.7, GPT-4o, Gemini, DeepSeek, Llama
  Best for: terminal-first workflows, solo developers, fast edits.
  Key feature: commits are automatically git-aware.
flags: [has-api, open-source, has-cli, has-free-tier]
---

## Overview

Aider is a CLI coding assistant that edits code directly in your repo. It understands git diffs, so it knows what changed and why. Connect it to Claude, GPT-4o, or any OpenAI-compatible endpoint.

## Key Features

- Edit local files directly with full git integration
- Works with Claude, GPT-4o, DeepSeek, Llama, Gemini
- Automatic git commits with sensible messages
- Multi-file editing across a codebase
- Supports OpenAI-compatible APIs (including Groq, OpenRouter)

## Pricing

Free and open-source (MIT license)
