#!/usr/bin/env python3
"""
Hermes Exploration Plugin — Integration Module

Enables Hermes agents to:
1. Search the discovery registry
2. Contribute new discoveries
3. Auto-discover tools while working
4. Update discovery quality scores

Usage:
    from hermes_exploration import ExplorationPlugin
    plugin = ExplorationPlugin(repo_path='/path/to/exploration-plugin')
    tools = plugin.search(query='web scraping')
    plugin.contribute(tool_data)
"""

import json
import os
import re
import subprocess
from datetime import date
from pathlib import Path
from typing import Any, Optional

DIRS = {
    'tool': 'tools',
    'api': 'apis', 
    'model': 'models',
}
CATEGORIES = {
    'tool': [
        'ai-coding', 'ai-writing', 'ai-image', 'ai-video', 'ai-audio',
        'ai-agents', 'productivity', 'automation', 'scraping',
        'api-development', 'infrastructure', 'security', 'research', 'other'
    ],
    'api': [
        'llm-provider', 'embedding', 'image', 'video', 'audio',
        'search', 'scraping-api', 'infrastructure', 'other'
    ],
    'model': [
        'llm-chat', 'llm-reasoning', 'embedding', 'vision',
        'image-gen', 'video-gen', 'audio-gen', 'multimodal', 'other'
    ]
}
FLAGS = [
    'has-api', 'open-source', 'has-free-tier', 'supports-webhook',
    'has-playground', 'supports-streaming', 'supports-vision',
    'supports-json-mode', 'supports-function-calling', 'supports-mcp',
    'self-hostable', 'has-docker', 'has-cli', 'has-mobile-app'
]


