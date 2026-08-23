# Changelog

All notable changes to viztools will be documented here.

This package versions **independently** of jematools, wherewhen, h3tools, and
tabtools.

---

## [Unreleased]

### Changed
- README — portable ``YOUR_LOCAL_PATH`` install; full ``viz`` helper catalogue;
  added **What this is not**, maturity note, and repo-local
  [COMPATIBILITY.md](COMPATIBILITY.md)
- Shipped [VIZTOOLS_CONTRACT.md](VIZTOOLS_CONTRACT.md) inside the package repo
  so GitHub clones no longer depend on a sibling workspace path

---

## [0.1.3] — 2026-06-25

### Added
- ``points_to_linestring`` — build a ``LineString`` from an ordered sequence of
  Shapely ``Point`` objects

### Changed
- ``plot_linestring`` — accepts ``MultiLineString``; plots each part; plural
  verbose message; ``label`` on first part only

---

## [0.1.2] — 2026-06-25

### Added
- ``plot_linestring`` — draw a Shapely ``LineString`` on a Matplotlib axis
- ``DEFAULT_LINESTRING_PLOT_CONFIG`` — module constant and top-level export

---

## [0.1.1] — 2026-06-17

### Changed
- README — test-count badge added (18 passing)

---

## [0.1.0] — 2026-06-08

### Added
- `viztools.viz.format_plot` — publication-quality axis styling (from Viz Functions.py)
- `viztools.viz.set_ax` — aspect-ratio axis limits via `wherewhen.geometry.get_bounds`
- Map layout helpers: `adjust_bbox_for_aspect`, `set_aspect_ratio`, `get_aspect_ratio`,
  `resize_to_aspect`, `to_box`, `remove_axis_ticks`
- `viztools.viz.normalize_hex_color` — CSS3 name / hex normalisation
- `viztools.palettes` — ColorBrewer2 JSON loader with `get_palette`, `get_cmap`,
  `list_palettes`, and `ANOMALY_PALETTE` (RdBu 9-class diverging)
- Bundled data: `colorbrewer2_ranges.json`, `colorbrewer2_789.json`
- Import-time load notice via `wherewhen._messages.loaded()`
- Tests covering contract requirements and palette loading

### Dependencies
- `matplotlib`, `numpy`, `webcolors`, `wherewhen>=0.2.0`