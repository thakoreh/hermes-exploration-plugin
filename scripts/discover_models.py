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
import math
import os
import sys
import urllib.request
import urllib.error

PROVIDERS = {
    'openrouter': 'https://openrouter.ai/api/v1/models',
    'groq': 'https://api.groq.com/openai/v1/models',
}


def price_per_million(value):
    """Negative routing sentinels and absent/nonfinite rates are not fixed prices."""
    if value is None:
        return None
    try:
        price = float(value) * 1_000_000
    except (ValueError, TypeError):
        return None
    return price if math.isfinite(price) and price >= 0 else None


def format_price(value, precision=4):
    return f'${value:.{precision}f}/M' if value is not None else 'variable/unknown'


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
        if not isinstance(pricing, dict):
            raise ValueError('model pricing must be an object')
        models.append({
            'id': m.get('id', ''),
            'name': m.get('name', ''),
            'description': m.get('description', '')[:200],
            'context_length': m.get('context_length', 0),
            'price_input': price_per_million(pricing.get('prompt')),
            'price_output': price_per_million(pricing.get('completion')),
            'supports_vision': m.get('supports_vision', False),
            'supports_function_calling': m.get('supports_function_calling', False),
            'supports_streaming': m.get('supports_streaming', True),
        })
    return sorted(models, key=lambda x: (x['price_output'] is None, x['price_output'] or 0))


def list_groq_models() -> list[dict]:
    """List all Groq models."""
    key = os.getenv('GROQ_API_KEY')
    if not key:
        raise ValueError('GROQ_API_KEY is required for Groq model metadata')
    data = fetch_json(PROVIDERS['groq'], headers={'Authorization': f'Bearer {key}'})
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
        models = [m for m in models if (m.get('price_output') == 0 if task.lower() == 'cheap'
                  else any(k in m['id'].lower() for k in keywords))]

    if max_price is not None:
        models = [m for m in models if m.get('price_output') is not None and m['price_output'] <= max_price]

    return models


def main():
    parser = argparse.ArgumentParser(description='LLM Model Discovery')
    parser.add_argument('--provider', choices=['openrouter', 'groq', 'all'], default='openrouter')
    parser.add_argument('--compare', nargs='+', help='Compare specific model IDs')
    parser.add_argument('--task', help='Filter by task: coding, reasoning, vision, fast, cheap')
    parser.add_argument('--max-price', type=float, help='Max price per M output tokens')
    parser.add_argument('--top', type=int, default=20, help='Number of results')
    args = parser.parse_args()
    if args.max_price is not None and (not math.isfinite(args.max_price) or args.max_price < 0):
        parser.error('--max-price must be finite and non-negative')
    if args.top < 1:
        parser.error('--top must be positive')

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
            print(f"    price: {format_price(m['price_input'], 6)} in, {format_price(m['price_output'], 6)} out")
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
            print(f"    context: {m['context_length']:,} tokens | {format_price(m['price_output'])} out")
            feats = [f for f in ['vision', 'function_calling', 'streaming'] if m.get(f'supports_{f}')]
            if feats:
                print(f"    {', '.join(feats)}")

    if args.provider in ('groq', 'all'):
        print('[Groq Models]')
        print('=' * 70)
        models = list_groq_models()
        for m in models[:args.top]:
            print(f"  {m['name']} | context: {m['context_length']:,}")


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        raise SystemExit(1)
