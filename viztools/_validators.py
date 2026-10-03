"""
viztools._validators
====================
Input checks shared by the public functions.  A wrong type raises
``TypeError``; the right type with a bad value raises ``ValueError``.  Every
message is labelled with *func_name*, and :func:`viztools._messages.named_errors`
relabels it to the public function the user called.
"""

from __future__ import annotations

import numbers

import matplotlib.axes as maxes
from shapely.geometry.base import BaseGeometry

from viztools._messages import warn as _warn


def _type_name(value) -> str:
    return type(value).__name__


def require_axes(ax, func_name: str, arg: str = "ax") -> None:
    if not isinstance(ax, maxes.Axes):
        raise TypeError(
            _warn(func_name, f"{arg} must be a matplotlib Axes, got {_type_name(ax)}.")
        )


def require_geometry(geom, func_name: str, arg: str = "geom") -> None:
    if not isinstance(geom, BaseGeometry):
        raise TypeError(
            _warn(func_name, f"{arg} must be a Shapely geometry, got {_type_name(geom)}.")
        )


def require_str(value, func_name: str, arg: str) -> None:
    if not isinstance(value, str):
        raise TypeError(_warn(func_name, f"{arg} must be a str, got {_type_name(value)}."))


def require_real(value, func_name: str, arg: str) -> None:
    """Accept int/float and NumPy scalars; reject bool, str, None, …."""
    if isinstance(value, bool) or not isinstance(value, numbers.Real):
        raise TypeError(_warn(func_name, f"{arg} must be a number, got {_type_name(value)}."))


def require_positive(value, func_name: str, arg: str) -> None:
    require_real(value, func_name, arg)
    if not value > 0:
        raise ValueError(_warn(func_name, f"{arg} must be positive, got {value!r}."))
