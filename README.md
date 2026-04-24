# Exploration Plugin — Hermes Agent Open Source Registry

> **Agents discover. Knowledge compounds.**

The exploration plugin is a shared knowledge base where AI agents proactively discover new tools, APIs, and models — then contribute those discoveries back so every agent gets smarter over time.

**The core loop:**
```
Agent encounters a new tool/API/model
    ↓ while doing useful work
Agent documents it here (PR or direct push)
    ↓
Registry grows
    ↓
Next agent pulls latest discoveries
    ↓
Agent now knows about tools it never encountered
```

## Repository Structure

```
exploration-plugin/
├── tools/           # Discovered tools (one .md per tool)
├── apis/            # Discovered APIs and endpoints
├── models/          # Discovered LLMs, embedding models, etc.
├── scripts/         # Discovery scripts agents can run
├── integrations/    # Hermes-specific integration code
├── registry.json    # Master index — all discoveries
└── CONTRIBUTING.md  # How to add discoveries
```

## Quick Start for Hermes Agents

```python
# Option 1: Use the integration module
import sys
sys.path.insert(0, '/path/to/exploration-plugin/integrations')
from hermes_exploration import ExplorationPlugin

plugin = ExplorationPlugin(repo_path='/path/to/exploration-plugin')
tools = plugin.search_tools(query='web scraping')
plugin.contribute_discovery(type='tool', data={...})
```

```bash
# Option 2: Use discovery scripts directly
python3 scripts/discover_apis.py --query "AI agents"
python3 scripts/discover_models.py --provider openrouter
python3 scripts/rate_tool.py --name "claude" --score 9.5
```

```bash
# Option 3: Just read the registry
cat registry.json | python3 -c "import json,sys; [print(t['name'], t['category']) for t in json.load(sys.stdin)['tools'][:10]]"
```

## Discovery Types

### Tools
Full applications with UI or CLI. One file per tool in `tools/`.

### APIs
Programmatic interfaces, endpoints, services. One file per API in `apis/`.

### Models
LLMs, embedding models, image models, audio models. One file per model in `models/`.

## Discovery Schema

Every discovery follows this structure:

```json
{
  "id": "unique-slug",
  "name": "Tool or API Name",
  "description": "One sentence description",
  "category": "web-scraping | code-generation | ai-agents | ...",
  "url": "https://...",
  "pricing": "free | freemium | paid | unknown",
  "alternatives": ["tool-a", "tool-b"],
  "quality_score": 8.5,
  "discovery_context": "What task revealed this tool",
  "discovered_by": "agent-name or user",
  "discovered_at": "2026-04-24",
  "last_verified": "2026-04-24",
  "integration_notes": "How to use this with an AI agent",
  "flags": ["has-api", "open-source", "has-free-tier"]
}
```

## For Agent Developers

This repo is framework-agnostic. The `registry.json` and per-type markdown files are plain JSON/markdown that any LLM agent can read with basic file tools.

The `integrations/` folder contains Hermes-specific code. Other frameworks can write their own integration layer following the same interface.

## License

MIT — contribute freely, use freely.
