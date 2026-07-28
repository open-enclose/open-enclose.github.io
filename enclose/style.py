r"""Shared plotting conventions for the enclosure figures.

Ported from `Model_Construction.ipynb` cell 91 (`safe_log_power`, `style_axes`,
`common_labels`, `fill_between_sorted`) and cell 47 (the hatching idiom). Every figure in
`enclose.figures` is built from these instead of re-deriving axis cosmetics by hand, which
is how the six figure-producing cells drifted from each other in the first place (see
`REORGANIZATION_PROPOSAL.md`).

Color/linestyle convention actually in use across the source cells (preserved as-is, not
harmonized, since Phase 1's job is reproduction — harmonizing which planner color is
"correct" is a visible content change that belongs to a later, reviewed phase):

- Planner/first-best loci: `blue` in single-series figures (`social_optimum`,
  `social_opt_cond`, `comparison`), `black` in figures that overlay decentralized loci too
  (`nash_eq`, `nash_so_comp`, `monopoly`, `combined_4x4`).
- Decentralized/Nash loci: `red`.
- Monopoly loci: `green`.
- `dashed`: the conditional-optimum / global-games selection locus.
- `':'` (dotted): the vertical threshold lines at theta=1 and theta=theta_H.
"""

import numpy as np
from matplotlib.patches import Polygon as MplPolygon

COLOR_PLANNER_BLUE = "blue"
COLOR_PLANNER_BLACK = "black"
COLOR_DECENTRALIZED = "red"
COLOR_MONOPOLY = "green"
LINESTYLE_SELECTION = "dashed"
LINESTYLE_THRESHOLD = ":"
REGION_ALPHA = 0.12


def safe_log_power(expr, power=1.0, shift=0.0):
    """Return log((expr)**power) + shift, masking expr<=0 as NaN.

    Every locus has the form l_bar = [expr]^(1/alpha), where expr changes sign as theta
    crosses 1 or 1/alpha. This lets one theta grid carry every curve instead of hand-slicing
    the domain into pieces per branch.

    `shift` is also how the small hand-tuned offsets in the monopoly and comparison figures
    (previously buried literals like `- .03`) are applied — see the named constants in
    `enclose.figures`.
    """
    expr = np.asarray(expr, dtype=float)
    out = np.full_like(expr, np.nan, dtype=float)
    mask = np.isfinite(expr) & (expr > 0)
    out[mask] = np.log(expr[mask]**power) + shift
    return out


def style_axes(ax):
    """Hide ticks, keep only the left/bottom spines, thickened."""
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(2)
    ax.spines["bottom"].set_linewidth(2)


def common_labels(ax, fontsize=20):
    """theta/log-population-density axis labels, anchored at the axis tips.

    Wording: "log population density" — per the decision recorded in
    `paper/final_revisions.md` item 0.12 (matches the paper's prose and 5 of its 7 figures;
    the source notebook cells say "log labor density", the Feb 2026 appendix drift this
    corrects). `fontsize` defaults to the single-panel-figure convention (cells 26/36/45/47);
    `combined_4x4` overrides to the smaller multi-panel convention (cell 91).
    """
    ax.set_xlabel(r"$\theta$ (rel. TFP)", loc="right", fontsize=fontsize)
    ax.set_ylabel(r"$\ln(\overline{l})$ (log population density)", loc="top", fontsize=fontsize)


def fill_between_sorted(ax, x, y1, y2, where_mask, **kwargs):
    """fill_between, masked to the finite, where_mask-true portion of x/y1/y2."""
    m = where_mask & np.isfinite(x) & np.isfinite(y1) & np.isfinite(y2)
    ax.fill_between(x[m], y1[m], y2[m], **kwargs)


def fill_between_hatched(ax, x, y1, y2, hatch=".", edgecolor="red", alpha=0.75, **kwargs):
    """fill_between with the hatch idiom (cell 47): color='none', linewidth=0, hatch visible
    via edgecolor rather than facecolor."""
    ax.fill_between(x, y1, y2, alpha=alpha, hatch=hatch, color="none", linewidth=0.0,
                     edgecolor=edgecolor, **kwargs)


def hatch_polygon(ax, points, hatch=".", edgecolor="red"):
    """Hatch-fill an arbitrary polygon that fill_between can't reach (e.g. a triangular
    region between two curves with different x-domains). matplotlib requires setting
    hatch/edgecolor as attributes after construction for an unfilled Polygon to render one."""
    poly = ax.add_patch(MplPolygon(points, closed=True, fill=False, linewidth=0))
    poly.set_hatch(hatch)
    poly.set_edgecolor(edgecolor)
    return poly
