# pandai — small collection of games

This repository contains a few small Python games and a web UI:

- `games/brain_tease.py` — CLI brain-teaser game (riddles, math, scramble, memory, timed rounds).
- `games/webapp/` — Flask web UI and a simple Snake canvas game with leaderboard.

Quick start (dev):

```bash
# create and activate a venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r games/requirements.txt

# run the web UI (auto-picks free port if port in use)
python3 games/webapp/app.py 5000

# run the CLI game
python3 games/brain_tease.py
```

See `games/README.md` for more details about the individual games.
