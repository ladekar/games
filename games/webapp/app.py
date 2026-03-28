import os
import sys
import time
import random
import threading
import webbrowser
from flask import Flask, jsonify, render_template, request

# ensure parent folder (games/) is importable
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import puzzles

app = Flask(__name__, template_folder='templates', static_folder='static')

# in-memory store for outstanding questions
QUESTIONS = {}
SCORES_FILE = os.path.join(os.path.dirname(__file__), 'data', 'scores.json')
SCORES_LOCK = threading.Lock()


def ensure_scores_file():
    os.makedirs(os.path.dirname(SCORES_FILE), exist_ok=True)
    if not os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'w') as f:
            f.write('[]')


def make_question(category: str):
    if category == 'riddle':
        item = random.choice(puzzles.RIDDLES)
        return {'prompt': item['q'], 'answer': item['a']}
    if category == 'math':
        item = random.choice(puzzles.MATH_PUZZLES)
        return {'prompt': item['q'], 'answer': str(item['a'])}
    if category == 'scramble':
        word = random.choice(puzzles.SCRAMBLES)
        scrambled = ''.join(random.sample(word, len(word)))
        while scrambled == word:
            scrambled = ''.join(random.sample(word, len(word)))
        return {'prompt': scrambled, 'answer': word}
    if category == 'sequence':
        item = random.choice(puzzles.SEQUENCES)
        return {'prompt': ', '.join(str(x) for x in item['seq']), 'answer': str(item['next'])}
    if category == 'memory':
        item = random.choice(puzzles.MEMORY_ITEMS)
        return {'prompt': str(item), 'answer': str(item), 'show_seconds': 4}
    # random
    cat = random.choice(['riddle', 'math', 'scramble', 'sequence', 'memory'])
    q = make_question(cat)
    q['category'] = cat
    return q


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/brain')
def brain():
    return render_template('game.html')


@app.route('/snake')
def snake():
    return render_template('snake.html')


@app.route('/api/question')
def api_question():
    category = request.args.get('category', 'random')
    q = make_question(category)
    qid = f"{time.time()}-{random.randint(1000,9999)}"
    QUESTIONS[qid] = q['answer']
    payload = {'id': qid, 'prompt': q['prompt']}
    if 'category' in q:
        payload['category'] = q['category']
    if 'show_seconds' in q:
        payload['show_seconds'] = q['show_seconds']
    return jsonify(payload)


@app.route('/api/check', methods=['POST'])
def api_check():
    data = request.get_json(force=True)
    qid = data.get('id')
    ans = str(data.get('answer', '')).strip().lower()
    correct = QUESTIONS.get(qid)
    if correct is None:
        return jsonify({'ok': False, 'error': 'unknown question id'})
    result = str(correct).strip().lower() == ans
    return jsonify({'ok': True, 'result': bool(result), 'answer': correct})


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


@app.route('/api/score', methods=['POST'])
def api_score():
    data = request.get_json(force=True)
    # validate inputs
    raw_name = data.get('name', '')
    if not isinstance(raw_name, str) or not raw_name.strip():
        return jsonify({'ok': False, 'error': 'name required'}), 400
    name = raw_name.strip()[:64]
    # optional source (game identifier)
    source = str(data.get('source', 'snake'))[:32]
    try:
        score = int(data.get('score', 0))
    except Exception:
        return jsonify({'ok': False, 'error': 'invalid score'}), 400

    ensure_scores_file()
    import json
    with SCORES_LOCK:
        with open(SCORES_FILE, 'r') as f:
            arr = json.load(f)
        # maintain best score per (name, source)
        found = False
        for r in arr:
            if r.get('name') == name and r.get('source') == source:
                found = True
                if score > int(r.get('score', 0)):
                    r['score'] = score
                    r['ts'] = time.time()
                break
        if not found:
            arr.append({'name': name, 'score': score, 'ts': time.time(), 'source': source})
        # sort overall and trim
        arr = sorted(arr, key=lambda x: x.get('score', 0), reverse=True)[:1000]
        with open(SCORES_FILE, 'w') as f:
            json.dump(arr, f)
    return jsonify({'ok': True})


@app.route('/api/leaderboard')
def api_leaderboard():
    ensure_scores_file()
    import json
    with SCORES_LOCK:
        with open(SCORES_FILE, 'r') as f:
            arr = json.load(f)
    top = arr[:20]
    return jsonify({'ok': True, 'leaderboard': top})


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run Brain Tease webapp')
    parser.add_argument('port', nargs='?', type=int, help='port to run on')
    parser.add_argument('--host', default=os.environ.get('HOST', '127.0.0.1'))
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--open', action='store_true', help='Open browser when server is ready')
    args = parser.parse_args()

    port = args.port or int(os.environ.get('PORT', 5000))

    # find a free port if requested port is in use
    import socket

    def find_available_port(host, start_port, max_tries=100):
        for p in range(start_port, start_port + max_tries):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind((host, p))
                    return p
                except OSError:
                    continue
        # fallback: ask OS for an available port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, 0))
            return s.getsockname()[1]

    chosen_port = find_available_port(args.host, port)
    if chosen_port != port:
        print(f'Port {port} is in use; starting server on available port {chosen_port}')

    def open_when_ready(host, port):
        url = f'http://{host}:{port}/'
        for _ in range(30):
            try:
                import urllib.request
                with urllib.request.urlopen(url, timeout=1) as r:
                    if r.status == 200:
                        webbrowser.open(url)
                        return
            except Exception:
                time.sleep(0.2)

    if args.open:
        t = threading.Thread(target=open_when_ready, args=(args.host, chosen_port), daemon=True)
        t.start()

    app.run(host=args.host, port=chosen_port, debug=args.debug)
