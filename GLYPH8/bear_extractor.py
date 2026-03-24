"""
bear_extractor.py — Extract patterns, topics, and standalone lines from Bear notes.
Reads Bear's SQLite database directly. Builds a content database (JSON) for the site.

Output:
  content_db.json — all extracted content with topic tags, pattern scores, message candidates
  daily_messages.json — curated standalone lines for site daily rotation

This script measures what exists. It does not invent content.
"""

import sqlite3
import json
import re
import os
from collections import Counter
from datetime import datetime

# ── Configuration ──
BEAR_DB = os.path.expanduser(
    "~/Library/Group Containers/9K33E3U3T4.net.shinyfrog.bear/Application Data/database.sqlite"
)
# Fallback: if copied to Desktop
BEAR_DB_FALLBACK = os.path.expanduser("~/Desktop/bear_notes.sqlite")
# Sandbox fallback
BEAR_DB_SANDBOX = "/sessions/practical-dazzling-fermi/mnt/Desktop/bear_notes.sqlite"

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DB_PATH = os.path.join(OUTPUT_DIR, "content_db.json")
DAILY_MSG_PATH = os.path.join(OUTPUT_DIR, "daily_messages.json")

# ── Topic keywords (detected, not invented) ──
TOPIC_KEYWORDS = {
    "business": ["business", "llc", "heyer livin", "revenue", "brand", "marketing",
                  "client", "sales", "consulting", "entrepreneur", "store", "trademark"],
    "math": ["equation", "ratio", "convergence", "probability", "dataset", "simulation",
             "formula", "clustering", "band", "reference point", "coin", "glyph"],
    "family": ["mama", "father", "mother", "nanny", "papa", "grandmother", "grandfather",
               "sarah jane", "john lawrence", "jair", "valley", "lineage", "transmission"],
    "art": ["design", "art", "canvas", "illustration", "drawing", "creative",
            "collage", "color", "palette", "visual"],
    "justice": ["court", "legal", "law", "rights", "discrimination", "housing",
                "police", "justice", "freedom", "slavery", "protest", "inequality"],
    "education": ["class", "professor", "assignment", "lecture", "textbook", "university",
                  "study", "exam", "chapter", "statistics", "research", "academic"],
    "philosophy": ["consciousness", "reality", "truth", "existence", "god", "spirit",
                   "soul", "meaning", "life", "death", "purpose", "humanity"],
    "goals": ["goal", "plan", "month", "year", "future", "achieve", "build",
              "driving", "property", "wealth", "career", "job"],
    "identity": ["black", "culture", "heritage", "african", "oakland", "community",
                 "diaspora", "tradition", "oral", "ancestor"],
    "technology": ["code", "python", "website", "github", "engine", "database",
                   "algorithm", "software", "api", "server"]
}

# ── Stop words for pattern detection ──
STOP_WORDS = set("the a an is are was were be been being have has had do does did "
                 "will would shall should may might must can could of in to for on "
                 "with at by from as into through during before after above below "
                 "between out off over under again further then once here there when "
                 "where why how all each every both few more most other some such no "
                 "nor not only own same so than too very and but or if it its i my me "
                 "we our you your he his she her they them their what which who whom "
                 "this that these those am".split())


def connect_bear():
    """Connect to Bear's SQLite database."""
    if os.path.exists(BEAR_DB):
        return sqlite3.connect(BEAR_DB)
    if os.path.exists(BEAR_DB_FALLBACK):
        return sqlite3.connect(BEAR_DB_FALLBACK)
    if os.path.exists(BEAR_DB_SANDBOX):
        return sqlite3.connect(BEAR_DB_SANDBOX)
    raise FileNotFoundError(
        f"Bear database not found at:\n  {BEAR_DB}\n  {BEAR_DB_FALLBACK}\n"
        f"Copy it: cp ~/Library/Group\\ Containers/9K33E3U3T4.net.shinyfrog.bear/"
        f"Application\\ Data/database.sqlite ~/Desktop/bear_notes.sqlite"
    )


