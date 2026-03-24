"""
core/events.py — Event record operations.
Create, inspect, recompute, derive family keys.
"""

import datetime
from core.loader import load_all_events, save_event, next_event_id
from core.validator import is_valid_live


def compute_metrics(ev):
    """Recompute clustering_ratio and band membership from raw fields."""
    cd = ev.get("cycle_definition", {})
    ie = ev.get("irreversible_event", {})
    cycle_length = cd.get("cycle_length", 0)
    event_position = ie.get("event_position", 0)

    ref = 0.39
    band_min = 0.30
    band_max = 0.49

    if cycle_length and cycle_length > 0:
        ratio = event_position / cycle_length
    else:
        ratio = 0.0

    inside = band_min <= ratio <= band_max
    dist = abs(ratio - ref)

    return {
        "clustering_ratio": round(ratio, 6),
        "reference_point": ref,
        "convergence_band_min": band_min,
        "convergence_band_max": band_max,
        "inside_band": inside,
        "distance_from_reference": round(dist, 6)
    }


def derive_family_key(ev):
    """
    Derive a grouping key from domain + source_type + event_name.
    Falls back to domain + source_type + title if event_name missing.
    Used for frequency and judgment grouping.
    """
    domain = ev.get("domain", "unknown")
    stype = ev.get("source_type", "unknown")
    ie = ev.get("irreversible_event", {})
    ename = ie.get("event_name", "")
    if not ename:
        # Extract first meaningful chunk from title
        title = ev.get("title", "unknown")
        # Take first 3 words, lowercase, joined by underscore
        words = title.lower().split()[:3]
        ename = "_".join(words) if words else "unknown"
    return f"{domain}:{stype}:{ename}"


def recompute_all():
    """Recompute metrics for all events and save. Return count updated."""
    events, _ = load_all_events()
    updated = 0
    for ev in events:
        ev["metrics"] = compute_metrics(ev)
        if is_valid_live(ev) and ev.get("routing", {}).get("status") == "draft":
            ev["routing"]["status"] = "live"
        save_event(ev)
        updated += 1
    return updated


def create_event_from_input():
    """Interactive: create a new event record from terminal input. Returns the event dict."""
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    rid = next_event_id()

    print(f"\n  New event: {rid}")
    title = input("  Title: ").strip()
    domain = input("  Domain (research/paleography/art/books/languages/site/math/simulation): ").strip().lower()
    stype = input("  Source type (dataset/image/handwriting/text/book/essay/quote/...): ").strip().lower()

    print("  -- Cycle definition --")
    c_start = input("  Cycle start: ").strip()
    c_end = input("  Cycle end: ").strip()
    c_length_raw = input("  Cycle length (number): ").strip()
    c_unit = input("  Cycle unit (time/steps/days/years/trials/...): ").strip()
    try:
        c_length = float(c_length_raw)
    except ValueError:
        c_length = 0

    print("  -- Irreversible event --")
    e_name = input("  Event name: ").strip()
    e_def = input("  Event definition: ").strip()
    e_pos_raw = input("  Event position (number): ").strip()
    e_unit = input("  Event unit: ").strip()
    try:
        e_pos = float(e_pos_raw)
    except ValueError:
        e_pos = 0

    ev = {
        "record_id": rid,
        "source_id": f"source_{rid.split('_')[1]}",
        "domain": domain,
        "source_type": stype,
        "title": title,
        "cycle_definition": {
            "cycle_start": c_start,
            "cycle_end": c_end,
            "cycle_length": c_length,
            "cycle_unit": c_unit
        },
        "irreversible_event": {
            "event_name": e_name,
            "event_definition": e_def,
            "event_position": e_pos,
            "event_unit": e_unit
        },
        "metrics": {},
        "routing": {"route": "memory", "status": "draft"},
        "snapshot": {
            "snapshot_time": now,
            "run_id": f"run_{rid.split('_')[1]}",
            "tick_id": f"tick_{rid.split('_')[1]}",
            "version": "v1"
        },
        "relations": {
            "parent_record_id": None,
            "linked_records": [],
            "linked_files": []
        },
        "notes": {
            "method_note": "",
            "confidence_note": "",
            "review_note": ""
        }
    }

    ev["metrics"] = compute_metrics(ev)

    if is_valid_live(ev):
        ev["routing"]["status"] = "live"
        print(f"  Record valid. Status: live")
    else:
        print(f"  Record incomplete. Status: draft")

    save_event(ev)
    print(f"  Saved: events/{rid}.json")
    print(f"  Clustering ratio: {ev['metrics']['clustering_ratio']}")
    print(f"  Inside band: {ev['metrics']['inside_band']}\n")
    return ev
