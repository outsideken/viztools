# viztools API contract

Specification for the **viztools** package (Phase 2b) based on what downstream
toolkit packages need today.  **h3tools 0.5.0** (current) declares
`viztools>=0.1.0` as a firm dependency; **tabtools** and notebooks import
viztools directly for palettes and axis styling.

*Contract for the viztools public surface.  Package version **0.1.3**
requires ``wherewhen>=0.2.0``; h3tools typically declares ``viztools>=0.1.0``.
See [COMPATIBILITY.md](COMPATIBILITY.md).*

## Design principles

| Principle | Detail |
|---|---|
| **Direct import** | `from viztools.viz import format_plot` — not re-exported through h3tools or jematools |
| **Matplotlib-first** | Functions accept `matplotlib.axes.Axes`; no hard dependency on geopandas |
| **Composable** | h3tools draws hex cells; viztools styles axes; user adds colourbars/legends |
| **Independent versioning** | viztools versions on its own; dependents pin floors (e.g. `viztools>=0.1.0`) |

## Required surface — `viztools.viz`

### `format_plot`

Minimal, publication-quality axis formatting.  Source reference:
`00 - Python Scripts/Viz Functions.py`.

```python
def format_plot(
    ax: matplotlib.axes.Axes | None = None,
    *,
    font_size: int | float = 10,
    color: str = "black",
    tick_length: float = 4,
    tick_width: float = 1,
    tick_color: str | None = None,
    label_color: str | None = None,
    spines: Literal["none", "bottom", "left", "all", "minimal"] = "none",
    show_ticks: Literal["all", "x", "y", "both"] = "all",
    show_labels: Literal["all", "x", "y", "both"] = "all",
    grid: bool | str = False,
    facecolor: str = "white",
    title_size: int | None = None,
    label_size: int | None = None,
) -> matplotlib.axes.Axes:
    ...
```

**Behaviour contract**

- When `ax is None`, operates on `plt.gca()`.
- Returns the formatted `Axes` (enables chaining).
- Default `spines="none"` gives the classic open plot style used across JEMA notebooks.
- Must not mutate data artists — only axis chrome (ticks, spines, grid, facecolor).

**h3tools usage pattern (2c wire-up)**

```python
import matplotlib.pyplot as plt
from h3tools import plot_hex_heatmap
from viztools.viz import format_plot

fig, ax = plt.subplots()
norm = plot_hex_heatmap(ax, cell_values, cmap="YlOrRd")
format_plot(ax, font_size=8, color="#969696")
plt.colorbar(plt.cm.ScalarMappable(cmap="YlOrRd", norm=norm), ax=ax)
```

## Planned surface — `viztools.palettes` (Phase 2b)

Not required by h3tools 0.4.0, but specified here so h3/tab notebook code can
migrate off inline ColorBrewer dicts.

| Symbol | Purpose |
|---|---|
| `get_palette(name, n)` | Return `n` hex colours for a named ColorBrewer scheme |
| `get_cmap(name)` | Return a Matplotlib `ListedColormap` for choropleth/heatmap |
| `ANOMALY_PALETTE` | Signed diverging palette for tabtools anomaly maps |

**Choropleth contract for h3tools (Phase 2c — implemented in h3tools 0.5.0)**

- `plot_hex_heatmap` and `plot_h3_choropleth` accept ``palette=``, ``palette_n``, ``palette_kind``.
- ``palette=`` resolves through ``viztools.palettes.get_cmap``; ``cmap=`` still accepts
  Matplotlib names with ColorBrewer fallback.
- ``plot_hex_heatmap`` returns ``(norm, cmap)`` for colourbar wiring.

## Package skeleton (Phase 2b — implemented in `grok/viztools`)

```
viztools/
├── __init__.py          # ℹ️ [viztools] v<version> loaded.
├── _version.py
├── _messages.py         # re-export from wherewhen._messages
├── viz.py               # format_plot, set_ax (alias)
└── palettes.py          # ColorBrewer JSON loader + anomaly palette
```

## Dependencies

| Package | Required | Notes |
|---|---|---|
| `matplotlib` | Yes | Core plotting |
| `wherewhen` | Yes | `_messages.loaded()` and notification style |
| `webcolors` | Yes | CSS3 name → RGB (from Viz Functions.py) |
| `numpy` | Optional | palette interpolation |

## Test contract

Minimum tests before h3tools removes the `conftest.py` viztools stub (2c):

1. `format_plot` returns the same `Axes` instance passed in.
2. `format_plot(ax=None)` formats `plt.gca()` without error.
3. Default call hides all four spines.
4. `spines="minimal"` shows bottom and left only.

## Version floor

| Consumer | Declares |
|---|---|
| **h3tools 0.5.0** | `viztools>=0.1.0` |

Bump viztools minor when adding palette APIs; bump h3tools only when it starts
calling new viztools symbols (Phase 2c).