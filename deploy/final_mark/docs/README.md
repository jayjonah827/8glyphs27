# QmPYcVJCV8277 — Protected Core

This directory contains patent-sensitive, proprietary, and unreleased intellectual property.

## Access Rules

1. Nothing in this directory exports to public repos. Ever.
2. Nothing in this directory is referenced by name in public-facing code or comments.
3. GLYPH_KITCHEN/engine/ may import from this directory ONLY within the private repo.
4. Computed outputs (results, not formulas) flow: this directory → GLYPH_KITCHEN → GLYPHS.
5. Patent drafts stay here until filed with USPTO.
6. If this repo is ever forked publicly, this entire directory must be excluded.

## Contents

- formula/ — K(t) constraint detection formula implementation
- patent/ — provisional patent application drafts, inventor's disclosure
- theory/ — unreleased theoretical extensions (Glyph-Q Hamiltonian, epsilon quantum)
- internals/ — resolveField(), band derivation logic, core inventive steps

## What Goes Here

- Any code implementing the K(t) formula with full parameters
- resolveField() and field-resolution-before-choice logic
- Band boundary derivation (when built)
- Per-domain C, R, delta-S, epsilon values
- Hamiltonian eigenvalue construction
- Epsilon quantum derivation and proof
- Structural entanglement formal proofs
- Patent application documents
- Legal-sensitive research materials
- Private conceptual architecture

## What Does Not Go Here

- Public-facing content or assets
- Business operations or SOPs
- General research that can be published
- Portfolio works or showcase items
- Computed results (those go to GLYPH_KITCHEN or GLYPHS after computation)