def load_notes():
    """Load all active (non-trashed) notes from Bear."""
    conn = connect_bear()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ZTITLE, ZTEXT, ZCREATIONDATE, ZMODIFICATIONDATE
        FROM ZSFNOTE
        WHERE ZTRASHED = 0 AND ZPERMANENTLYDELETED = 0 AND ZENCRYPTED = 0
        ORDER BY ZMODIFICATIONDATE DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    notes = []
    for title, text, created, modified in rows:
        if not text:
            continue
        # Bear stores dates as Core Data timestamps (seconds since 2001-01-01)
        epoch_offset = 978307200  # difference between 2001-01-01 and 1970-01-01
        created_dt = datetime.fromtimestamp(created + epoch_offset).isoformat() if created else None
        modified_dt = datetime.fromtimestamp(modified + epoch_offset).isoformat() if modified else None

        notes.append({
            "title": title or "(untitled)",
            "text": text,
            "created": created_dt,
            "modified": modified_dt
        })
    return notes


def strip_bear_markup(text):
    """Remove Bear markdown/markup for clean text analysis."""
    # Remove Bear-specific tags like #tag/subtag
    text = re.sub(r'#[\w/\-]+', '', text)
    # Remove markdown headers
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    # Remove bold/italic markers
    text = re.sub(r'[*_]{1,3}', '', text)
    # Remove links
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove image refs
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # Remove file:// paths
    text = re.sub(r'file://\S+', '', text)
    # Clean up extra whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def extract_lines(text):
    """Extract individual lines from note text."""
    clean = strip_bear_markup(text)
    lines = []
    for line in clean.split('\n'):
        line = line.strip()
        if len(line) > 10:  # skip trivially short lines
            lines.append(line)
    return lines


def classify_topics(text):
    """Classify a note into topics based on keyword presence."""
    lower = text.lower()
    topics = []
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in lower)
        if score >= 2:
            topics.append({"topic": topic, "score": score})
    topics.sort(key=lambda x: x["score"], reverse=True)
    return [t["topic"] for t in topics]


def find_recurring_phrases(notes, min_count=3, min_words=2, max_words=5):
    """Find phrases that recur across multiple notes."""
    phrase_counter = Counter()

    for note in notes:
        clean = strip_bear_markup(note["text"]).lower()
        words = re.findall(r'\b[a-z]+\b', clean)
        words = [w for w in words if w not in STOP_WORDS and len(w) > 2]

        seen_in_note = set()
        for n in range(min_words, max_words + 1):
            for i in range(len(words) - n + 1):
                phrase = " ".join(words[i:i+n])
                if phrase not in seen_in_note:
                    seen_in_note.add(phrase)
                    phrase_counter[phrase] += 1

    # Filter to phrases appearing in min_count+ notes
    recurring = {phrase: count for phrase, count in phrase_counter.items()
                 if count >= min_count}
    return dict(sorted(recurring.items(), key=lambda x: x[1], reverse=True)[:100])


