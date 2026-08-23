"""
viztools.viz
============
Matplotlib axis styling and map layout helpers.

Ported from ``00 - Python Scripts/Viz Functions.py``.  Axis styling follows the
publication-quality defaults used across JEMA notebooks.

Functions
---------
format_plot
    Apply minimal, clean spine/tick styling to a Matplotlib axis.
set_ax
    Set axis limits to match a target aspect ratio (delegates to wherewhen).
normalize_hex_color
    Convert a CSS3 colour name or hex string to normalised hex.
adjust_bbox_for_aspect
    Expand a geographic bounding box to a target width/height ratio.
set_aspect_ratio
    Adjust axis xlim/ylim to a target aspect ratio.
get_aspect_ratio
    Return width/height of a Shapely geometry bounding box.
resize_to_aspect
    Resize a geometry envelope to an exact target aspect ratio.
to_box
    Return the axis-aligned bounding-box polygon of a geometry.
remove_axis_ticks
    Hide all tick marks and labels on an axis.
plot_linestring
    Draw a Shapely LineString or MultiLineString on a Matplotlib axis.
points_to_linestring
    Build a LineString from an ordered sequence of Shapely Points.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal, Tuple

import matplotlib.axes as maxes
import matplotlib.pyplot as plt
import numpy as np
import webcolors as _webcolors
from shapely import envelope
from shapely.geometry import LineString, MultiLineString, Point, Polygon
from shapely.geometry import box as shapely_box
from shapely.geometry.base import BaseGeometry

from viztools._messages import ok as _ok, warn as _warn
from wherewhen.geometry import get_bounds

__all__ = [
    "DEFAULT_LINESTRING_PLOT_CONFIG",
    "format_plot",
    "set_ax",
    "normalize_hex_color",
    "adjust_bbox_for_aspect",
    "set_aspect_ratio",
    "get_aspect_ratio",
    "resize_to_aspect",
    "to_box",
    "remove_axis_ticks",
    "plot_linestring",
    "points_to_linestring",
]

# Matplotlib ``Axes.plot`` defaults for :func:`plot_linestring`.
DEFAULT_LINESTRING_PLOT_CONFIG: dict[str, object] = {
    "color": "#3182bd",
    "linewidth": 1.0,
    "linestyle": "-",
    "zorder": 0,
}


def _plot_linestring_style(kwargs: dict) -> dict[str, object]:
    """Merge :data:`DEFAULT_LINESTRING_PLOT_CONFIG` with matplotlib ``plot`` *kwargs*."""
    style = DEFAULT_LINESTRING_PLOT_CONFIG.copy()
    style.update(kwargs)
    return style


def _linestring_parts(geometry: LineString | MultiLineString) -> list[LineString]:
    """Return non-empty ``LineString`` parts from *geometry*."""
    if isinstance(geometry, LineString):
        return [geometry] if not geometry.is_empty else []
    return [part for part in geometry.geoms if not part.is_empty]


def points_to_linestring(points: Sequence[Point]) -> LineString:
    """
    Connect an ordered sequence of Shapely Points into one LineString.

    Parameters
    ----------
    points : sequence of shapely.geometry.Point
        Vertices in path order.  At least two points are required.

    Returns
    -------
    shapely.geometry.LineString

    Raises
    ------
    ValueError
        If fewer than two points are supplied.
    """
    if len(points) < 2:
        raise ValueError(
            _warn(
                "points_to_linestring",
                "At least 2 Shapely Points are required to form a LineString.",
            )
        )
    return LineString([(p.x, p.y) for p in points])

TickLocation = Literal["all", "x", "y", "both"]
SpineMode = Literal["none", "bottom", "left", "all", "minimal"]


def format_plot(
    ax: maxes.Axes | None = None,
    *,
    font_size: int | float = 10,
    color: str = "black",
    tick_length: float = 4,
    tick_width: float = 1,
    tick_color: str | None = None,
    label_color: str | None = None,
    spines: SpineMode = "none",
    show_ticks: TickLocation = "all",
    show_labels: TickLocation = "all",
    grid: bool | str = False,
    facecolor: str = "white",
    title_size: int | None = None,
    label_size: int | None = None,
) -> maxes.Axes:
    """
    Clean, minimal, publication-quality axis formatting.

    Parameters
    ----------
    ax : matplotlib.axes.Axes, optional
        Axes to format.  Uses ``plt.gca()`` when ``None``.
    font_size : int or float, optional
        Base font size for tick labels.  Default ``10``.
    color : str, optional
        Main colour for ticks, labels, and spines.  Default ``'black'``.
    spines : {'none', 'bottom', 'left', 'all', 'minimal'}, optional
        Which spines to keep visible.  Default ``'none'``.
    show_ticks, show_labels : {'all', 'x', 'y', 'both'}, optional
        Control tick mark and label visibility independently.
    grid : bool or str, optional
        Add a light grid when truthy.  Default ``False``.
    facecolor : str, optional
        Axes background colour.  Default ``'white'``.

    Returns
    -------
    matplotlib.axes.Axes
        The formatted axes (enables chaining).
    """
    if ax is None:
        ax = plt.gca()

    tick_color = tick_color or color
    label_color = label_color or color

    for axis in ("x", "y"):
        if show_ticks in ("all", "both", axis):
            ax.tick_params(
                axis=axis,
                which="both",
                direction="out",
                length=tick_length,
                width=tick_width,
                color=tick_color,
                pad=4,
            )
        else:
            ax.tick_params(axis=axis, which="both", length=0)

        if show_labels in ("all", "both", axis):
            ax.tick_params(
                axis=axis,
                which="both",
                labelsize=font_size,
                labelcolor=label_color,
            )
        else:
            if axis == "x":
                ax.set_xticklabels([])
            else:
                ax.set_yticklabels([])

    visible_spines = {
        "none":     [],
        "bottom":   ["bottom"],
        "left":     ["left"],
        "all":      ["top", "bottom", "left", "right"],
        "minimal":  ["bottom", "left"],
    }.get(spines, spines if isinstance(spines, list) else [])

    for name, spine in ax.spines.items():
        spine.set_visible(name in visible_spines)
        if name in visible_spines:
            spine.set_color(color)
            spine.set_linewidth(1)

    if grid:
        ax.grid(
            True,
            which="major" if grid is True else grid,
            ls="--",
            lw=0.5,
            color="#888888",
            alpha=0.4,
            zorder=0,
        )

    ax.set_facecolor(facecolor)

    if title_size is not None and ax.get_title():
        ax.title.set_size(title_size)
    if label_size is not None:
        ax.xaxis.label.set_size(label_size)
        ax.yaxis.label.set_size(label_size)

    return ax


def set_ax(
    ax: plt.Axes,
    target_aspect: float,
    fit_mode: Literal["contain", "cover", "fit-width", "fit-height"] = "contain",
    tolerance: float = 1e-8,
) -> Tuple[float, float, float, float]:
    """
    Adjust axis limits to match *target_aspect* using wherewhen bounds logic.

    Reads the current data extent from ``ax.dataLim``, computes new limits,
    and applies them via ``set_xlim`` / ``set_ylim``.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axis whose limits will be adjusted.  Must already contain plotted data.
    target_aspect : float
        Desired width-to-height ratio (must be positive).
    fit_mode : {'contain', 'cover', 'fit-width', 'fit-height'}, optional
        How to reconcile data extent with the target ratio.  Default ``'contain'``.
    tolerance : float, optional
        Minimum dimension treated as non-degenerate.  Default ``1e-8``.

    Returns
    -------
    tuple[float, float, float, float]
        New limits as ``(xmin, ymin, xmax, ymax)``.
    """
    if not isinstance(ax, plt.Axes):
        raise TypeError(
            _warn("set_ax", f"Expected matplotlib.axes.Axes, got {type(ax).__name__}.")
        )
    if not isinstance(target_aspect, (int, float)) or target_aspect <= 0:
        raise ValueError(
            _warn("set_ax", f"target_aspect must be positive, got {target_aspect!r}.")
        )

    dl = ax.dataLim
    if not np.isfinite(dl.x0) or not np.isfinite(dl.x1):
        raise ValueError(
            _warn("set_ax", "Axis has no finite data.  Plot data before calling set_ax().")
        )

    data_box = shapely_box(dl.x0, dl.y0, dl.x1, dl.y1)
    xmin, ymin, xmax, ymax = get_bounds(
        data_box, target_aspect, fit_mode=fit_mode, tolerance=tolerance
    )
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    return xmin, ymin, xmax, ymax


def normalize_hex_color(color: str) -> str:
    """
    Convert a CSS3 colour name or hex string to a normalised lowercase hex code.

    Parameters
    ----------
    color : str
        Web colour name (e.g. ``'red'``) or hex code (e.g. ``'#FF0000'``).

    Returns
    -------
    str
        Normalised hex string (e.g. ``'#ff0000'``).

    Raises
    ------
    ValueError
        If *color* is not a recognised name or valid hex code.
    """
    try:
        if color.startswith("#"):
            _webcolors.hex_to_rgb(color)
            return _webcolors.normalize_hex(color)
        return _webcolors.normalize_hex(_webcolors.name_to_hex(color))
    except (ValueError, AttributeError) as exc:
        raise ValueError(_warn("normalize_hex_color", f"Invalid color: {color}")) from exc


def adjust_bbox_for_aspect(
    lon1: float,
    lon2: float,
    lat1: float,
    lat2: float,
    target_aspect: float,
) -> Tuple[float, float, float, float]:
    """
    Adjust a geographic bounding box to match a target width/height ratio.

    Preserves the centre point and expands the larger dimension as needed.
    """
    current_lon_span = lon2 - lon1
    current_lat_span = lat2 - lat1
    current_aspect = current_lon_span / current_lat_span
    center_lon = (lon1 + lon2) / 2
    center_lat = (lat1 + lat2) / 2

    if current_aspect > target_aspect:
        new_lat_span = current_lon_span / target_aspect
        half_lat = new_lat_span / 2
        return lon1, lon2, center_lat - half_lat, center_lat + half_lat

    new_lon_span = current_lat_span * target_aspect
    half_lon = new_lon_span / 2
    return center_lon - half_lon, center_lon + half_lon, lat1, lat2


def set_aspect_ratio(ax: plt.Axes, target_aspect: float = 16 / 9) -> None:
    """Adjust *ax* xlim/ylim to *target_aspect* after plotting."""
    lon1, lon2 = ax.get_xlim()
    lat1, lat2 = ax.get_ylim()
    lon1, lon2, lat1, lat2 = adjust_bbox_for_aspect(
        lon1, lon2, lat1, lat2, target_aspect
    )
    ax.set_xlim(lon1, lon2)
    ax.set_ylim(lat1, lat2)


def get_aspect_ratio(geom: BaseGeometry) -> float:
    """Return width/height of *geom*'s bounding box."""
    if geom.is_empty:
        raise ValueError(_warn("get_aspect_ratio", "Cannot compute aspect ratio of empty geometry."))
    minx, miny, maxx, maxy = geom.bounds
    width = maxx - minx
    height = maxy - miny
    if height == 0:
        raise ValueError(_warn("get_aspect_ratio", "Geometry has zero height."))
    if width == 0:
        raise ValueError(_warn("get_aspect_ratio", "Geometry has zero width."))
    return width / height


