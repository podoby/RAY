import json
import typer

from .db import init_db, log_session
from .sanitize import sanitize_text
from .mistral_client import call_ray_model
from .config import settings
from .report import render_markdown_report
from ray.file_loader import load_file, infer_file_context

app = typer.Typer(help="Ray: Offensive and Defensive Penetration Testing Assistant (API + optional fine-tuning)")

@app.command()
def init():
    """Initialize local database."""
    init_db()
    typer.echo(f"Initialized DB at {settings.db_path}")

@app.command()
def analyze(
    prompt: str = typer.Argument(None, help="Describe findings or paste tool output."),
    file: str = typer.Option(None, "--file", "-f", help="Path to code or scan result file."),
    model: str = typer.Option(None, help="Optional model override."),
    out: str = typer.Option("ray_report.txt", help="Output report file."),
):
    try:
        if file:
            file_content = load_file(file)
            file_context = infer_file_context(file)

            combined_prompt = f"""
You are an ethical web security and red teaming analysis assistant.

The following input is {file_context}. Analyze it at a high level for:
- Security risks or misconfigurations
- Indicators of potential vulnerabilities
- Defensive and mitigation recommendations


INPUT CONTENT:
----------------
{file_content}
----------------
"""
            cleaned = sanitize_text(combined_prompt)

        else:
            if not prompt:
                raise ValueError("Either a prompt or a file must be provided.")
            cleaned = sanitize_text(prompt)

        response_text = call_ray_model(cleaned, model=model)

        typer.echo("\n--- Ray Analysis ---\n")
        typer.echo(response_text)

        # ✅ THIS must align with typer.echo(), not deeper
        with open(out, "w", encoding="utf-8") as f:
            f.write(response_text)

        typer.echo(f"\nReport saved to {out}")

    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)

