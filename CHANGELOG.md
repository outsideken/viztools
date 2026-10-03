# Changelog

All notable changes to viztools will be documented here.

This package versions **independently** of jematools, wherewhen, h3tools, and
tabtools.

---

## [Unreleased]

---

## [0.1.4] — 2026-10-03

### Fixed
- ``format_plot(spines=[...])`` crashed with ``unhashable type: 'list'`` (#4).
  A list or tuple of spine names now works as documented; a name the axis
  doesn't have raises ``ValueError``. Preset strings are unchanged.

### Changed
- **Errors name the function you called** (#2), matching jematools, h3tools and
  wherewhen. Every public function is wrapped by ``named_errors``, so an error
  raised in a helper, another viztools function or wherewhen is relabelled
  ``⚠️ [<function you called>]``. Example: ``get_cmap`` used to report
  ``[get_palette]``, and ``set_ax`` reported wherewhen's ``[get_bounds]``.
- **Wrong input types raise a labelled ``TypeError``** instead of a raw
  ``AttributeError``/``TypeError`` from inside matplotlib or Shapely, e.g.
  ``format_plot("bad")``, ``get_palette(None)``, ``get_aspect_ratio(None)``.
  A right type with a bad value raises ``ValueError``.
- Exception classes that changed on bad input (successful calls are unchanged):
  - ``plot_linestring`` with a non-line geometry: ``ValueError`` → ``TypeError``
  - ``get_palette`` / ``get_cmap`` with a non-int ``n``: ``ValueError`` → ``TypeError``
  - ``set_ax`` with a non-number ``target_aspect``: ``ValueError`` → ``TypeError``
  - ``normalize_hex_color`` with a non-str: ``ValueError`` → ``TypeError``
  - ``adjust_bbox_for_aspect`` with zero height or ``target_aspect=0``:
    ``ZeroDivisionError`` → ``ValueError``; a negative ``target_aspect`` returned
    an upside-down box and is now a ``ValueError``
  - ``set_aspect_ratio`` with ``target_aspect=0``: matplotlib's unlabelled
    ``ValueError`` → labelled ``ValueError``
  - ``resize_to_aspect`` with a non-positive ``target_aspect``: raw ``TypeError``
    → ``ValueError``
  - ``list_palettes`` with ``n < 1``: returned a list, now ``ValueError``
  - ``points_to_linestring`` with non-Point items: ``AttributeError`` → ``TypeError``
- ``get_palette`` / ``get_cmap`` accept NumPy integers for ``n`` (they were
  rejected with ``ValueError``); ``n=True`` is now a ``TypeError`` (it returned
  one colour before).
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