# PRIVATE-FIRST CODEBASE ARCHITECTURE
## hlvn-private — April 2, 2026

---

## SECTION 1 — PRIVATE-FIRST SYSTEM PURPOSE

This codebase is the single controlled source for the entire Heyer Livin system. It governs:

- All operational logic (SOPs, workflows, site paths, stack relationships)
- All research and prototype code (Glyph engine, simulations, validation scripts)
- All portfolio-ready and public-facing content (finished works, exports, showcase assets)
- All protected intellectual property (K(t) formula, patent-sensitive architecture, private frameworks)

It does NOT yet control:

- Wix deployment (heyerlivin.com)
- Fourthwall storefront (heyerlivin.shop)
- GitHub Pages public deployment (glyphhrlvn4culturalnav.space)
- Notion content sync (glyphhrlvn4culturalnav.store)

Those are downstream consumers. This repo is the upstream source. Nothing goes public until it exits this repo through a controlled export path.

---

## SECTION 2 — PRIVATE REPO STRATEGY

Three options ranked:

**Option A: One private monorepo** — RECOMMENDED
- Single `hlvn-private` repo, private on GitHub (jayjonah827/hlvn-private)
- Four master sections as top-level directories
- QmPYcVJCV8277 isolated via .gitignore rules + separate encryption-ready folder
- Public repos (8glyphs27, future heyerlivin-site) pull from export directories only
- Simplest to maintain. One clone. One backup. One source of truth.

**Option B: One private core + future public repos**
- Same as A but formalizes the relationship to 8glyphs27 and future repos
- Public repos are separate GitHub repos that receive exported content
- This is what Option A becomes naturally when public deployment starts

**Option C: Multiple private repos from the start**
- Splits QmPYcVJCV8277 into its own repo immediately
- Adds overhead with no current benefit. The monorepo .gitignore achieves the same isolation.

**Decision: Option A.** One private monorepo. Name: `hlvn-private`. The protected layer stays inside it but is excluded from any future public fork or export.

---

## SECTION 3 — FOUR-SECTION CODE MAPPING

### 1. HEYER_LIVIN_GLYPH_RECORDS/

**Role:** Operational system layer. Infrastructure. Business logic. Deployment config.

**Contains:**
- Site architecture configs (Wix, Fourthwall, GitHub Pages, Notion)
- DNS records and domain mapping docs
- Deployment scripts and checklists
- SOPs (standard operating procedures)
- Workflow definitions
- Commerce stack configuration (Fourthwall, Stripe, payment flows)
- Integration scripts (Notion API, Wix API, Cloudflare Workers)
- Business operations docs (LLC records, vendor relationships)
- Environment configs (.env templates, API key placeholders)

**Does NOT contain:**
- Research data or experiments
- Finished portfolio pieces
- Protected formulas or patent logic
- Raw datasets

**Type:** Config, scripts, operational documentation, integration code.

### 2. GLYPH_KITCHEN/

**Role:** Research and development layer. Experiments. Prototypes. Validation.

**Contains:**
- Glyph-8 engine code (glyph8.py, simulations)
- Glyph-Q quantum specification (conceptual, not operational)
- Dataset processing scripts
- Statistical validation scripts
- SNT integration layer
- Distribution tables and computed outputs
- Comparative models
- Working drafts of research writing
- Prototype logic for SaaS tool
- Test harnesses for constraint detection
- Source material references (not the sources themselves)

**Does NOT contain:**
- The K(t) formula implementation (that is QmPYcVJCV8277)
- Finished publications
- Business SOPs
- Public-facing assets

**Type:** Python code, data processing scripts, research notebooks, working docs.

### 3. GLYPHS/

**Role:** Portfolio and public-facing layer. Finished works. Showcase.

**Contains:**
- Finished HTML blocks (01-home, 02-shop, 03-about, 04-portfolio, 05-blog)
- Public site pages (export-ready for Wix, GitHub Pages)
- Portfolio case studies
- Published writing
- Design assets (SVGs, icons, brand marks)
- Product images and descriptions
- Presentation decks
- Identity works and brand system files
- The Coin / Book of Life public materials
- Export-ready content for all four domains

**Does NOT contain:**
- Unfinished research
- Protected logic
- Internal SOPs
- Raw experiment data

**Type:** HTML, CSS, JS, SVG, images, markdown, export-ready content.

### 4. QmPYcVJCV8277/

