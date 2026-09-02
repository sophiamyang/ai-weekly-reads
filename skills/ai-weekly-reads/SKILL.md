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

## Cloud Knowledge-Base Persistence

The knowledge base persists across ephemeral cloud sessions in the private repo `sophiamyang/ai-knowledge-base`, nested as a second git repo at `knowledge_base/.git` inside this checkout. That repo is a shared store, not owned by this pipeline — other workflows publish transcripts and notes into it too, so treat its note schema as a contract (documented in its `KB_README.md`) rather than something to change unilaterally, and never assume every note there came from this pipeline. The main repo keeps tracking `knowledge_base/Home.md`, `README.md`, and `templates/`; the KB repo tracks the generated stores (`raw_transcripts/`, `resources/`, `weekly_books/`, `sources/`, `people/`, `topics/`, `indexes/`) and ignores the main-repo-owned files via its own `.gitignore`.

- At session start (if the environment setup script has not already done it): attach `sophiamyang/ai-knowledge-base` with push access, then from the checkout root run:

  ```bash
  git clone https://github.com/sophiamyang/ai-knowledge-base /tmp/kb && \
    mv /tmp/kb/.git knowledge_base/.git && rm -rf /tmp/kb && \
    git -C knowledge_base checkout -- .
  git -C knowledge_base config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*' && \
    git -C knowledge_base fetch origin
  ```

  The second command asserts the fetch refspec. A plain clone sets it, but a `.git` assembled any other way (`init` + `remote add` + `pull`) leaves it unset, and then `origin/main` never exists: `git status` cannot report ahead/behind and the only way to tell whether the KB is pushed is `git ls-remote`. It is idempotent, so run it unconditionally.
- Verify the restore before processing anything: `git -C knowledge_base status -sb` should print `## main...origin/main`, and `knowledge_base/resources/` should already be populated. An empty `resources/` means the restore failed, and the run will re-transcribe everything it has already done — burning the Gemini daily quota and the caption rate limit for nothing.
- After a successful weekly run: commit and push `knowledge_base/` to the KB repo's `main` branch (message like "Weekly knowledge-base update YYYY-MM-DD") in addition to the normal public-edition commit in the main repo.
- The KB repo must stay private: `raw_transcripts/` holds verbatim third-party content that must never be published in the public repo or editions.

## Weekly Discovery

Each run checks the configured source inspection windows, filters recurring sources to the configured publication window, computes stable IDs, skips resources that already exist in `knowledge_base/resources/`, and processes every new in-window item it discovers.

- Use `publication_window_days` in `config/settings.json` for the weekly publishing window; the default is 7.
- Use `lookback_count` in `config/sources.json` as the per-source inspection limit before publication-date filtering; older `latest_count` configs are still supported.
- Increase `publication_window_days`, `lookback_count`, or both when a source publishes heavily or the weekly run has been skipped.
- `max_items_per_run` in `config/settings.json` is an optional safety cap; `0` means unlimited.
- `weekly_resource_limit` controls how many recent resource notes are included in the weekly book.
- YouTube channels use `yt-dlp --flat-playlist` to collect recent video URLs. Preserve explicit channel tabs such as `/streams`; they intentionally restrict discovery to that content type.
- Channel items whose publication date cannot be resolved are treated as outside the weekly window and skipped, so a transient yt-dlp metadata failure cannot flood a run with the full lookback backlog. Podcast RSS items with missing dates are still included.
- Transcript acquisition constraints (YouTube bot checks, caption throttling, the Gemini fallback, podcast RSS handling) are documented in the reusable `youtube-transcripts` and `podcast-transcripts` skills. The essentials this pipeline depends on are repeated below so a run never depends on those being loaded.
- All yt-dlp calls pin `player_client=ios` (`ytdlp_player_client_args` / `ytdlp_extractor_args` in `scripts/utils.py`); exactly one client, since a fallback list re-triggers the block. Without it videos lose their publication date and are silently dropped from the weekly window.
- `fetch_youtube_captions` paces requests, retries a blocked video, and circuit-breaks after a streak so a hardened block cannot add ~25 minutes to a run.
- `scripts/transcription/gemini.py` is the working fallback from a blocked IP: it hands the video URL to the Gemini Interactions API, which fetches server-side. Needs `GEMINI_API_KEY`. Settings: `youtube_transcription_provider` (default `gemini`) and `youtube_transcription_model` (default `gemini-3.7-flash`). Free tier allows 8 hours of video per day; a heavy backlog rolls to the next run.
- Its output is stored as an ordinary raw transcript, so summaries still come from Mistral and read consistently across sources.
- Audio download is not a workaround for blocked captions: the ios client exposes no audio-only formats.
- Podcasts use RSS feeds and stable IDs derived from GUID/link/audio URL.
- `source_type` describes how an item was fetched/transcribed; optional `content_type` describes how the digest should label it, such as YouTube-hosted podcasts.
- `follow_builders` settings can adapt a compatible JSON feed for podcast transcript ingestion.
- `follow_builders` is disabled by default; enable it only when a local `base_url` is configured.
- `follow_builders.include_podcasts` is disabled by default so local RSS/podcast handling remains primary.
- External feed windows can be shorter than the AI Weekly Reads weekly window. Schedule `scripts/update_knowledge_base.py` more often when you need to cache fast-moving feeds before the Sunday digest.