def resize_to_aspect(
    geom: BaseGeometry,
    target_aspect: float,
    preserve_area: bool = True,
) -> Polygon:
    """Return an axis-aligned rectangle centred on *geom* with *target_aspect*."""
    if geom.is_empty:
        return Polygon()

    bbox = envelope(geom)
    minx, miny, maxx, maxy = bbox.bounds
    cx = (minx + maxx) / 2
    cy = (miny + maxy) / 2
    current_width = maxx - minx
    current_height = maxy - miny
    current_aspect = current_width / current_height if current_height else 0

    if preserve_area:
        area = bbox.area
        height = (area / target_aspect) ** 0.5
        width = height * target_aspect
    elif current_aspect > target_aspect:
        width = current_width
        height = current_width / target_aspect
    else:
        height = current_height
        width = current_height * target_aspect

    half_w, half_h = width / 2, height / 2
    return shapely_box(cx - half_w, cy - half_h, cx + half_w, cy + half_h)


def to_box(geom: BaseGeometry) -> Polygon:
    """Return the axis-aligned bounding-box polygon of *geom*."""
    return envelope(geom)


def remove_axis_ticks(ax: plt.Axes) -> None:
    """Hide all tick marks and labels on *ax*."""
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.set_yticks([])
    ax.set_yticklabels([])