**Role:** Protected core. Patent-sensitive. Private formulas. Unreleased theory.

**Contains:**
- K(t) constraint detection formula (full implementation)
- resolveField() logic (core inventive step)
- Dual-coin system internals
- Band derivation logic (when built — currently hardcoded)
- Per-domain C, R, ΔS, ε values
- Patent application drafts
- Legal-sensitive documents
- Private frameworks and internal models
- Unreleased theoretical extensions
- Glyph-Q Hamiltonian construction details
- Epsilon quantum derivation
- Structural entanglement proofs
- Anything that should not appear in public repos

**Does NOT contain:**
- Public-facing content
- Business operations
- General research that can be published
- Portfolio assets

**Type:** Protected Python code, protected documentation, patent drafts, restricted configs.

---

## SECTION 4 — INTERNAL ARCHITECTURE

```
hlvn-private/
├── HEYER_LIVIN_GLYPH_RECORDS/   # Operations layer
│   ├── sites/                    # Site configs per domain
│   ├── deploy/                   # Deployment scripts + checklists
│   ├── sops/                     # Standard operating procedures
│   ├── integrations/             # API scripts (Notion, Wix, Cloudflare)
│   ├── commerce/                 # Fourthwall, payment, product configs
│   └── dns/                      # DNS records, domain mapping
│
├── GLYPH_KITCHEN/                # R&D layer
│   ├── engine/                   # Glyph-8 core engine
│   ├── quantum/                  # Glyph-Q conceptual specs
│   ├── datasets/                 # Processed data (NOT raw protected data)
│   ├── validation/               # Statistical tests, replication scripts
│   ├── prototypes/               # SaaS tool prototypes, UI experiments
│   ├── snt/                      # Standard Normal Table integration
│   └── drafts/                   # Working research writing
│
├── GLYPHS/                       # Portfolio / public layer
│   ├── sites/                    # Export-ready site content per domain
│   │   ├── wix/                  # heyerlivin.com content
│   │   ├── fourthwall/           # heyerlivin.shop blocks
│   │   ├── github_pages/         # glyphhrlvn4culturalnav.space
│   │   └── notion/               # glyphhrlvn4culturalnav.store
│   ├── portfolio/                # Case studies, finished works
│   ├── products/                 # Product descriptions, images
│   ├── icons/                    # GLYPH_ICONS (101 SVGs)
│   ├── writing/                  # Published / publish-ready writing
│   └── presentations/            # Decks, visual presentations
│
├── QmPYcVJCV8277/                # Protected core (NEVER exported)
│   ├── formula/                  # K(t) implementation
│   ├── patent/                   # Patent drafts and legal docs
│   ├── theory/                   # Unreleased theoretical work
│   ├── internals/                # resolveField(), band derivation
│   └── README.md                 # Access rules
│
├── _shared/                      # Shared utilities
│   ├── fonts/                    # Font families (from uploaded HTML)
│   └── styles/                   # Shared CSS/design tokens
│
├── _config/                      # Repo-level configuration
│   ├── .env.template             # API keys placeholder (no real keys)
│   ├── exports.yaml              # Defines what can be exported where
│   └── domains.yaml              # Domain-to-platform mapping
│
├── _exports/                     # Staging area for public deployment
│   ├── wix/                      # Ready to push to Wix
│   ├── github_site1/             # Ready to push to 8glyphs27
│   ├── github_site2/             # Ready to push to .space domain
│   └── notion/                   # Ready to sync to Notion
│
├── .gitignore                    # Blocks QmPYcVJCV8277 from public forks
├── README.md                     # Private repo README
└── RULES.md                      # Implementation rules (Section 10)
```

**Layer breakdown:**

- **App layer:** GLYPH_KITCHEN/engine/, GLYPH_KITCHEN/prototypes/
- **Content layer:** GLYPHS/ (all subdirectories)
- **Integration layer:** HEYER_LIVIN_GLYPH_RECORDS/integrations/, HEYER_LIVIN_GLYPH_RECORDS/deploy/
- **Research layer:** GLYPH_KITCHEN/ (engine, quantum, validation, snt, drafts)
- **Protected layer:** QmPYcVJCV8277/ (entire directory)
- **Config layer:** _config/, .gitignore, domain configs
- **Shared utilities:** _shared/ (fonts, styles, common assets)

---

## SECTION 5 — PROTECTED LOGIC ISOLATION

