import importlib.util
import os


def load_app_mod():
    here = os.path.dirname(__file__)
    app_path = os.path.join(here, '..', 'webapp', 'app.py')
    app_path = os.path.normpath(app_path)
    spec = importlib.util.spec_from_file_location('webapp_app', app_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_health_and_leaderboard():
    mod = load_app_mod()
    app = getattr(mod, 'app')
    client = app.test_client()

    r = client.get('/health')
    assert r.status_code == 200
    data = r.get_json()
    assert data and data.get('status') == 'ok'

    r = client.get('/api/leaderboard')
    assert r.status_code == 200
    data = r.get_json()
    assert data and data.get('ok') is True
