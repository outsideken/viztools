"""
viztools._messages
==================
Shared notification helpers — re-exported from wherewhen — and the
:func:`named_errors` decorator that makes every public function's errors name
that function (#2).  Same mechanism as ``h3tools._messages.named_errors`` and
``jematools._errors.named_errors``.
"""

from __future__ import annotations

import functools
import re

from wherewhen._messages import info, loaded, note, ok, skip, warn

__all__ = ["warn", "info", "skip", "note", "ok", "loaded", "named_errors"]

# "⚠️ [label] text" / "❌ [label] text": the toolkit's message prefix.
_LABEL = re.compile(r"^(\S+ )\[[A-Za-z_][A-Za-z0-9_]*\]")


def _relabel(exc: BaseException, func_name: str) -> None:
    """Point a toolkit error's ``[label]`` at *func_name*, in place."""
    if not (exc.args and isinstance(exc.args[0], str)):
        return
    original = exc.args[0]
    relabelled = _LABEL.sub(lambda m: f"{m.group(1)}[{func_name}]", original, count=1)
    if relabelled == original:
        return
    exc.args = (relabelled,) + exc.args[1:]
    # ImportError (and subclasses) print .msg, not args.
    if getattr(exc, "msg", None) == original:
        exc.msg = relabelled


def named_errors(func):
    """
    Decorate a public function so its toolkit errors name it.

    A labelled error (``⚠️ [x] …`` / ``❌ [x] …``) escaping *func*, from its own
    checks, a helper, another public function or wherewhen, is relabelled
    ``[func.__name__]`` and the same exception object is re-raised (class,
    traceback and the rest of the message unchanged).  Nested public calls
    relabel on the way out, so the error names the outermost function, which
    is the one the user called.  Unlabelled errors pass through untouched.
    """
    name = func.__name__

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            _relabel(exc, name)
            raise

    return wrapper
