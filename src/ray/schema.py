RAY_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "finding_summary": {"type": "string"},
        "risk": {"type": "string", "enum": ["Low", "Medium", "High", "Critical"]},
        "evidence": {"type": "array", "items": {"type": "string"}},
        "recommended_actions": {"type": "array", "items": {"type": "string"}},
        "validation_steps": {"type": "array", "items": {"type": "string"}},
        "references": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "finding_summary",
        "risk",
        "evidence",
        "recommended_actions",
        "validation_steps",
        "references",
    ],
    "additionalProperties": False,
}