# viztools compatibility

`viztools` versions **independently** of jematools, wherewhen, h3tools, and
tabtools.  Dependents declare a minimum floor (e.g. `viztools>=0.1.0`).

## This package

| Item | Value |
|---|---|
| **Current version** | `0.1.3` |
| **Requires** | `wherewhen>=0.2.0` |
| **Python** | `>=3.9` |

## Downstream floors (typical)

| Consumer | Declares |
|---|---|
| h3tools **0.8.0b1** | `viztools>=0.1.3` (raised from `>=0.1.0` for linestring helpers) |
| tabtools / notebooks | import viztools directly for palettes and `format_plot` |

Current freeze stack: wherewhen **0.2.6** + viztools **0.1.3** + h3tools **0.8.0b1**.

Behaviour expectations for consumers: [VIZTOOLS_CONTRACT.md](VIZTOOLS_CONTRACT.md).

A fuller dated multi-package test matrix may live in a sibling toolkit
workspace.  This file is enough for a GitHub-only clone of `viztools`.

## Release checklist

1. Bump `viztools/_version.py`
2. Bump matching `version` in `pyproject.toml`
3. Add an entry to `CHANGELOG.md`
4. Sync README version / test-count badges
5. Update `VIZTOOLS_CONTRACT.md` if the public contract changes
6. Git tag: `viztools-vX.Y.Z`
7. Bump dependent floors only when those packages start calling new APIs — then
   re-test the stack