### What belongs in QmPYcVJCV8277/

- K(t) = C × (1 - R) × ΔS + ε — full parameterized implementation
- resolveField() function — the core inventive step (field resolution before choice)
- Band derivation code (when 0.30/0.50 boundaries are derived, not hardcoded)
- Per-domain constraint parameters (C, R, ΔS, ε for each of 12 datasets)
- Hamiltonian construction (8x8 matrix, eigenvalue computation)
- Epsilon quantum proof (√2 - 1 derivation and constraint operator)
- Patent drafts: PATENT_COMPLETE_FINAL, PATENT_v2_SYSTEM_SPEC, provisional, inventor's disclosure
- 04_LEGAL contents
- Structural entanglement proof details
- Any formula or logic that constitutes the inventive step

### What should NEVER be imported directly into public-facing code

- No file in QmPYcVJCV8277/ should be imported by any file in GLYPHS/
- No file in QmPYcVJCV8277/ should be referenced in _exports/
- No file in QmPYcVJCV8277/ should appear in any public git commit

### How outputs can be derived without exposing internals

The pattern is: **QmPYcVJCV8277 → GLYPH_KITCHEN → GLYPHS**

1. Protected formula lives in QmPYcVJCV8277/formula/
2. GLYPH_KITCHEN/engine/ imports the formula via a local path ONLY in the private repo
3. GLYPH_KITCHEN/engine/ produces computed results (distribution tables, classifications, zone outputs)
4. Those RESULTS (not the formula) move to GLYPHS/ as finished outputs
5. GLYPHS/ content is what gets exported to public sites

The formula never leaves QmPYcVJCV8277. Only its outputs do.

### Preventing accidental leakage

1. `.gitignore` at repo root blocks `QmPYcVJCV8277/` from any fork or public push
2. `_config/exports.yaml` explicitly lists what CAN be exported — QmPYcVJCV8277 is excluded
3. `QmPYcVJCV8277/README.md` states access rules in plain language
4. When public repos are created, they pull from `_exports/` only — never from root
5. Pre-commit hook (future) checks that no file path containing `QmPYcVJCV8277` appears in staged commits to public branches

---

## SECTION 6 — NOTION / WIX / PUBLIC FUTURE HOOKS

### Notion Integration (glyphhrlvn4culturalnav.store)

- Content source: GLYPHS/sites/notion/
- Integration script: HEYER_LIVIN_GLYPH_RECORDS/integrations/notion_sync.py (placeholder)
- Notion API proxy: existing notion-proxy.js Cloudflare Worker (reference in integrations/)
- Content types: gallery pages, portfolio entries, showcase items
- NOT built yet. Hook = the folder structure and a config stub in _config/domains.yaml

### Wix Content Support (heyerlivin.com)

- Content source: GLYPHS/sites/wix/
- Export target: _exports/wix/
- Content types: Book of Life pages, public front door content
- Wix MCP tools available (ManageWixSite, WixSiteBuilder) for future use
- NOT built yet. Hook = folder + export path

### Git Site 1 (8glyphs27 — existing public repo)

- Content source: GLYPHS/sites/github_pages/
- Export target: _exports/github_site1/
- Maps to existing jayjonah827/8glyphs27 repo
- Contains Glyph simulation UI, research presentation
- NOT rebuilt yet. Hook = export path that will replace the current wrong-structure repo

### Git Site 2 (glyphhrlvn4culturalnav.space)

- Content source: GLYPHS/sites/github_pages/ (separate subdirectory or branch)
- Export target: _exports/github_site2/
- Pre-patent provisional research engine
- Post-patent becomes the public constraint detection tool pitch
- NOT built yet. Hook = folder + domain config

### domains.yaml stub defines all four:

```yaml
domains:
  heyerlivin.com:
    platform: wix
    content_source: GLYPHS/sites/wix/
    export_target: _exports/wix/
    status: not_connected
  heyerlivin.shop:
    platform: fourthwall
    content_source: GLYPHS/sites/fourthwall/
    export_target: null  # direct paste into Fourthwall dashboard
    status: connected
  glyphhrlvn4culturalnav.space:
    platform: github_pages
    content_source: GLYPHS/sites/github_pages/
    export_target: _exports/github_site2/
    status: not_connected
  glyphhrlvn4culturalnav.store:
    platform: notion
    content_source: GLYPHS/sites/notion/
    export_target: _exports/notion/
    status: not_connected
```

