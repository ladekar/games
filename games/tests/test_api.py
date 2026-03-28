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
    return mod.app


def test_question_and_check():
    app = load_app()
    client = app.test_client()

    # request a question
    r = client.get('/api/question?category=riddle')
    assert r.status_code == 200
    q = r.get_json()
    assert 'id' in q and 'prompt' in q

    # check with wrong answer
    payload = {'id': q['id'], 'answer': 'wrong-answer'}
    r2 = client.post('/api/check', json=payload)
    assert r2.status_code == 200
    res = r2.get_json()
    assert res.get('ok') is True and 'result' in res


def test_score_submission_validation():
    app = load_app()
    client = app.test_client()

    # missing name should return 400
    r = client.post('/api/score', json={'score': 5})
    assert r.status_code == 400

    # valid submission
    r2 = client.post('/api/score', json={'name': 'pytest-user', 'score': 2, 'source': 'tests'})
    assert r2.status_code == 200
    data = r2.get_json()
    assert data.get('ok') is True
