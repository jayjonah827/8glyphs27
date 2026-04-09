#!/usr/bin/env python3
"""
GLYPH-8  —  Local event-cycle intelligence engine.
Not an AI. A math-based system that grows with what you teach it.
Runs entirely on your computer. Nothing goes anywhere.

Modes:
  [F] FRAMEWORK   — 1+2=3 knowledge base
  [M] MATH        — Bayesian difficulty tracker
  [L] LOG         — daily observations, pattern finder
  [E] EVENTS      — glyph event records, convergence band
  [S] SUMMARY     — totals by domain/route/status/band
  [R] FREQUENCY   — recurrence by family
  [J] JUDGMENT    — bounded labels from frequency
  [A] ARCHIVE     — snapshot and restore state
  [I] INTAKE      — manifest tracking for incoming data
  [G] SIMULATIONS — run random games, collect convergence data
  [Q] QUIT

All data stored locally in events/, glyph8_data/, archive/, intake/.
"""

import os, sys, json, math, random, re, datetime
from collections import Counter, defaultdict

# Add project root to path so core/ imports work
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.paths import DATA_DIR, EVENTS_DIR, SCHEMA_DIR
from core import loader, validator, events as ev_mod, summary, frequency, judgment, routing, archive, manifests

# ─────────────────────────────────────────────
#  UTILITIES
# ─────────────────────────────────────────────

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner(mode_name, color_code):
    print(f"\033[{color_code}m")
    print("╔══════════════════════════════════════╗")
    print(f"║  GLYPH-8  ·  {mode_name:<24}║")
    print("╚══════════════════════════════════════╝")
    print("\033[0m")

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

# ─────────────────────────────────────────────
#  MODE F — FRAMEWORK
# ─────────────────────────────────────────────

def tfidf_score(query_tokens, doc_tokens, all_docs):
    tf = Counter(doc_tokens)
    total = len(doc_tokens)
    df = Counter()
    for d in all_docs:
        for word in set(d):
            df[word] += 1
    n = len(all_docs)
    score = 0.0
    for token in query_tokens:
        if token in tf and tf[token] > 0:
            t = tf[token] / total
            idf = math.log((n + 1) / (df.get(token, 0) + 1))
            score += t * idf
    return score

def mode_framework():
    kb = loader.load_data("framework_kb.json", [])
    banner("FRAMEWORK MODE", "32")
    print("Teach me your 1+2=3 system. I store what you write.")
    print("Commands:  add | ask | list | delete | back\n")
    while True:
        cmd = input("F> ").strip().lower()
        if cmd == "back":
            break
        elif cmd == "add":
            title = input("  Title / concept name: ").strip()
            print("  Write the entry (end with a line containing only '---'):")
            lines = []
            while True:
                line = input()
                if line.strip() == "---":
                    break
                lines.append(line)
            body = "\n".join(lines)
            kb.append({"title": title, "body": body, "added": str(datetime.date.today())})
            loader.save_data("framework_kb.json", kb)
            print(f"  Stored: '{title}'\n")
        elif cmd == "list":
            if not kb:
                print("  Nothing stored yet.\n")
            for i, entry in enumerate(kb):
                print(f"  [{i}] {entry['title']}  ({entry.get('added','')})")
            print()
        elif cmd == "ask":
            if not kb:
                print("  Nothing stored yet. Use 'add' first.\n")
                continue
            query = input("  Ask: ").strip()
            q_tokens = tokenize(query)
            all_doc_tokens = [tokenize(e["title"] + " " + e["body"]) for e in kb]
            if len(kb) == 1:
                overlap = set(q_tokens) & set(all_doc_tokens[0])
                if overlap:
                    e = kb[0]
                    print(f"\n  ── {e['title']}")
                    print(f"  {e['body'][:400]}{'...' if len(e['body'])>400 else ''}\n")
                else:
                    print("  No match. Try words from what you stored.\n")
                continue
            scores = [(tfidf_score(q_tokens, dt, all_doc_tokens), i)
                      for i, dt in enumerate(all_doc_tokens)]
            scores.sort(reverse=True)
            top = scores[:3]
            print()
            for score, idx in top:
                if score > 0:
                    e = kb[idx]
                    print(f"  ── {e['title']} (relevance: {score:.3f})")
                    print(f"  {e['body'][:300]}{'...' if len(e['body'])>300 else ''}")
                    print()
            if all(s == 0 for s, _ in top):
                print("  No match found. Try different words or add more entries.\n")
        elif cmd.startswith("delete"):
            parts = cmd.split()
            if len(parts) == 2 and parts[1].isdigit():
                idx = int(parts[1])
                if 0 <= idx < len(kb):
                    removed = kb.pop(idx)
                    loader.save_data("framework_kb.json", kb)
                    print(f"  Removed: '{removed['title']}'\n")
                else:
                    print("  Index out of range.\n")
        elif cmd == "help":
            print("  add      — add a concept to the knowledge base")
            print("  ask      — ask a question, get the most relevant entries back")
            print("  list     — see all stored entries")
            print("  delete N — remove entry by number\n")

