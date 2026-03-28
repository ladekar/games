import importlib.util
import os
import json


def load_app():
    here = os.path.dirname(__file__)
    app_path = os.path.join(here, '..', 'webapp', 'app.py')
    app_path = os.path.normpath(app_path)
    spec = importlib.util.spec_from_file_location('webapp_app', app_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_leaderboard_write_and_best_merge(tmp_path):
    # backup existing scores file if present
    mod = load_app()
    app = mod.app
    data_dir = os.path.join(os.path.dirname(mod.__file__), 'data')
    scores_file = os.path.join(data_dir, 'scores.json')

    backup = None
    if os.path.exists(scores_file):
        with open(scores_file, 'rb') as f:
            backup = f.read()

    # ensure clean state
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
    with open(scores_file, 'w') as f:
        json.dump([], f)

    client = app.test_client()

    # submit a score
    r = client.post('/api/score', json={'name': 'lead-test', 'score': 5, 'source': 'tests'})
    assert r.status_code == 200
    # submit a lower score (should not replace)
    r2 = client.post('/api/score', json={'name': 'lead-test', 'score': 3, 'source': 'tests'})
    assert r2.status_code == 200

    # submit a higher score (should replace)
    r3 = client.post('/api/score', json={'name': 'lead-test', 'score': 8, 'source': 'tests'})
    assert r3.status_code == 200

    # read file and assert best is 8
    with open(scores_file, 'r') as f:
        arr = json.load(f)
    found = [e for e in arr if e.get('name') == 'lead-test' and e.get('source') == 'tests']
    assert found and int(found[0].get('score', 0)) == 8

    # cleanup: restore backup or remove file
    if backup is not None:
        with open(scores_file, 'wb') as f:
            f.write(backup)
    else:
        os.remove(scores_file)
