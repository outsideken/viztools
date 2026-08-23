"""Tests for viztools.viz — contract from VIZTOOLS_CONTRACT.md."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pytest
from shapely.geometry import LineString, MultiLineString, Point, box

from viztools.viz import (
    DEFAULT_LINESTRING_PLOT_CONFIG,
    adjust_bbox_for_aspect,
    format_plot,
    get_aspect_ratio,
    normalize_hex_color,
    plot_linestring,
    points_to_linestring,
    set_ax,
)


class TestFormatPlot:
    def test_returns_same_axes(self):
        fig, ax = plt.subplots()
        result = format_plot(ax)
        assert result is ax
        plt.close(fig)

    def test_none_uses_gca(self):
        fig, ax = plt.subplots()
        plt.sca(ax)
        result = format_plot(None)
        assert result is ax
        plt.close(fig)

    def test_default_hides_all_spines(self):
        fig, ax = plt.subplots()
        format_plot(ax)
        assert all(not spine.get_visible() for spine in ax.spines.values())
        plt.close(fig)

    def test_minimal_shows_bottom_and_left(self):
        fig, ax = plt.subplots()
        format_plot(ax, spines="minimal")
        assert ax.spines["bottom"].get_visible()
        assert ax.spines["left"].get_visible()
        assert not ax.spines["top"].get_visible()
        assert not ax.spines["right"].get_visible()
        plt.close(fig)


class TestSetAx:
    def test_contain_expands_shorter_dimension(self):
        fig, ax = plt.subplots()
        ax.plot([0, 10], [0, 6])
        limits = set_ax(ax, 16 / 9)
        assert len(limits) == 4
        xmin, ymin, xmax, ymax = limits
        assert (xmax - xmin) / (ymax - ymin) == pytest.approx(16 / 9, rel=1e-6)
        plt.close(fig)


class TestMapHelpers:
    def test_adjust_bbox_preserves_center(self):
        lon1, lon2, lat1, lat2 = adjust_bbox_for_aspect(-10, 5, 45, 55, 16 / 9)
        assert lon1 < -10 or lon2 > 5 or lat1 < 45 or lat2 > 55
        assert (lon1 + lon2) / 2 == pytest.approx(-2.5)
        assert (lat1 + lat2) / 2 == pytest.approx(50.0)

    def test_get_aspect_ratio_landscape(self):
        assert get_aspect_ratio(box(0, 0, 16, 9)) == pytest.approx(16 / 9)


class TestNormalizeHexColor:
    def test_hex_passthrough(self):
        assert normalize_hex_color("#FF0000") == "#ff0000"

    def test_name_to_hex(self):
        assert normalize_hex_color("red") == "#ff0000"

    def test_invalid_raises(self):
        with pytest.raises(ValueError, match="Invalid color"):
            normalize_hex_color("not-a-color")


class TestPlotLinestring:
    def test_draws_on_axes(self):
        fig, ax = plt.subplots()
        plot_linestring(ax, LineString([(0, 0), (1, 1)]), verbose=False)
        assert len(ax.lines) == 1
        plt.close(fig)

    def test_kwargs_override_defaults(self):
        fig, ax = plt.subplots()
        plot_linestring(
            ax,
            LineString([(0, 0), (1, 0)]),
            color="#525252",
            linestyle="--",
            verbose=False,
        )
        line = ax.lines[0]
        assert line.get_color() == "#525252"
        assert line.get_linestyle() == "--"
        plt.close(fig)

    def test_empty_raises(self):
        fig, ax = plt.subplots()
        with pytest.raises(ValueError, match="non-empty"):
            plot_linestring(ax, LineString(), verbose=False)
        plt.close(fig)

    def test_invalid_type_raises(self):
        fig, ax = plt.subplots()
        with pytest.raises(ValueError, match="non-empty"):
            plot_linestring(ax, box(0, 0, 1, 1), verbose=False)
        plt.close(fig)

    def test_default_config_not_mutated(self):
        fig, ax = plt.subplots()
        plot_linestring(ax, LineString([(0, 0), (1, 1)]), color="red", verbose=False)
        assert DEFAULT_LINESTRING_PLOT_CONFIG["color"] == "#3182bd"
        plt.close(fig)

    def test_verbose_message(self, capsys):
        fig, ax = plt.subplots()
        plot_linestring(ax, LineString([(0, 0), (1, 1)]))
        out = capsys.readouterr().out
        assert "✅ [plot_linestring] 1 line added to plot" in out
        plt.close(fig)

    def test_multilinestring(self):
        fig, ax = plt.subplots()
        geom = MultiLineString(
            [LineString([(0, 0), (1, 0)]), LineString([(0, 1), (1, 1)])]
        )
        plot_linestring(ax, geom, verbose=False)
        assert len(ax.lines) == 2
        plt.close(fig)

    def test_multilinestring_verbose_plural(self, capsys):
        fig, ax = plt.subplots()
        geom = MultiLineString(
            [LineString([(0, 0), (1, 0)]), LineString([(0, 1), (1, 1)])]
        )
        plot_linestring(ax, geom)
        out = capsys.readouterr().out
        assert "✅ [plot_linestring] 2 lines added to plot" in out
        plt.close(fig)

    def test_label_on_first_part_only(self):
        fig, ax = plt.subplots()
        geom = MultiLineString(
            [LineString([(0, 0), (1, 0)]), LineString([(0, 1), (1, 1)])]
        )
        plot_linestring(ax, geom, label="route", verbose=False)
        assert ax.lines[0].get_label() == "route"
        assert ax.lines[1].get_label() == "_nolegend_"
        plt.close(fig)


class TestPointsToLinestring:
    def test_builds_linestring(self):
        line = points_to_linestring([Point(1, 2), Point(3, 4)])
        assert isinstance(line, LineString)
        assert list(line.coords) == [(1.0, 2.0), (3.0, 4.0)]

    def test_too_few_points_raises(self):
        with pytest.raises(ValueError, match="At least 2"):
            points_to_linestring([Point(0, 0)])