class ExplorationPlugin:
    """Main plugin class for Hermes agents."""

    def __init__(self, repo_path: str = None):
        if repo_path is None:
            repo_path = os.environ.get('EXPLORATION_PLUGIN_PATH', '/opt/exploration-plugin')
        self.repo_path = Path(repo_path)
        self.registry_path = self.repo_path / 'registry.json'
        self._ensure_registry()

    def _ensure_registry(self):
        if not self.registry_path.exists():
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.registry_path, 'w') as f:
                json.dump({'version': '1.0.0', 'tools': [], 'apis': [], 'models': [], 'stats': {}}, f, indent=2)

    def _load_registry(self) -> dict:
        with open(self.registry_path) as f:
            return json.load(f)

    def _save_registry(self, registry: dict):
        with open(self.registry_path, 'w') as f:
            json.dump(registry, f, indent=2)

    # ─── Search ───────────────────────────────────────────────────────────────

    def search(
        self,
        query: str = None,
        type: str = None,
        category: str = None,
        pricing: str = None,
        min_score: float = None,
        limit: int = 20,
    ) -> list[dict]:
        """
        Search discoveries by query, type, category, pricing, or quality score.

        Examples:
            plugin.search(query='web scraping')
            plugin.search(type='model', category='llm-chat', min_score=8.0)
            plugin.search(pricing='free')
        """
        registry = self._load_registry()
        all_items = []
        for disc_type in ['tools', 'apis', 'models']:
            for item in registry.get(disc_type, []):
                item['_type'] = disc_type.rstrip('s')
                all_items.append(item)

        if query:
            q = query.lower()
            all_items = [
                i for i in all_items
                if q in i.get('name', '').lower()
                or q in i.get('description', '').lower()
                or any(q in alt.lower() for alt in i.get('alternatives', []))
            ]

        if type:
            all_items = [i for i in all_items if i['_type'] == type]

        if category:
            all_items = [i for i in all_items if i.get('category') == category]

        if pricing:
            all_items = [i for i in all_items if i.get('pricing') == pricing]

        if min_score is not None:
            all_items = [
                i for i in all_items
                if i.get('quality_score', 0) >= min_score
            ]

        return all_items[:limit]

    def search_tools(self, query: str = None, limit: int = 20) -> list[dict]:
        """Search tools only."""
        return self.search(query=query, type='tool', limit=limit)

    def search_apis(self, query: str = None, limit: int = 20) -> list[dict]:
        """Search APIs only."""
        return self.search(query=query, type='api', limit=limit)

    def search_models(self, query: str = None, limit: int = 20) -> list[dict]:
        """Search models only."""
        return self.search(query=query, type='model', limit=limit)

    # ─── Contribute ──────────────────────────────────────────────────────────

    def contribute(
        self,
        data: dict,
        type: str = 'tool',
        author: str = 'hermes-agent',
        auto_commit: bool = True,
    ) -> str:
        """
        Add a new discovery to the registry.

        Args:
            data: Discovery data (name, description, url, etc.)
            type: 'tool' | 'api' | 'model'
            author: Who discovered this
            auto_commit: If True, commit and push changes

        Returns:
            The slug/id of the new discovery
        """
        slug = self._slugify(data.get('name', data.get('id', 'unknown')))
        data['id'] = slug
        data['discovered_by'] = author
        data['discovered_at'] = str(date.today())
        data['last_verified'] = str(date.today())
        data.setdefault('category', 'other')
        data.setdefault('pricing', 'unknown')
        data.setdefault('alternatives', [])

        # Write discovery file
        disc_dir = self.repo_path / DIRS[type]
        disc_dir.mkdir(parents=True, exist_ok=True)
        disc_file = disc_dir / f'{slug}.md'

        with open(disc_file, 'w') as f:
            f.write('---\n')
            yaml_safe = {k: v for k, v in data.items() if v is not None}
            # Handle lists on separate lines
            for key in ['alternatives', 'flags']:
                if key in yaml_safe and isinstance(yaml_safe[key], list):
                    yaml_safe[key] = yaml_safe[key]
            json.dump(yaml_safe, f, indent=2)
            f.write('\n---\n\n')
            if 'integration_notes' in data:
                f.write(data['integration_notes'].strip() + '\n')

        # Update registry
        registry = self._load_registry()
        registry_key = f'{type}s'  # tool → tools
        existing = [i for i in registry.get(registry_key, []) if i.get('id') != slug]
        existing.append(data)
        registry[registry_key] = existing
        self._save_registry(registry)

        # Git commit
        if auto_commit:
            self._git_add_commit(str(disc_file), f"discover: {slug} — {data.get('description', '')[:50]}")

        return slug

    def update_score(self, slug: str, score: float, author: str = 'hermes-agent'):
        """Update the quality score for an existing discovery."""
        registry = self._load_registry()
        updated = False

        for key in ['tools', 'apis', 'models']:
            for item in registry.get(key, []):
                if item.get('id') == slug:
                    item['quality_score'] = score
                    item['last_verified'] = str(date.today())
                    updated = True

        if updated:
            self._save_registry(registry)
            # Also update the markdown file
            for disc_type, dir_key in [('tool', 'tools'), ('api', 'apis'), ('model', 'models')]:
                fpath = self.repo_path / dir_key / f'{slug}.md'
                if fpath.exists():
                    content = fpath.read_text()
                    # Update quality_score in frontmatter
                    content = re.sub(
                        r'^quality_score:.*$',
                        f'quality_score: {score}',
                        content,
                        flags=re.MULTILINE
                    )
                    content = re.sub(
                        r'^last_verified:.*$',
                        f'last_verified: {date.today()}',
                        content,
                        flags=re.MULTILINE
                    )
                    fpath.write_text(content)
                    self._git_add_commit(str(fpath), f"score: {slug} → {score}/10 by {author}")

        return updated

    # ─── Auto-Discovery ───────────────────────────────────────────────────────

    def find_in_code(self, file_path: str) -> list[dict]:
        """
        Scan a file for API keys, endpoints, and tool references.
        Useful for discovering which services a codebase already uses.
        """
        findings = []
        try:
            with open(file_path) as f:
                content = f.read()

            # Detect API provider patterns
            providers = {
                'openai': 'OpenAI',
                'anthropic': 'Anthropic',
                'google': 'Google AI / Vertex',
                'mistralai': 'Mistral AI',
                'groq': 'Groq',
                'openrouter': 'OpenRouter',
                'replicate': 'Replicate',
                'modal': 'Modal',
                'firecrawl': 'Firecrawl',
                'tavily': 'Tavily',
                'jina': 'Jina AI',
                'cohere': 'Cohere',
                'together': 'Together AI',
            }

            for pattern, name in providers.items():
                if pattern in content.lower():
                    findings.append({
                        'type': 'llm-provider',
                        'name': name,
                        'context': f'Found reference to {name} in {file_path}',
                    })

            # Detect endpoint URLs
            endpoints = re.findall(r'https?://[^\s"\')]+(?:api|ai|cloud|api)[^\s"\')]*', content)
            for ep in endpoints[:5]:  # limit noise
                findings.append({
                    'type': 'endpoint',
                    'url': ep,
                    'context': f'Found endpoint in {file_path}',
                })

        except Exception as e:
            pass

        return findings

    def suggest_from_error(self, error_msg: str) -> list[dict]:
        """
        Given an error message, suggest tools/models that might help.
        This is the "exploration while working" loop.
        """
        suggestions = []
        error_lower = error_msg.lower()

        if 'rate limit' in error_lower or '429' in error_msg:
            suggestions.extend(self.search(query='rate limit handling'))

        if 'context window' in error_lower or 'too many tokens' in error_lower:
            suggestions.extend(self.search_models(query='long context'))

        if 'api key' in error_lower or 'authentication' in error_lower:
            suggestions.extend(self.search(query='API management'))

        if 'gpu' in error_lower or 'cuda' in error_lower:
            suggestions.extend(self.search(query='GPU cloud'))

        if 'image' in error_lower or 'vision' in error_lower:
            suggestions.extend(self.search_models(query='vision'))

        return suggestions

    # ─── Git helpers ─────────────────────────────────────────────────────────

    def _git_add_commit(self, path: str, message: str):
        """Run git add + commit. Silently fails if not a git repo."""
        try:
            subprocess.run(['git', 'add', path], cwd=self.repo_path,
                         capture_output=True, timeout=10)
            subprocess.run(['git', 'commit', '-m', message],
                         cwd=self.repo_path, capture_output=True, timeout=10)
        except Exception:
            pass  # Non-git repos or detached state — skip silently

    # ─── Utilities ───────────────────────────────────────────────────────────

    @staticmethod
    def _slugify(text: str) -> str:
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s-]', '', text)
        text = re.sub(r'[\s]+', '-', text)
        return text[:60].strip('-')

    def stats(self) -> dict:
        """Return registry statistics."""
        registry = self._load_registry()
        stats = {
            'tools': len(registry.get('tools', [])),
            'apis': len(registry.get('apis', [])),
            'models': len(registry.get('models', [])),
            'by_category': {},
            'by_pricing': {},
            'avg_score': None,
        }
        all_items = registry.get('tools', []) + registry.get('apis', []) + registry.get('models', [])
        scores = [i.get('quality_score') for i in all_items if i.get('quality_score')]
        if scores:
            stats['avg_score'] = round(sum(scores) / len(scores), 1)
        return stats


