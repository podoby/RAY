from mistralai import Mistral
from .config import settings


def call_ray_model(user_prompt: str, model: str | None = None) -> str:
    """
    Calls the Mistral model and returns the raw response text.
    The response may contain explanations and/or JSON. Call Mistral Chat Completions using the official Python SDK. :contentReference[oaicite:2]{index=2}
    No format checking is performed.
    """

    if not settings.mistral_api_key:
        raise RuntimeError("Missing MISTRAL_API_KEY")

    use_model = model or settings.model

    with Mistral(api_key=settings.mistral_api_key) as client:
        response = client.chat.complete(
            model=use_model,
            messages=[
                {"role": "system", "content": settings.system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,
        )

    return response.choices[0].message.content.strip()