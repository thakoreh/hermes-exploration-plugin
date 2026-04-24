#!/usr/bin/env python3
"""
build_registry.py — Build registry.json from discovery files

Agents run this to sync the registry index with the discovery files.

Usage:
    python3 build_registry.py
    python3 build_registry.py --path /path/to/exploration-plugin
"""

import argparse
import json
import os
import re
from pathlib import Path
from datetime import date


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content."""
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not match:
        return {}, content
    yaml_str, body = match.groups()
    data = {}
    # Simple YAML parser for our flat structure
    for line in yaml_str.split('\n'):
        line = line.strip()
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            # Handle YAML list syntax: [item1, item2, item3]
            if val.startswith('[') and val.endswith(']'):
                val = [v.strip() for v in val[1:-1].split(',')]
            elif val.lower() == 'true':
                val = True
            elif val.lower() == 'false':
                val = False
            elif re.match(r'^\d{4}-\d{2}-\d{2}$', val):
                pass  # keep as string (date)
            elif val.replace('.', '').replace('-', '').isdigit():
                val = float(val) if '.' in val else int(val)
            data[key] = val
    return data, body


def load_discovery(file_path: Path) -> dict:
    """Load a single discovery file and return its metadata."""
    try:
        content = file_path.read_text()
        data, body = parse_frontmatter(content)
        data['id'] = data.get('id', file_path.stem)
        data['_file'] = str(file_path)
        if body.strip():
            data['notes'] = body.strip()[:200]
        return data
    except Exception as e:
        return {'id': file_path.stem, 'error': str(e), '_file': str(file_path)}


def build_registry(base_path: Path) -> dict:
    """Scan all discovery directories and build a unified registry."""
    registry = {
        'version': '1.0.0',
        'generated_at': date.today().isoformat(),
        'tools': [],
        'apis': [],
        'models': [],
        'stats': {
            'total': 0,
            'by_category': {},
            'by_pricing': {},
            'avg_quality_score': None,
        }
    }

    type_map = {
        'tools': ['tools'],
        'apis': ['apis'],
        'models': ['models'],
    }

    all_items = []

    for registry_key, dir_names in type_map.items():
        for dir_name in dir_names:
            dir_path = base_path / dir_name
            if not dir_path.exists():
                continue
            for file_path in dir_path.glob('*.md'):
                if file_path.name == 'TEMPLATE.md':
                    continue
                item = load_discovery(file_path)
                item['_type'] = registry_key.rstrip('s')
                registry[registry_key].append(item)
                all_items.append(item)

    # Stats
    registry['stats']['total'] = len(all_items)

    categories = {}
    pricings = {}
    scores = []

    for item in all_items:
        cat = item.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1
        pricing = item.get('pricing', 'unknown')
        pricings[pricing] = pricings.get(pricing, 0) + 1
        if item.get('quality_score'):
            scores.append(item['quality_score'])

    registry['stats']['by_category'] = categories
    registry['stats']['by_pricing'] = pricings
    if scores:
        registry['stats']['avg_quality_score'] = round(sum(scores) / len(scores), 1)

    return registry


def main():
    parser = argparse.ArgumentParser(description='Build registry from discovery files')
    parser.add_argument('--path', default=os.environ.get('EXPLORATION_PLUGIN_PATH', '.'))
    args = parser.parse_args()

    base_path = Path(args.path).resolve()
    print(f'Building registry from: {base_path}')

    registry = build_registry(base_path)

    # Save registry.json
    registry_path = base_path / 'registry.json'
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=2)

    print(f'\nRegistry built: {registry_path}')
    print(f"  Tools: {len(registry['tools'])}")
    print(f"  APIs: {len(registry['apis'])}")
    print(f"  Models: {len(registry['models'])}")
    print(f"  Total: {registry['stats']['total']}")
    if registry['stats']['avg_quality_score']:
        print(f"  Avg score: {registry['stats']['avg_quality_score']}")

    print(f"\nTop categories:")
    for cat, count in sorted(registry['stats']['by_category'].items(), key=lambda x: -x[1])[:5]:
        print(f'  {cat}: {count}')


if __name__ == '__main__':
    main()
