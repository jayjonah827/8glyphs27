"""
core/judgment.py — Bounded labels from frequency data.
No freeform opinions. No invented evidence.
Labels derived strictly from thresholds on event count and in-band frequency.

General labels (all domains):
  sparse         — fewer than 3 records in the family
  emerging       — 3-9 records, any in-band frequency
  stable         — 10+ records, in-band frequency 20%-60%
  strong         — 10+ records, in-band frequency > 60%
  outlier-heavy  — 10+ records, in-band frequency < 20%

Simulation tendency labels (simulation domain only):
  symmetric-outside   — mean ratio outside band [0.30, 0.49]
  structural-inside   — mean ratio inside band, distance from 0.39 > 0.025
  near-reference      — mean ratio inside band, distance from 0.39 <= 0.025
"""

from core.frequency import build_frequency_table


# ── General thresholds ──
MIN_FOR_EMERGING = 3
MIN_FOR_ASSESSED = 10
BAND_LOW = 0.20
BAND_HIGH = 0.60

# ── Simulation tendency thresholds ──
CONVERGENCE_BAND_MIN = 0.30
CONVERGENCE_BAND_MAX = 0.49
REFERENCE_POINT = 0.39
NEAR_REF_DELTA = 0.025


def label_family(total, in_band_freq):
    """
    Return one bounded label for a single family.
    """
    if total < MIN_FOR_EMERGING:
        return "sparse"
    if total < MIN_FOR_ASSESSED:
        return "emerging"
    # 10+ records: assess band frequency
    if in_band_freq < BAND_LOW:
        return "outlier-heavy"
    if in_band_freq > BAND_HIGH:
        return "strong"
    return "stable"


def classify_simulation_tendency(mean_ratio):
    """
    Classify a simulation family by WHERE its mean ratio falls.
    Returns one of: symmetric-outside, structural-inside, near-reference.
    This is a measurement classification, not an opinion.
    """
    inside_band = CONVERGENCE_BAND_MIN <= mean_ratio <= CONVERGENCE_BAND_MAX
    if not inside_band:
        return "symmetric-outside"
    dist = abs(mean_ratio - REFERENCE_POINT)
    if dist <= NEAR_REF_DELTA:
        return "near-reference"
    return "structural-inside"


def is_simulation_family(family_key):
    """Return True if this family_key belongs to simulation domain."""
    return family_key.startswith("simulation:")


def build_judgments():
    """
    Label every family from the frequency table.
    Returns list of dicts: family_key, total, in_band_frequency, label
    Simulation families also get a 'tendency' field.
    """
    freq = build_frequency_table()
    result = []
    for row in freq:
        label = label_family(row["total"], row["in_band_frequency"])
        entry = {
            "family_key": row["family_key"],
            "total": row["total"],
            "in_band": row["in_band"],
            "in_band_frequency": row["in_band_frequency"],
            "mean_ratio": row["mean_ratio"],
            "label": label,
            "tendency": None
        }
        if is_simulation_family(row["family_key"]):
            entry["tendency"] = classify_simulation_tendency(row["mean_ratio"])
        result.append(entry)
    return result


def print_judgments():
    """Print judgment labels to terminal."""
    judgments = build_judgments()
    if not judgments:
        print("  No events to judge.\n")
        return

    # Split simulation vs non-simulation
    sim_judgments = [j for j in judgments if j["tendency"] is not None]
    other_judgments = [j for j in judgments if j["tendency"] is None]

    # Group by label for counts
    by_label = {}
    for j in judgments:
        lbl = j["label"]
        if lbl not in by_label:
            by_label[lbl] = []
        by_label[lbl].append(j)

    label_order = ["strong", "stable", "emerging", "sparse", "outlier-heavy"]
    tendency_order = ["near-reference", "structural-inside", "symmetric-outside"]

    # ── Non-simulation families ──
    if other_judgments:
        print(f"\n  JUDGMENT — bounded labels from event frequency\n")
        print(f"  {'Family':<50} {'N':>4} {'InBand':>6} {'Freq':>6} {'Label':>14}")
        print(f"  {'─'*50} {'─'*4} {'─'*6} {'─'*6} {'─'*14}")

        for j in sorted(other_judgments, key=lambda x: label_order.index(x["label"]) if x["label"] in label_order else 99):
            fk = j["family_key"]
            if len(fk) > 48:
                fk = fk[:45] + "..."
            print(f"  {fk:<50} {j['total']:>4} {j['in_band']:>6} {j['in_band_frequency']:>5.0%} {j['label']:>14}")

    # ── Simulation families with tendency ──
    if sim_judgments:
        print(f"\n  SIMULATION TENDENCY — classification by ratio position\n")
        print(f"  {'Family':<50} {'N':>4} {'MeanR':>8} {'Tendency':>22}")
        print(f"  {'─'*50} {'─'*4} {'─'*8} {'─'*22}")

        for j in sorted(sim_judgments, key=lambda x: tendency_order.index(x["tendency"]) if x["tendency"] in tendency_order else 99):
            fk = j["family_key"]
            if len(fk) > 48:
                fk = fk[:45] + "..."
            print(f"  {fk:<50} {j['total']:>4} {j['mean_ratio']:>8.4f} {j['tendency']:>22}")

        print(f"\n  Tendency counts:")
        by_tendency = {}
        for j in sim_judgments:
            t = j["tendency"]
            by_tendency[t] = by_tendency.get(t, 0) + 1
        for t in tendency_order:
            if by_tendency.get(t, 0):
                print(f"    {t:<22} {by_tendency[t]}")

    # ── Label summary ──
    print(f"\n  Label counts (all families):")
    for lbl in label_order:
        count = len(by_label.get(lbl, []))
        if count:
            print(f"    {lbl:<14} {count}")
    print()
