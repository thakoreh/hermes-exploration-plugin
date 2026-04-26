---
id: n8n
name: n8n
description: Open-source workflow automation platform. Connect 400+ integrations, build AI agents with memory, and automate business processes without writing code.
category: automation
url: https://n8n.io
pricing: freemium
alternatives:
  - zapier
  - make
  - workflow-engine
quality_score: 9.0
discovery_context: Needed to connect LLM outputs to CRM, email, and webhook destinations without backend code
discovered_by: hermes-agents
discovered_at: 2026-04-25
last_verified: 2026-04-25
flags:
  - has-api
  - open-source
  - has-free-tier
  - has-ai-features
  - has-workflow-builder
Best for: Business process automation, AI agent workflows, connecting LLM outputs to real systems
Free: Self-host free, cloud free tier available
Install: docker run -it --name n8n -p 5678:5678 n8nio/n8n
---

# n8n

n8n is a workflow automation platform that balances power with accessibility. It has 400+ integrations including OpenAI, Anthropic, Slack, GitHub, Postgres, and more. Build AI agents with memory, loop over data, handle errors gracefully.

## Key Features

- **Visual workflow builder** — drag-and-drop nodes, no code required
- **AI nodes built-in** — chat, memory, document processing, LLM chain
- **400+ integrations** — databases, APIs, SaaS tools, webhooks
- **Self-hostable** — one Docker command, full control
- **Code execution** — add JavaScript/Python inline for custom logic
- **Error workflows** — trigger separate flow on failure
- **Credentials** — reusable auth across workflows

## AI Agent Features

n8n has dedicated AI agent nodes that can:
- Use OpenAI function calling / Anthropic tool use
- Maintain conversation memory
- Call multiple tools in a single workflow
- Loop until a condition is met
- Process files, URLs, and structured data

## Pricing

- **Self-hosted**: Free (Apache 2.0)
- **Cloud**: Free tier (100 executions), paid plans from $20/mo
