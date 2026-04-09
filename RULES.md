# IMPLEMENTATION RULES — hlvn-private

These rules govern all work in this repository. They prevent disorder and protect intellectual property during public deployment.

## Naming

- Four master sections use EXACT names: HEYER_LIVIN_GLYPH_RECORDS, GLYPH_KITCHEN, GLYPHS, QmPYcVJCV8277
- No renaming. No abbreviation in directory names.
- Subdirectories: lowercase_snake_case
- Files: lowercase_snake_case with extensions

## Repo Boundaries

- `hlvn-private` is PRIVATE. Never make public.
- Public repos are SEPARATE repositories.
- Public repos pull from `_exports/` only.
- No symlinks or submodules between private and public repos.

## Exports

- Only files staged in `_exports/` may be copied to public repos.
- `_config/exports.yaml` is the allowlist.
- Export is manual or scripted — never automatic sync.

## Derived Public Outputs

- Computed results (tables, classifications, zone outputs) can be exported.
- The formula that produced them cannot.
- Flow: QmPYcVJCV8277 → GLYPH_KITCHEN computes → result to GLYPHS → export

## Environment and Secrets

- `.env` is NEVER committed.
- `.env.template` shows required keys with empty values.
- No API keys in code. No tokens in committed files. No passwords anywhere.

## Protected Formulas

- K(t) implementation: QmPYcVJCV8277/formula/
- resolveField(): QmPYcVJCV8277/internals/
- Band derivation: QmPYcVJCV8277/internals/
- Hamiltonian construction: QmPYcVJCV8277/theory/
- These files do not move.

## Code Comments

- No comments in GLYPH_KITCHEN or GLYPHS that reference QmPYcVJCV8277 by name.
- No comments describing formula parameters in public-facing code.
- Comments in QmPYcVJCV8277 are unrestricted.

## Documentation

- Public-facing docs: GLYPHS/
- Internal docs: HEYER_LIVIN_GLYPH_RECORDS/ or GLYPH_KITCHEN/
- Protected docs: QmPYcVJCV8277/
- This file (RULES.md) is the enforcement document.

## Git Workflow

- main branch = full private codebase
- Export to public repos via `_exports/` copy, not branch push
- Commit messages: prefix with section name (e.g., `[KITCHEN] add validation script`)
- Never commit to a public repo from inside this repo