# ─────────────────────────────────────────────
#  MODE M — MATH
# ─────────────────────────────────────────────

MATH_TOPICS = {
    "probability":    ["basic probability", "conditional probability", "Bayes theorem",
                       "probability distributions", "expected value", "variance",
                       "law of large numbers", "central limit theorem"],
    "linear_algebra": ["vectors", "vector addition", "dot product", "matrices",
                       "matrix multiplication", "determinants", "eigenvalues",
                       "eigenvectors", "linear transformations"],
    "calculus":       ["limits", "derivatives", "chain rule", "product rule",
                       "integration", "fundamental theorem", "multivariable derivatives",
                       "gradient", "partial derivatives"],
    "statistics":     ["descriptive stats", "mean median mode", "standard deviation",
                       "hypothesis testing", "t-test", "p-value", "regression",
                       "correlation", "confidence intervals"],
}

def mode_math():
    progress = loader.load_data("math_progress.json", {})
    for category, topics in MATH_TOPICS.items():
        for t in topics:
            if t not in progress:
                progress[t] = {"attempts": 0, "correct": 0, "category": category}
    banner("MATH MODE", "33")
    print("Track your math work. I find your weakest area and send you there next.")
    print("Commands:  log | status | suggest | history | back\n")
    while True:
        cmd = input("M> ").strip().lower()
        if cmd == "back":
            loader.save_data("math_progress.json", progress)
            break
        elif cmd == "suggest":
            def beta_mean(t):
                d = progress[t]
                return (d["correct"] + 1) / (d["attempts"] + 2)
            weakest = sorted(progress.keys(), key=beta_mean)[:5]
            print("\n  Next suggested topics (weakest first):")
            for i, t in enumerate(weakest):
                d = progress[t]
                p = beta_mean(t)
                bar = "█" * int(p * 10) + "░" * (10 - int(p * 10))
                print(f"  {i+1}. {t:<35} [{bar}] {p:.0%}  ({d['attempts']} attempts)")
            print()
        elif cmd == "log":
            print("  What topic did you work on?")
            topic = input("  Topic: ").strip().lower()
            matches = [t for t in progress if topic in t or t in topic]
            if not matches:
                print(f"  '{topic}' not in list. Adding as new topic.\n")
                progress[topic] = {"attempts": 0, "correct": 0, "category": "custom"}
                matches = [topic]
            if len(matches) > 1:
                print("  Multiple matches:")
                for i, m in enumerate(matches):
                    print(f"    [{i}] {m}")
                idx = input("  Pick number: ").strip()
                topic = matches[int(idx)] if idx.isdigit() and int(idx) < len(matches) else matches[0]
            else:
                topic = matches[0]
            result = input(f"  Got it right? (y/n): ").strip().lower()
            correct = result == "y"
            progress[topic]["attempts"] += 1
            if correct:
                progress[topic]["correct"] += 1
            def beta_mean(t):
                d = progress[t]
                return (d["correct"] + 1) / (d["attempts"] + 2)
            p = beta_mean(topic)
            print(f"  {topic}: estimated mastery {p:.0%}  ({progress[topic]['correct']}/{progress[topic]['attempts']})\n")
            loader.save_data("math_progress.json", progress)
        elif cmd == "status":
            def beta_mean(t):
                d = progress[t]
                return (d["correct"] + 1) / (d["attempts"] + 2)
            by_category = defaultdict(list)
            for t, d in progress.items():
                by_category[d["category"]].append((t, beta_mean(t), d["attempts"]))
            for cat, items in sorted(by_category.items()):
                items.sort(key=lambda x: x[1])
                print(f"\n  {cat.upper()}")
                for topic, p, attempts in items:
                    bar = "█" * int(p * 10) + "░" * (10 - int(p * 10))
                    print(f"  {topic:<35} [{bar}] {p:.0%}  (n={attempts})")
            print()
        elif cmd == "history":
            total_attempts = sum(d["attempts"] for d in progress.values())
            total_correct = sum(d["correct"] for d in progress.values())
            if total_attempts:
                print(f"\n  Total problems logged: {total_attempts}")
                print(f"  Overall correct: {total_correct} ({total_correct/total_attempts:.0%})\n")
            else:
                print("  Nothing logged yet.\n")

