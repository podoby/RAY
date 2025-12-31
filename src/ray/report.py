import json
from datetime import datetime

def render_markdown_report(result: dict) -> str:
    lines = []
    lines.append(f"# Ray Report ({datetime.utcnow().isoformat()} UTC)")
    lines.append("")
    lines.append(f"## Summary\n{result['finding_summary']}")
    lines.append("")
    lines.append(f"## Risk\n**{result['risk']}**")
    lines.append("")
    lines.append("## Evidence")
    for e in result["evidence"]:
        lines.append(f"- {e}")
    lines.append("")
    lines.append("## Recommended Actions")
    for a in result["recommended_actions"]:
        lines.append(f"- {a}")
    lines.append("")
    lines.append("## Validation Steps")
    for v in result["validation_steps"]:
        lines.append(f"- {v}")
    lines.append("")
    lines.append("## References")
    for r in result["references"]:
        lines.append(f"- {r}")
    lines.append("")
    lines.append("## Raw JSON")
    lines.append("```json")
    lines.append(json.dumps(result, indent=2))
    lines.append("```")
    return "\n".join(lines)