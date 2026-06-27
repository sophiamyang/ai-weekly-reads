from __future__ import annotations

import argparse
import os

from config import load_settings
from project_paths import ROOT
from utils import load_dotenv


def main() -> None:
    parser = argparse.ArgumentParser(description="Check which Mistral services this API key can access.")
    parser.add_argument("--batch", action="store_true", help="Submit a tiny Batch API job to test batch access.")
    parser.add_argument("--audio-url", help="Transcribe a public audio URL to test audio transcription access.")
    args = parser.parse_args()

    load_dotenv(ROOT / ".env")
    settings = load_settings()
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("MISTRAL_API_KEY: missing")
        return

    print("MISTRAL_API_KEY: present")
    client = _client(api_key)
    _check_chat(client, settings.summary_model)

    if args.audio_url:
        _check_audio(client, settings.transcription_model, args.audio_url)
    else:
        print("Audio transcription: skipped (pass --audio-url to test)")

    if args.batch:
        _check_batch(client, settings.summary_model)
    else:
        print("Batch API: skipped (pass --batch to test; may create a tiny billable job)")


def _client(api_key: str):
    from mistralai.client import Mistral

    return Mistral(api_key=api_key)


def _check_chat(client, model: str) -> None:
    try:
        response = client.chat.complete(
            model=model,
            messages=[{"role": "user", "content": "Reply with OK."}],
            timeout_ms=60_000,
        )
        text = response.choices[0].message.content
        print(f"Chat completions: ok ({model}) -> {str(text).strip()[:40]}")
    except Exception as exc:
        print(f"Chat completions: failed ({model}) -> {exc}")


def _check_audio(client, model: str, audio_url: str) -> None:
    try:
        response = client.audio.transcriptions.complete(
            model=model,
            file_url=audio_url,
            timeout_ms=120_000,
        )
        print(f"Audio transcription: ok ({model}) -> {response.text[:80]}")
    except Exception as exc:
        print(f"Audio transcription: failed ({model}) -> {exc}")


def _check_batch(client, model: str) -> None:
    try:
        job = client.batch.jobs.create(
            endpoint="/v1/chat/completions",
            model=model,
            requests=[
                {
                    "custom_id": "access-check",
                    "body": {
                        "messages": [{"role": "user", "content": "Reply with OK."}],
                        "max_tokens": 8,
                    },
                }
            ],
            metadata={"project": "ai-weekly-reads", "job_type": "access-check"},
            timeout_hours=1,
        )
        print(f"Batch API: ok ({model}) -> job {job.id} status {job.status}")
    except Exception as exc:
        print(f"Batch API: failed ({model}) -> {exc}")


if __name__ == "__main__":
    main()
