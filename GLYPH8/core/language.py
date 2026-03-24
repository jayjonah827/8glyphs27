"""
core/language.py — Language domain support.
Handles language-note event records and multilingual source tracking.
"""

from core.loader import load_all_events
from core.events import derive_family_key
from collections import Counter


def get_language_events():
    """Return all events in the languages domain."""
    events, _ = load_all_events()
    return [ev for ev in events if ev.get("domain") == "languages"]


def language_summary():
    """Summary stats for languages domain."""
    events = get_language_events()
    if not events:
        return {"total": 0, "by_source_type": {}, "families": []}

    by_stype = Counter(ev.get("source_type", "unknown") for ev in events)

    families = {}
    for ev in events:
        fk = derive_family_key(ev)
        if fk not in families:
            families[fk] = {"count": 0, "ratios": []}
        families[fk]["count"] += 1
        r = ev.get("metrics", {}).get("clustering_ratio")
        if r is not None:
            families[fk]["ratios"].append(r)

    fam_list = []
    for fk, data in families.items():
        mean_r = round(sum(data["ratios"]) / len(data["ratios"]), 6) if data["ratios"] else 0.0
        fam_list.append({"family_key": fk, "count": data["count"], "mean_ratio": mean_r})

    return {
        "total": len(events),
        "by_source_type": dict(by_stype),
        "families": fam_list
    }


def print_language_status():
    """Print language domain status to terminal."""
    s = language_summary()
    print(f"\n  LANGUAGES — {s['total']} records")
    if s["total"] == 0:
        print("  No language records yet.\n")
        return
    if s["by_source_type"]:
        print(f"  By source type:")
        for st, c in s["by_source_type"].items():
            print(f"    {st:<20} {c}")
    if s["families"]:
        print(f"  Families:")
        for f in s["families"]:
            print(f"    {f['family_key']:<40} n={f['count']}  mean_ratio={f['mean_ratio']:.4f}")
    print()
