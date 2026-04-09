# Private Boundary Notes

This repository runs in private-only mode, but boundaries are still documented for safe downstream export design.

## Protected Boundary

- `QmPYcVJCV8277` is treated as protected-core conceptual boundary.
- Any future public-safe export must not leak protected internals, hidden parameters, or direct formula implementation details.

## Public Contract Rule

- Public surfaces should expose derived outputs, schema-safe summaries, and sanitized analytics only.
- Internal mechanics remain on `MySide`; published interfaces remain on `PublicSide`.
