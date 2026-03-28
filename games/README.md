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
