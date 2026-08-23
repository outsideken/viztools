"""Tests for viztools.palettes ColorBrewer loading."""

from __future__ import annotations

import matplotlib.colors as mcolors
import pytest

from viztools.palettes import ANOMALY_PALETTE, get_cmap, get_palette, list_palettes


class TestGetPalette:
    def test_ylorrd_9_exact(self):
        colors = get_palette("YlOrRd", n=9)
        assert len(colors) == 9
        assert all(c.startswith("#") for c in colors)

    def test_blues_7_from_789_json(self):
        colors = get_palette("Blues", n=7)
        assert len(colors) == 7
        assert colors[0] == "#f7fbff"

    def test_rdbu_diverging_9(self):
        colors = get_palette("RdBu", n=9, kind="diverging")
        assert len(colors) == 9

    def test_interpolate_to_5_classes(self):
        colors = get_palette("YlOrRd", n=5)
        assert len(colors) == 5

    def test_unknown_palette_raises(self):
        with pytest.raises(ValueError, match="not found"):
            get_palette("NotAPalette", n=9)


class TestGetCmap:
    def test_returns_listed_colormap(self):
        cmap = get_cmap("YlOrRd", n=9)
        assert isinstance(cmap, mcolors.ListedColormap)
        assert cmap.N == 9


class TestAnomalyPalette:
    def test_has_nine_diverging_colours(self):
        assert len(ANOMALY_PALETTE) == 9
        assert ANOMALY_PALETTE == get_palette("RdBu", n=9, kind="diverging")


class TestListPalettes:
    def test_returns_sorted_names(self):
        names = list_palettes(kind="sequential", n=9, print_catalogue=False)
        assert "YlOrRd" in names
        assert names == sorted(names)