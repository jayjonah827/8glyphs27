"""
core/manifests.py — Intake manifest support layer.
Prepares the system to accept structured manifests for:
  research, paleography, art, books, languages

A manifest is a JSON file in intake/ that declares:
  - source files to process
  - domain assignment
  - expected record count
  - processing status
"""

import os, json, datetime
from core.paths import INTAKE_DIR
from core.loader import load_json, save_json


MANIFEST_DOMAINS = ["research", "paleography", "art", "books", "languages"]


def create_manifest(domain, title, source_files, notes=""):
    """
    Create a new intake manifest.
    Returns the manifest dict and filepath.
    """
    if domain not in MANIFEST_DOMAINS:
        raise ValueError(f"domain must be one of {MANIFEST_DOMAINS}")

    now = datetime.datetime.now()
    stamp = now.strftime("%Y%m%d_%H%M%S")
    manifest_id = f"manifest_{domain}_{stamp}"

    manifest = {
        "manifest_id": manifest_id,
        "domain": domain,
        "title": title,
        "created": now.isoformat(),
        "source_files": source_files,
        "expected_records": len(source_files),
        "processed_records": 0,
        "status": "pending",  # pending, processing, complete, failed
        "notes": notes,
        "event_ids": []
    }

    fpath = os.path.join(INTAKE_DIR, f"{manifest_id}.json")
    save_json(fpath, manifest)
    return manifest, fpath


def load_all_manifests():
    """Load all manifests from intake/."""
    manifests = []
    if not os.path.isdir(INTAKE_DIR):
        return manifests
    for fname in sorted(os.listdir(INTAKE_DIR)):
        if fname.startswith("manifest_") and fname.endswith(".json"):
            fpath = os.path.join(INTAKE_DIR, fname)
            m = load_json(fpath, None)
            if m and "manifest_id" in m:
                manifests.append(m)
    return manifests


def update_manifest(manifest_id, updates):
    """Update fields on an existing manifest."""
    fpath = os.path.join(INTAKE_DIR, f"{manifest_id}.json")
    m = load_json(fpath, None)
    if not m:
        return None
    m.update(updates)
    save_json(fpath, m)
    return m


def print_manifest_status():
    """Print intake manifest status to terminal."""
    manifests = load_all_manifests()
    print(f"\n  Intake manifests: {len(manifests)}")
    if not manifests:
        print("  No manifests created yet.")
        print("  Supported domains: " + ", ".join(MANIFEST_DOMAINS))
        print()
        return
    print()
    print(f"  {'ID':<40} {'Domain':<14} {'Status':<12} {'Files':>5} {'Done':>5}")
    print(f"  {'─'*40} {'─'*14} {'─'*12} {'─'*5} {'─'*5}")
    for m in manifests:
        mid = m.get("manifest_id", "?")
        if len(mid) > 38:
            mid = mid[:35] + "..."
        print(f"  {mid:<40} {m.get('domain','?'):<14} {m.get('status','?'):<12} {m.get('expected_records',0):>5} {m.get('processed_records',0):>5}")
    print()
