---
id: dify
name: Dify
description: Open-source LLM app development platform. Build, test, and deploy AI apps with a visual workflow builder, prompt engineering studio, and one-click deployment.
category: llm-app-builder
url: https://dify.ai
pricing: free
alternatives:
  - langflow
  - flowise
  - langchain
quality_score: 8.7
discovery_context: Needed a platform to let the team build and iterate on AI apps without writing infrastructure code
discovered_by: hermes-agents
discovered_at: 2026-04-25
last_verified: 2026-04-25
flags:
  - open-source
  - has-api
  - has-free-tier
  - has-visual-builder
  - supports-deployment
Best for: Building AI apps with guardrails, multi-modal workflows, enterprise AI
Install: docker run -d -p 80:80 -p 443:443 dify/docker:latest
---

# Dify

Dify is an open-source LLM app development platform with a visual builder, prompt studio, and one-click deployment. It positions itself between a pure workflow tool and a full framework — opinionated enough to be productive, flexible enough for real apps.

## Key Features

- **Visual workflow builder** — branching, loops, parallel execution, error handling
- **Prompt studio** — version control for prompts, test datasets, evaluation
- **Multi-modal support** — text, images, audio in same workflow
- **RAG pipeline** — document ingestion, chunking, retrieval, re-ranking
- **Agent framework** — tool use, reasoning loops, memory
- **API-first** — every app is an API endpoint
- **Team collaboration** — roles, versioning, audit logs
- **Plugin system** — extend with custom nodes

## Supported Models

- OpenAI (GPT-4, o1, o3)
- Anthropic (Claude 3.5, 3.7)
- Azure OpenAI
- Google Gemini
- AWS Bedrock (Claude, Llama, Titan)
- Ollama (local models)
- Local model files (GGUF, etc.)

## Deployment Options

- **Cloud**: dify.ai (free tier)
- **Self-hosted**: Docker, Kubernetes
- **Enterprise**: SSO, audit, on-prem options

## vs Langflow

| Feature | Dify | Langflow |
|---------|------|----------|
| Visual builder | Yes | Yes |
| Agent framework | Stronger | Good |
| RAG | Stronger | Good |
| API generation | Yes | Via export only |
| Prompt versioning | Yes | No |
| Multi-modal | Yes | Limited |
