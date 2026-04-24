#!/usr/bin/env python3
"""
discover_tools.py — Scan for new tools related to a task

Usage:
    python3 discover_tools.py --query "web scraping"
    python3 discover_tools.py --scan-repo /path/to/repo
    python3 discover_tools.py --list-categories
"""

import argparse
import json
import os
import re
import urllib.request
import urllib.error
from pathlib import Path

TOOL_DIRECTORIES = [
    'https://api.publicapis.org/entries?category=development',
    'https://api.publicapis.org/entries?category=business',
    'https://api.publicapis.org/entries?category=science',
]


def fetch_json(url: str, timeout: int = 10) -> dict:
    req = urllib.request.Request(url, headers={'User-Agent': 'exploration-plugin/1.0'})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def search_public_apis(query: str = None, category: str = None) -> list[dict]:
    """Search PublicAPIs.org."""
    url = 'https://api.publicapis.org/entries'
    if category:
        url += f'?category={category}'
    try:
        data = fetch_json(url)
        results = []
        for entry in data.get('entries', []):
            desc = entry.get('Description', '').lower()
            name = entry.get('API', '').lower()
            q = (query or '').lower()
            if q and q not in name and q not in desc:
                continue
            results.append({
                'name': entry.get('API'),
                'description': entry.get('Description'),
                'url': entry.get('Link'),
                'category': entry.get('Category'),
                'https': entry.get('HTTPS'),
                'auth': entry.get('Auth', 'None'),
                'cors': entry.get('Cors', 'unknown'),
            })
        return results
    except Exception as e:
        return [{'error': str(e)}]


def scan_repo(repo_path: str) -> dict:
    """
    Scan a repository for tool/API usage patterns.
    Returns a report of detected services.
    """
    path = Path(repo_path)
    if not path.exists():
        return {'error': f'Path not found: {repo_path}'}

    detected = {
        'services': {},      # service name -> context
        'endpoints': [],     # URL patterns found
        'api_keys': [],      # Named API key patterns
        'packages': [],      # package managers (pip, npm, etc.)
        'models': [],        # LLM models mentioned
    }

    # Known service patterns
    SERVICE_PATTERNS = {
        'openai': 'OpenAI (GPT, DALL-E, Whisper)',
        'anthropic': 'Anthropic (Claude)',
        'google': 'Google AI (Gemini, PaLM)',
        'mistralai': 'Mistral AI',
        'groq': 'Groq',
        'openrouter': 'OpenRouter',
        'replicate': 'Replicate',
        'modal': 'Modal',
        'firecrawl': 'Firecrawl',
        'tavily': 'Tavily Search',
        'jina': 'Jina AI (embeddings, reader)',
        'cohere': 'Cohere',
        'together': 'Together AI',
        'cloudflare': 'Cloudflare (Workers, R2)',
        'vercel': 'Vercel',
        'supabase': 'Supabase',
        'planetsscale': 'PlanetScale',
        'pinecone': 'Pinecone',
        'weaviate': 'Weaviate',
        'chromadb': 'ChromaDB',
        'qdrant': 'Qdrant',
        'lanceDb': 'LanceDB',
        'postgres': 'PostgreSQL',
        'redis': 'Redis',
        'slack': 'Slack API',
        'discord': 'Discord API',
        'stripe': 'Stripe',
        'sendgrid': 'SendGrid',
        'resend': 'Resend',
        'github': 'GitHub API',
        'aws': 'AWS',
        'gcp': 'Google Cloud',
    }

    # File extensions to scan
    CODE_EXTS = {'.py', '.js', '.ts', '.tsx', '.json', '.yaml', '.yml', '.toml', '.env', '.md'}

    for file_path in path.rglob('*'):
        if not file_path.is_file():
            continue
        if file_path.suffix not in CODE_EXTS:
            continue
        # Skip node_modules, .git, __pycache__, etc.
        skip_dirs = {'node_modules', '.git', '__pycache__', '.venv', 'dist', 'build', '.next', '.cache'}
        if any(part in skip_dirs for part in file_path.parts):
            continue

        try:
            content = file_path.read_text(errors='ignore')
        except Exception:
            continue

        # Check for service patterns
        for pattern, name in SERVICE_PATTERNS.items():
            if pattern in content.lower():
                if name not in detected['services']:
                    detected['services'][name] = []
                detected['services'][name].append(str(file_path.relative_to(path)))

        # Check for URLs/endpoints
        urls = re.findall(r'https?://[^\s"\')\]]+(?:api|[^\s"\')\]]*api[^\s"\')\]]*)', content)
        for url in urls[:10]:  # limit noise per file
            if url not in detected['endpoints']:
                detected['endpoints'].append(url)

        # Check for API key patterns
        key_patterns = re.findall(r'(?:api[_-]?key|apikey|API_KEY)[^=]*=[\s"\']([A-Za-z0-9_\-]{20,})', content)
        for key in key_patterns[:3]:
            if len(key) > 20:
                detected['api_keys'].append({
                    'name': key[:8] + '...',
                    'file': str(file_path.relative_to(path)),
                })

        # Check for LLM model names
        MODEL_PATTERNS = [
            'gpt-4', 'gpt-3.5', 'claude-3', 'claude-2', 'gemini',
            'llama-3', 'llama-2', 'mistral', 'mixtral', 'phi-3',
            'command-r', 'dbrx', 'qwen', 'yi-', 'gemma-',
        ]
        for model in MODEL_PATTERNS:
            if model in content.lower():
                if model not in detected['models']:
                    detected['models'].append(model)

        # Check package files
        if file_path.name == 'requirements.txt':
            deps = content.split('\n')
            detected['packages'].extend([d.strip() for d in deps if d.strip() and not d.startswith('#')])
        elif file_path.name == 'package.json':
            try:
                pkg = json.loads(content)
                deps = list(pkg.get('dependencies', {}).keys())
                detected['packages'].extend(deps)
            except Exception:
                pass

    return detected


