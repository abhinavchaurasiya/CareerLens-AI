# CareerLens AI — 7th Semester 5-Star Project

A Career & Placement Intelligence System for B.Tech CS (DS+AI).

## Features
- PDF/TXT resume upload
- Resume text extraction
- Explainable skill extraction
- Profile score
- Hybrid job matching: 75% skill overlap + 25% text cosine similarity
- Skill-gap detection
- Job-role dashboard
- Career assistant
- SQLite database
- Responsive premium frontend
- Dark/light theme
- No AI API key required

## Run
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Test
Open http://127.0.0.1:5000/health

## Viva
Explain Flask, SQLite, PDF extraction, skill dictionary, cosine similarity, hybrid scoring, skill-gap recommendation and how embeddings/real job APIs could improve the system.
