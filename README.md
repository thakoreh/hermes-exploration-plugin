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

Then start a new Hermes chat (or restart your own running gateway).
```

After installing, try:
```
/explore web scraping
/explore llm cheap
/explore deploy docker
```

---

### Alternative: pip install

Install into the **same Python environment as Hermes**, then enable the
`exploration` entry point. The wheel includes a read-only registry snapshot;
it does not need a separate clone for search.

```bash
python -m pip install hermes-exploration
```

Then manually add `exploration` to your plugins list in `~/.hermes/config.yaml`:

```yaml
plugins:
  enabled:
    - exploration
```

Then restart Hermes: `hermes gateway restart`

---

**Windows note:** `hermes plugins install` works in PowerShell and Command Prompt.
For manual paths, use `$HOME` in PowerShell or `%USERPROFILE%` in Command Prompt;
Command Prompt does not expand `~`. The default config is
`%USERPROFILE%\.hermes\config.yaml`. `HERMES_HOME` overrides the Hermes profile.

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

# 2. Create venv and install (Python 3.9+)
python -m venv .venv
source .venv/bin/activate
pip install -e .

# 3. Configure (optional)
export EXPLORATION_READONLY=true   # disable all push operations
```

In PowerShell, activate with `.\.venv\Scripts\Activate.ps1` and configure with
`$env:EXPLORATION_READONLY = 'true'`. To use a different local registry for
`/explore`, set `EXPLORATION_PLUGIN_PATH` to its directory. A missing override
reports an error instead of silently searching another registry. The slash
command only reads local data and never calls a model provider or pushes changes.

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
    read_only=True,
)

# Discover
plugin.search(query='web scraping')
plugin.search_in_context(domain='llm', working_dir='/project')
plugin.suggest_from_error('tried to browse the web but no browser available')

# Contributions: edit a discovery markdown file in your fork, rebuild the
# registry with scripts/build_registry.py, then review and commit the diff.
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
  "description": "One sentence description (max 200 chars)",
  "id": "tool-name",
  "category": "ai-agents",
  "pricing": "unknown",
  "discovered_by": "agent-name or username",
  "discovered_at": "2026-05-02",
  "url": "https://example.com"
}
```

Full schema: `schemas/discovery.schema.json`.

## Discovery scripts and local checks

```bash
python scripts/discover_tools.py --help
python scripts/discover_apis.py --help
python scripts/discover_models.py --help
python scripts/discover_tools.py --scan-repo /path/to/synthetic-or-approved-repo
python scripts/discover_models.py --provider openrouter --max-price 1.00
```

OpenRouter metadata uses a public read-only endpoint. Prices shown by both model
scripts are dollars per **million** tokens. Groq metadata requires `GROQ_API_KEY`;
the script reports a missing key without making a request. `--provider all`
queries both providers. Discovery scripts report provider failures with a nonzero
exit code. Catalog availability and prices can change; these scripts do not call
inference or verify every catalog entry. Repository scans read local files, so
only point them at a directory you intend to inspect.

```bash
python -m pip install -e ".[dev]" build
python -m pytest -q
python -m build
```

Tests use synthetic registries and provider metadata without credentials or
external writes. After building, install the wheel into a new virtual environment
and invoke `/explore` from outside this checkout to verify packaged data.

---

## License

MIT — contribute freely, use freely.
