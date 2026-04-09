# Merge Validation Report

## Conflict and Overwrite Checks

Observed overwrite operations from merge logs:

- `.merge_step2.log`: 15 overwrite/update operations
- `.merge_step3.log`: 18 overwrite/update operations
- `.merge_docs_downloads.log`: 0 overwrite/update operations
- `.merge_docs_glyph8.log`: 11 overwrite/update operations

Applied precedence:

1. `/Users/jayjonah/8glyphs27/GLYPH8` (final winner on conflicts)
2. `/Users/jayjonah/Downloads/8glyphs27-main`
3. `/Users/jayjonah/8glyphs27-BACKUP-PRIOR-ART-2026-04-02/GLYPH8`

## Runtime Hygiene Checks

- Root-level binary-like files after cleanup: 0
- Root-level lock/temp placeholders removed: yes
- `*.pyc` and `__pycache__` cleanup: applied
- Root research binaries relocated to: `references/research_binaries/`

## Mechanism Smoke Checks

- `event_schema_v1.json` loaded successfully
- `gev_*.json` parsed (29 records)
- required top-level fields present in sample record
- context index inputs valid JSON:
  - `messages.json`
  - `content_db.json`
  - `daily_messages.json`
- deploy artifact path verified:
  - `deploy/final_mark/docs/DEPLOYMENT_RUNBOOK.md`

## Python Sanity Checks

`py_compile` passed for:

- `GLYPH8/glyph_system.py`
- `GLYPH8/glyph_constraint.py`
- `GLYPH8/downloads_extractor.py`
- `GLYPH8/automation.py`
