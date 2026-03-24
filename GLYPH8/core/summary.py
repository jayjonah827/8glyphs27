"""
core/summary.py — Aggregate summaries of all event records.
Total counts, by-domain, by-route, by-status, band stats, mean ratio.
"""

from collections import Counter
from core.loader import load_all_events
from core.validator import is_valid_live


def build_summary():
    """
    Build full summary dict from all loaded events.
    Returns dict with all counts and stats.
    """
    events, errors = load_all_events()

    total = len(events)
    valid_live = sum(1 for ev in events if is_valid_live(ev))

    by_domain = Counter(ev.get("domain", "unknown") for ev in events)
    by_route = Counter(ev.get("routing", {}).get("route", "unknown") for ev in events)
    by_status = Counter(ev.get("routing", {}).get("status", "unknown") for ev in events)

    ratios = []
    inside_count = 0
    for ev in events:
        m = ev.get("metrics", {})
        r = m.get("clustering_ratio")
        if r is not None:
            ratios.append(r)
            if m.get("inside_band", False):
                inside_count += 1

    band_stats = {}
    if ratios:
        band_stats["total_with_ratio"] = len(ratios)
        band_stats["inside_band"] = inside_count
        band_stats["outside_band"] = len(ratios) - inside_count
        band_stats["min_ratio"] = round(min(ratios), 6)
        band_stats["max_ratio"] = round(max(ratios), 6)
        band_stats["mean_ratio"] = round(sum(ratios) / len(ratios), 6)

    return {
        "total_records": total,
        "valid_for_live": valid_live,
        "skipped_errors": len(errors),
        "error_files": errors,
        "by_domain": dict(by_domain),
        "by_route": dict(by_route),
        "by_status": dict(by_status),
        "band_stats": band_stats,
    }


def print_summary():
    """Print full summary to terminal."""
    s = build_summary()

    print(f"\n  Total event records: {s['total_records']}")
    if s["skipped_errors"]:
        print(f"  Skipped (malformed): {s['skipped_errors']}")
    if s["total_records"] == 0:
        print("  No events loaded.\n")
        return

    print(f"  Valid for live: {s['valid_for_live']} / {s['total_records']}")

    print("\n  BY DOMAIN:")
    for d, c in sorted(s["by_domain"].items()):
        print(f"    {d:<16} {c}")

    print("\n  BY ROUTE:")
    for r, c in sorted(s["by_route"].items()):
        print(f"    {r:<16} {c}")

    print("\n  BY STATUS:")
    for st, c in sorted(s["by_status"].items()):
        print(f"    {st:<16} {c}")

    bs = s["band_stats"]
    if bs:
        print(f"\n  CONVERGENCE BAND:")
        print(f"    Inside band:  {bs['inside_band']} / {bs['total_with_ratio']}")
        print(f"    Outside band: {bs['outside_band']} / {bs['total_with_ratio']}")
        print(f"    Ratio range:  {bs['min_ratio']:.4f} \u2014 {bs['max_ratio']:.4f}")
        print(f"    Mean ratio:   {bs['mean_ratio']:.4f}")

    print()
