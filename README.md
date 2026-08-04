# FactoryAssist AI

FactoryAssist AI is a manufacturing reaction-plan assistant that helps operators and maintenance teams respond safely and consistently to equipment issues.

## MVP features

- Clickable investor and executive demo
- Equipment selection
- Structured reaction plans
- Safety and escalation guidance
- Sample maintenance history
- Manager reliability dashboard
- FastAPI backend with sample reaction-plan matching

## Project structure

```text
FactoryAssist-AI/
├── frontend/
│   └── index.html
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   └── data/
│   │       └── reaction_plans.json
│   └── requirements.txt
├── docs/
│   ├── DEMO_SCRIPT.md
│   └── PILOT_PLAN.md
├── .gitignore
└── README.md
```

## Run the clickable prototype

Open `frontend/index.html` in a browser.

## Run the API

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then visit:

- API health: `http://127.0.0.1:8000/`
- API docs: `http://127.0.0.1:8000/docs`

## Example request

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"equipment_id":"PRESS-004","problem":"The press is losing pressure"}'
```

## Suggested GitHub repository name

`FactoryAssist-AI`

## Recommended next milestones

1. Replace sample matching with an approved knowledge retrieval system.
2. Add user authentication and tenant separation.
3. Store equipment and incident records in PostgreSQL.
4. Add document upload and source citations.
5. Pilot with one production line and measure response time.
