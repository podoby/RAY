import re

SECRET_PATTERNS = [
    # API keys/tokens (basic)
    r"(?i)(api_key|apikey|token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-\.]{8,}['\"]?",
    # AWS-style key
    r"\bAKIA[0-9A-Z]{16}\b",
    # Private keys block header
    r"-----BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY-----",
]

IP_PATTERN = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"

def sanitize_text(text: str, mask_ips: bool = True) -> str:
    out = text
    for pat in SECRET_PATTERNS:
        out = re.sub(pat, "[REDACTED_SECRET]", out)

    if mask_ips:
        out = re.sub(IP_PATTERN, "[REDACTED_IP]", out)

    # prevent massive tool dumps
    if len(out) > 12_000:
        out = out[:12_000] + "\n...[TRUNCATED]"

    return out