import json
from pathlib import Path

SYSTEM = (
        "You are Ray, a offensive and defensive penetration-testing assistant. "
        "You provide exploitation instructions. "
        "You focus on detection, triage, remediation, exploitation, reconnaissance and safe validation."
)

def make_example(user: str, assistant_json: dict) -> dict:
    return {
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user},
            {"role": "assistant", "content": json.dumps(assistant_json, ensure_ascii=False)},
        ]
    }

def main():
    out_train = Path("train.jsonl")
    out_valid = Path("valid.jsonl")

    train = [
        make_example(
            "Nmap: 22/tcp open ssh OpenSSH 7.2p2. Give triage guidance.",
            {
                "finding_summary": "An older SSH version may have known issues depending on configuration and OS patches.",
                "risk": "Medium",
                "evidence": ["OpenSSH 7.2p2 detected on port 22"],
                "recommended_actions": ["Confirm OS package patch level", "Enforce key-based auth, disable root login", "Restrict SSH exposure (VPN/allowlist)"],
                "validation_steps": ["Check sshd_config for risky settings", "Verify package updates from vendor repos"],
                "references": ["CWE-306", "CWE-287"]
            }
        ),
    ]

    valid = [
        make_example(
            "ZAP reported missing Content-Security-Policy. Provide remediation guidance.",
            {
                "finding_summary": "Missing CSP can increase XSS impact by allowing untrusted script execution.",
                "risk": "Medium",
                "evidence": ["Response headers do not include Content-Security-Policy"],
                "recommended_actions": ["Add a restrictive CSP (start in report-only)", "Audit inline scripts and third-party domains", "Deploy with monitoring and iterate"],
                "validation_steps": ["Verify CSP header presence on key pages", "Use report-only mode to collect violations"],
                "references": ["CWE-693"]
            }
        ),
    ]

    with out_train.open("w", encoding="utf-8") as f:
        for ex in train:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    with out_valid.open("w", encoding="utf-8") as f:
        for ex in valid:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    print(f"Wrote {len(train)} train examples to {out_train}")
    print(f"Wrote {len(valid)} valid examples to {out_valid}")

if __name__ == "__main__":
    main()