#!/usr/bin/env python3
"""
discover_models.py — Find and compare LLM models

Usage:
    python3 discover_models.py --provider openrouter
    python3 discover_models.py --compare "claude-3.5-sonnet" "gpt-4o" "gemini-1.5-pro"
    python3 discover_models.py --task coding --max-price 1.00
"""

import argparse
import json
import urllib.request

PROVIDERS = {
    'openrouter': 'https://openrouter.ai/api/v1/models',
    'groq': 'https://api.groq.com/openai/v1/models',
}


def fetch_json(url: str, headers: dict = None, timeout: int = 15) -> dict:
    req = urllib.request.Request(url, headers={
        'User-Agent': 'exploration-plugin/1.0',
        **(headers or {})
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def list_openrouter_models() -> list[dict]:
    """List all OpenRouter models with pricing and context."""
    data = fetch_json(PROVIDERS['openrouter'])
    models = []
    for m in data.get('data', []):
        pricing = m.get('pricing', {}) or {}
        models.append({
            'id': m.get('id', ''),
            'name': m.get('name', ''),
            'description': m.get('description', '')[:200],
            'context_length': m.get('context_length', 0),
            'price_input': pricing.get('prompt', 0),
            'price_output': pricing.get('completion', 0),
            'supports_vision': m.get('supports_vision', False),
            'supports_function_calling': m.get('supports_function_calling', False),
            'supports_streaming': m.get('supports_streaming', True),
        })
    return sorted(models, key=lambda x: x['price_output'])


def list_groq_models() -> list[dict]:
    """List all Groq models."""
    data = fetch_json(PROVIDERS['groq'], headers={'Authorization': 'Bearer dummy'})
    # Groq doesn't need auth for listing — it's just metadata
    models = []
    for m in data.get('data', []):
        models.append({
            'id': m.get('id', ''),
            'name': m.get('id', ''),
            'context_length': m.get('context_window', 0),
        })
    return sorted(models, key=lambda x: x['id'])


def compare_models(model_ids: list[str]) -> dict:
    """Compare specific models by fetching from OpenRouter."""
    models = list_openrouter_models()
    found = {m['id'].lower(): m for m in models}
    results = []
    for mid in model_ids:
        for m in models:
            if mid.lower() in m['id'].lower():
                results.append(m)
                break
        else:
            results.append({'id': mid, 'error': 'not found on OpenRouter'})
    return results


def filter_by_task(models: list[dict], task: str = None, max_price: float = None) -> list[dict]:
    """Filter models by task type or max price."""
    if task:
        task_keywords = {
            'coding': ['code', 'claude', 'gpt-4', 'gemini'],
            'reasoning': ['o1', 'o3', 'deepseek', 'r1'],
            'vision': ['vision', 'claude', 'gpt-4o', 'gemini'],
            'fast': ['fast', 'haiku', 'mini', 'flash'],
            'cheap': ['free', '0.00'],
        }
        keywords = task_keywords.get(task.lower(), [task.lower()])
        models = [m for m in models if any(k in m['id'].lower() for k in keywords)]

    if max_price:
        models = [m for m in models if m.get('price_output', 999) <= max_price]

    return models


def main():
    parser = argparse.ArgumentParser(description='LLM Model Discovery')
    parser.add_argument('--provider', choices=['openrouter', 'groq', 'all'], default='openrouter')
    parser.add_argument('--compare', nargs='+', help='Compare specific model IDs')
    parser.add_argument('--task', help='Filter by task: coding, reasoning, vision, fast, cheap')
    parser.add_argument('--max-price', type=float, help='Max price per M output tokens')
    parser.add_argument('--top', type=int, default=20, help='Number of results')
    args = parser.parse_args()

    if args.compare:
        print(f'Comparing: {args.compare}')
        print('=' * 70)
        results = compare_models(args.compare)
        for m in results:
            if 'error' in m:
                print(f"  {m['id']}: {m['error']}")
                continue
            print(f"\n  {m['name']}")
            print(f"    context: {m['context_length']:,} tokens")
            print(f"    price: ${m['price_input']:.6f}/M in, ${m['price_output']:.6f}/M out")
            features = []
            if m.get('supports_vision'): features.append('vision')
            if m.get('supports_function_calling'): features.append('function_calling')
            if m.get('supports_streaming'): features.append('streaming')
            if features:
                print(f"    features: {', '.join(features)}")
        return

    if args.provider in ('openrouter', 'all'):
        print('[OpenRouter Models]')
        print('=' * 70)
        models = list_openrouter_models()
        if args.task or args.max_price:
            models = filter_by_task(models, args.task, args.max_price)
        for m in models[:args.top]:
            print(f"\n  {m['name']}")
            print(f"    {m['description'][:120]}...")
            print(f"    context: {m['context_length']:,} tokens | ${m['price_output']:.4f}/M out")
            feats = [f for f in ['vision', 'function_calling', 'streaming'] if m.get(f'supports_{f}')]
            if feats:
                print(f"    {', '.join(feats)}")

    if args.provider == 'groq':
        print('[Groq Models]')
        print('=' * 70)
        models = list_groq_models()
        for m in models[:args.top]:
            print(f"  {m['name']} | context: {m['context_length']:,}")


if __name__ == '__main__':
    main()
