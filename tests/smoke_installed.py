"""Run with `python -I tests/smoke_installed.py` after installing the wheel."""

from importlib.metadata import entry_points
from pathlib import Path
import sys

import hermes_exploration as exploration


assert Path(sys.prefix) in Path(exploration.__file__).parents
points = entry_points()
plugins = points.select(group='hermes_agent.plugins') if hasattr(points, 'select') else points.get('hermes_agent.plugins', [])
entry = next(ep for ep in plugins if ep.name == 'exploration')
assert entry.load() is exploration.register
plugin = exploration._get_plugin()
assert plugin is not None
assert plugin.read_only
assert plugin.search('scraping')
assert 'Usage:' in exploration._handle_explore('')
assert 'discoveries' in exploration._handle_explore('scraping')
assert 'No discoveries' in exploration._handle_explore('synthetic-no-match-1234')
print('Installed wheel: entry point, bundled registry, help, search, and no-match passed')
