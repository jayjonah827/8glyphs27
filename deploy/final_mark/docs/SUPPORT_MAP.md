# CLAIMS SUPPORT MAP — Source Verification
## Heyer Livin LLC | K(t) Patent | 2026-03-29 | Sweep-Verified

### CLAIM 1 (Method — Independent)
**Element: Receive dataset, compute K(t), classify into 3 zones**

| Sub-element | Source | Path | Verified |
|-------------|--------|------|----------|
| K(t) formula | PATENT_v2_SYSTEM_SPEC | DECK_4/patent_ip/ | YES doc, NO code |
| Dataset receipt | glyph8.py Intake mode | CIA/wrriten layer/03_RESEARCH/GLYPH8/ | YES |
| 3-zone classification | glyph_simulations.py write_event() | Same | YES — band_min=0.30, band_max=0.49 |
| 4 comparison modes | glyph8.py 10 modes | Same | YES |

### CLAIM 2 (Dependent on 1)
**Element: resolveField() before choose()**

| Sub-element | Source | Path | Verified |
|-------------|--------|------|----------|
| Field-first architecture | PATENT_v2_SYSTEM_SPEC | DECK_4/patent_ip/ | YES |
| Code implementation | 7 game functions | CIA/wrriten layer/03_RESEARCH/GLYPH8/ | YES logic, NO naming |

### CLAIM 3 (Dependent on 1)
**Element: Dual-coin randomization**

| Sub-element | Source | Path | Verified |
|-------------|--------|------|----------|
| Two-stage random | All 7 games | CIA/wrriten layer/03_RESEARCH/GLYPH8/ | YES |

### CLAIM 4 (Dependent on 1)
**Element: Applied across 2+ domains**

| Sub-element | Source | Path | Verified |
|-------------|--------|------|----------|
| 12 datasets | ChoiceIsNotChance_13Tests_MasterDataset.xlsx | DECK_2/datasets/ | YES |
| 7+ domains | CLAUDE.md convergence proof | .claude/CLAUDE.md | YES — food service, historical demographics, politics, discrimination, labor, ancient civilizations, consumer branding, electoral |

### CLAIM 5 (Dependent on 1)
**Element: Structural constant converges to ~0.39**

| Sub-element | Source | Path | Verified |
|-------------|--------|------|----------|
| Grand mean 0.390992 | CLAUDE.md | .claude/CLAUDE.md | YES |
| SD 0.019778 | CLAUDE.md | .claude/CLAUDE.md | YES |
| 95% CI [0.3798, 0.4022] | CLAUDE.md | .claude/CLAUDE.md | YES |
| 13 statistical tests | CLAUDE.md | .claude/CLAUDE.md | YES — Tests A-F, p values |
| 12 individual values | CLAUDE.md table | .claude/CLAUDE.md | YES — range 0.35 to 0.43 |

### CLAIM 6 (System — Independent)
**Element: Processor, memory, instructions executing K(t)**

| Sub-element | Source | Path | Verified |
|-------------|--------|------|----------|
| Standard patent language | PATENT_v2_SYSTEM_SPEC | DECK_4/patent_ip/ | YES |
| Running code | glyph8.py (662 lines) | CIA/wrriten layer/03_RESEARCH/GLYPH8/ | YES |

### CLAIM 7 (Dependent on 6)
**Element: 21-field event records**

| Sub-element | Source | Path | Verified |
|-------------|--------|------|----------|
| Event schema spec | Documentation | Memory file 04 | YES |
| write_event() | glyph_simulations.py | CIA/wrriten layer/03_RESEARCH/GLYPH8/ | PARTIAL — fewer than 21 fields |

### CLAIM 8 (Dependent on 6)
**Element: Checkpoint captures**

| Sub-element | Source | Path | Verified |
|-------------|--------|------|----------|
| Checkpoint list | glyph_simulations.py | CIA/wrriten layer/03_RESEARCH/GLYPH8/ | YES — [1K, 10K, 100K, 500K, 1M] |

### CLAIM 9 (CRM — Independent)
**Element: Non-transitory CRM for constraint-informed customer management**

| Sub-element | Source | Path | Verified |
|-------------|--------|------|----------|
| CRM description | PATENT_v2_SYSTEM_SPEC | DECK_4/patent_ip/ | YES doc, NO code |

### CLAIM 10 (Dependent on 9)
**Element: Constraint detection informs resource allocation**

| Sub-element | Source | Path | Verified |
|-------------|--------|------|----------|
| Resource allocation | PATENT_v2_SYSTEM_SPEC | DECK_4/patent_ip/ | YES doc, NO code |

### VERIFICATION SUMMARY

| Claims | File-Backed | Doc-Only | Gap |
|--------|-------------|----------|-----|
| 1-5 (Method) | YES | K(t) formula | resolveField() naming |
| 6-8 (System) | YES | — | Event schema field count |
| 9-10 (CRM) | NO | YES | No CRM code exists |

**8 of 10 claims have verifiable file-backed support.**
**2 claims (CRM) are document-only. Acceptable for provisional filing.**