# ─────────────────────────────────────────────
#  MODE L — LOG + PATTERN FINDER
# ─────────────────────────────────────────────

STOPWORDS = set("a an the is are was were be been being have has had do does did will would could should may might shall can i me my we our you your he she it its they them their and or but not so if of in on at to for with by from up about into than then that this what when where who how".split())

def extract_keywords(text):
    tokens = tokenize(text)
    return [t for t in tokens if t not in STOPWORDS and len(t) > 2]

def markov_build(texts, order=1):
    chain = defaultdict(list)
    for text in texts:
        words = text.lower().split()
        for i in range(len(words) - order):
            key = tuple(words[i:i+order])
            chain[key].append(words[i+order])
    return dict(chain)

def markov_generate(chain, seed_word=None, length=20, order=1):
    if not chain:
        return ""
    keys = list(chain.keys())
    if seed_word:
        matches = [k for k in keys if k[0] == seed_word.lower()]
        start = random.choice(matches) if matches else random.choice(keys)
    else:
        start = random.choice(keys)
    result = list(start)
    current = start
    for _ in range(length):
        if current in chain and chain[current]:
            next_word = random.choice(chain[current])
            result.append(next_word)
            current = tuple(result[-order:])
        else:
            break
    return " ".join(result)

def mode_log():
    logs = loader.load_data("log_entries.json", [])
    banner("LOG MODE", "36")
    print("Write daily. I find your patterns over time.")
    print("Commands:  write | patterns | themes | generate | review | back\n")
    while True:
        cmd = input("L> ").strip().lower()
        if cmd == "back":
            break
        elif cmd == "write":
            today = str(datetime.date.today())
            print(f"  [{today}] Write your observation (end with '---'):")
            lines = []
            while True:
                line = input("  ")
                if line.strip() == "---":
                    break
                lines.append(line)
            text = " ".join(lines)
            logs.append({"date": today, "text": text})
            loader.save_data("log_entries.json", logs)
            print(f"  Logged. Total entries: {len(logs)}\n")
        elif cmd == "patterns":
            if len(logs) < 3:
                print("  Need at least 3 entries to find patterns. Keep writing.\n")
                continue
            all_keywords = []
            for entry in logs:
                all_keywords.extend(extract_keywords(entry["text"]))
            freq = Counter(all_keywords)
            print(f"\n  Top recurring words across {len(logs)} entries:")
            for word, count in freq.most_common(15):
                bar = "█" * min(count, 30)
                print(f"  {word:<20} {bar} ({count})")
            print()
        elif cmd == "themes":
            if len(logs) < 5:
                print("  Need at least 5 entries for theme analysis.\n")
                continue
            weekly = defaultdict(list)
            for entry in logs:
                try:
                    d = datetime.date.fromisoformat(entry["date"])
                    week = d.isocalendar()[:2]
                    weekly[week].extend(extract_keywords(entry["text"]))
                except:
                    pass
            print(f"\n  Themes by week:")
            for week in sorted(weekly.keys())[-6:]:
                freq = Counter(weekly[week])
                top = [w for w, _ in freq.most_common(5)]
                print(f"  Week {week[1]}/{week[0]}: {', '.join(top)}")
            print()
        elif cmd == "generate":
            if len(logs) < 5:
                print("  Need at least 5 entries to generate.\n")
                continue
            texts = [e["text"] for e in logs]
            chain = markov_build(texts, order=2)
            seed = input("  Seed word (or press Enter for random): ").strip() or None
            generated = markov_generate(chain, seed_word=seed, length=25, order=2)
            print(f"\n  Generated from your patterns:\n  \"{generated}\"\n")
        elif cmd == "review":
            if not logs:
                print("  No entries yet.\n")
                continue
            n = min(10, len(logs))
            print(f"\n  Last {n} entries:")
            for entry in logs[-n:]:
                print(f"  [{entry['date']}] {entry['text'][:120]}{'...' if len(entry['text'])>120 else ''}")
            print()

