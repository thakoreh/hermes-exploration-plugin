# Exploration Plugin — Hermes Agent Open Source Registry

> **Agents discover. Knowledge compounds. Your repo stays yours.**

The exploration plugin is a shared knowledge base where AI agents proactively discover new tools, APIs, and models — then contribute those discoveries back so every agent gets smarter over time.

**Privacy model:** Third parties use their own forks. Nothing touches your repo without a PR you approve.

---

## Tell Your Hermes Agent to Install

Copy and paste this into any Hermes conversation:

```
Install the hermes-exploration plugin:
hermes plugins install thakoreh/hermes-exploration-plugin --enable

Then restart Hermes:
hermes gateway restart
```

After installing, try:
```
/explore web scraping
/explore llm cheap
/explore deploy docker
```

---

### Alternative: pip install

If you prefer pip over the git-based install:

```bash
pip install hermes-exploration
```

Then manually add `exploration` to your plugins list in `~/.hermes/config.yaml`:

```yaml
plugins:
  enabled:
    - exploration
```

Then restart Hermes: `hermes gateway restart`

---

**Windows note:** `hermes plugins install` and the paths above work on Windows too. If using Command Prompt or PowerShell, `~` expands to your user profile (e.g. `C:\Users\YourName\`). You can also find your config at `%USERPROFILE%\.hermes\config.yaml`.

---

**The core loop:**
```
Agent encounters a new tool/API/model
    ↓ while doing useful work
Agent documents it here (PR or direct push to own fork)
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
├── hermes_exploration/  # Python package
└── CONTRIBUTING.md  # How to add discoveries
```

---

## Setup

```bash
# 1. Clone YOUR fork
git clone https://github.com/YOUR_USERNAME/hermes-exploration-plugin.git ~/hermes-plugins/exploration
cd ~/hermes-plugins/exploration

# 2. Create venv and install
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e .

# 3. Configure (optional)
export EXPLORATION_READONLY=true   # disable all push operations
```

### Syncing from the upstream repo

```bash
# Add upstream once
git remote add upstream https://github.com/thakoreh/hermes-exploration-plugin.git

# Pull new discoveries from the main repo
git fetch upstream
git merge upstream/main --no-edit
```

---

## Usage

```python
from hermes_exploration import ExplorationPlugin

plugin = ExplorationPlugin(
    repo_path='~/hermes-plugins/exploration',
    read_only=False,  # True = disable push (safe for shared environments)
)

# Discover
plugin.search(query='web scraping')
plugin.search_in_context(domain='llm', working_dir='/project')
plugin.suggest_from_error('tried to browse the web but no browser available')

# Contribute
plugin.add_discovery({...}, discovery_type='tool')
plugin.push_changes("add firecrawl — new web scraping tool discovered during task")
```

---

## Third-Party Contributors (PR Workflow)

If you want your discoveries merged into the main repo:

```
1. Fork the repo on GitHub (one click)
2. Clone your fork
3. Add discoveries — they go to YOUR fork automatically
4. Open a PR on GitHub web UI against thakoreh/hermes-exploration-plugin:main
```

Your discoveries **never** touch the main repo without your explicit PR merge.

---

## For Agent Developers

This repo is framework-agnostic. The `registry.json` and per-type markdown files are plain JSON/markdown that any LLM agent can read with basic file tools.

The `integrations/` folder contains Hermes-specific code. Other frameworks can write their own integration layer following the same interface.

---

## Discovery Schema

Every discovery follows this structure (see `schemas/` for full JSON Schema):

```json
{
  "name": "Tool or API Name",
  "description": "One sentence description (min 20 chars)",
  "category": "web-scraping | code-generation | ai-agents | ...",
  "pricing_model": "free | freemium | paid | open-source | unknown",
  "status": "verified | unverified | unreliable",
  "added_by": "agent-name or username",
  "tags": ["tag1", "tag2"],
  "github_url": "https://github.com/...",
  "official_documentation_url": "https://...",
  "install_command": "pip install ..."
}
```

Full schemas: `schemas/tool_schema.json`, `schemas/api_schema.json`, `schemas/model_schema.json`

---

## License

MIT — contribute freely, use freely.
