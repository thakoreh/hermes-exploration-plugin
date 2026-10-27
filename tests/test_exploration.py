import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

import hermes_exploration as exploration


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def registry(tmp_path, monkeypatch):
    (tmp_path / 'registry.json').write_text(json.dumps({
        'tools': [{'name': 'Synthetic scraper', 'description': 'Read synthetic web pages', 'pricing': 'free'}],
        'apis': [], 'models': [],
    }), encoding='utf-8')
    monkeypatch.setenv('EXPLORATION_PLUGIN_PATH', str(tmp_path))
    return tmp_path


def test_directory_plugin_loads_without_pip_dependencies(tmp_path):
    plugin = tmp_path / 'plugins' / 'hermes-exploration-plugin'
    plugin.mkdir(parents=True)
    for name in ('__init__.py', 'plugin.yaml', 'registry.json'):
        shutil.copy(ROOT / name, plugin / name)
    shutil.copytree(ROOT / 'hermes_exploration', plugin / 'hermes_exploration', ignore=shutil.ignore_patterns('__pycache__'))
    # Hermes loads a directory as a package, rather than adding it to sys.path.
    script = '''
import importlib.util, sys
from pathlib import Path
path = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location('hermes_plugin_exploration', path / '__init__.py', submodule_search_locations=[str(path)])
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
class Context:
    def register_hook(self, *args): pass
    def register_command(self, name, handler, **kwargs):
        assert name == 'explore'
        assert kwargs['args_hint'] == '<query>'
        assert 'Usage:' in handler('')
        assert 'discoveries' in handler('scraping')
module.register(Context())
'''
    proc = subprocess.run([sys.executable, '-I', '-S', '-c', script, str(plugin)], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr


def test_source_registry_is_found(monkeypatch):
    monkeypatch.delenv('EXPLORATION_PLUGIN_PATH', raising=False)
    monkeypatch.setattr(Path, 'expanduser', lambda self: self)
    assert exploration._get_plugin().search('scraping')


def test_empty_help_search_pricing_and_repeat(registry):
    assert '1 tools' in exploration._handle_explore('')
    assert 'Synthetic scraper (free)' in exploration._handle_explore('scraper')
    assert 'No discoveries' in exploration._handle_explore('not-present')
    assert 'Synthetic scraper (free)' in exploration._handle_explore('scraper')


def test_explicit_missing_path_does_not_fall_back(tmp_path, monkeypatch):
    monkeypatch.setenv('EXPLORATION_PLUGIN_PATH', str(tmp_path / 'missing'))
    assert 'registry not found' in exploration._handle_explore('x')
    assert not (tmp_path / 'missing').exists()


@pytest.mark.parametrize('content', ['{', '[]', '{"tools": null}', '{"apis": [42]}'])
def test_corrupt_registry_reports_error_without_overwriting(registry, content):
    path = registry / 'registry.json'
    path.write_text(content, encoding='utf-8')
    assert 'Could not read' in exploration._handle_explore('x')
    assert path.read_text(encoding='utf-8') == content


def test_readonly_missing_registry_does_not_create_files(tmp_path):
    path = tmp_path / 'missing'
    plugin = exploration.ExplorationPlugin(str(path), read_only=True)
    assert not path.exists()
    assert 'push disabled' in plugin.push_changes()['error']


def test_empty_registry(registry):
    (registry / 'registry.json').write_text('{}', encoding='utf-8')
    assert '0 tools' in exploration._handle_explore('')
    assert 'No discoveries' in exploration._handle_explore('x')


def test_search_limits_types_and_unicode(registry):
    plugin = exploration.ExplorationPlugin(str(registry))
    assert plugin.search('scraper', limit=0) == []
    assert plugin.search('scraper', discovery_type='api') == []
    with pytest.raises(ValueError):
        plugin.search('x', discovery_type='invalid')
    with pytest.raises(ValueError):
        plugin.search('x', limit=-1)
    plugin._write_registry({'tools': [{'name': 'Café', 'description': 'UTF-8 fixture'}]})
    assert plugin.search('café')[0]['name'] == 'Café'


def test_interrupted_and_repeated_sessions_cleanup(registry):
    exploration._session_tools.clear()
    exploration._session_suggestions.clear()
    exploration._on_post_tool_call(tool_name='scraper', session_id='fixture')
    exploration._on_post_tool_call(tool_name='scraper', session_id='fixture')
    assert exploration._session_tools['fixture'] == ['scraper']
    exploration._on_session_end(session_id='fixture')
    assert exploration._session_suggestions['fixture']
    exploration._on_post_tool_call(tool_name='scraper', session_id='fixture')
    exploration._on_session_end(session_id='fixture', interrupted=True)
    assert 'fixture' not in exploration._session_tools
    assert 'fixture' not in exploration._session_suggestions
    exploration._on_post_tool_call(tool_name='scraper', task_id='task-only')
    exploration._on_session_end(task_id='task-only', completed=False)
    assert 'task-only' not in exploration._session_tools
