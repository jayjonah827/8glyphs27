"""
core/validator.py — Validate event records against schema rules.
No external dependencies. Pure field checks.
"""


REQUIRED_TOP_LEVEL = [
    "record_id", "source_id", "domain", "source_type", "title",
    "cycle_definition", "irreversible_event", "metrics",
    "routing", "snapshot", "relations", "notes"
]

VALID_DOMAINS = [
    "research", "paleography", "art", "books",
    "languages", "site", "math", "simulation"
]

VALID_SOURCE_TYPES = [
    "dataset", "image", "handwriting", "mirror-writing",
    "text", "book", "language-note", "chart",
    "simulation", "web-export", "essay", "quote"
]

VALID_ROUTES = [
    "memory", "archive", "site", "gallery",
    "blog", "math", "research", "reject"
]

VALID_STATUSES = [
    "draft", "live", "archived", "flagged", "rejected"
]

LIVE_REQUIRES = [
    "cycle_definition.cycle_start",
    "cycle_definition.cycle_end",
    "irreversible_event.event_definition",
    "irreversible_event.event_position"
]


def _get_nested(ev, dotpath):
    """Get a nested value by dot-separated path."""
    parts = dotpath.split(".")
    obj = ev
    for p in parts:
        if isinstance(obj, dict):
            obj = obj.get(p)
        else:
            return None
    return obj


def has_required_fields(ev):
    """Check all required top-level fields are present."""
    missing = [f for f in REQUIRED_TOP_LEVEL if f not in ev]
    return missing


def is_valid_live(ev):
    """
    Check the four fields required for a live record.
    Returns True if all four are non-empty/non-None.
    """
    for path in LIVE_REQUIRES:
        val = _get_nested(ev, path)
        if val is None or val == "":
            return False
    return True


def validate_enums(ev):
    """
    Check domain, source_type, route, status against allowed values.
    Returns list of violations as strings.
    """
    violations = []
    domain = ev.get("domain")
    if domain and domain not in VALID_DOMAINS:
        violations.append(f"domain '{domain}' not in {VALID_DOMAINS}")

    stype = ev.get("source_type")
    if stype and stype not in VALID_SOURCE_TYPES:
        violations.append(f"source_type '{stype}' not in {VALID_SOURCE_TYPES}")

    route = ev.get("routing", {}).get("route")
    if route and route not in VALID_ROUTES:
        violations.append(f"route '{route}' not in {VALID_ROUTES}")

    status = ev.get("routing", {}).get("status")
    if status and status not in VALID_STATUSES:
        violations.append(f"status '{status}' not in {VALID_STATUSES}")

    return violations


def full_validate(ev):
    """
    Run all validation checks on one event record.
    Returns dict: {
        "valid": bool,
        "live_ready": bool,
        "missing_fields": [],
        "enum_violations": [],
    }
    """
    missing = has_required_fields(ev)
    enums = validate_enums(ev)
    live = is_valid_live(ev)
    valid = len(missing) == 0 and len(enums) == 0
    return {
        "valid": valid,
        "live_ready": live,
        "missing_fields": missing,
        "enum_violations": enums,
    }
