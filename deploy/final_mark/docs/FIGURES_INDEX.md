# FIGURES INDEX — K(t) Patent Filing
## Heyer Livin LLC | 2026-03-29 | Sweep-Verified

### FIGURES THAT EXIST (extractable from current outputs)

| Fig | Description | Source | Status |
|-----|-------------|--------|--------|
| F1 | Glyph-Q Imaginary Time Evolution (tau=0 at 0.500 collapsing to tau→inf at 0.390) | glyph_quantum_spec.py → GlyphQ_TimeEvolution.png | EXISTS — regenerate with seed=42 |
| F2 | Simulation convergence checkpoints (7 games × 5 checkpoints) | glyph_simulations.py checkpoint output | EXTRACTABLE — run simulations, capture checkpoint data |
| F3 | 12-dataset structural constants scatter plot | CLAUDE.md convergence proof table | EXTRACTABLE — plot from verified data |

### FIGURES TO CREATE

| Fig | Description | Content | Priority |
|-----|-------------|---------|----------|
| F4 | System architecture diagram | resolveField() → choose() pipeline, 4 comparison modes as inputs, 3-zone output | MUST CREATE — core patent figure |
| F5 | Three-zone band diagram | Number line [0, 1] with SUBORDINATED [0, 0.30), STRUCTURAL [0.30, 0.50), DOMINANT [0.50, 1.0]. Attractor line at 0.39. | MUST CREATE |
| F6 | 12-dataset convergence scatter | All 12 structural constants plotted, grand mean line at 0.390992, 95% CI band [0.3798, 0.4022] | MUST CREATE |
| F7 | Event record schema diagram | 21-field JSON structure with field groupings | SHOULD CREATE |
| F8 | Dual-coin mechanism flowchart | First coin → field selection → second coin → outcome within field | SHOULD CREATE |
| F9 | K(t) formula diagram | C × (1 − e^(−R × t)) × (1 + ΔS) − ε with labeled components | SHOULD CREATE |
| F10 | Eigenspectrum diagram | 8 eigenvalues [0.39, 0.50, 0.61, 0.72, 0.83, 0.94, 1.05, 1.16] with ground state highlighted | CAN WAIT |

### FIGURE GENERATION TRACEABILITY

- F1: glyph_quantum_spec.py line ~600, seed np.random.default_rng(42), output GlyphQ_TimeEvolution.png
- F2: glyph_simulations.py checkpoint list [1000, 10000, 100000, 500000, 1000000], NO SEED — add random.seed(42) first
- F3: Data from CLAUDE.md STRUCTURAL CLUSTERING table, 12 rows
- F4-F9: No existing code. Create with matplotlib, SVG, or drawing tool.
- F10: glyph_quantum_spec.py build_hamiltonian() eigenvalues, seed=42

### TOTAL: 10 figures mapped. 1 exists. 2 extractable. 7 to create. 4 needed for filing.
