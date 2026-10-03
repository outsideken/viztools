"""
viztools.palettes
=================
ColorBrewer2 palette loading and Matplotlib colormap helpers.

Bundled JSON sources:

* ``colorbrewer2_ranges.json`` — full 3–11 class palettes (sequential,
  diverging, qualitative)
* ``colorbrewer2_789.json`` — curated 7/8/9-class palettes from the
  ``00 - Colors`` notebook

Functions
---------
get_palette
    Return *n* hex colours for a named ColorBrewer scheme.
get_cmap
    Return a Matplotlib ``ListedColormap`` for choropleth/heatmap use.
list_palettes
    Print or return available palette names for a given type and class count.
"""

from __future__ import annotations

import json
import numbers
from functools import lru_cache
from pathlib import Path
from typing import Literal

import matplotlib.colors as mcolors
import numpy as np

from viztools._messages import named_errors as _named_errors, warn as _warn
from viztools._validators import require_str as _require_str

__all__ = [
    "ANOMALY_PALETTE",
    "get_palette",
    "get_cmap",
    "list_palettes",
]

PaletteKind = Literal["sequential", "diverging", "qualitative"]

_KIND_ALIASES = {
    "seq": "sequential",
    "sequential": "sequential",
    "div": "diverging",
    "diverging": "diverging",
    "qual": "qualitative",
    "qualitative": "qualitative",
}

_NAME_ALIASES = {
    "grays": "Grays",
    "greys": "Greys",
}

_SPELLING_VARIANTS = {
    "Grays": ("Grays", "Greys"),
    "Greys": ("Greys", "Grays"),
}

_RANGES_KIND_MAP = {
    "sequential": "Sequential",
    "diverging": "Diverging",
    "qualitative": "Qualitative",
}

_DATA_DIR = Path(__file__).resolve().parent / "data"


@lru_cache(maxsize=1)
def _load_ranges() -> dict:
    text = (_DATA_DIR / "colorbrewer2_ranges.json").read_text(encoding="utf-8")
    return json.loads(text)


@lru_cache(maxsize=1)
def _load_789() -> dict:
    text = (_DATA_DIR / "colorbrewer2_789.json").read_text(encoding="utf-8")
    return json.loads(text)


def _check_class_count(n, func_name: str, *, allow_none: bool = False) -> None:
    """n is an int (NumPy ints too, not bool) of at least 1, or None when allowed."""
    if n is None and allow_none:
        return
    if isinstance(n, bool) or not isinstance(n, numbers.Integral):
        raise TypeError(_warn(func_name, f"n must be an int, got {type(n).__name__}."))
    if n < 1:
        raise ValueError(_warn(func_name, f"n must be a positive integer, got {n!r}."))


def _normalize_kind(kind: str) -> str:
    _require_str(kind, "get_palette", "kind")
    key = kind.strip().lower()
    if key not in _KIND_ALIASES:
        raise ValueError(
            _warn(
                "get_palette",
                f"kind must be 'sequential', 'diverging', or 'qualitative', got {kind!r}.",
            )
        )
    return _KIND_ALIASES[key]


def _normalize_name(name: str) -> str:
    stripped = name.strip()
    return _NAME_ALIASES.get(stripped.lower(), stripped)


def _interpolate_colors(colors: list[str], n: int) -> list[str]:
    if n <= 0:
        raise ValueError(_warn("get_palette", "n must be a positive integer."))
    if n == 1:
        return [colors[0]]
    if n == len(colors):
        return list(colors)
    rgb = np.array([mcolors.to_rgb(c) for c in colors], dtype=float)
    positions = np.linspace(0, len(rgb) - 1, n)
    lower = np.floor(positions).astype(int)
    upper = np.ceil(positions).astype(int)
    weight = positions - lower
    blended = rgb[lower] * (1 - weight[:, None]) + rgb[upper] * weight[:, None]
    return [mcolors.to_hex(tuple(c)) for c in blended]


def _lookup_789(kind: str, name: str, n: int) -> list[str] | None:
    data = _load_789()
    bucket = data.get(kind, {})
    class_bucket = bucket.get(str(n), bucket.get(n))
    if not class_bucket:
        return None
    return class_bucket.get(name)


