# viztools

Workspace-wide rules (single checkout, GitHub installs, shared venv, how Claude and
Cursor work together) are in `../AGENTS.md`. This file covers viztools only.

## What it is

Matplotlib axis styling, map layout helpers, and ColorBrewer palettes for notebooks.
h3tools depends on it; jematools does not. It is **notebook-only** code, so the JEMA
sandbox rules don't apply here, and `from __future__ import annotations` is fine.

## Layout

- `viztools/` — the package: `viz.py` (axis styling, layout, linestring helpers),
  `palettes.py` (ColorBrewer), `data/*.json` (palette data), `_messages.py`,
  `_version.py`.
- `tests/` — pytest suite. CI (`.github/workflows/ci.yml`) runs it headless
  (`MPLBACKEND=Agg`) on `ubuntu-24.04` in two jobs, each on Python 3.12 and 3.9:
  `test` against wherewhen `main`, and `test (declared wherewhen floor)` against the
  release tag of the `wherewhen>=` floor in `pyproject.toml` (#11, #13).
- `VIZTOOLS_CONTRACT.md` — the API contract with h3tools. Check it before changing a
  public function's signature or defaults.
- `CHANGELOG.md` — record every user-visible change under `[Unreleased]`.

## Rules

- Keep `requires-python >=3.9` true; the 3.9 CI jobs check it.
- Declare only a released wherewhen version as the floor (`wherewhen>=X.Y.Z` with a
  `wherewhen-vX.Y.Z` tag). The floor job installs that tag and fails if there is none.
  Raise the floor when the code needs something newer, in the same PR.
- `format_plot()` applies its own `facecolor` (default `"white"`), which overwrites any
  earlier `ax.set_facecolor()`. That is known behaviour, not a bug to fix in passing.
- h3-tools CI installs viztools from GitHub `main`. Before merging, run h3-tools' suite
  against your branch: from `../h3-tools`,
  `PYTHONPATH=../viztools ../.venv/bin/python -m pytest -q`.
- Releases follow the checklist in `COMPATIBILITY.md`.

## Testing

`../.venv/bin/python -m pytest -q` from the repo root (about a second).

## Open work

Track to-dos as GitHub issues on outsideken/viztools, claimed with the
`agent:claude` / `agent:cursor` labels.