def extract_standalone_messages(notes, min_len=40, max_len=200):
    """
    Extract lines that work as standalone daily messages.
    Criteria: declarative, self-contained, human-written prose.
    Filters out: URLs, code, academic logistics, data rows, lists,
    timestamps, filenames, bare labels, and fragmented text.
    """
    candidates = []
    seen = set()

    # Patterns that indicate data rows, not prose
    DATA_PATTERNS = re.compile(
        r'^\d+[\s,\t]|'           # starts with number + separator (CSV/table rows)
        r'^\s*[-•]\s|'            # bullet list items
        r'^\s*\d+\.\s|'           # numbered list items
        r'\t.*\t|'                # tab-separated data
        r',\s*\d+\.\d+|'         # comma-separated decimals (dataset)
        r'^\w+:\s*$|'            # bare labels like "Title:"
        r'^\[.*\]$|'             # bracketed metadata
        r'^\(.*\)$|'             # parenthetical-only lines
        r'^\d{1,2}[:/]\d{2}|'   # timestamps
        r'\.(py|js|html|css|json|csv|txt|md|pdf|png|jpg|svg)\b|'  # filenames
        r'^(true|false|null|none|nan)\s*$'  # bare data values
    , re.IGNORECASE)

    SKIP_FRAGMENTS = [
        "http", "file://", "import ", "def ", "class ", "```",
        "assignment", "submit", "chapter ", "page ", "quiz",
        "homework", "due date", "grading", "exam ", "midterm",
        "final exam", "syllabus", "lecture ",
        "=", "+=", "->", "=>", "||", "&&",  # code operators
        "{", "}", "< /", "/>",               # code brackets
        "select ", "from ", "where ",         # SQL
        "null", "undefined", "function(",     # code
        "todo:", "fixme:", "hack:",           # code comments
        "screenshot", "attached", "see below",
        "click here", "tap to", "swipe",
        "price:", "qty:", "sku:", "item #",   # commerce data
        "row ", "column ", "cell ",           # spreadsheet refs
        "recipe:", "steep ", "simmer ", "blend ",  # recipes
        "tbsp", "tsp", "cup ", "oz ",              # measurements
        "day 1", "day 2", "day 3", "day 4", "day 5",  # calendars
        "day 6", "day 7", "day 8", "day 9",
        "day 10", "day 11", "day 12", "day 13",
        "day 14", "day 15", "day 16", "day 17",
        "day 18", "day 19", "day 20", "day 21",
        "day 22", "day 23", "day 24", "day 25",
        "day 26", "day 27", "day 28", "day 29", "day 30",
        "reel ", "static ", "story ",  # social media calendar
        "cta ", "countdown ",
        "◦\t", "◦ ", "•\t",           # outline markers
        "analysis:", "transition to",  # academic outline
        "body paragraph", "thesis statement",
        "disembarked", "embarked", "voyage",  # slave trade dataset
        "captured", "intended destination",
        "use ", "why it works",        # instructional
    ]

    for note in notes:
        lines = extract_lines(note["text"])
        topics = classify_topics(note["text"])

        for line in lines:
            lower = line.lower().strip()

            # Skip unwanted fragments
            if any(skip in lower for skip in SKIP_FRAGMENTS):
                continue

            # Length filter — tighter minimum catches more prose
            if len(line) < min_len or len(line) > max_len:
                continue

            # Skip data patterns
            if DATA_PATTERNS.search(line):
                continue

            # Skip lines that are mostly numbers or code
            alpha_ratio = sum(1 for c in line if c.isalpha()) / len(line)
            if alpha_ratio < 0.6:
                continue

            # Skip ALL CAPS lines longer than 60 chars (headers/labels)
            if line.isupper() and len(line) > 60:
                continue

            # Require at least one space (filters single-word lines)
            if ' ' not in line.strip():
                continue

            # Require at least 5 words — real sentences
            word_count = len(line.split())
            if word_count < 5:
                continue

            # Must contain at least one lowercase letter (filters ALL-CAPS headers)
            if not any(c.islower() for c in line):
                continue

            # Sentence quality: should end with period, question mark, or no trailing colon/dash
            last_char = line.rstrip()[-1] if line.rstrip() else ''
            if last_char in [':', '—', '–', '-', ',']:
                continue

            # Skip lines with excessive punctuation (code, data)
            punct_ratio = sum(1 for c in line if c in '()[]{}|<>=+*&^%$@~`\\') / len(line)
            if punct_ratio > 0.08:
                continue

            # Dedup
            normalized = lower
            if normalized in seen:
                continue
            seen.add(normalized)

            # Score for personal voice quality
            score = 0
            # First person = personal writing
            if any(p in lower for p in [' i ', ' my ', ' me ', "i'm", "i've", ' we ', ' our ']):
                score += 3
            # Declarative endings
            if line.rstrip().endswith('.'):
                score += 2
            # Philosophical/reflective markers
            if any(w in lower for w in ['truth', 'reality', 'meaning', 'consciousness',
                                         'freedom', 'culture', 'purpose', 'power',
                                         'system', 'pattern', 'living', 'higher']):
                score += 2
            # Penalize instructional/reference tone
            if any(w in lower for w in ['module', 'lesson', 'step ', 'access ',
                                         'ebook', 'credit score', 'credit card',
                                         'payment', 'billing', 'enrollment',
                                         'graphic design', 'accounting']):
                score -= 3
            # Penalize quotes (not original voice)
            if line.startswith('"') or line.startswith('"') or line.startswith("'"):
                score -= 1

            if score < 1:
                continue

            candidates.append({
                "text": line,
                "source_title": note["title"],
                "topics": topics[:3],
                "length": len(line),
                "word_count": word_count,
                "voice_score": score,
                "created": note["created"]
            })

    # Sort by voice score descending, cap at 500 for daily rotation
    candidates.sort(key=lambda x: x["voice_score"], reverse=True)
    return candidates[:500]


