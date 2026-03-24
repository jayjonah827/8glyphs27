"""
core/research.py — Research domain support.
Handles datasets, simulations, and structured research event records.
"""

from core.loader import load_all_events
from core.events import derive_family_key
from collections import Counter


def get_research_events():
    """Return all events in research or simulation domains."""
    events, _ = load_all_events()
    return [ev for ev in events if ev.get("domain") in ("research", "simulation")]


def research_summary():
    """Summary stats for research + simulation domains."""
    events = get_research_events()
    if not events:
        return {"total": 0, "by_domain": {}, "by_source_type": {}, "families": []}

    by_domain = Counter(ev.get("domain") for ev in events)
    by_stype = Counter(ev.get("source_type", "unknown") for ev in events)

    families = {}
    for ev in events:
        fk = derive_family_key(ev)
        if fk not in families:
            families[fk] = {"count": 0, "ratios": [], "inside": 0}
        families[fk]["count"] += 1
        m = ev.get("metrics", {})
        r = m.get("clustering_ratio")
        if r is not None:
            families[fk]["ratios"].append(r)
            if m.get("inside_band", False):
                families[fk]["inside"] += 1

    fam_list = []
    for fk, data in families.items():
        mean_r = round(sum(data["ratios"]) / len(data["ratios"]), 6) if data["ratios"] else 0.0
        fam_list.append({
            "family_key": fk,
            "count": data["count"],
            "inside_band": data["inside"],
            "mean_ratio": mean_r
        })
    fam_list.sort(key=lambda x: x["count"], reverse=True)

    return {
        "total": len(events),
        "by_domain": dict(by_domain),
        "by_source_type": dict(by_stype),
        "families": fam_list
    }


def print_research_status():
    """Print research domain status to terminal."""
    s = research_summary()
    print(f"\n  RESEARCH — {s['total']} records")
    if s["total"] == 0:
        print("  No research records yet.\n")
        return
    if s["by_domain"]:
        print(f"  By domain:")
        for d, c in s["by_domain"].items():
            print(f"    {d:<14} {c}")
    if s["by_source_type"]:
        print(f"  By source type:")
        for st, c in s["by_source_type"].items():
            print(f"    {st:<14} {c}")
    if s["families"]:
        print(f"\n  {'Family':<45} {'N':>4} {'InBand':>6} {'MeanR':>8}")
        print(f"  {'─'*45} {'─'*4} {'─'*6} {'─'*8}")
        for f in s["families"]:
            fk = f["family_key"]
            if len(fk) > 43:
                fk = fk[:40] + "..."
            print(f"  {fk:<45} {f['count']:>4} {f['inside_band']:>6} {f['mean_ratio']:>8.4f}")
    print()