def _lookup_ranges(kind: str, name: str, n: int) -> list[str] | None:
    data = _load_ranges()
    section = data.get(_RANGES_KIND_MAP[kind], {})
    colors = section.get(name)
    if not colors:
        return None
    if n == len(colors):
        return list(colors)
    if n < len(colors):
        return _interpolate_colors(colors, n)
    return None


@_named_errors
def get_palette(
    name: str,
    n: int = 9,
    kind: PaletteKind = "sequential",
) -> list[str]:
    """
    Return *n* hex colours for a named ColorBrewer2 scheme.

    Parameters
    ----------
    name : str
        Palette name (e.g. ``"YlOrRd"``, ``"RdBu"``, ``"Set1"``).
    n : int, optional
        Number of colour classes.  Default ``9``.  Exact 7/8/9-class palettes
        are served from the curated JSON; other counts are interpolated from
        the full-range palettes when possible.
    kind : {'sequential', 'diverging', 'qualitative'}, optional
        Palette family.  Default ``'sequential'``.

    Returns
    -------
    list[str]
        Hex colour strings (e.g. ``'#fc8d59'``).

    Raises
    ------
    TypeError
        If *name* or *kind* is not a str, or *n* is not an int.
    ValueError
        If *n* is below 1, *kind* is unknown, or the palette is not found.
    """
    _require_str(name, "get_palette", "name")
    _check_class_count(n, "get_palette")

    palette_kind = _normalize_kind(kind)
    palette_name = _normalize_name(name)
    candidates = _SPELLING_VARIANTS.get(palette_name, (palette_name,))

    for candidate in candidates:
        if n in (7, 8, 9):
            hit = _lookup_789(palette_kind, candidate, n)
            if hit:
                return list(hit)

        hit = _lookup_ranges(palette_kind, candidate, n)
        if hit:
            return hit

    raise ValueError(
        _warn(
            "get_palette",
            f"Palette {palette_name!r} ({palette_kind}, n={n}) not found. "
            f"Use list_palettes(kind={palette_kind!r}, n={n}) to browse.",
        )
    )


@_named_errors
def get_cmap(
    name: str,
    n: int = 9,
    kind: PaletteKind = "sequential",
) -> mcolors.ListedColormap:
    """
    Return a Matplotlib ``ListedColormap`` built from a ColorBrewer palette.

    Parameters
    ----------
    name : str
        Palette name (e.g. ``"YlOrRd"``).
    n : int, optional
        Number of colour classes.  Default ``9``.
    kind : {'sequential', 'diverging', 'qualitative'}, optional
        Palette family.  Default ``'sequential'``.

    Returns
    -------
    matplotlib.colors.ListedColormap
        Colormap ready for choropleth or heatmap plotting.
    """
    colors = get_palette(name, n=n, kind=kind)
    return mcolors.ListedColormap(colors, name=f"{name}_{n}")


@_named_errors
def list_palettes(
    kind: PaletteKind = "sequential",
    n: int | None = 9,
    *,
    print_catalogue: bool = True,
) -> list[str]:
    """
    List available ColorBrewer palette names.

    Parameters
    ----------
    kind : {'sequential', 'diverging', 'qualitative'}, optional
        Palette family to list.  Default ``'sequential'``.
    n : int, optional
        When provided, restrict to palettes available at that class count.
        Default ``9``.  Pass ``None`` to list all names in the full-range JSON.
    print_catalogue : bool, optional
        When ``True`` (default), print a formatted catalogue to stdout.

    Returns
    -------
    list[str]
        Sorted palette names.
    """
    _check_class_count(n, "list_palettes", allow_none=True)
    palette_kind = _normalize_kind(kind)
    names: set[str] = set()

    if n in (7, 8, 9):
        bucket = _load_789().get(palette_kind, {}).get(str(n), {})
        names.update(bucket.keys())

    section = _load_ranges().get(_RANGES_KIND_MAP[palette_kind], {})
    for palette_name, colors in section.items():
        if n is None or n <= len(colors):
            names.add(palette_name)

    result = sorted(names)
    if print_catalogue:
        label = f"{palette_kind}" + (f", n={n}" if n is not None else "")
        print(f"\n{'─' * 40}")
        print(f"  ColorBrewer — {label}")
        print(f"{'─' * 40}")
        for palette_name in result:
            print(f"  {palette_name}")
    return result


ANOMALY_PALETTE: list[str] = get_palette("RdBu", n=9, kind="diverging")