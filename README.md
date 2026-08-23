# viztools

![Version](https://img.shields.io/badge/version-0.1.3-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-29%20passing-brightgreen)

Matplotlib axis styling, map layout helpers, and ColorBrewer palettes for the
JEMA toolkit.  Versions independently of jematools, wherewhen, h3tools, and
tabtools.  See [CHANGELOG.md](CHANGELOG.md) and
[COMPATIBILITY.md](COMPATIBILITY.md).

Import directly — not re-exported through h3tools or jematools.

**Status:** early `0.1.x`.  Stable for notebook axis styling and ColorBrewer
palettes; linestring helpers are newer.  Not a cartography stack.

---

## Installation

Install **wherewhen** first (declared dependency), then viztools.  Replace
`YOUR_LOCAL_PATH` with the parent folder that contains both repos.

```bash
pip install -e "YOUR_LOCAL_PATH/wherewhen"
pip install -e "YOUR_LOCAL_PATH/viztools"
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
from viztools.viz import (
    format_plot,
    plot_linestring,
    points_to_linestring,
    set_ax,
    normalize_hex_color,
    adjust_bbox_for_aspect,
    set_aspect_ratio,
    get_aspect_ratio,
    resize_to_aspect,
    to_box,
    remove_axis_ticks,
)

format_plot(ax, spines="minimal", font_size=9, color="#333333")
plot_linestring(
    ax,
    points_to_linestring([Point(51.4142, 35.6961), Point(50.8764, 34.6400)]),
    linestyle="--",
)
set_ax(ax, target_aspect=16 / 9)          # after plotting data
normalize_hex_color("steelblue")            # → '#4682b4'
```

| Helper | Role |
|---|---|
| `format_plot` | Publication-quality spines / ticks / grid |
| `set_ax` | Match axis limits to a target aspect (via wherewhen) |
| `plot_linestring` / `points_to_linestring` | Draw paths; MultiLineString supported |
| `adjust_bbox_for_aspect` / `set_aspect_ratio` | Expand bbox / limits to a ratio |
| `get_aspect_ratio` / `resize_to_aspect` / `to_box` | Envelope aspect helpers |
| `remove_axis_ticks` | Hide tick marks and labels |
| `normalize_hex_color` | CSS3 name or hex → normalised hex |

`format_plot` defaults to hidden spines (classic open plot style).  Full
behaviour contract: [VIZTOOLS_CONTRACT.md](VIZTOOLS_CONTRACT.md).

### `palettes` — ColorBrewer2

```python
from viztools.palettes import get_palette, get_cmap, list_palettes, ANOMALY_PALETTE

colors = get_palette("YlOrRd", n=9)                    # list of hex strings
cmap   = get_cmap("Blues", n=7)                        # ListedColormap
names  = list_palettes(kind="sequential", n=9)         # available names
anomaly = ANOMALY_PALETTE                              # RdBu 9-class diverging
```

Bundled JSON sources:

| File | Contents |
|------|----------|
| `colorbrewer2_ranges.json` | Full 3–11 class palettes |
| `colorbrewer2_789.json` | Curated 7/8/9-class palettes |

---

## What this is not

- **Not a mapping SDK** — no tiles, basemaps, Folium, PyDeck, or Cartopy.
- **Not geodesic framing** — aspect helpers use planar bounding-box math.
- **Not perceptual colour science** — palette interpolation is linear in RGB
  (fine for notebooks; not Lab/OKLCH).
- **Not a substitute for h3tools drawing** — hex heatmaps/choropleths stay in
  h3tools; viztools styles axes and supplies palettes.

---

## Compatibility

| Item | Value |
|---|---|
| **Current version** | `0.1.3` |
| **Requires** | `wherewhen>=0.2.0` |
| **Typical consumer** | h3tools declares `viztools>=0.1.0` |

See [COMPATIBILITY.md](COMPATIBILITY.md) and [VIZTOOLS_CONTRACT.md](VIZTOOLS_CONTRACT.md).

---

## Tests

Install wherewhen first (see Installation), then:

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

---

## License

MIT