# ─────────────────────────────────────────────
#  MODE E — EVENTS
# ─────────────────────────────────────────────

def mode_events():
    banner("EVENTS MODE", "35")
    schema = loader.load_event_schema()
    if schema:
        print(f"  Schema loaded: {schema.get('schema_name', '?')} ({schema.get('$schema_version', '?')})")
    else:
        print("  WARNING: schemas/event_schema_v1.json not found.")
    all_events, errors = loader.load_all_events()
    print(f"  {len(all_events)} event records loaded.")
    if errors:
        print(f"  {len(errors)} files skipped.")
    print("\n  Commands:  summary | list | inspect | create | recompute | validate | back\n")
    while True:
        cmd = input("E> ").strip().lower()
        if cmd == "back":
            break
        elif cmd == "summary":
            summary.print_summary()
        elif cmd == "list":
            all_events, _ = loader.load_all_events()
            if not all_events:
                print("  No events.\n")
                continue
            for ev in all_events:
                rid = ev.get("record_id", "?")
                title = ev.get("title", "?")
                domain = ev.get("domain", "?")
                status = ev.get("routing", {}).get("status", "?")
                ratio = ev.get("metrics", {}).get("clustering_ratio", "?")
                band = "Y" if ev.get("metrics", {}).get("inside_band") else "N"
                print(f"  {rid}  {domain:<14} {status:<8} r={ratio}  band={band}  {title}")
            print()
        elif cmd == "inspect":
            all_events, _ = loader.load_all_events()
            if not all_events:
                print("  No events loaded.\n")
                continue
            rid = input("  Record ID (e.g. gev_000001): ").strip()
            match = [ev for ev in all_events if ev.get("record_id") == rid]
            if not match:
                print(f"  No record found for '{rid}'.\n")
                continue
            print(json.dumps(match[0], indent=2))
            print()
        elif cmd == "create":
            ev_mod.create_event_from_input()
        elif cmd == "recompute":
            count = ev_mod.recompute_all()
            print(f"  Recomputed metrics for {count} events.\n")
        elif cmd == "validate":
            all_events, errors = loader.load_all_events()
            print(f"\n  Validating {len(all_events)} records...")
            for ev in all_events:
                v = validator.full_validate(ev)
                rid = ev.get("record_id", "?")
                status = "OK" if v["valid"] else "ISSUES"
                live = "LIVE" if v["live_ready"] else "NOT-LIVE"
                print(f"  {rid}  {status:<8} {live:<10}", end="")
                if v["missing_fields"]:
                    print(f"  missing: {v['missing_fields']}", end="")
                if v["enum_violations"]:
                    print(f"  enums: {v['enum_violations']}", end="")
                print()
            print()
        elif cmd == "help":
            print("  summary   — total counts by domain, route, status, convergence")
            print("  list      — one-line per event")
            print("  inspect   — full JSON of one record")
            print("  create    — new event from terminal input")
            print("  recompute — recalculate all metrics from raw fields")
            print("  validate  — check all records against schema rules")
            print("  back      — return to main menu\n")

