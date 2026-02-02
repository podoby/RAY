from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".php", ".js", ".py"}

MAX_FILE_SIZE = 99_000


def load_file(path: str) -> str:
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError("Input file does not exist.")

    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {file_path.suffix}")

    if file_path.stat().st_size > MAX_FILE_SIZE:
        raise ValueError("File too large for analysis.")

    return file_path.read_text(encoding="utf-8", errors="ignore")


def infer_file_context(filename: str) -> str:
    if filename.endswith((".php", ".js", ".py", ".java")):
        return "source code"
    return "security scan output"

