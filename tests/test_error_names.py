"""
Every public function's errors name that function (#2).

An error should tell the user where it happened: the function they called,
not a helper, another viztools function, or wherewhen underneath.  A wrong
type raises TypeError; the right type with a bad value raises ValueError.
Mirrors ``tests/test_error_names.py`` in h3tools, jematools and wherewhen.
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402
from shapely.geometry import LineString, Point, Polygon, box  # noqa: E402

import viztools  # noqa: E402


@pytest.fixture(autouse=True)
def _close_figures():
    yield
    plt.close("all")


def _ax():
    return plt.subplots()[1]


def _ax_with_data():
    ax = _ax()
    ax.plot([0, 2], [0, 1])
    return ax


# Wrong type for the first argument: function name -> (call, exception class)
BAD_CALLS = {
    "get_palette": (lambda: viztools.get_palette(None), TypeError),
    "get_cmap": (lambda: viztools.get_cmap(None), TypeError),
    "list_palettes": (lambda: viztools.list_palettes(None, print_catalogue=False), TypeError),
    "format_plot": (lambda: viztools.format_plot("bad"), TypeError),
    "plot_linestring": (lambda: viztools.plot_linestring(None, LineString([(0, 0), (1, 1)])), TypeError),
    "points_to_linestring": (lambda: viztools.points_to_linestring(None), TypeError),
    "set_ax": (lambda: viztools.set_ax(None, 1.0), TypeError),
    "normalize_hex_color": (lambda: viztools.normalize_hex_color(None), TypeError),
    "adjust_bbox_for_aspect": (lambda: viztools.adjust_bbox_for_aspect("0", 1, 0, 1, 1.0), TypeError),
    "set_aspect_ratio": (lambda: viztools.set_aspect_ratio(None), TypeError),
    "get_aspect_ratio": (lambda: viztools.get_aspect_ratio(None), TypeError),
    "resize_to_aspect": (lambda: viztools.resize_to_aspect(None, 1.0), TypeError),
    "to_box": (lambda: viztools.to_box("bad"), TypeError),
    "remove_axis_ticks": (lambda: viztools.remove_axis_ticks(None), TypeError),
    "list_functions": (lambda: viztools.list_functions(None), TypeError),
}


def _public_functions():
    return {
        n for n in viztools.__all__
        if callable(getattr(viztools, n)) and not isinstance(getattr(viztools, n), type)
    }


def test_every_public_function_is_covered():
    assert set(BAD_CALLS) == _public_functions()


def test_every_public_function_carries_named_errors():
    # The decorator is what guarantees the outermost function's name, so a new
    # public function without it fails here.
    missing = sorted(n for n in _public_functions() if not hasattr(getattr(viztools, n), "__wrapped__"))
    assert missing == []


@pytest.mark.parametrize("name", sorted(BAD_CALLS))
def test_wrong_type_names_the_function_called(name):
    call, exc_class = BAD_CALLS[name]
    with pytest.raises(Exception) as excinfo:
        call()
    assert type(excinfo.value) is exc_class, f"{name}: {type(excinfo.value).__name__}: {excinfo.value}"
    assert str(excinfo.value).startswith(f"⚠️ [{name}] "), str(excinfo.value)


# Bad values, later arguments, and hand-offs to another viztools function or
# to wherewhen: (function name, call, exception class)
MORE_BAD_CALLS = [
    ("get_palette", lambda: viztools.get_palette("YlOrRd", n=0), ValueError),
    ("get_palette", lambda: viztools.get_palette("YlOrRd", n=2.5), TypeError),
    ("get_palette", lambda: viztools.get_palette("YlOrRd", n=True), TypeError),
    ("get_palette", lambda: viztools.get_palette("YlOrRd", kind=3), TypeError),
    ("get_palette", lambda: viztools.get_palette("YlOrRd", kind="bogus"), ValueError),
    ("get_palette", lambda: viztools.get_palette("NoSuchPalette"), ValueError),
    ("get_cmap", lambda: viztools.get_cmap("YlOrRd", n=0), ValueError),
    ("get_cmap", lambda: viztools.get_cmap("YlOrRd", kind="bogus"), ValueError),
    ("get_cmap", lambda: viztools.get_cmap("NoSuchPalette"), ValueError),
    ("list_palettes", lambda: viztools.list_palettes("bogus", print_catalogue=False), ValueError),
    ("list_palettes", lambda: viztools.list_palettes(n=0, print_catalogue=False), ValueError),
    ("list_palettes", lambda: viztools.list_palettes(n="9", print_catalogue=False), TypeError),
    ("plot_linestring", lambda: viztools.plot_linestring(_ax(), box(0, 0, 1, 1)), TypeError),
    ("plot_linestring", lambda: viztools.plot_linestring(_ax(), LineString()), ValueError),
    ("points_to_linestring", lambda: viztools.points_to_linestring([Point(0, 0)]), ValueError),
    ("points_to_linestring", lambda: viztools.points_to_linestring([(0, 0), (1, 1)]), TypeError),
    ("points_to_linestring", lambda: viztools.points_to_linestring("ab"), TypeError),
    ("set_ax", lambda: viztools.set_ax(_ax_with_data(), "wide"), TypeError),
    ("set_ax", lambda: viztools.set_ax(_ax_with_data(), -1.0), ValueError),
    ("set_ax", lambda: viztools.set_ax(_ax(), 1.0), ValueError),
    ("set_ax", lambda: viztools.set_ax(_ax_with_data(), 1.0, fit_mode="bogus"), ValueError),
    ("normalize_hex_color", lambda: viztools.normalize_hex_color("notacolor"), ValueError),
    ("adjust_bbox_for_aspect", lambda: viztools.adjust_bbox_for_aspect(0, 1, 0, 1, 0), ValueError),
    ("adjust_bbox_for_aspect", lambda: viztools.adjust_bbox_for_aspect(0, 1, 5, 5, 1.0), ValueError),
    ("set_aspect_ratio", lambda: viztools.set_aspect_ratio(_ax(), 0), ValueError),
    ("set_aspect_ratio", lambda: viztools.set_aspect_ratio(_ax(), "16:9"), TypeError),
    ("get_aspect_ratio", lambda: viztools.get_aspect_ratio(Polygon()), ValueError),
    ("get_aspect_ratio", lambda: viztools.get_aspect_ratio(LineString([(0, 0), (1, 0)])), ValueError),
    ("resize_to_aspect", lambda: viztools.resize_to_aspect(box(0, 0, 1, 1), -1.0), ValueError),
    ("resize_to_aspect", lambda: viztools.resize_to_aspect(box(0, 0, 1, 1), None), TypeError),
]


@pytest.mark.parametrize(
    "name, call, exc_class", MORE_BAD_CALLS,
    ids=[f"{n}-{i}" for i, (n, _, _) in enumerate(MORE_BAD_CALLS)],
)
def test_bad_values_and_delegated_errors_name_the_function_called(name, call, exc_class):
    with pytest.raises(Exception) as excinfo:
        call()
    assert type(excinfo.value) is exc_class, f"{name}: {type(excinfo.value).__name__}: {excinfo.value}"
    assert str(excinfo.value).startswith(f"⚠️ [{name}] "), str(excinfo.value)


def test_numpy_numbers_are_accepted():
    # ax.get_xlim() and pandas hand back NumPy scalars; they must keep working.
    assert len(viztools.get_palette("YlOrRd", n=np.int64(7))) == 7
    assert viztools.adjust_bbox_for_aspect(np.float64(0), 2.0, 0.0, 1.0, np.float32(1.0))
    ax = _ax_with_data()
    viztools.set_ax(ax, np.float64(1.5))


def test_relabelling_keeps_the_exception_class_and_object():
    from viztools._messages import named_errors, warn

    errors = [ValueError(warn("inner", "v")), TypeError(warn("inner", "t")),
              ImportError("❌ [inner] needs a package"), KeyError(warn("inner", "k"))]
    for original in errors:
        @named_errors
        def outer():
            raise original

        with pytest.raises(type(original)) as excinfo:
            outer()
        assert excinfo.value is original
        assert "[outer]" in str(excinfo.value) and "[inner]" not in str(excinfo.value)


def test_unlabelled_errors_pass_through_unchanged():
    from viztools._messages import named_errors

    @named_errors
    def outer():
        raise ZeroDivisionError("division by zero")

    with pytest.raises(ZeroDivisionError, match=r"^division by zero$"):
        outer()