# ─────────────────────────────────────────────
#  MODE S — SUMMARY
# ─────────────────────────────────────────────

def mode_summary():
    banner("SUMMARY MODE", "34")
    summary.print_summary()
    print("  Press Enter to return.")
    input()

# ─────────────────────────────────────────────
#  MODE R — FREQUENCY
# ─────────────────────────────────────────────

def mode_frequency():
    banner("FREQUENCY MODE", "33")
    frequency.print_frequency_table()
    print("  Press Enter to return.")
    input()

# ─────────────────────────────────────────────
#  MODE J — JUDGMENT
# ─────────────────────────────────────────────

def mode_judgment():
    banner("JUDGMENT MODE", "31")
    judgment.print_judgments()
    print("  Press Enter to return.")
    input()

# ─────────────────────────────────────────────
#  MODE A — ARCHIVE
# ─────────────────────────────────────────────

def mode_archive():
    banner("ARCHIVE MODE", "90")
    archive.print_archive_status()
    print("  Commands:  snap | list | restore | back\n")
    while True:
        cmd = input("A> ").strip().lower()
        if cmd == "back":
            break
        elif cmd == "snap":
            reason = input("  Reason (or press Enter for 'manual'): ").strip() or "manual"
            snap_dir, count = archive.create_snapshot(reason)
            print(f"  Snapshot created: {count} records archived.")
            print(f"  Location: {snap_dir}\n")
        elif cmd == "list":
            archive.print_archive_status()
        elif cmd == "restore":
            snapshots = archive.list_snapshots()
            if not snapshots:
                print("  No snapshots to restore from.\n")
                continue
            sid = input("  Snapshot ID to restore: ").strip()
            confirm = input(f"  Restore from {sid}? Current state will be archived first. (y/n): ").strip().lower()
            if confirm == "y":
                count, backup = archive.restore_snapshot(sid)
                if count > 0:
                    print(f"  Restored {count} records from {sid}.")
                    print(f"  Previous state backed up.\n")
                else:
                    print(f"  Snapshot '{sid}' not found or empty.\n")
        elif cmd == "help":
            print("  snap    — create a snapshot of current events")
            print("  list    — show all snapshots")
            print("  restore — restore from a snapshot (auto-backs up current first)")
            print("  back    — return to main menu\n")

# ─────────────────────────────────────────────
#  MODE I — INTAKE
# ─────────────────────────────────────────────

def mode_intake():
    banner("INTAKE MODE", "36")
    manifests.print_manifest_status()
    print("  Commands:  status | create | back\n")
    while True:
        cmd = input("I> ").strip().lower()
        if cmd == "back":
            break
        elif cmd == "status":
            manifests.print_manifest_status()
        elif cmd == "create":
            domain = input("  Domain (research/paleography/art/books/languages): ").strip().lower()
            title = input("  Manifest title: ").strip()
            print("  Source files (one per line, '---' to end):")
            files = []
            while True:
                line = input("  ").strip()
                if line == "---":
                    break
                if line:
                    files.append(line)
            notes = input("  Notes (optional): ").strip()
            try:
                m, fpath = manifests.create_manifest(domain, title, files, notes)
                print(f"  Manifest created: {m['manifest_id']}")
                print(f"  Files: {len(files)}  Status: pending\n")
            except ValueError as e:
                print(f"  Error: {e}\n")
        elif cmd == "help":
            print("  status  — show all manifests")
            print("  create  — create a new intake manifest")
            print("  back    — return to main menu\n")

# ─────────────────────────────────────────────
#  MODE G — SIMULATIONS
# ─────────────────────────────────────────────

