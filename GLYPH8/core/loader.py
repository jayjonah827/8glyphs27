"""
core/loader.py — Load and save JSON data safely.
All file I/O for the GLYPH8 system goes through here.
"""

import os, json
from core.paths import DATA_DIR, EVENTS_DIR, SCHEMA_FILE


def load_json(filepath, default=None):
    """Load JSON from filepath. Return default on any failure."""
    if default is None:
        default = {}
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError, OSError):
        return default


def save_json(filepath, data):
    """Save data as JSON to filepath."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def load_data(filename, default=None):
    """Load from glyph8_data/ by filename."""
    if default is None:
        default = {}
    return load_json(os.path.join(DATA_DIR, filename), default)


def save_data(filename, data):
    """Save to glyph8_data/ by filename."""
    save_json(os.path.join(DATA_DIR, filename), data)


def load_event_schema():
    """Load event_schema_v1.json. Return dict or None."""
    schema = load_json(SCHEMA_FILE, None)
    return schema


def load_all_events():
    """
    Load all valid event records from events/.
    Returns (events_list, error_filenames).
    Skips malformed files and non-record JSON.
    """
    events = []
    errors = []
    if not os.path.isdir(EVENTS_DIR):
        return events, errors
    for fname in sorted(os.listdir(EVENTS_DIR)):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(EVENTS_DIR, fname)
        try:
            with open(fpath) as f:
                data = json.load(f)
            if isinstance(data, dict) and "record_id" in data:
                events.append(data)
            else:
                errors.append(fname)
        except (json.JSONDecodeError, IOError, OSError):
            errors.append(fname)
    return events, errors


def save_event(ev):
    """Save one event record to events/."""
    rid = ev.get("record_id", "gev_unknown")
    fpath = os.path.join(EVENTS_DIR, f"{rid}.json")
    save_json(fpath, ev)
    return fpath


def next_event_id():
    """Return the next available event record ID."""
    events, _ = load_all_events()
    # Find max numeric suffix
    max_num = 0
    for ev in events:
        rid = ev.get("record_id", "")
        if rid.startswith("gev_"):
            try:
                num = int(rid.split("_")[1])
                if num > max_num:
                    max_num = num
            except (IndexError, ValueError):
                pass
    return f"gev_{max_num + 1:06d}"
