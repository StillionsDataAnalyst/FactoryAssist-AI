from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

DATA_FILE = Path(__file__).parent / "data" / "reaction_plans.json"

app = FastAPI(
    title="FactoryAssist AI API",
    version="0.1.0",
    description="MVP API for approved manufacturing reaction plans.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this before production.
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class IssueRequest(BaseModel):
    equipment_id: str = Field(min_length=2, max_length=40)
    problem: str = Field(min_length=3, max_length=1000)


def load_plans() -> list[dict[str, Any]]:
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def score_plan(problem: str, plan: dict[str, Any]) -> int:
    normalized = problem.lower()
    return sum(1 for keyword in plan["keywords"] if keyword.lower() in normalized)


@app.get("/")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "FactoryAssist AI"}


@app.get("/reaction-plans")
def list_reaction_plans() -> list[dict[str, Any]]:
    return load_plans()


@app.post("/ask")
def ask(request: IssueRequest) -> dict[str, Any]:
    plans = load_plans()
    ranked = sorted(
        ((score_plan(request.problem, plan), plan) for plan in plans),
        key=lambda item: item[0],
        reverse=True,
    )

    best_score, best_plan = ranked[0]

    if best_score == 0:
        return {
            "equipment_id": request.equipment_id,
            "status": "needs_clarification",
            "message": (
                "I could not match this issue to an approved reaction plan. "
                "Stop if an immediate safety risk exists and contact the supervisor "
                "or maintenance team."
            ),
            "questions": [
                "What alarm or code is displayed?",
                "What sound, smell, leak, or motion changed?",
            ],
        }

    return {
        "equipment_id": request.equipment_id,
        "status": "matched",
        **best_plan,
        "disclaimer": (
            "Use this guidance only with your site's approved procedures. "
            "Do not bypass guards, interlocks, or lockout/tagout requirements."
        ),
    }
