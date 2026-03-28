"""Small CLI helper to submit a score to the local Pandai webapp leaderboard.

Usage:
  python3 submit_score.py --name "Player" --score 12 --port 5000 --source snake
"""
import argparse
import json
import urllib.request

def submit(name, score, host='127.0.0.1', port=5000, source='snake'):
    url = f'http://{host}:{port}/api/score'
    payload = json.dumps({'name': name, 'score': score, 'source': source}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req, timeout=5) as r:
        print(r.read().decode())

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--name', required=True)
    p.add_argument('--score', required=True, type=int)
    p.add_argument('--host', default='127.0.0.1')
    p.add_argument('--port', default=5000, type=int)
    p.add_argument('--source', default='snake')
    args = p.parse_args()
    submit(args.name, args.score, args.host, args.port, args.source)

if __name__ == '__main__':
    main()