## Mistral

- Read `MISTRAL_API_KEY` from `.env` or the shell.
- Default summaries use Mistral Batch API with `mistral-small-latest`.
- If the small-model batch fails or returns unusable structured summaries, cancel it if possible and retry the batch once with `summary_fallback_model`, defaulting to `mistral-medium-latest`.
- Transcription fallback uses Mistral transcription after publisher transcripts and YouTube captions fail.
- If Batch returns billing/access errors, check `scripts/check_mistral_access.py --batch` and temporarily use `"summary_mode": "direct"` only if needed.

## Kindle Delivery

General Kindle/Gmail mechanics are in the reusable `kindle-delivery` skill. Project specifics:

- Keep personal delivery values in `.env`, especially `KINDLE_EMAIL` and `KINDLE_SENDER_EMAIL`; do not commit real Kindle addresses, OAuth credentials, OAuth tokens, or app passwords.
- Preferred Gmail delivery uses `KINDLE_DELIVERY_METHOD=gmail_api`, `GMAIL_CREDENTIALS_PATH=config/private/gmail_credentials.json`, and `GMAIL_TOKEN_PATH=config/private/gmail_token.json`.
- Run `.venv/bin/python scripts/setup_gmail_oauth.py` after downloading a Google OAuth Desktop app client JSON.
- The configured sender must be added to Amazon's approved personal document email list.
- SMTP remains available with `KINDLE_DELIVERY_METHOD=smtp`, but it requires a Gmail app password.
- Apple Mail remains available with `KINDLE_DELIVERY_METHOD=apple_mail`, but only when the macOS Mail app has a configured sending account.
- If Mail has no configured accounts, delivery is skipped and should not be recorded as sent.
- Successful sends are recorded in `output/_metadata/kindle_delivery.json`; do not resend the same digest unless the user asks for `--force`.
- Setting `send_to_kindle: false` on a resource note excludes it from the generated weekly book entirely — the digest, public editions, EPUB, and Substack export all build from the same book. Excluded notes are logged during the build.
- Full transcript appendices are deterministically cleaned for reading before EPUB generation. `rewrite_full_transcripts: true` additionally runs a cached Mistral rewrite; raw transcripts remain unchanged.

## Substack

Full background is in the reusable `substack-publishing` skill. What this pipeline needs:

- Substack has no publishing API. Its Cloudflare protection keys on the **source IP**: this cloud environment and a residential IP are not challenged; GitHub Actions runner IPs are challenged on both HTML and the JSON API. Do not move drafting to Actions — a workflow for it was tried and removed. Never try to defeat the challenge or disable certificate verification.
- `scripts/post_to_substack.py` drafts over the JSON API using the `python-substack` package and the `substack.sid` cookie in `SUBSTACK_SID`. Run it from the weekly cloud session. It creates a draft and never publishes; the user reviews and publishes.
- `scripts/substack.py` shadows the `python-substack` package. `_load_substack_api` in `post_to_substack.py` is a context manager that drops the scripts directory from `sys.path`, evicts cached `substack*` modules, yields the library's `Api`, and restores the repo module on exit. Preserve that guard, and keep it wrapping every call on the `Api` rather than just the import: the library defers `from substack.post import Post` and `from substack import mdrender` to draft-creation time, so restoring too early breaks drafting.
- `create_draft_from_markdown` takes `(title, markdown, ...)`. Pass by keyword; a positional body silently lands in the title. The draft is returned nested under `draft`, not as a top-level `id`. `python-substack` is pinned to `>=0.6,<0.7` because the API surface changed across releases.
- On failure it falls back to `scripts/email_substack_post.py`, which emails the post using the Kindle Gmail credentials. A failed draft is never a reason to abandon the run.
- The cookie grants full account access and expires without warning. A 401/403 means re-export it from the browser, not that the pipeline is broken.
- `scripts/create_substack_draft.py` drives a browser and works only locally, from a residential IP. It contains interactive prompts routed through a helper that fails loudly when no terminal is attached.

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
.venv/bin/python scripts/email_substack_post.py
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
