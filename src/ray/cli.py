import json
import typer

from .db import init_db, log_session
from .sanitize import sanitize_text
from .mistral_client import call_ray_model
from .config import settings
from .report import render_markdown_report

app = typer.Typer(help="Ray: Offensive and Defensive Penetration Testing Assistant (API + optional fine-tuning)")

@app.command()
def init():
    """Initialize local database."""
    init_db()
    typer.echo(f"Initialized DB at {settings.db_path}")

@app.command()
def analyze(
    prompt: str = typer.Argument(..., help="Describe findings or paste tool output."),
    model: str = typer.Option(None, help="Optional model override."),
    out: str = typer.Option("ray_report.txt", help="Output report file."),
):
    """
    Analyze security findings offensively and defensively (triage + exploitation + mitigations + safe validation). 
    """

    init_db()

    cleaned = sanitize_text(prompt)

    response_text = call_ray_model(cleaned, model=model)

    # Save report
    with open(out, "w", encoding="utf-8") as f:
        f.write(response_text)

    log_session(
        user_input=cleaned,
        model_name=model or settings.model,
        response_json=response_text,  # storing raw response
    )

    typer.echo("\n--- Ray Analysis ---\n")
    typer.echo(response_text)
    typer.echo(f"\nReport saved to {out}")