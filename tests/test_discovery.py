import importlib.util
from pathlib import Path
import sys
import subprocess
import urllib.error

import pytest


def script(name):
    path = Path(__file__).resolve().parents[1] / 'scripts' / (name + '.py')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def public_api():
    return {'entries': [{'API': 'Fixture API', 'Description': 'Synthetic test catalog',
                         'Link': 'https://example.test', 'Category': 'Tests',
                         'HTTPS': True, 'Auth': '', 'Cors': 'yes'}]}


@pytest.fixture
def models():
    return {'data': [
        {'id': 'fixture/paid', 'name': 'Paid', 'pricing': {'prompt': '0.000001', 'completion': '0.000002'}},
        {'id': 'fixture/free', 'name': 'Free', 'pricing': {'prompt': '0', 'completion': '0'}},
    ]}


def test_tools_cli_success_and_empty(monkeypatch, capsys, public_api):
    tools = script('discover_tools')
    monkeypatch.setattr(tools, 'fetch_json', lambda url: public_api)
    monkeypatch.setattr(sys, 'argv', ['discover_tools.py', '--query', 'fixture'])
    assert tools.main() == 0
    assert 'HTTPS: True' in capsys.readouterr().out
    monkeypatch.setattr(tools, 'fetch_json', lambda url: {'entries': []})
    assert tools.main() == 0
    assert 'No tools found' in capsys.readouterr().out


@pytest.mark.parametrize('module_name', ['discover_tools', 'discover_apis'])
def test_catalog_failure_reports_nonzero(monkeypatch, capsys, module_name):
    module = script(module_name)
    def fail(url):
        raise urllib.error.URLError('synthetic unavailable')
    monkeypatch.setattr(module, 'fetch_json', fail)
    monkeypatch.setattr(sys, 'argv', [module_name + '.py'])
    assert module.main() == 1
    assert 'synthetic unavailable' in capsys.readouterr().out


def test_api_models_use_object_pricing_and_provider_id(monkeypatch, models):
    api = script('discover_apis')
    monkeypatch.setattr(api, 'fetch_json', lambda url: models)
    results = api.search_openrouter()
    assert results[0]['price_per_m_output'] == 2
    assert results[0]['id'] == 'fixture/paid'
    assert results[0]['url'] == 'https://openrouter.ai/fixture/paid'


def test_api_name_search_and_cors_is_not_free_pricing(monkeypatch, public_api):
    api = script('discover_apis')
    monkeypatch.setattr(api, 'fetch_json', lambda url: public_api)
    assert api.search_public_apis(query='fixture')[0]['pricing'] == 'unknown'


def test_models_prices_sort_filter_zero_and_compare(monkeypatch, models):
    model = script('discover_models')
    monkeypatch.setattr(model, 'fetch_json', lambda url: models)
    results = model.list_openrouter_models()
    assert [item['id'] for item in results] == ['fixture/free', 'fixture/paid']
    assert results[1]['price_input'] == 1
    assert results[1]['price_output'] == 2
    assert model.filter_by_task(results, max_price=0) == [results[0]]
    assert model.filter_by_task(results, task='cheap') == [results[0]]
    assert model.compare_models(['fixture/paid', 'absent'])[1]['error']


def test_groq_missing_key_does_not_make_request(monkeypatch):
    model = script('discover_models')
    monkeypatch.delenv('GROQ_API_KEY', raising=False)
    monkeypatch.setattr(model, 'fetch_json', lambda *a, **k: pytest.fail('network should not be called'))
    with pytest.raises(ValueError, match='GROQ_API_KEY'):
        model.list_groq_models()


def test_all_provider_branch_uses_both(monkeypatch, capsys):
    model = script('discover_models')
    monkeypatch.setattr(model, 'list_openrouter_models', lambda: [])
    monkeypatch.setattr(model, 'list_groq_models', lambda: [])
    monkeypatch.setattr(sys, 'argv', ['discover_models.py', '--provider', 'all'])
    model.main()
    out = capsys.readouterr().out
    assert '[OpenRouter Models]' in out and '[Groq Models]' in out


@pytest.mark.parametrize('args', [['--top', '0'], ['--max-price', '-1'], ['--max-price', 'nan']])
def test_invalid_model_args_fail_before_network(monkeypatch, args):
    model = script('discover_models')
    monkeypatch.setattr(sys, 'argv', ['discover_models.py'] + args)
    with pytest.raises(SystemExit) as error:
        model.main()
    assert error.value.code == 2


@pytest.mark.parametrize('price', [None, '-1', 'NaN', 'Infinity', 'unknown', '', '1e308'])
def test_unknown_and_dynamic_prices_are_not_numeric(monkeypatch, price):
    data = {'data': [{'id': 'fixture/dynamic', 'name': 'Router',
                     'pricing': {'prompt': price, 'completion': price}}]}
    model = script('discover_models')
    monkeypatch.setattr(model, 'fetch_json', lambda url: data)
    results = model.list_openrouter_models()
    assert results[0]['price_input'] is None and results[0]['price_output'] is None
    assert model.format_price(results[0]['price_output']) == 'variable/unknown'
    assert model.filter_by_task(results, max_price=100) == []
    assert model.filter_by_task(results, task='cheap') == []
    api = script('discover_apis')
    monkeypatch.setattr(api, 'fetch_json', lambda url: data)
    assert api.search_openrouter()[0]['price_per_m_output'] is None


def test_api_cli_displays_unknown_price(monkeypatch, capsys):
    api = script('discover_apis')
    monkeypatch.setattr(api, 'fetch_json', lambda url: {
        'data': [{'id': 'fixture/router', 'name': 'Router', 'pricing': {'completion': '-1'}}],
        'entries': [],
    })
    monkeypatch.setattr(sys, 'argv', ['discover_apis.py'])
    assert api.main() == 0
    output = capsys.readouterr().out
    assert 'variable/unknown' in output
    assert '$-' not in output


def test_scan_missing_and_empty_fixture(monkeypatch, tmp_path):
    tools = script('discover_tools')
    assert 'error' in tools.scan_repo(str(tmp_path / 'missing'))
    assert not tools.scan_repo(str(tmp_path))['services']
    (tmp_path / 'package.json').write_text('{"dependencies":{"fixture":"1"}}', encoding='utf-8')
    assert tools.scan_repo(str(tmp_path))['packages'] == ['fixture']


@pytest.mark.parametrize('module_name', ['discover_tools', 'discover_apis', 'discover_models'])
def test_real_cli_provider_failure_is_nonzero_without_traceback(module_name):
    path = Path(__file__).resolve().parents[1] / 'scripts' / (module_name + '.py')
    code = '''
import runpy, sys, urllib.error
from unittest.mock import patch
sys.argv = [sys.argv[1]]
with patch('urllib.request.urlopen', side_effect=urllib.error.URLError('synthetic outage')):
    runpy.run_path(sys.argv[0], run_name='__main__')
'''
    process = subprocess.run([sys.executable, '-I', '-c', code, str(path)], capture_output=True, text=True)
    assert process.returncode == 1
    assert 'synthetic outage' in process.stdout + process.stderr
    assert 'Traceback' not in process.stdout + process.stderr
