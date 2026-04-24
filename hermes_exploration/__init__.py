"""
Exploration Plugin — Hermes Agent
=================================
Proactively discovers tools, APIs, and models based on session activity.

This module serves as the Hermes plugin entry point AND contains the core
ExplorationPlugin logic. It can be installed as a pip package with the
`hermes_agent.plugins` entry point.

For development (without pip install), copy to: ~/.hermes/plugins/exploration/
"""

from __future__ import annotations

import json
import logging
import os
import re
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import git

logger = logging.getLogger(__name__)

# ── Capability gap patterns ───────────────────────────────────────────────────

_ERROR_CONTEXT_MAP = {
    "browser":          ["firecrawl", "jina-reader", "browser-use", "scrapfly", "apify"],
    "web scraping":     ["firecrawl", "jina-reader", "scrapingbee", "scrapfly", "apify"],
    "web crawl":        ["firecrawl", "jina-reader", "apify", "crawlee"],
    "scrape":           ["firecrawl", "jina-reader", "scrapingbee"],
    "fetch html":       ["jina-reader", "firecrawl", "requests-html"],
    "llm":              ["openrouter", "groq", "replicate", "fireworks", "together"],
    "language model":   ["openrouter", "groq", "replicate", "fireworks"],
    "embeddings":       ["jina-ai", "voyage-ai", "cohere", "mistral-embed"],
    "api":              ["tavily", "serpapi", "jina-ai"],
    "search":           ["tavily", "serpapi", "duckduckgo"],
    "database":         ["convex", "supabase", "planetscale", "xata", "neon"],
    "email":            ["resend", "sendgrid", "postmark", "himalaya"],
    "deploy":           ["vercel", "railway", "render", "coolify", "fly.io"],
    "docker":           ["docker-management", "container-tools"],
    "serverless":       ["modal", "aws-lambda", "cloudflare-workers"],
    "pdf":              ["pymupdf", "pdfplumber", "nougat", "marker-pdf"],
    "code":             ["aider", "Continue", "cursor", "windsurf", "cline"],
}

# ── Session state ─────────────────────────────────────────────────────────────

_session_tools: Dict[str, List[str]] = {}
_session_suggestions: Dict[str, List[Dict[str, str]]] = {}


# ── Core ExplorationPlugin ────────────────────────────────────────────────────