---

## SECTION 7 — FOLDER / REPO STRUCTURE

See SECTION 4 for the full tree. Repeated here as the definitive reference:

```
hlvn-private/
│
├── HEYER_LIVIN_GLYPH_RECORDS/
│   ├── sites/
│   │   ├── wix.yaml
│   │   ├── fourthwall.yaml
│   │   ├── github_pages.yaml
│   │   └── notion.yaml
│   ├── deploy/
│   │   └── DEPLOY_CHECKLIST.md
│   ├── sops/
│   │   └── .gitkeep
│   ├── integrations/
│   │   ├── notion_sync.py         # placeholder
│   │   └── cloudflare_worker.js   # reference copy of notion-proxy
│   ├── commerce/
│   │   └── fourthwall_config.yaml
│   └── dns/
│       └── heyerlivin_com.zone    # DNS export reference
│
├── GLYPH_KITCHEN/
│   ├── engine/
│   │   ├── glyph8.py              # core engine (public-safe version)
│   │   ├── glyph_simulations.py
│   │   └── requirements.txt
│   ├── quantum/
│   │   └── glyph_q_spec.md        # conceptual spec (no formula)
│   ├── datasets/
│   │   └── .gitkeep
│   ├── validation/
│   │   └── replication_tests.py   # placeholder
│   ├── prototypes/
│   │   └── .gitkeep
│   ├── snt/
│   │   └── snt_integration.py     # placeholder
│   └── drafts/
│       └── .gitkeep
│
├── GLYPHS/
│   ├── sites/
│   │   ├── wix/
│   │   │   └── .gitkeep
│   │   ├── fourthwall/
│   │   │   ├── 01-home-brand.html
│   │   │   ├── 02-shop.html
│   │   │   ├── 03-about.html
│   │   │   ├── 04-portfolio.html
│   │   │   └── 05-blog.html
│   │   ├── github_pages/
│   │   │   └── .gitkeep
│   │   └── notion/
│   │       └── .gitkeep
│   ├── portfolio/
│   │   └── .gitkeep
│   ├── products/
│   │   └── .gitkeep
│   ├── icons/
│   │   └── .gitkeep               # GLYPH_ICONS SVGs go here
│   ├── writing/
│   │   └── .gitkeep
│   └── presentations/
│       └── .gitkeep
│
├── QmPYcVJCV8277/
│   ├── formula/
│   │   └── kt_implementation.py   # K(t) full formula
│   ├── patent/
│   │   └── .gitkeep               # patent docs go here
│   ├── theory/
│   │   └── .gitkeep
│   ├── internals/
│   │   └── resolve_field.py       # core inventive step
│   └── README.md                  # access rules
│
├── _shared/
│   ├── fonts/
│   │   └── font_families.html     # uploaded font reference
│   └── styles/
│       └── tokens.css             # design tokens placeholder
│
├── _config/
│   ├── .env.template
│   ├── exports.yaml
│   └── domains.yaml
│
├── _exports/
│   ├── wix/
│   │   └── .gitkeep
│   ├── github_site1/
│   │   └── .gitkeep
│   ├── github_site2/
│   │   └── .gitkeep
│   └── notion/
│       └── .gitkeep
│
├── .gitignore
├── README.md
└── RULES.md
```

---

## SECTION 8 — INITIAL FILE SET

| File | Section | Type | Purpose |
|------|---------|------|---------|
| `.gitignore` | root | config | Blocks QmPYcVJCV8277/, .env, __pycache__, .DS_Store from public exposure |
| `README.md` | root | doc | Private repo purpose, section map, access rules |
| `RULES.md` | root | doc | Implementation rules (Section 10 content) |
| `_config/domains.yaml` | config | config | Four-domain mapping with platform and status |
| `_config/exports.yaml` | config | config | Allowlist of what can be exported to public repos |
| `_config/.env.template` | config | config | API key placeholders (Notion, Wix, GitHub, Fourthwall) |
| `QmPYcVJCV8277/README.md` | protected | doc | Access rules, what belongs here, isolation policy |
| `HEYER_LIVIN_GLYPH_RECORDS/dns/heyerlivin_com.zone` | operations | config | DNS export from CLAUDE.md for reference |
| `HEYER_LIVIN_GLYPH_RECORDS/deploy/DEPLOY_CHECKLIST.md` | operations | doc | Step-by-step for each platform deployment |
| `GLYPH_KITCHEN/engine/requirements.txt` | research | config | Python dependencies for Glyph engine |

