"""
core/routing.py — Decide where records go based on validity, domain, family, status.
Destinations: memory, archive, research, site, gallery, blog, reject
"""

from core.loader import load_all_events, save_event
from core.validator import is_valid_live, validate_enums
from core.events import derive_family_key


# Default routing rules by domain
DOMAIN_ROUTES = {
    "research":     "research",
    "simulation":   "research",
    "math":         "math",
    "paleography":  "memory",
    "art":          "gallery",
    "books":        "memory",
    "languages":    "memory",
    "site":         "site",
}

# Override routes by status
STATUS_OVERRIDES = {
    "rejected":  "reject",
    "archived":  "archive",
    "flagged":   "memory",   # flagged stays in memory for review
}


def suggest_route(ev):
    """
    Suggest a route for one event record.
    Priority: status override > domain default > memory fallback.
    Returns route string.
    """
    status = ev.get("routing", {}).get("status", "draft")
    domain = ev.get("domain", "")

    # Status overrides first
    if status in STATUS_OVERRIDES:
        return STATUS_OVERRIDES[status]

    # If not valid for live, hold in memory
    if not is_valid_live(ev):
        return "memory"

    # Domain-based routing
    return DOMAIN_ROUTES.get(domain, "memory")


def apply_routing(ev, force=False):
    """
    Apply suggested route to an event record.
    If force=True, overwrite existing route.
    If force=False, only apply if current route is 'memory' (default).
    Returns (event, changed_bool).
    """
    current_route = ev.get("routing", {}).get("route", "memory")
    suggested = suggest_route(ev)

    if force or current_route == "memory":
        if suggested != current_route:
            ev.setdefault("routing", {})["route"] = suggested
            return ev, True
    return ev, False


def route_all(force=False):
    """
    Run routing on all events. Save any changes.
    Returns (total_checked, total_changed).
    """
    events, _ = load_all_events()
    changed = 0
    for ev in events:
        ev, did_change = apply_routing(ev, force=force)
        if did_change:
            save_event(ev)
            changed += 1
    return len(events), changed


def print_routing_report():
    """Print routing analysis to terminal."""
    events, _ = load_all_events()
    if not events:
        print("  No events to route.\n")
        return

    print(f"\n  ROUTING ANALYSIS — {len(events)} records\n")
    print(f"  {'Record':<14} {'Domain':<14} {'Status':<10} {'Current':<10} {'Suggested':<10} {'Match':>5}")
    print(f"  {'─'*14} {'─'*14} {'─'*10} {'─'*10} {'─'*10} {'─'*5}")

    mismatches = 0
    for ev in events:
        rid = ev.get("record_id", "?")
        domain = ev.get("domain", "?")
        status = ev.get("routing", {}).get("status", "?")
        current = ev.get("routing", {}).get("route", "?")
        suggested = suggest_route(ev)
        match = "Y" if current == suggested else "N"
        if current != suggested:
            mismatches += 1
        print(f"  {rid:<14} {domain:<14} {status:<10} {current:<10} {suggested:<10} {match:>5}")

    print(f"\n  Mismatches: {mismatches} / {len(events)}")
    if mismatches > 0:
        print(f"  Use 'apply' to update routes, or 'force' to overwrite all.\n")
    else:
        print(f"  All routes match suggested destinations.\n")
