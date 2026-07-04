---
name: ai-weekly-reads
description: Use when running, auditing, maintaining, extending, or troubleshooting the AI Weekly Reads workflow, including source discovery, transcripts, Mistral summaries, the Obsidian knowledge base, weekly digest generation, Substack publishing, Kindle delivery, and GitHub commits.
---

# AI Weekly Reads

Work from the AI Weekly Reads repository root.

## Architecture

- `config/sources.json` is the recurring source registry.
- `config/settings.example.json` is the shareable settings template; local `config/settings.json` is ignored by Git.
- `inbox/links.example.txt` is the shareable inbox template; local `inbox/links.txt` is ignored by Git.
- `inbox/links.txt` is for one-off links collected during the week.
- `knowledge_base/raw_transcripts/` is the canonical local raw transcript/text store.
- `knowledge_base/resources/` is the canonical local clean reading-note store.
- `knowledge_base/weekly_books/` stores local Markdown weekly books for Obsidian.
- `knowledge_base/sources/`, `knowledge_base/people/`, `knowledge_base/topics/`, and `knowledge_base/indexes/` are generated local graph hubs. Resources link to source, speaker, and topic hubs; weekly books link to included resources. The default global graph shows only resources and topics.
- `latest.md` is the top-level public, tracked, summaries-only book for the most recently refreshed public edition, whether it came from a weekly run or a one-shot playlist run.
- `latest.epub` is the top-level public tracked EPUB companion for the most recently refreshed public edition when EPUB generation is available.
- `weekly/latest.md` is the public, tracked, summaries-only weekly book. Each weekly build overwrites it; never include full transcripts or private delivery data there.
- `weekly/latest.epub` is the public tracked EPUB companion for the latest weekly build when EPUB generation is available.
- `one-shot/latest.md` is the public, tracked, summaries-only one-shot playlist book. Each one-shot playlist build overwrites it.
- `one-shot/latest.epub` is the public tracked EPUB companion for the latest one-shot playlist build when EPUB generation is available.
- `output/` is disposable build output, temporary media/summary scratch, and last-run metadata.
- `assets/kindle.css` is the EPUB reading stylesheet. Keep the page pure white with black text and avoid shaded content blocks that reduce Kindle contrast.
- Generated Obsidian notes should use Properties-friendly YAML. Keep note type, source, status, priority, and language as Properties. Only resource notes should have tags, using 2-4 controlled `topic/...` values for central subject matter; do not create operational tags.
- Resource notes should store principal guests or speakers in the `speakers` property. Kindle metadata should display the human-readable podcast/channel name as the link label and never print a bare source URL.
- Generated knowledge-base notes, local settings, and inbox links are local-only and ignored by Git. Keep workflow code, prompts, shareable config, and templates in Git; do not re-add generated/private files unless the user explicitly asks.
- GitHub Actions is for lightweight repo health only. Do not turn it into the primary content runner unless the user explicitly chooses cloud-hosted knowledge-base state and GitHub secrets for delivery.
- Do not recreate a durable `data/` folder.

## Weekly Discovery

Each run checks the configured source inspection windows, filters recurring sources to the configured publication window, computes stable IDs, skips resources that already exist in `knowledge_base/resources/`, and processes every new in-window item it discovers.

- Use `publication_window_days` in `config/settings.json` for the weekly publishing window; the default is 7.
- Use `lookback_count` in `config/sources.json` as the per-source inspection limit before publication-date filtering; older `latest_count` configs are still supported.
- Increase `publication_window_days`, `lookback_count`, or both when a source publishes heavily or the weekly run has been skipped.
- `max_items_per_run` in `config/settings.json` is an optional safety cap; `0` means unlimited.
- `weekly_resource_limit` controls how many recent resource notes are included in the weekly book.
- YouTube channels use `yt-dlp --flat-playlist` to collect recent video URLs. Preserve explicit channel tabs such as `/streams`; they intentionally restrict discovery to that content type.
- Channel items whose publication date cannot be resolved are treated as outside the weekly window and skipped, so a transient yt-dlp metadata failure cannot flood a run with the full lookback backlog. Podcast RSS items with missing dates are still included.
- Podcasts use RSS feeds and stable IDs derived from GUID/link/audio URL.
- `source_type` describes how an item was fetched/transcribed; optional `content_type` describes how the digest should label it, such as YouTube-hosted podcasts.
- `follow_builders` settings can adapt a compatible JSON feed for podcast transcript ingestion.
- `follow_builders` is disabled by default; enable it only when a local `base_url` is configured.
- `follow_builders.include_podcasts` is disabled by default so local RSS/podcast handling remains primary.
- External feed windows can be shorter than the AI Weekly Reads weekly window. Schedule `scripts/update_knowledge_base.py` more often when you need to cache fast-moving feeds before the Sunday digest.