---

## SECTION 9 — FIRST BUILD PHASE

### Create now:
- Full folder tree (all directories)
- .gitignore with QmPYcVJCV8277 isolation
- README.md (repo purpose and map)
- RULES.md (implementation rules)
- _config/domains.yaml (four-domain config)
- _config/exports.yaml (export allowlist)
- _config/.env.template (key placeholders)
- QmPYcVJCV8277/README.md (access policy)

### Scaffold now (placeholder files):
- GLYPH_KITCHEN/engine/requirements.txt
- HEYER_LIVIN_GLYPH_RECORDS/deploy/DEPLOY_CHECKLIST.md
- All .gitkeep files for empty directories

### Leave as placeholder:
- All integration scripts (notion_sync.py, cloudflare_worker.js)
- All site content in GLYPHS/sites/ (will be populated from existing files)
- All dataset files in GLYPH_KITCHEN/datasets/
- Patent docs in QmPYcVJCV8277/patent/ (copy from existing when ready)
- Engine code in GLYPH_KITCHEN/engine/ (copy from existing DECK_2 when ready)

### Do not attempt yet:
- Wix site build
- GitHub Pages deployment
- Notion sync implementation
- Public repo creation
- Fourthwall block rebuild (blocks 02 and 03 already exist in workspace history)
- Moving existing files from CIA folder into this structure (separate session)

### First milestone proves:
- The four-section structure holds without overlap
- QmPYcVJCV8277 is genuinely isolated via .gitignore
- Export paths exist and are clearly separated from source paths
- The repo can be initialized as a private GitHub repo
- No protected logic leaks into any exportable directory

---

## SECTION 10 — IMPLEMENTATION RULES

### Naming
- Four master sections use EXACT names: HEYER_LIVIN_GLYPH_RECORDS, GLYPH_KITCHEN, GLYPHS, QmPYcVJCV8277
- No renaming. No abbreviation in folder names.
- Subdirectories use lowercase_snake_case
- Files use lowercase_snake_case with extensions

### Repo boundaries
- `hlvn-private` is PRIVATE. Never make public.
- Public repos (8glyphs27, future sites) are SEPARATE repositories
- Public repos pull from `_exports/` only
- No symlinks or submodules between private and public repos

### Exports
- Only files in `_exports/` may be copied to public repos
- `_config/exports.yaml` is the allowlist — if it's not listed, it doesn't export
- Export is a manual copy or script — never an automatic sync that could leak

### Derived public outputs
- Research results (computed tables, zone classifications) can be exported
- The formula that produced them cannot
- Pattern: QmPYcVJCV8277 → GLYPH_KITCHEN computes → result goes to GLYPHS → export

### Environment files
- `.env` is NEVER committed (in .gitignore)
- `.env.template` shows required keys with empty values
- Real keys stay in local environment only

### Secrets
- No API keys in code
- No tokens in committed files
- No passwords anywhere in the repo

### Protected formulas
- K(t) implementation stays in QmPYcVJCV8277/formula/
- resolveField() stays in QmPYcVJCV8277/internals/
- Band derivation logic stays in QmPYcVJCV8277/internals/
- Hamiltonian eigenvalue construction stays in QmPYcVJCV8277/theory/

### Code comments
- No comments in GLYPH_KITCHEN or GLYPHS code that reference QmPYcVJCV8277 by name
- No comments that describe the formula's parameters
- Comments in QmPYcVJCV8277 are unrestricted (it's protected)

### Documentation
- Public-facing docs go in GLYPHS/
- Internal-only docs go in HEYER_LIVIN_GLYPH_RECORDS/ or GLYPH_KITCHEN/
- Protected docs go in QmPYcVJCV8277/
- RULES.md at root is the enforcement document

---

## SECTION 11 — FINAL RECOMMENDATION

**Build `hlvn-private` as a single private GitHub monorepo with four master section directories, a protected core isolated by .gitignore, and an export staging area that gates all public deployment.**

Initialize it today. Move existing files into it in a follow-up session. Do not touch public sites until this structure holds and QmPYcVJCV8277 isolation is confirmed.

The repo name is `hlvn-private`. The first commit contains the scaffold only. No content migration in the first commit. Content comes in after the structure is verified.
