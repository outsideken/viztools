"""
viztools
========
Matplotlib axis styling, map layout helpers, and ColorBrewer palettes.

Bottom-layer visualization package for the JEMA toolkit.  Import directly::

    from viztools.viz import format_plot
    from viztools.palettes import get_palette, get_cmap

Consumed by ``h3tools`` (axis styling in notebooks) and future ``tabtools``
(anomaly palettes).  Depends on ``wherewhen>=0.2.0`` for bounds helpers and
notification style.

On first import prints ``ℹ️ [viztools] v<version> loaded.``
"""

from viztools._version import __version__

from viztools.palettes import ANOMALY_PALETTE, get_cmap, get_palette, list_palettes
from viztools.viz import (
    DEFAULT_LINESTRING_PLOT_CONFIG,
    adjust_bbox_for_aspect,
    format_plot,
    get_aspect_ratio,
    normalize_hex_color,
    plot_linestring,
    points_to_linestring,
    remove_axis_ticks,
    resize_to_aspect,
    set_aspect_ratio,
    set_ax,
    to_box,
)

__all__ = [
    # palettes
    "ANOMALY_PALETTE",
    "get_palette",
    "get_cmap",
    "list_palettes",
    # viz
    "DEFAULT_LINESTRING_PLOT_CONFIG",
    "format_plot",
    "plot_linestring",
    "points_to_linestring",
    "set_ax",
    "normalize_hex_color",
    "adjust_bbox_for_aspect",
    "set_aspect_ratio",
    "get_aspect_ratio",
    "resize_to_aspect",
    "to_box",
    "remove_axis_ticks",
    "list_functions",
]


def list_functions(query: str = "") -> None:
    """Print a catalogue of public viztools functions grouped by module."""
    import inspect
    from viztools import palettes, viz

    sections = [
        ("palettes", palettes),
        ("viz",      viz),
    ]
    q = query.strip().lower()

    for section_name, module in sections:
        names = getattr(module, "__all__", [])
        funcs = [
            (name, getattr(module, name))
            for name in names
            if name != "ANOMALY_PALETTE"
            and inspect.isfunction(getattr(module, name, None))
        ]
        if q:
            funcs = [
                (n, o) for n, o in funcs
                if q in n.lower() or q in (inspect.getdoc(o) or "").split("\n")[0].lower()
            ]
        if not funcs:
            continue
        print(f"\n{'─' * 60}")
        print(f"  {section_name}")
        print(f"{'─' * 60}")
        for name, obj in funcs:
            doc = inspect.getdoc(obj) or ""
            summary = doc.split("\n")[0]
            print(f"  {name:<35} {summary}")


from viztools._messages import loaded as _loaded

_loaded("viztools", __version__)