#!/usr/bin/env python3
"""
discover_apis.py — Scan for interesting APIs

Agents run this to find new APIs relevant to their task.
Scans common API directories and discovery services.

Usage:
    python3 discover_apis.py --query "AI agents"
    python3 discover_apis.py --list-providers
    python3 discover_apis.py --category llm-provider
"""

import argparse
import json
import math
import urllib.request
import urllib.error
import time
from urllib.parse import urlencode

# API discovery sources
SOURCES = {
    'openrouter_models': 'https://openrouter.ai/api/v1/models',
    'public_apis': 'https://api.publicapis.org/entries',
    'rapid_api': 'https://api.rapidapi.com',
}


def price_per_million(value):
    if value is None:
        return None
    try:
        price = float(value) * 1_000_000
    except (ValueError, TypeError):
        return None
    return price if math.isfinite(price) and price >= 0 else None


def fetch_json(url: str, timeout: int = 10) -> dict:
    req = urllib.request.Request(url, headers={'User-Agent': 'exploration-plugin/1.0'})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def search_openrouter(query: str = None) -> list[dict]:
    """Get models from OpenRouter. Free, no auth required."""
    try:
        data = fetch_json(SOURCES['openrouter_models'])
        models = []
        for m in data.get('data', []):
            name = m.get('name', '')
            context = m.get('context_length', 0)
            pricing = m.get('pricing') or {}
            price_per_m = price_per_million(pricing.get('completion'))
            model_id = m.get('id', '')
            models.append({
                'id': model_id,
                'name': name,
                'description': m.get('description', '')[:150],
                'context_window': context,
                'price_per_m_output': price_per_m,
                'category': 'llm-provider',
                'url': 'https://openrouter.ai/' + model_id,
                'pricing': 'freemium',
                'flags': ['has-api', 'has-free-tier', 'supports-streaming'],
            })
        if query:
            q = query.lower()
            models = [m for m in models if q in m['name'].lower() or q in m['description'].lower()]
        return models[:20]
    except Exception as e:
        return [{'error': str(e), 'source': 'openrouter'}]


def search_public_apis(category: str = None, query: str = None) -> list[dict]:
    """Search PublicAPIs.org for free APIs."""
    try:
        url = 'https://api.publicapis.org/entries'
        if category:
            url += '?' + urlencode({'category': category})
        data = fetch_json(url)
        apis = []
        for entry in data.get('entries', []):
            if query and query.lower() not in (entry.get('Description', '') + ' ' + entry.get('API', '')).lower():
                continue
            apis.append({
                'name': entry.get('API', ''),
                'description': entry.get('Description', ''),
                'url': entry.get('Link', ''),
                'category': entry.get('Category', ''),
                'https': entry.get('HTTPS', False),
                'auth': entry.get('Auth', ''),
                'pricing': 'unknown',
            })
        return apis[:20]
    except Exception as e:
        return [{'error': str(e), 'source': 'publicapis'}]


def main():
    parser = argparse.ArgumentParser(description='API Discovery')
    parser.add_argument('--query', help='Search query')
    parser.add_argument('--category', help='Filter by category')
    parser.add_argument('--list-categories', action='store_true')
    args = parser.parse_args()

    if args.list_categories:
        print('Available API categories from PublicAPIs:')
        try:
            data = fetch_json('https://api.publicapis.org/categories')
            for cat in data.get('categories', []):
                print(f'  {cat}')
        except Exception as e:
            print(f'Error: {e}')
            return 1
        return

    print(f'Searching for: {args.query or "all APIs"}')
    print('=' * 60)

    # Always show OpenRouter models (most useful for agents)
    print('\n[OpenRouter Models — free LLM APIs]')
    failed = False
    models = search_openrouter(args.query)
    for m in models:
        if 'error' in m:
            print(f'  Error: {m["error"]}')
            failed = True
            continue
        print(f"  {m['name']}")
        print(f"    {m['description'][:100]}...")
        price = m['price_per_m_output']
        price_label = f'${price:.4f}/M' if price is not None else 'variable/unknown'
        print(f"    context: {m['context_window']} tokens | price: {price_label} output")
        print()

    print('\n[Public APIs]')
    apis = search_public_apis(category=args.category, query=args.query)
    for a in apis:
        if 'error' in a:
            print(f'  Error: {a["error"]}')
            failed = True
            continue
        print(f"  {a['name']} ({a['category']})")
        print(f"    {a['description']}")
        print(f"    {a['url']} | HTTPS: {a['https']} | Auth: {a['auth']}")
        print()
    if not models and not apis:
        print('No APIs found.')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