def mode_simulations():
    banner("SIMULATIONS MODE", "33")
    sim_path = os.path.join(ROOT_DIR, "glyph_simulations.py")
    if not os.path.exists(sim_path):
        print("  ERROR: glyph_simulations.py not found.")
        print(f"  Expected: {sim_path}")
        print("  Press Enter to return.")
        input()
        return

    import importlib.util
    spec = importlib.util.spec_from_file_location("glyph_simulations", sim_path)
    sims = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sims)

    print("  Games loaded:")
    for gk, _, desc, _ in sims.ALL_GAMES:
        print(f"    {gk:<20} {desc}")
    print(f"\n  Commands:  runall | quick | single | list | back\n")
    while True:
        cmd = input("G> ").strip().lower()
        if cmd == "back":
            break
        elif cmd == "runall":
            n_raw = input("  Trials per game (default 1000000, max 10000000): ").strip()
            n = int(n_raw) if n_raw.isdigit() else 1000000
            n = min(n, 10000000)
            if n < 1:
                n = 1000000
            print(f"  Running {n:,} trials per game...")
            sims.run_all_trials(n)
        elif cmd == "quick":
            print("  Running all games at 10,000 trials (fast test)...")
            sims.run_all_trials(10000)
        elif cmd == "single":
            game = input("  Game key: ").strip().lower()
            n_raw = input("  Trials (default 1000000, max 10000000): ").strip()
            n = int(n_raw) if n_raw.isdigit() else 1000000
            n = min(n, 10000000)
            if n < 1:
                n = 1000000
            sims.run_single(game, n)
        elif cmd == "list":
            print("\n  Available games:")
            for gk, _, desc, _ in sims.ALL_GAMES:
                print(f"    {gk:<20} {desc}")
            print()
        elif cmd == "help":
            print("  runall  — run all 7 games in sequence (specify trial count)")
            print("  quick   — run all 7 games at 10K trials (fast test)")
            print("  single  — run one game by key name")
            print("  list    — show available games")
            print("  back    — return to main menu\n")

# ─────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────

MENU_ITEMS = [
    ("F", "Framework",   "1+2=3, Heyer Livin knowledge base"),
    ("M", "Math",        "track progress, find weak spots"),
    ("L", "Log",         "daily entries, pattern finder"),
    ("E", "Events",      "glyph event records, convergence band"),
    ("S", "Summary",     "totals by domain, route, status, band"),
    ("R", "Frequency",   "recurrence by event family"),
    ("J", "Judgment",    "bounded labels from frequency"),
    ("A", "Archive",     "snapshot and restore state"),
    ("I", "Intake",      "manifest tracking for incoming data"),
    ("G", "Simulations", "run random games, collect convergence data"),
    ("Q", "Quit",        ""),
]

MENU_DISPATCH = {
    "F": mode_framework,
    "M": mode_math,
    "L": mode_log,
    "E": mode_events,
    "S": mode_summary,
    "R": mode_frequency,
    "J": mode_judgment,
    "A": mode_archive,
    "I": mode_intake,
    "G": mode_simulations,
}

def print_menu():
    for key, name, desc in MENU_ITEMS:
        if key == "Q":
            print(f"  [{key}]  {name}")
        else:
            print(f"  [{key}]  {name:<14} — {desc}")
    print()

def main_menu_header():
    keys = " ".join(f"[{k}]{n}" for k, n, _ in MENU_ITEMS)
    print(f"  {keys}\n")

def main():
    clear()
    print("\033[32m")
    print("  ╔════════════════════════════════════════════╗")
    print("  ║                                            ║")
    print("  ║   G L Y P H - 8                            ║")
    print("  ║   Local event-cycle intelligence engine     ║")
    print("  ║   Math-based. Honest. Yours.               ║")
    print("  ║                                            ║")
    print("  ╚════════════════════════════════════════════╝")
    print("\033[0m")
    print_menu()

    while True:
        choice = input("GLYPH-8> ").strip().upper()
        if choice == "Q":
            print("\n  Data saved locally. See events/, glyph8_data/, archive/.\n")
            break
        elif choice in MENU_DISPATCH:
            clear()
            MENU_DISPATCH[choice]()
            clear()
            main_menu_header()
        else:
            valid = " / ".join(k for k, _, _ in MENU_ITEMS)
            print(f"  {valid}\n")

if __name__ == "__main__":
    main()
