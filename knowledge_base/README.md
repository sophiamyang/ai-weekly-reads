# AI Weekly Reads Obsidian Vault

Open this `knowledge_base/` folder as an Obsidian vault.

Each processed video, podcast episode, RSS item, or web transcript stores its raw text under `raw_transcripts/`. After summarization, it gets a clean reading note under `resources/`.

`raw_transcripts/` is the canonical local transcript/text store. Generated Kindle files and run scratch data live under the root project `output/` folder, not in this vault.

The weekly Kindle book is compiled from these resource files and saved under `weekly_books/`. That means the archive stays useful even after a digest is sent: you can search it, recompile older items, or manually edit a resource before the next weekly packet.

The graph is organized around generated `topics/`, `sources/`, and `people/` hub notes. Resource notes link to their central topics, podcast/channel, and principal speakers, while weekly books link back to every included resource.

The default global graph intentionally shows only resource and topic notes. Sources, people, raw transcripts, weekly compilations, indexes, templates, and repository files remain searchable but are hidden from the graph because they otherwise obscure the subject clusters.

Generated notes are intentionally local-only. `raw_transcripts/`, `resources/`, and `weekly_books/` are ignored by Git so GitHub stores the workflow, not the personal reading archive.

## Resource Shape

Each resource contains:

- title and source metadata
- the structured summary
- main ideas, Q&A, notable details, actionable takeaways, entities, and reading priority
- a link to the raw transcript-only note

Files are named with a date, source type, short title slug, and stable ID.

## Obsidian Fields

Generated resources include frontmatter fields for:

- `type`
- `aliases`
- `speakers`
- `status`
- `priority`
- `send_to_kindle`
- `language` on weekly books
- 2-4 controlled `topic/...` tags on resource notes

Tags describe subject matter, such as `topic/coding-agents`, `topic/model-evaluation`, and `topic/ai-infrastructure`. Note type, source, status, priority, and language remain Properties because they are operational metadata, not knowledge topics. Raw transcripts, people, sources, indexes, and weekly books do not add tags.

The weekly compiler currently includes the most recent resources inside the configured publication window. Later it can be changed to include only notes where `send_to_kindle: true`.

## Maintenance

From the project root, run `scripts/audit_knowledge_base.py` to check for missing raw transcripts, duplicate IDs, placeholder summaries, or very short transcripts.

Run `scripts/normalize_knowledge_base.py` after hand-editing or migrating notes to keep Obsidian frontmatter consistent.

## Sources

Recurring source lists live in `../config/sources.json`. The current registry includes configured YouTube channels and podcast RSS feeds.

YouTube is a discovery/transcript source, not always the editorial format. YouTube channels can set `content_type: podcast` when the digest should label them as podcasts.

`config/sources.json` is also where weekly source depth is controlled. `lookback_count` means "look this many items back every run"; already-summarized items are reused instead of reprocessed. Older `latest_count` entries still work, but new source entries should use `lookback_count`.

An optional `follow_builders`-compatible podcast feed can be adapted through `../config/settings.json`. If an external feed has a short upstream window, run `scripts/update_knowledge_base.py` more often so those sources are cached before the Sunday digest.