# ─── CLI for agents ───────────────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Exploration Plugin CLI')
    parser.add_argument('--path', default=os.environ.get('EXPLORATION_PLUGIN_PATH', '.'))
    sub = parser.add_subparsers(dest='cmd')

    search = sub.add_parser('search')
    search.add_argument('query', nargs='?', default='')
    search.add_argument('--type', choices=['tool', 'api', 'model'])
    search.add_argument('--category')
    search.add_argument('--pricing')
    search.add_argument('--min-score', type=float)

    contribute = sub.add_parser('contribute')
    contribute.add_argument('--name', required=True)
    contribute.add_argument('--description', required=True)
    contribute.add_argument('--url', required=True)
    contribute.add_argument('--type', default='tool')
    contribute.add_argument('--category', default='other')
    contribute.add_argument('--pricing', default='unknown')

    sub.add_parser('stats')

    args = parser.parse_args()
    plugin = ExplorationPlugin(repo_path=args.path)

    if args.cmd == 'search':
        results = plugin.search(
            query=args.query or None,
            type=args.type,
            category=args.category,
            pricing=args.pricing,
            min_score=args.min_score,
        )
        for item in results:
            print(f"  [{item['_type']}] {item['name']} — {item.get('description', '')}")
            print(f"    score: {item.get('quality_score', '?')}/10 | pricing: {item.get('pricing', '?')}")
            print(f"    url: {item.get('url', '')}")
            print()

    elif args.cmd == 'contribute':
        slug = plugin.contribute({
            'name': args.name,
            'description': args.description,
            'url': args.url,
            'category': args.category,
            'pricing': args.pricing,
        }, type=args.type)
        print(f"Added: {slug}")

    elif args.cmd == 'stats':
        s = plugin.stats()
        print(f"  Tools: {s['tools']}")
        print(f"  APIs: {s['apis']}")
        print(f"  Models: {s['models']}")
        print(f"  Avg score: {s['avg_score'] or 'N/A'}")