def find_writing_patterns(notes):
    """Analyze writing patterns: avg sentence length, vocabulary density, etc."""
    all_words = []
    sentence_lengths = []
    line_counts = []

    for note in notes:
        clean = strip_bear_markup(note["text"])
        words = re.findall(r'\b[a-z]+\b', clean.lower())
        all_words.extend(words)

        sentences = re.split(r'[.!?]+', clean)
        for s in sentences:
            s_words = s.split()
            if len(s_words) > 2:
                sentence_lengths.append(len(s_words))

        line_counts.append(len(clean.split('\n')))

    word_freq = Counter(all_words)
    # Filter out stop words for meaningful frequency
    meaningful = {w: c for w, c in word_freq.items()
                  if w not in STOP_WORDS and len(w) > 2}
    top_words = dict(sorted(meaningful.items(), key=lambda x: x[1], reverse=True)[:50])

    return {
        "total_notes": len(notes),
        "total_words": len(all_words),
        "unique_words": len(set(all_words)),
        "vocabulary_density": round(len(set(all_words)) / max(len(all_words), 1), 4),
        "avg_sentence_length": round(sum(sentence_lengths) / max(len(sentence_lengths), 1), 1),
        "avg_note_lines": round(sum(line_counts) / max(len(line_counts), 1), 1),
        "top_50_words": top_words
    }


def build_content_database():
    """Main pipeline: load → analyze → classify → output."""
    print("  Loading Bear notes...")
    notes = load_notes()
    print(f"  Found {len(notes)} active notes.\n")

    # Classify each note
    print("  Classifying topics...")
    classified = []
    topic_counts = Counter()
    for note in notes:
        topics = classify_topics(note["text"])
        for t in topics:
            topic_counts[t] += 1
        classified.append({
            "title": note["title"],
            "topics": topics,
            "line_count": len(extract_lines(note["text"])),
            "created": note["created"],
            "modified": note["modified"]
        })

    # Extract standalone messages
    print("  Extracting standalone messages...")
    messages = extract_standalone_messages(notes)
    print(f"  Found {len(messages)} message candidates.\n")

    # Find recurring phrases
    print("  Finding recurring phrases...")
    recurring = find_recurring_phrases(notes)
    print(f"  Found {len(recurring)} recurring phrases.\n")

    # Writing patterns
    print("  Analyzing writing patterns...")
    patterns = find_writing_patterns(notes)

    # Build output
    content_db = {
        "extracted": datetime.now().isoformat(),
        "source": "Bear notes database",
        "stats": patterns,
        "topic_distribution": dict(topic_counts.most_common()),
        "recurring_phrases": recurring,
        "notes_classified": classified,
        "message_candidates": len(messages)
    }

    # Save content DB
    with open(CONTENT_DB_PATH, 'w') as f:
        json.dump(content_db, f, indent=2)
    print(f"  Saved: {CONTENT_DB_PATH}")

    # Save daily messages
    daily = {
        "generated": datetime.now().isoformat(),
        "total": len(messages),
        "messages": messages
    }
    with open(DAILY_MSG_PATH, 'w') as f:
        json.dump(daily, f, indent=2)
    print(f"  Saved: {DAILY_MSG_PATH}")

    # Print summary
    print(f"\n  ═══════════════════════════════════════")
    print(f"  BEAR EXTRACTION COMPLETE")
    print(f"  ═══════════════════════════════════════")
    print(f"  Notes analyzed:       {patterns['total_notes']}")
    print(f"  Total words:          {patterns['total_words']:,}")
    print(f"  Unique words:         {patterns['unique_words']:,}")
    print(f"  Vocabulary density:   {patterns['vocabulary_density']:.2%}")
    print(f"  Avg sentence length:  {patterns['avg_sentence_length']} words")
    print(f"  Message candidates:   {len(messages)}")
    print(f"  Recurring phrases:    {len(recurring)}")
    print(f"\n  Topic distribution:")
    for topic, count in topic_counts.most_common():
        bar = "█" * min(count, 40)
        print(f"    {topic:<14} {count:>3} {bar}")
    print(f"\n  Top 10 words:")
    for word, count in list(patterns["top_50_words"].items())[:10]:
        print(f"    {word:<20} {count:>4}")
    print()


if __name__ == "__main__":
    build_content_database()