def main():
    parser = argparse.ArgumentParser(description='Tool Discovery')
    parser.add_argument('--query', help='Search query')
    parser.add_argument('--scan-repo', help='Path to repository to scan')
    parser.add_argument('--list-categories', action='store_true')
    args = parser.parse_args()

    if args.list_categories:
        print('Available API categories:')
        try:
            data = fetch_json('https://api.publicapis.org/categories')
            for cat in data.get('categories', []):
                print(f'  {cat}')
        except Exception as e:
            print(f'Error: {e}')
        return

    if args.scan_repo:
        print(f'Scanning repo: {args.scan_repo}')
        print('=' * 60)
        report = scan_repo(args.scan_repo)
        if 'error' in report:
            print(f'Error: {report["error"]}')
            return

        if report['services']:
            print(f'\n[{len(report["services"])} Services Detected]')
            for svc, files in report['services'].items():
                print(f'  {svc}')
                for f in files[:3]:
                    print(f'    → {f}')
                if len(files) > 3:
                    print(f'    → ...and {len(files)-3} more')

        if report['models']:
            print(f'\n[LLM Models Detected]')
            for m in report['models']:
                print(f'  {m}')

        if report['packages']:
            print(f'\n[Packages ({len(report["packages"])})]')
            for p in report['packages'][:15]:
                print(f'  {p}')
            if len(report['packages']) > 15:
                print(f'  ...and {len(report["packages"])-15} more')

        if report['endpoints']:
            print(f'\n[{len(report["endpoints"])} API Endpoints Found]')
            for ep in report['endpoints'][:10]:
                print(f'  {ep}')

        if not report['services'] and not report['models'] and not report['packages']:
            print('No services, models, or packages detected.')

        return

    # Default: search public APIs
    print(f'Searching tools for: {args.query or "all"}')
    print('=' * 60)
    results = search_public_apis(query=args.query)
    for r in results:
        if 'error' in r:
            print(f'Error: {r["error"]}')
            continue
        print(f"\n  {r['name']} ({r['category']})")
        print(f"  {r['description']}")
        print(f"  {r['url']} | HTTPS: {r['HTTPS']} | Auth: {r['auth']}")


if __name__ == '__main__':
    main()
