from __future__ import annotations


def build_validation_schema() -> dict:
    section_score = {
        "type": "object",
        "properties": {
            "section": {"type": "string"},
            "score": {"type": "number"},
            "status": {"type": "string"},
            "summary": {"type": "string"},
            "evidence": {
                "type": "array",
                "items": {"type": "string"},
            },
            "gaps": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["section", "score", "status", "summary", "evidence", "gaps"],
        "additionalProperties": False,
    }

    requirement_check = {
        "type": "object",
        "properties": {
            "requirement": {"type": "string"},
            "satisfied": {"type": "boolean"},
            "confidence": {"type": "number"},
            "evidence": {
                "type": "array",
                "items": {"type": "string"},
            },
            "notes": {"type": "string"},
        },
        "required": ["requirement", "satisfied", "confidence", "evidence", "notes"],
        "additionalProperties": False,
    }

    return {
        "name": "planning_validation_report",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "overall_score": {"type": "number"},
                "verdict": {"type": "string"},
                "summary": {"type": "string"},
                "section_scores": {
                    "type": "array",
                    "items": section_score,
                },
                "requirement_checks": {
                    "type": "array",
                    "items": requirement_check,
                },
                "major_risks": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "recommended_actions": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
            "required": [
                "title",
                "overall_score",
                "verdict",
                "summary",
                "section_scores",
                "requirement_checks",
                "major_risks",
                "recommended_actions",
            ],
            "additionalProperties": False,
        },
    }