## Mistral

- Read `MISTRAL_API_KEY` from `.env` or the shell.
- Default summaries use Mistral Batch API.
- Transcription fallback uses Mistral transcription after publisher transcripts and YouTube captions fail.
- If Batch returns billing/access errors, check `scripts/check_mistral_access.py --batch` and temporarily use `"summary_mode": "direct"` only if needed.

## Kindle Delivery

- Keep personal delivery values in `.env`, especially `KINDLE_EMAIL` and `KINDLE_SENDER_EMAIL`; do not commit real Kindle addresses, OAuth credentials, OAuth tokens, or app passwords.
- Preferred Gmail delivery uses `KINDLE_DELIVERY_METHOD=gmail_api`, `GMAIL_CREDENTIALS_PATH=config/private/gmail_credentials.json`, and `GMAIL_TOKEN_PATH=config/private/gmail_token.json`.
- Run `.venv/bin/python scripts/setup_gmail_oauth.py` after downloading a Google OAuth Desktop app client JSON.
- The configured sender must be added to Amazon's approved personal document email list.
- SMTP remains available with `KINDLE_DELIVERY_METHOD=smtp`, but it requires a Gmail app password.
- Apple Mail remains available with `KINDLE_DELIVERY_METHOD=apple_mail`, but only when the macOS Mail app has a configured sending account.
- If Mail has no configured accounts, delivery is skipped and should not be recorded as sent.
- Successful sends are recorded in `output/_metadata/kindle_delivery.json`; do not resend the same digest unless the user asks for `--force`.
- Setting `send_to_kindle: false` on a resource note excludes it from the generated weekly book entirely — the digest, public editions, EPUB, and Substack export all build from the same book. Excluded notes are logged during the build.

## Commands

Default build commands generate artifacts only. Distribution is a separate explicit step.

```bash
.venv/bin/python scripts/update_knowledge_base.py
.venv/bin/python scripts/build_latest_digest.py
.venv/bin/python scripts/build_weekly_digest.py
.venv/bin/python scripts/build_latest_digest.py --send-kindle
.venv/bin/python scripts/build_weekly_digest.py --send-kindle
.venv/bin/python scripts/build_playlist_digest.py "https://www.youtube.com/playlist?list=PLAYLIST_ID"
.venv/bin/python scripts/build_playlist_digest.py "https://www.youtube.com/playlist?list=PLAYLIST_ID" --send-kindle --substack
.venv/bin/python scripts/setup_gmail_oauth.py
.venv/bin/python scripts/send_latest_to_kindle.py
.venv/bin/python scripts/send_latest_to_kindle.py --force
.venv/bin/python scripts/check_repo_health.py
.venv/bin/python scripts/audit_knowledge_base.py
.venv/bin/python scripts/normalize_knowledge_base.py
.venv/bin/python scripts/check_mistral_access.py --batch
```

Networked build/transcript commands may require user approval in restricted environments.

## Verification

Before committing meaningful changes:

```bash
find scripts -name '*.py' -print0 | xargs -0 .venv/bin/python -m py_compile
.venv/bin/python scripts/check_repo_health.py
.venv/bin/python scripts/audit_knowledge_base.py
git status --short
```

Also spot-check that generated weekly-book tables of contents include source labels and that full transcripts remain in `knowledge_base/raw_transcripts/`, not in resource notes.
