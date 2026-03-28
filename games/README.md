# Brain Tease & Mindset — Games folder

This folder contains a terminal brain-teaser game.
# Brain Tease & Mindset — Games folder

This folder contains a terminal brain-teaser game.

Run

```bash
cd pandai
python3 games/brain_tease.py
```

Files
- `brain_tease.py`: main CLI game
- `puzzles.py`: puzzle data

Features
- Timed round mode (choose number of questions and seconds per question).

Web UI
- A small Flask-based web UI is available under `games/webapp`.
- Install dependencies and run:

```bash
pip install -r games/requirements.txt
python3 games/webapp/app.py
```

Then open http://127.0.0.1:5000 in your browser.

Docker
```bash
cd games/webapp
docker build -t pandai-webapp .
docker run -p 5000:5000 pandai-webapp
```

Production (Gunicorn)
```bash
# build the production image (uses Dockerfile.prod)
cd games/webapp
docker build -f Dockerfile.prod -t pandai-webapp:prod .

# run on port 8000
docker run -p 8000:8000 pandai-webapp:prod

# the app will be available at http://127.0.0.1:8000
```

CLI Auto-submit
```bash
# run CLI and auto-submit final score when it beats current best
python3 games/brain_tease.py --auto-submit --submit-host 127.0.0.1 --submit-port 5000 --submit-source brain-tease

# interactive mode will prompt for a display name (or set $USER in env)
```