def plot_linestring(
    ax: plt.Axes,
    linestring: LineString | MultiLineString,
    verbose: bool = True,
    **kwargs,
) -> None:
    """
    Draw a Shapely LineString or MultiLineString on *ax*.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The target axis on which to draw.
    linestring : shapely.geometry.LineString or shapely.geometry.MultiLineString
        Line geometry to plot.  Must contain at least one non-empty part.
    verbose : bool, optional
        When ``True`` (default), print a one-line status message on success.
    **kwargs
        Matplotlib ``Axes.plot`` keywords (``color``, ``linewidth``,
        ``linestyle``, ``zorder``, ``label``, …).  Override
        :data:`DEFAULT_LINESTRING_PLOT_CONFIG` defaults.
        ``label`` is applied to the first part only.

    Returns
    -------
    None
        Modifies *ax* in place.

    Raises
    ------
    ValueError
        If *linestring* is not a non-empty LineString or MultiLineString.

    See Also
    --------
    points_to_linestring : Build a LineString from Shapely Points.
    DEFAULT_LINESTRING_PLOT_CONFIG : Default ``Axes.plot`` keyword dictionary.
    h3tools.plot_hex : Draw H3 cell boundaries as filled polygons instead.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from shapely.geometry import LineString
    >>> fig, ax = plt.subplots()
    >>> plot_linestring(ax, LineString([(0, 0), (1, 1)]), color="gray", linestyle="--")
    >>> plt.close()
    """
    if not isinstance(linestring, (LineString, MultiLineString)):
        raise ValueError(
            _warn(
                "plot_linestring",
                "linestring must be a non-empty LineString or MultiLineString.",
            )
        )

    parts = _linestring_parts(linestring)
    if not parts:
        raise ValueError(
            _warn(
                "plot_linestring",
                "linestring must be a non-empty LineString or MultiLineString.",
            )
        )

    base_style = _plot_linestring_style(kwargs)
    for i, part in enumerate(parts):
        line_kw = base_style.copy()
        if i > 0:
            line_kw["label"] = "_nolegend_"
        x, y = part.xy
        ax.plot(x, y, **line_kw)

    if verbose:
        n = len(parts)
        print(
            _ok(
                "plot_linestring",
                f"{n} line{'s' if n != 1 else ''} added to plot",
            )
        )