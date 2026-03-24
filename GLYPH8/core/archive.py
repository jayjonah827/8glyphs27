"""
core/archive.py — Snapshot logic for major state changes.
Preserve history locally. Never overwrite important state without archiving first.
"""

import os, json, datetime, shutil
from core.paths import ARCHIVE_DIR, EVENTS_DIR, ARCHIVE_LOG
from core.loader import load_json, save_json, load_all_events


def _archive_log():
    """Load archive log (list of snapshot entries)."""
    return load_json(ARCHIVE_LOG, [])


def _save_archive_log(log):
    """Save archive log."""
    save_json(ARCHIVE_LOG, log)


def create_snapshot(reason="manual"):
    """
    Snapshot the current state of events/ into archive/snap_YYYYMMDD_HHMMSS/.
    Copies all event JSON files into the snapshot folder.
    Logs the snapshot in archive_log.json.
    Returns the snapshot directory path.
    """
    now = datetime.datetime.now()
    stamp = now.strftime("%Y%m%d_%H%M%S")
    snap_dir = os.path.join(ARCHIVE_DIR, f"snap_{stamp}")
    os.makedirs(snap_dir, exist_ok=True)

    # Copy all event files
    count = 0
    if os.path.isdir(EVENTS_DIR):
        for fname in os.listdir(EVENTS_DIR):
            if fname.endswith(".json"):
                src = os.path.join(EVENTS_DIR, fname)
                dst = os.path.join(snap_dir, fname)
                shutil.copy2(src, dst)
                count += 1

    # Log it
    log = _archive_log()
    entry = {
        "snapshot_id": f"snap_{stamp}",
        "timestamp": now.isoformat(),
        "reason": reason,
        "event_count": count,
        "path": snap_dir
    }
    log.append(entry)
    _save_archive_log(log)

    return snap_dir, count


def list_snapshots():
    """Return list of all snapshot entries from the archive log."""
    return _archive_log()


def restore_snapshot(snapshot_id):
    """
    Restore events/ from a snapshot. Archives current state first.
    Returns (restored_count, backup_path).
    """
    log = _archive_log()
    match = [e for e in log if e["snapshot_id"] == snapshot_id]
    if not match:
        return 0, None

    snap_path = match[0]["path"]
    if not os.path.isdir(snap_path):
        return 0, None

    # Archive current state first
    backup_path, _ = create_snapshot(reason=f"pre-restore backup before {snapshot_id}")

    # Clear events/
    if os.path.isdir(EVENTS_DIR):
        for fname in os.listdir(EVENTS_DIR):
            if fname.endswith(".json"):
                os.remove(os.path.join(EVENTS_DIR, fname))

    # Copy from snapshot
    count = 0
    for fname in os.listdir(snap_path):
        if fname.endswith(".json"):
            src = os.path.join(snap_path, fname)
            dst = os.path.join(EVENTS_DIR, fname)
            shutil.copy2(src, dst)
            count += 1

    return count, backup_path


def print_archive_status():
    """Print archive status to terminal."""
    snapshots = list_snapshots()
    print(f"\n  Archive snapshots: {len(snapshots)}")
    if not snapshots:
        print("  No snapshots taken yet. Use 'snap' to create one.\n")
        return
    print()
    for s in snapshots[-10:]:  # show last 10
        print(f"  {s['snapshot_id']}  {s['timestamp'][:19]}  records={s['event_count']}  reason={s['reason']}")
    if len(snapshots) > 10:
        print(f"  ... and {len(snapshots) - 10} older snapshots")
    print()
