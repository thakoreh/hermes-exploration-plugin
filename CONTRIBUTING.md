# Contributing Discoveries

This plugin grows through contributions. Every agent or user who discovers a new tool, API, or model adds to the shared knowledge base.

## What Counts as a Discovery?

**A discovery is any tool, API, or model that:**
- You encountered while doing actual work
- Isn't already in the registry
- You can provide accurate, verifiable information about

**NOT a discovery:**
- Something you researched specifically to "fill the registry" without using it
- Duplicate of an existing entry (check `registry.json` first)
- Unverifiable claims (fake benchmarks, non-existent products)

## How to Contribute

### Option 1: Direct Push (Trusted Agents)
If you have write access, add directly:

```bash
# Clone the repo
git clone https://github.com/your-org/exploration-plugin.git
cd exploration-plugin

# Add your discovery
cp tools/TEMPLATE.md tools/my-discovery.md
# Edit the file with real data

# Push
git add tools/my-discovery.md
git commit -m "discover: my-discovery — [brief description]"
git push
```

### Option 2: Pull Request (Anyone)
1. Fork the repo
2. Add your discovery following the schema
3. Open a PR with:
   - Discovery type in title: `[tool]`, `[api]`, or `[model]`
   - Brief description of why this is interesting
   - Context: what task revealed this discovery

### Option 3: GitHub Issue (Quick Fills)
If you just want to flag a discovery without writing the full entry:
```markdown
**Tool:** Name
**URL:** https://...
**Category:** ...
**Discovered via:** [what you were doing]
**Notes:** [anything interesting]
```

## Discovery Quality Standards

### Required Fields
- `name` — exact official name
- `description` — one sentence, no marketing fluff
- `category` — from the standard category list
- `url` — official website or docs
- `pricing` — free | freemium | paid | unknown
- `discovery_context` — what task revealed this
- `discovered_by` — agent name or "human:[name]"

### Optional but Valuable
- `alternatives` — known competitors
- `quality_score` — 1-10 based on your experience (not benchmarks)
- `integration_notes` — how an agent could use this
- `flags` — `has-api`, `open-source`, `has-free-tier`, `supports-webhook`, etc.

### Verification
- Verify the URL actually loads
- Verify pricing from the official pricing page
- Don't guess benchmark numbers

## Categories

### Tools
```
ai-coding          — code editors, copilots, refactoring tools
ai-writing         — copy, content, email writing
ai-image           — generation, editing, manipulation
ai-video           — generation, editing
ai-audio           — TTS, STT, music generation
ai-agents          — autonomous agent frameworks
productivity       — general productivity tools
automation         — workflow automation, Zapier-style
scraping           — web scraping, data extraction
api-development    — API design, testing, docs
infrastructure     — deployment, monitoring, DevOps
security           — SAST, secret scanning, pen testing
research           — literature search, paper analysis
other              — doesn't fit elsewhere
```

### APIs
```
llm-provider       — LLM API providers
embedding          — embedding/model APIs
image              — image generation, editing APIs
video              — video APIs
audio              — speech, music APIs
search             — search APIs
scraping           — scraping APIs
infrastructure     — cloud, deployment APIs
other              — doesn't fit elsewhere
```

### Models
```
llm-chat           — instruction-following chat models
llm-reasoning      — reasoning/coding focused models
embedding          — text embedding models
vision             — image understanding models
image-gen          — text-to-image models
video-gen          — video generation models
audio-gen          — audio/music generation models
multimodal         — models with multiple modalities
other              — doesn't fit elsewhere
```

## Formatting Rules

- Use **lowercase slug** for filenames: `claude-code.md`, not `Claude-Code.md`
- One discovery per file
- Frontmatter for metadata, prose for context
- No em-dashes, no exclamation marks, no "revolutionary"
- Write like a developer describing tools to peers

## Discovery Examples

### Great Discovery
```markdown
---
id: windsurf
name: Windsurf
category: ai-coding
url: https://codeium.com/windsurf
pricing: freemium
alternatives: [cursor, claude-code, github-copilot]
discovery_context: "Looking for an alternative to Cursor for a React project"
discovered_by: agent-01
last_verified: 2026-04-24
flags: [has-api, supports-mcp, has-free-tier]
---

Windsurf (formerly Codeium) is an AI-powered IDE from Cognition. The Cascade agent can handle multi-file refactoring that Cursor struggles with. Free tier includes 75 messages/month. Has native MCP support.
```

### Discovery That Needs Work
```markdown
# Windsurf

This is an AMAZING tool! 🚀 I found it while coding and it's REVOLUTIONARY!

It does AI coding and has great features...
<!-- AVOID: marketing fluff, no facts, wrong format -->
```
