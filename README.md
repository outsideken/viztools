# viztools

![Version](https://img.shields.io/badge/version-0.1.3-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-29%20passing-brightgreen)

Matplotlib axis styling, map layout helpers, and ColorBrewer palettes for the
JEMA toolkit.  Versions independently of jematools, wherewhen, h3tools, and
tabtools.  See [CHANGELOG.md](CHANGELOG.md) and workspace
[COMPATIBILITY.md](../COMPATIBILITY.md).

Import directly — not re-exported through h3tools or jematools.

---

## Installation

```bash
pip install -e ~/Desktop/Working/grok/wherewhen
pip install -e ~/Desktop/Working/grok/viztools
```

---

## Quick start

```python
import matplotlib.pyplot as plt
from viztools.viz import format_plot
from viztools.palettes import get_palette, get_cmap

fig, ax = plt.subplots()
ax.bar(["A", "B", "C"], [3, 7, 5], color=get_palette("YlOrRd", n=3))
format_plot(ax, font_size=8, color="#969696")
plt.show()
```

```python
import viztools
viztools.list_functions()
```

---

## Modules

### `viz` — axis styling and map layout

```python
from shapely.geometry import Point
from viztools.viz import format_plot, plot_linestring, points_to_linestring, set_ax, normalize_hex_color

format_plot(ax, spines="minimal", font_size=9, color="#333333")
plot_linestring(
    ax,
    points_to_linestring([Point(51.4142, 35.6961), Point(50.8764, 34.6400)]),
    linestyle="--",
)
set_ax(ax, target_aspect=16 / 9)          # after plotting data
normalize_hex_color("steelblue")            # → '#4682b4'
```

`format_plot` defaults to hidden spines (classic open plot style).  See
`grok/VIZTOOLS_CONTRACT.md` for the full signature.

### `palettes` — ColorBrewer2

```python
from viztools.palettes import get_palette, get_cmap, ANOMALY_PALETTE

colors = get_palette("YlOrRd", n=9)                    # list of hex strings
cmap   = get_cmap("Blues", n=7)                        # ListedColormap
anomaly = ANOMALY_PALETTE                              # RdBu 9-class diverging
```

Bundled JSON sources:

| File | Contents |
|------|----------|
| `colorbrewer2_ranges.json` | Full 3–11 class palettes |
| `colorbrewer2_789.json` | Curated 7/8/9-class palettes |

---

## Tests

```bash
cd /path/to/viztools
pytest tests/ -q
```

---

## Dependencies

| Package | Required | Purpose |
|---------|----------|---------|
| `matplotlib` | Yes | Plotting |
| `numpy` | Yes | Palette interpolation |
| `webcolors` | Yes | CSS3 colour names |
| `wherewhen` | Yes | `get_bounds`, notification helpers |
| `shapely` | Transitive | Geometry helpers in `viz` (via wherewhen) |