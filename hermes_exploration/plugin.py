"""
ExplorationPlugin — core class for the Hermes exploration plugin.
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import git
from .schemas import DiscoverySchema, SCHEMAS

# ── helpers ────────────────────────────────────────────────────────────────────

def _load_json(path: Path) -> Dict[str, Any]:
    with open(path) as f:
        return json.load(f)

def _save_json(path: Path, data: Dict[str, Any]) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    path.write_text(path.read_text() + "\n")  # trailing newline

# ── ExplorationPlugin ──────────────────────────────────────────────────────────

class ExplorationPlugin:
    """
    Agents use this to discover and contribute tools, APIs, and models.

    Usage:
        plugin = ExplorationPlugin(repo_path="~/hermes-plugins/exploration")
        plugin.search(query="web scraping")
        plugin.search_in_context(domain="llm")
        plugin.suggest_from_error("no browser available")
        plugin.add_discovery({...})
    """

    # categories that map to discovery types
    ERROR_CONTEXT_MAP = {
        "browser":          "tool",
        "web scraping":     "tool",
        "web crawl":       "tool",
        "scrape":          "tool",
        "fetch html":      "tool",
        "llm":             "model",
        "language model":  "model",
        "embeddings":      "model",
        "api":             "api",
        "search":          "api",
        "email":           "tool",
        "database":        "tool",
        "pdf":             "tool",
        "csv":             "tool",
        "excel":           "tool",
        "image":           "tool",
        "video":           "tool",
        "audio":           "tool",
        "deploy":          "tool",
        "docker":          "tool",
        "cloud":           "tool",
        "serverless":      "tool",
        "function":        "tool",
        "schedule":        "tool",
        "cron":            "tool",
    }

    ERROR_SUGGESTIONS = {
        "browser": [
            "firecrawl", "jina-reader", "browser-use", "scrapfly", "serpapi",
        ],
        "web scraping": [
            "firecrawl", "jina-reader", "scrapingbee", "scrapfly", "apify",
        ],
        "llm": [
            "openrouter", "replicate", "groq", "fireworks", "together",
        ],
        "language model": [
            "openrouter", "replicate", "groq", "fireworks", "together",
        ],
        "embeddings": [
            "jina-ai", "voyage-ai", "cohere", "openai-embeddings", "mistral-embed",
        ],
        "api": [
            "tavily", "serpapi", "jina-ai", "public-apis", "api-fairy",
        ],
        "database": [
            "convex", "supabase", "planetscale", "xata", "neon",
        ],
        "email": [
            "resend", "sendgrid", "postmark", "mailgun", "himalaya",
        ],
        "deploy": [
            "vercel", "railway", "render", "coolify", "fly.io",
        ],
        "docker": [
            "docker-management", "container-tools", "podman", "docker-slim",
        ],
        "serverless": [
            "modal", "aws-lambda", "netlify-functions", "cloudflare-workers",
        ],
        "pdf": [
            "pymupdf", "pdfplumber", "nougat", "marker-pdf", "docling",
        ],
        "code": [
            "aider", ".Continue", "cursor", "windsurf", "cline",
        ],
    }

    def __init__(self, repo_path: str, read_only: bool = False):
        self.repo_path = Path(os.path.expanduser(repo_path)).resolve()
        self.registry_path = self.repo_path / "registry.json"
        self.read_only = read_only or os.getenv("EXPLORATION_READONLY", "").lower() in ("true", "1", "yes")
        self._ensure_registry()

    # ── registry ────────────────────────────────────────────────────────────

    def _ensure_registry(self) -> None:
        if not self.registry_path.exists():
            _save_json(self.registry_path, {"tools": [], "apis": [], "models": []})

    def _read_registry(self) -> Dict[str, List[Dict]]:
        return _load_json(self.registry_path)

    def _write_registry(self, registry: Dict[str, List[Dict]]) -> None:
        _save_json(self.registry_path, registry)

    # ── search ───────────────────────────────────────────────────────────────

    def search(
        self,
        query: str,
        discovery_type: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Full-text search across all discoveries.
        """
        registry = self._read_registry()
        query_lower = query.lower()
        results = []

        types_to_search = (
            [discovery_type + "s"]
            if discovery_type and discovery_type + "s" in registry
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

    def search_in_context(
        self,
        domain: str,
        working_dir: Optional[str] = None,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Domain-aware search. Also checks working_dir for already-installed tools.
        """
        already_installed: set = set()
        if working_dir:
            wd = Path(os.path.expanduser(working_dir))
            for req_file in wd.rglob("requirements*.txt"):
                try:
                    already_installed.update(line.strip().split("==")[0]
                                             for line in req_file.read_text().splitlines()
                                             if line.strip() and not line.startswith("#"))
                except Exception:
                    pass
            for lock_file in wd.rglob("package.json"):
                try:
                    already_installed.update(json.loads(lock_file.read_text())
                                             .get("dependencies", {}).keys())
                except Exception:
                    pass

        candidates = self.search(query=domain, limit=20)
        if already_installed:
            candidates = [c for c in candidates if c["name"] not in already_installed]
        return candidates[:limit]

    def suggest_from_error(self, error_message: str) -> List[Dict[str, Any]]:
        """
        Map an error or capability gap to known-good alternatives.
        """
        error_lower = error_message.lower()
        matched_keys = [
            key for key in self.ERROR_CONTEXT_MAP
            if key in error_lower
        ]

        suggestions: List[Dict[str, Any]] = []
        seen_names: set = set()

        for key in matched_keys:
            names = self.ERROR_SUGGESTIONS.get(key, [])
            for name in names:
                if name in seen_names:
                    continue
                seen_names.add(name)
                # look up in registry
                found = self.search(query=name, limit=1)
                if found:
                    suggestions.extend(found)
                else:
                    suggestions.append({
                        "name": name,
                        "type": self.ERROR_CONTEXT_MAP[key],
                        "description": f"Suggested for: {key}",
                        "status": "unverified",
                    })
        return suggestions

    # ── contribute ───────────────────────────────────────────────────────────

    def add_discovery(
        self,
        data: Dict[str, Any],
        discovery_type: Optional[str] = None,
    ) -> tuple[bool, List[str]]:
        """
        Add a new discovery. Type is inferred from data or explicitly passed.
        Returns (is_valid, errors).
        """
        dtype = discovery_type or data.get("type", "")
        if not dtype:
            return False, ["discovery_type must be passed or data must contain 'type'"]

        dtype_map = {"tool": "tools", "api": "apis", "model": "models"}
        key = dtype_map.get(dtype)
        if key is None:
            return False, [f"Unknown type: {dtype}. Must be one of: tool, api, model"]

        valid, errors = DiscoverySchema.validate(dtype, data)
        if not valid:
            return False, errors

        registry = self._read_registry()

        # avoid duplicates by name
        if any(item["name"] == data["name"] for item in registry.get(key, [])):
            return False, [f"'{data['name']}' already exists in {key}"]

        data["type"] = dtype
        registry[key].append(data)
        self._write_registry(registry)

        # also write to category subdir
        subdir = self.repo_path / key / f"{data['name'].replace(' ', '-')}.md"
        subdir.parent.mkdir(parents=True, exist_ok=True)
        subdir.write_text(self._to_md(data, dtype))

        return True, []

    # ── git ──────────────────────────────────────────────────────────────────

    def git_status(self) -> Dict[str, Any]:
        try:
            repo = git.Repo(self.repo_path)
            return {
                "dirty": repo.is_dirty(),
                "untracked_files": repo.untracked_files,
                "branch": repo.active_branch.name,
                "ahead": repo.iter_commits(f"origin/{repo.active_branch.name}..{repo.active_branch.name}"),
            }
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

    # ── stats ────────────────────────────────────────────────────────────────

    def get_registry_stats(self) -> Dict[str, int]:
        registry = self._read_registry()
        return {key: len(val) for key, val in registry.items()}

    # ── internal ─────────────────────────────────────────────────────────────

    @staticmethod
    def _to_md(data: Dict[str, Any], dtype: str) -> str:
        lines = [
            f"# {data['name']}  ",
            f"**Type:** {dtype}  ",
            f"**Status:** {data.get('status', 'unverified')}  ",
            "",
            data.get("description", ""),
            "",
        ]
        for key in ["use_cases", "strengths", "tags"]:
            if data.get(key):
                lines.append(f"- **{key}:** {', '.join(data[key])}")
        for key, val in data.items():
            if key not in ["name", "description", "type", "status", "use_cases",
                            "strengths", "tags", "added_by"] and val:
                lines.append(f"- **{key}:** {val}")
        lines.extend(["", f"_Added by: {data.get('added_by', 'unknown')}_"])
        return "\n".join(lines)
