"""
core/frequency.py — Group events by family and compute recurrence stats.
Family key = domain:source_type:event_name
"""

from collections import defaultdict
from core.loader import load_all_events
from core.events import derive_family_key


def build_frequency_table():
    """
    Group all events by family_key.
    For each family, compute:
      - total records
      - in-band count
      - in-band frequency (proportion)
      - mean ratio
    Returns list of dicts sorted by total descending.
    """
    events, _ = load_all_events()
    families = defaultdict(lambda: {
        "family_key": "",
        "total": 0,
        "in_band": 0,
        "ratios": [],
        "records": []
    })

    for ev in events:
        fk = derive_family_key(ev)
        fam = families[fk]
        fam["family_key"] = fk
        fam["total"] += 1
        fam["records"].append(ev.get("record_id", "?"))

        m = ev.get("metrics", {})
        ratio = m.get("clustering_ratio")
        if ratio is not None:
            fam["ratios"].append(ratio)
            if m.get("inside_band", False):
                fam["in_band"] += 1

    # Build output
    result = []
    for fk, fam in families.items():
        ratios = fam["ratios"]
        mean_ratio = round(sum(ratios) / len(ratios), 6) if ratios else 0.0
        in_band_freq = round(fam["in_band"] / fam["total"], 4) if fam["total"] > 0 else 0.0

        result.append({
            "family_key": fk,
            "total": fam["total"],
            "in_band": fam["in_band"],
            "in_band_frequency": in_band_freq,
            "mean_ratio": mean_ratio,
            "records": fam["records"]
        })

    result.sort(key=lambda x: x["total"], reverse=True)
    return result


def print_frequency_table():
    """Print frequency table to terminal."""
    table = build_frequency_table()
    if not table:
        print("  No events to analyze.\n")
        return

    print(f"\n  {'Family':<50} {'Total':>5} {'InBand':>6} {'Freq':>6} {'MeanR':>8}")
    print(f"  {'─'*50} {'─'*5} {'─'*6} {'─'*6} {'─'*8}")

    for row in table:
        fk = row["family_key"]
        if len(fk) > 48:
            fk = fk[:45] + "..."
        print(f"  {fk:<50} {row['total']:>5} {row['in_band']:>6} {row['in_band_frequency']:>5.0%} {row['mean_ratio']:>8.4f}")

    print()