class ExplorationPlugin:
    """
    Agents use this to discover and contribute tools, APIs, and models.
    Used by both the slash command handler and the library interface.
    """

    def __init__(self, repo_path: str, read_only: bool = False):
        self.repo_path = Path(os.path.expanduser(repo_path)).resolve()
        self.registry_path = self.repo_path / "registry.json"
        self.read_only = read_only or os.getenv("EXPLORATION_READONLY", "").lower() in ("true", "1", "yes")
        self._ensure_registry()

    def _ensure_registry(self) -> None:
        if not self.registry_path.exists():
            Path(self.registry_path).parent.mkdir(parents=True, exist_ok=True)
            with open(self.registry_path, "w") as f:
                json.dump({"version": 1, "generated_at": "", "tools": [], "apis": [], "models": [], "stats": {}}, f)

    def _read_registry(self) -> Dict[str, List[Dict]]:
        try:
            with open(self.registry_path) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"version": 1, "generated_at": "", "tools": [], "apis": [], "models": [], "stats": {}}

    def _write_registry(self, registry: Dict) -> None:
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.registry_path, "w") as f:
            json.dump(registry, f, indent=2)

    def search(self, query: str, discovery_type: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        registry = self._read_registry()
        query_lower = query.lower()
        results = []
        types_to_search = (
            [discovery_type + "s"] if discovery_type and discovery_type + "s" in registry
            else ["tools", "apis", "models"]
        )
        for dtype in types_to_search:
            for item in registry.get(dtype, []):
                score = 0
                text = json.dumps(item, ensure_ascii=False).lower()
                for word in query_lower.split():
                    score += text.count(word) * (2 if word in text[:100] else 1)
                if score > 0:
                    results.append({**item, "type": dtype[:-1], "_score": score})
        results.sort(key=lambda x: x.pop("_score"), reverse=True)
        return results[:limit]

    def search_in_context(self, domain: str, working_dir: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        already_installed: set = set()
        if working_dir:
            wd = Path(os.path.expanduser(working_dir))
            for req_file in wd.rglob("requirements*.txt"):
                try:
                    already_installed.update(line.strip().split("==")[0] for line in req_file.read_text().splitlines() if line.strip() and not line.startswith("#"))
                except Exception:
                    pass
        candidates = self.search(query=domain, limit=20)
        if already_installed:
            candidates = [c for c in candidates if c["name"] not in already_installed]
        return candidates[:limit]

    def suggest_from_error(self, error_message: str) -> List[Dict[str, Any]]:
        error_lower = error_message.lower()
        matched_keys = [key for key in _ERROR_CONTEXT_MAP if key in error_lower]
        suggestions: List[Dict[str, Any]] = []
        seen_names: set = set()
        for key in matched_keys:
            for name in _ERROR_CONTEXT_MAP[key]:
                if name in seen_names:
                    continue
                seen_names.add(name)
                found = self.search(query=name, limit=1)
                if found:
                    suggestions.extend(found)
                else:
                    suggestions.append({"name": name, "type": "tool", "description": f"Suggested for: {key}", "status": "unverified"})
        return suggestions

    def get_registry_stats(self) -> Dict[str, int]:
        registry = self._read_registry()
        return {key: len(val) for key, val in registry.items() if key not in ("version", "generated_at", "stats")}

    def git_status(self) -> Dict[str, Any]:
        try:
            repo = git.Repo(self.repo_path)
            return {"dirty": repo.is_dirty(), "branch": repo.active_branch.name, "untracked_files": repo.untracked_files}
        except Exception as e:
            return {"error": str(e)}

    def push_changes(self, message: str = "Update registry") -> Dict[str, str]:
        if self.read_only:
            return {"error": "read_only mode is enabled — push disabled"}
        try:
            repo = git.Repo(self.repo_path)
            repo.index.add([str(self.registry_path)])
            repo.index.commit(message)
            origin = repo.remote("origin")
            origin.push()
            return {"status": "pushed", "commit": message}
        except Exception as e:
            return {"error": str(e)}


# ── Plugin helpers ─────────────────────────────────────────────────────────────

def _get_plugin(repo_path: Optional[str] = None) -> Optional[ExplorationPlugin]:
    """Get an ExplorationPlugin instance, trying multiple possible locations."""
    paths_to_try = []
    if repo_path:
        paths_to_try.append(Path(repo_path).expanduser())
    # Try git repo first
    git_repo = Path("~/hermes-plugins/hermes-exploration-plugin").expanduser()
    if git_repo.exists():
        paths_to_try.append(git_repo)
    # Try the plugin directory itself
    plugin_dir = Path(__file__).parent
    paths_to_try.append(plugin_dir)

    for path in paths_to_try:
        try:
            registry = path / "registry.json"
            if registry.exists():
                return ExplorationPlugin(repo_path=str(path))
        except Exception:
            pass
    return None


# ── Hooks ─────────────────────────────────────────────────────────────────────

def _on_post_tool_call(
    tool_name: str = "",
    args: Optional[Dict[str, Any]] = None,
    result: Any = None,
    task_id: str = "",
    session_id: str = "",
    tool_call_id: str = "",
    **_: Any,
) -> None:
    """Track which tools were used during the session."""
    key = task_id or session_id or "default"
    if tool_name:
        if key not in _session_tools:
            _session_tools[key] = []
        if tool_name not in _session_tools[key]:
            _session_tools[key].append(tool_name)


def _on_session_end(session_id: str = "", completed: bool = True, interrupted: bool = False, task_id: str = "", **_: None) -> None:
    """At session end, analyze session and surface relevant discoveries."""
    global _session_suggestions
    if not session_id:
        return

    key = task_id or session_id or "default"
    used_tools = _session_tools.pop(key, [])

    plugin = _get_plugin()
    if not plugin:
        return

    suggestions: List[Dict[str, str]] = []
    for tool in used_tools:
        related = plugin.search(query=tool, limit=2)
        for r in related:
            if r["name"] not in used_tools:
                suggestions.append({"name": r["name"], "type": r.get("type", ""), "description": r.get("description", "")[:80]})

    seen = set()
    unique = []
    for s in suggestions:
        if s["name"] not in seen:
            seen.add(s["name"])
            unique.append(s)

    if unique:
        _session_suggestions[session_id] = unique


# ── Slash command ──────────────────────────────────────────────────────────────

_EXPLORE_HELP = """\
/explore <query> — Search the tool/API/model registry

Examples:
  /explore web scraping
  /explore llm cheap
  /explore deploy docker
"""


def _handle_explore(raw_args: str) -> Optional[str]:
    args = raw_args.strip()
    plugin = _get_plugin()

    if not plugin:
        return "Exploration registry not found. Install hermes-exploration or clone https://github.com/thakoreh/hermes-exploration-plugin"

    if not args:
        stats = plugin.get_registry_stats()
        return (
            f"🔍 Exploration Registry\n"
            f"   {stats.get('tools', 0)} tools · {stats.get('apis', 0)} APIs · {stats.get('models', 0)} models\n\n"
            f"Usage: /explore <query>\n"
            f"Example: /explore web scraping"
        )

    results = plugin.search(query=args, limit=8)
    if not results:
        return f"No discoveries found for '{args}'. Try /explore <topic>."

    lines = [f"🔍 {len(results)} discoveries for '{args}':", ""]
    for r in results:
        dtype = r.get("type", "")
        name = r.get("name", "")
        desc = r.get("description", "")[:70]
        price = r.get("pricing_model", "unknown")
        lines.append(f"  [{dtype}] {name} ({price})")
        lines.append(f"         {desc}...")
    return "\n".join(lines)


# ── Plugin registration ────────────────────────────────────────────────────────

def register(ctx) -> None:
    """
    Called by Hermes when the plugin is loaded.
    ctx is a PluginContext instance.
    """
    ctx.register_hook("post_tool_call", _on_post_tool_call)
    ctx.register_hook("on_session_end", _on_session_end)
    ctx.register_command(
        "explore",
        handler=_handle_explore,
        description="Search the tool/API/model discovery registry.",
    )
    logger.info("exploration plugin loaded — /explore, on_session_end, post_tool_call active")
