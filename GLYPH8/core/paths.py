"""
core/paths.py — All filesystem paths for GLYPH8.
Single source of truth. Every module imports from here.
"""

import os

# Root = wherever glyph8.py lives (one level up from core/)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR     = os.path.join(ROOT_DIR, "glyph8_data")
EVENTS_DIR   = os.path.join(ROOT_DIR, "events")
SCHEMA_DIR   = os.path.join(ROOT_DIR, "schemas")
ARCHIVE_DIR  = os.path.join(ROOT_DIR, "archive")
INTAKE_DIR   = os.path.join(ROOT_DIR, "intake")
CORE_DIR     = os.path.join(ROOT_DIR, "core")

# Key files
SCHEMA_FILE      = os.path.join(SCHEMA_DIR, "event_schema_v1.json")
FRAMEWORK_KB     = os.path.join(DATA_DIR, "framework_kb.json")
MATH_PROGRESS    = os.path.join(DATA_DIR, "math_progress.json")
LOG_ENTRIES      = os.path.join(DATA_DIR, "log_entries.json")
FEED_STATE       = os.path.join(ROOT_DIR, "feed_state.json")
ARCHIVE_LOG      = os.path.join(ARCHIVE_DIR, "archive_log.json")

# Ensure directories exist
for d in [DATA_DIR, EVENTS_DIR, SCHEMA_DIR, ARCHIVE_DIR, INTAKE_DIR]:
    os.makedirs(d, exist_ok=True)
