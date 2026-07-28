r"""One function per paper figure. Each returns (fig, ax) — nothing is saved here;
`scripts/make_figures.py` handles output paths.

Sources (see `REORGANIZATION_PROPOSAL.md` for the fragmentation this consolidates):
`social_optimum`/`nash_equilibrium`/`monopoly`/`comparison` port `Model_Construction.ipynb`
cells 26/36/45/47; `combined_4x4` ports cell 91; `trajectories` ports
`generate_trajectories_figure.py`, already well-designed and only lightly adapted here to
call `enclose.loci` instead of its own inline copies of the same formulas.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon

from . import loci
from .style import (
    COLOR_DECENTRALIZED,
    COLOR_MONOPOLY,
    COLOR_PLANNER_BLACK,
    COLOR_PLANNER_BLUE,
    LINESTYLE_SELECTION,
    LINESTYLE_THRESHOLD,
    REGION_ALPHA,
    common_labels,
    fill_between_sorted,
    style_axes,
)

ALP = loci.ALP
C = loci.C
CV = loci.CV

# Named visual-separation offsets, replacing the buried `- .03` / `- .017` literals in the
# source cells (cell 45, cell 47) that nudge near-coincident loci apart so both are visible.
MONOPOLY_VISUAL_SHIFT = -0.03
COMPARISON_VISUAL_SHIFT = -0.017


def social_optimum(cond_opt=True, ax=None):
    """social_optimum.png (cond_opt=False) / social_opt_cond.png (cond_opt=True).

    Source: Model_Construction.ipynb cell 26.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))
    else:
        fig = ax.figure

    the_1 = np.arange(1.1, 2.1, 0.01)
    the_r1 = np.arange(1.1, CV, 0.01)
    the_r2 = np.arange(CV, 2.1, 0.01)

    l01, l11 = loci.ln_l01(the_1), loci.ln_l11(the_1)
    ax.plot(the_1, l01, color=COLOR_PLANNER_BLUE)
    ax.plot(the_1, l11, color=COLOR_PLANNER_BLUE)

    if cond_opt:
        # ps0/ps1/ps: the conditional-optimum "selection" loci. ps0 coincides with the
        # second-best no-enclosure threshold (ln_lc0); ps1 coincides with the decentralized
        # full-enclosure threshold (ln_ld1) -- a real economic coincidence, not reuse for
        # convenience.
        ps0, ps1, ps = loci.ln_lc0(the_r2), loci.ln_ld1(the_r2), loci.ln_ls(the_r1)
        ax.plot(the_r2, ps0, color=COLOR_PLANNER_BLUE, linestyle=LINESTYLE_SELECTION)
        ax.plot(the_r2, ps1, color=COLOR_PLANNER_BLUE, linestyle=LINESTYLE_SELECTION)
        ax.plot(the_r1, ps, color=COLOR_PLANNER_BLUE, linestyle=LINESTYLE_SELECTION, linewidth=2)
        ax.axvline(CV, ymax=0.95, linestyle=LINESTYLE_THRESHOLD, color="black")

    ax.axvline(1, ymax=0.95, linestyle=LINESTYLE_THRESHOLD, color="black")

    ep = np.max(the_1) + 0.021
    ax.text(ep, np.min(l01), r"$\bar l^1_0$", fontsize=16)
    ax.text(ep, np.min(l11) + 0.05, r"$\bar l^1_1$", fontsize=16)

    if cond_opt:
        ax.text(ep, np.min(ps0), r"$\bar l^s_0$", fontsize=16)
        ax.text(ep, np.min(ps1) - 0.05, r"$\bar l^s_1$", fontsize=16)
        ax.text(the_r1[0] - 0.04, ps[0] - 0.04, r"$\bar l^s$", fontsize=16)
        ax.text(CV - 0.04, np.min(l01) - 0.5, r"$\theta_H=\frac{1}{\alpha}$", fontsize=16)
        ax.text(1.2, np.max(l11) - 0.5, r"$Low-TFP$", fontsize=22)
        ax.text(1.58, np.max(l11) - 0.5, r"$High-TFP$", fontsize=22)
    else:
        ax.text(1.3, 0.9, "Partial enclosure", rotation=-25, size=18)

    ax.text(1, np.min(l01) - 0.5, r"$1$", fontsize=16)
    ax.text(1.2, 0.1, "No enclosure", rotation=-45, size=20)
    ax.text(1.34, 1.8, "Full enclosure", rotation=-15, size=18)

    fill_between_sorted(ax, the_1, l01, l11, np.ones_like(the_1, bool), alpha=REGION_ALPHA, color="C0")

    style_axes(ax)
    common_labels(ax)
    return fig, ax


def nash_equilibrium(full_diag=True, ax=None):
    """nash_so_comp.png (full_diag=True) / nash_eq.png (full_diag=False).

    Source: Model_Construction.ipynb cell 36.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))
    else:
        fig = ax.figure

    the_1 = np.arange(1.1, 2.1, 0.01)
    the_d = np.arange(0.8, 2.1, 0.01)
    the_gg = np.arange(0.8, CV, 0.01)

    l01, l11 = loci.ln_l01(the_1), loci.ln_l11(the_1)
    l0d, l1d = loci.ln_ld0(the_d), loci.ln_ld1(the_d)
    pdgg = loci.ln_gg(the_gg)

    ep = np.max(the_1) + 0.021

    if full_diag:
        ax.plot(the_1, l01, color=COLOR_PLANNER_BLACK)
        ax.plot(the_1, l11, color=COLOR_PLANNER_BLACK)
        ax.text(ep, np.min(l01), r"$\bar l^1_0$", fontsize=16)
        ax.text(ep, np.min(l11) + 0.05, r"$\bar l^1_1$", fontsize=16)

    ax.plot(the_d, l0d, color=COLOR_DECENTRALIZED)
    ax.plot(the_d, l1d, color=COLOR_DECENTRALIZED)
    ax.plot(the_gg, pdgg, color=COLOR_DECENTRALIZED, linestyle=LINESTYLE_SELECTION, linewidth=2)

    ax.axvline(CV, ymax=0.95, linestyle=LINESTYLE_THRESHOLD, color="black")
    ax.axvline(1, ymax=0.95, linestyle=LINESTYLE_THRESHOLD, color="black")

    ax.text(ep, np.min(l0d), r"$\bar l^d_0$", fontsize=16)
    ax.text(the_gg[0] - 0.05, pdgg[0] + 0.04, r"$\bar l^d_{gg}$", fontsize=16)
    ax.text(the_gg[0] - 0.05, l0d[0] + 0.04, r"$\bar l^d_{0}$", fontsize=16)
    ax.text(the_gg[0] - 0.05, l1d[0] + 0.04, r"$\bar l^d_1$", fontsize=16)

    if full_diag:
        ax.text(ep, np.min(l1d) - 0.07, r"$\bar l^d_1$", fontsize=16)
        ax.text(CV - 0.05, np.min(l0d) - 1.75, r"$\theta_H=\frac{1}{\alpha}$", fontsize=16)
        ax.text(1, np.min(l0d) - 1.75, r"$1$", fontsize=16)
        fill_between_sorted(ax, the_1, l01, l11, np.ones_like(the_1, bool), alpha=REGION_ALPHA, color="C0")
    else:
        ax.text(ep, np.min(l1d), r"$\bar l^d_1$", fontsize=16)
        ax.text(CV - 0.05, np.min(l0d) - 0.5, r"$\theta_H=\frac{1}{\alpha}$", fontsize=16)
        ax.text(1, np.min(l0d) - 0.5, r"$1$", fontsize=16)

    ax.text(1.1, 0.1, "No enclosure", rotation=-25, size=20)
    ax.text(1.34, 1.8, "Full enclosure", rotation=-25, size=18)
    ax.text(1.7, 0.1, "Partial enclosure", rotation=-15, size=18)
    ax.text(0.9, 1.7, "Multiplicity", rotation=-25, size=18)
    ax.text(1.2, np.max(l11) - 0.5, r"$Low-TFP$", fontsize=22)
    ax.text(1.58, np.max(l11) - 0.5, r"$High-TFP$", fontsize=22)

    fill_between_sorted(ax, the_d, l0d, l1d, the_d > CV, alpha=REGION_ALPHA, color="C3")
    fill_between_sorted(ax, the_d, l1d, l0d, the_d < CV, alpha=REGION_ALPHA, color="C3")

    style_axes(ax)
    common_labels(ax)
    return fig, ax


def monopoly(ax=None):
    """monopoly.png.

    Source: Model_Construction.ipynb cell 45.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))
    else:
        fig = ax.figure

    the_1 = np.arange(1.1, 2.1, 0.01)
    the_d = np.arange(CV, 2.1, 0.01)
    the_gg = np.arange(0.8, CV, 0.01)
    the_r2 = np.arange(CV, 2.1, 0.01)

    l01, l11 = loci.ln_l01(the_1), loci.ln_l11(the_1)
    l0d, l1d = loci.ln_ld0(the_d), loci.ln_ld1(the_d)
    pdgg = loci.ln_gg(the_gg)

    # Monopoly loci: the low-TFP and the coincident-with-ln_ld0 high-TFP line both get the
    # same visual-separation shift; the third (ln_lm1) doesn't need one (see loci.ln_lm1).
    pm = loci.ln_lm0(the_gg) + MONOPOLY_VISUAL_SHIFT
    pm0 = loci.ln_ld0(the_r2) + MONOPOLY_VISUAL_SHIFT
    pm1 = loci.ln_lm1(the_r2)

    ep = np.max(the_1) + 0.021

    ax.plot(the_1, l01, color=COLOR_PLANNER_BLACK)
    ax.plot(the_1, l11, color=COLOR_PLANNER_BLACK)
    ax.text(ep, np.min(l01), r"$\bar l^1_0$", fontsize=16)
    ax.text(ep, np.min(l11) + 0.05, r"$\bar l^1_1$", fontsize=16)

    ax.plot(the_d, l0d, color=COLOR_DECENTRALIZED)
    ax.plot(the_d, l1d, color=COLOR_DECENTRALIZED)
    ax.plot(the_gg, pdgg, color=COLOR_DECENTRALIZED, linestyle=LINESTYLE_SELECTION, linewidth=2)

    ax.axvline(CV, ymax=0.95, linestyle=LINESTYLE_THRESHOLD, color="black")
    ax.axvline(1, ymax=0.95, linestyle=LINESTYLE_THRESHOLD, color="black")

    ax.plot(the_gg, pm, color=COLOR_MONOPOLY, linewidth=2)
    ax.plot(the_r2, pm0, color=COLOR_MONOPOLY, linewidth=2)
    ax.plot(the_r2, pm1, color=COLOR_MONOPOLY, linewidth=2)

    ax.text(ep, np.min(l0d), r"$\bar l^d_0, \bar l^m_0$", fontsize=16)
    ax.text(np.max(the_gg) - 0.64, np.min(pdgg) + 0.38, r"$\bar l^d_1, \bar l^m$", fontsize=16)
    ax.text(ep, np.min(l1d) - 0.1, r"$\bar l^d_1$", fontsize=16)

    fill_between_sorted(ax, the_1, l01, l11, np.ones_like(the_1, bool), alpha=REGION_ALPHA, color="C0")
    fill_between_sorted(ax, the_d, l0d, l1d, the_d > CV, alpha=REGION_ALPHA, color="C3")

    ax.text(CV - 0.05, np.min(l0d) - 1.75, r"$\theta_H=\frac{1}{\alpha}$", fontsize=16)
    ax.text(1, np.min(l0d) - 1.75, r"$1$", fontsize=16)

    # No explicit color, matching the source: matplotlib's default color cycle applies.
    ax.scatter(1.05, 1.75)
    ax.text(1.07, 1.77, "A", fontsize=20)
    ax.scatter(2.05, 1.1)
    ax.text(2.07, 1.12, "B", fontsize=20)

    ax.text(np.max(the_r2) + 0.04, np.max(pm1), r"$\bar l_1^m$", fontsize=16)
    ax.text(1.2, np.max(l11) - 0.5, r"$Low-TFP$", fontsize=22)
    ax.text(1.58, np.max(l11) - 0.5, r"$High-TFP$", fontsize=22)

    style_axes(ax)
    common_labels(ax)
    return fig, ax


def comparison(ax=None):
    """comparison.png. `cond_opt` isn't exposed here: the source cell's cond_opt=False
    branch saves to the same filename as cond_opt=True, so the True (full) version is
    what's actually always published.

    Source: Model_Construction.ipynb cell 47.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))
    else:
        fig = ax.figure

    the_1 = np.arange(1.1, 2.1, 0.01)
    the_r1 = np.arange(1.1, CV, 0.01)
    the_r2 = np.arange(CV, 2.1, 0.01)
    exr = np.arange(0.9, 1.1, 0.01)  # extends the gg locus below theta=1.1

    l01, l11 = loci.ln_l01(the_1), loci.ln_l11(the_1)
    ps0, ps1, ps = loci.ln_lc0(the_r2), loci.ln_ld1(the_r2), loci.ln_ls(the_r1)
    l0d, l1d = loci.ln_ld0(the_r2), loci.ln_ld1(the_r2)
    pdgg = loci.ln_gg(the_r1)
    pdgge = loci.ln_gg(exr)

    ax.plot(the_1, l01, color=COLOR_PLANNER_BLUE, alpha=0.54)
    ax.plot(the_1, l11, color=COLOR_PLANNER_BLUE, alpha=0.54)

    ax.plot(the_r2, ps0, color=COLOR_PLANNER_BLUE, linestyle=LINESTYLE_SELECTION)
    ax.plot(the_r2, ps1 + COMPARISON_VISUAL_SHIFT, color=COLOR_PLANNER_BLUE, linestyle=LINESTYLE_SELECTION)
    ax.plot(the_r1, ps, color=COLOR_PLANNER_BLUE, linestyle=LINESTYLE_SELECTION, linewidth=2)
    ax.plot(the_r2, l0d, color=COLOR_DECENTRALIZED)
    ax.plot(the_r2, l1d, color=COLOR_DECENTRALIZED, linewidth=2)
    # solid here (not dashed, unlike nash_equilibrium/monopoly's gg locus)
    ax.plot(the_r1, pdgg, color=COLOR_DECENTRALIZED, linewidth=2)
    ax.plot(exr, pdgge, color=COLOR_DECENTRALIZED, linewidth=2)

    ax.axvline(CV, ymax=0.95, linestyle=LINESTYLE_THRESHOLD, color="black")
    ax.axvline(1, ymax=0.95, linestyle=LINESTYLE_THRESHOLD, color="black")

    ep = np.max(the_1) + 0.021
    ax.text(ep, np.min(l01), r"$\bar l^1_0$", fontsize=16)
    ax.text(ep, np.min(l11) + 0.05, r"$\bar l^1_1$", fontsize=16)
    ax.text(the_r1[0] - 0.25, pdgg[0] + 0.5, r"$\bar l^d_{gg}$", fontsize=16)
    ax.text(ep, np.min(ps0), r"$\bar l^s_0$", fontsize=16)
    ax.text(ep, np.min(ps1) - 0.05, r"$\bar l^s_1, \bar l^d_1$", fontsize=16)
    ax.text(ep, np.min(l0d), r"$\bar l^d_0$", fontsize=16)
    ax.text(CV - 0.04, np.min(l01) - 0.5, r"$\theta_H=\frac{1}{\alpha}$", fontsize=16)
    ax.text(1, np.min(l01) - 0.5, r"$1$", fontsize=16)
    ax.text(the_r1[0] - 0.03, pdgg[0] + 1.56, r"$\bar l^s$", fontsize=16)

    ax.fill_between(the_1, l01, l11, alpha=0.05, color="C0")
    ax.fill_between(the_r1, pdgg, ps, alpha=0.75, hatch=".", color="none", linewidth=0.0, edgecolor="red")
    ax.fill_between(the_r2, l0d, ps0, alpha=0.5, hatch="...", color="none", linewidth=0.0, edgecolor="blue")
    ax.fill_between(the_r2, l0d, l1d, alpha=0.5, hatch="..", color="none", linewidth=0.0, edgecolor="blue")

    # Triangular over-enclosure region below theta=1.1: fill_between can't reach it since
    # the gg locus and the extended gg locus don't share an x-domain there.
    poly_points = [
        [exr[0], pdgge[0]],
        [the_r1[0], pdgg[0]],
        [the_r1[0], ps[0]],
        [exr[0], ps[0] + 0.3],
    ]
    triang = ax.add_patch(MplPolygon(poly_points, closed=True, fill=False, linewidth=0))
    triang.set_hatch(".")
    triang.set_edgecolor("red")

    style_axes(ax)
    # Bare wording (no "(rel. TFP)"/"(log population density)" descriptor), matching the
    # source cell -- but right/top-anchored like common_labels(), not the default centered
    # position, which collides with the in-plot theta_H annotation.
    ax.set_xlabel(r"$\theta$", loc="right", fontsize=20)
    ax.set_ylabel(r"$\ln(\overline{l})$", loc="top", fontsize=20)
    return fig, ax


def combined_4x4(mu=1.0, tau=1.0):
    """new_comp_fig4x4.png: four panels (a) mu=0,tau=0  (b) mu=1,tau=0  (c) mu=0,tau=1
    (d) mu=1,tau=1.

    Source: Model_Construction.ipynb cell 91.

    Panel (d) is a placeholder, ported faithfully from the source: it draws the
    planner/first-best band twice in two fill colors rather than a real combined
    governance-and-compensation locus. No such locus is derived anywhere in either
    codebase (see REORGANIZATION_PROPOSAL.md, Finding C) — deriving one is tracked as a
    separate follow-up, decoupled from this migration so it doesn't block reproducing
    what's currently published.
    """
    start, finish, step = 1.1, 2.1, 0.01
    cv12 = ((1 - mu) * (1 - ALP) + ALP) / ALP

    the_1 = np.arange(start, finish, step)
    the_d = np.arange(0.8, finish, step)
    the_gg = np.arange(0.8, CV, step)
    the_ggmu = np.arange(0.8, cv12, step)

    fig, ax = plt.subplots(2, 2, figsize=(12, 9))
    fig.tight_layout(pad=6.0)

    l01, l11 = loci.ln_l01(the_1), loci.ln_l11(the_1)

    # ---- panel a: mu=0, tau=0 ----
    a = ax[0, 0]
    a.plot(the_1, l01, color=COLOR_PLANNER_BLACK)
    a.plot(the_1, l11, color=COLOR_PLANNER_BLACK)
    fill_between_sorted(a, the_1, l01, l11, np.ones_like(the_1, bool), alpha=REGION_ALPHA, color="C0")

    l0d, l1d = loci.ln_ld0(the_d), loci.ln_ld1(the_d)
    pdgg = loci.ln_gg(the_gg)
    a.plot(the_d, l0d, color=COLOR_DECENTRALIZED)
    a.plot(the_d, l1d, color=COLOR_DECENTRALIZED)
    a.plot(the_gg, pdgg, color=COLOR_DECENTRALIZED, linestyle=LINESTYLE_SELECTION, linewidth=2)

    the_r1 = the_1
    the_r2 = the_1
    # ln_lc0's argument goes negative below theta_H; evaluated here on the full the_1
    # domain (matching cell 91's structure) and masked out immediately afterward, so the
    # resulting NaNs below theta_H are expected, not a bug -- suppress the warning.
    with np.errstate(invalid="ignore"):
        ps = np.where(the_r1 < CV, loci.ln_ls(the_r1), np.nan)
        ps0 = np.where(the_r2 > CV, loci.ln_lc0(the_r2), np.nan)
    ps1 = np.where(the_r2 > CV, loci.ln_ld1(the_r2), np.nan)

    a.plot(the_r1, ps, linestyle=LINESTYLE_SELECTION, color=COLOR_PLANNER_BLUE, linewidth=2)
    a.plot(the_r2, ps0, linestyle=LINESTYLE_SELECTION, color=COLOR_PLANNER_BLUE, linewidth=2)
    a.plot(the_r2, ps1, linestyle=LINESTYLE_SELECTION, color=COLOR_PLANNER_BLUE, linewidth=2)

    a.axvline(CV, ymax=0.95, linestyle=LINESTYLE_THRESHOLD, color="black")
    a.axvline(1, ymax=0.95, linestyle=LINESTYLE_THRESHOLD, color="black")

    fill_between_sorted(a, the_d, l0d, l1d, the_d > CV, alpha=REGION_ALPHA, color="C3")
    fill_between_sorted(a, the_d, l1d, l0d, the_d < CV, alpha=REGION_ALPHA, color="C3")

    a.set_title(r"a: $\mu=0,\tau=0$", fontsize=15)
    common_labels(a, fontsize=12)
    style_axes(a)

    # ---- panel b: mu=1, tau=0 ----
    b = ax[0, 1]
    b.plot(the_1, l01, color=COLOR_PLANNER_BLACK)
    b.plot(the_1, l11, color=COLOR_PLANNER_BLACK)
    fill_between_sorted(b, the_1, l01, l11, np.ones_like(the_1, bool), alpha=REGION_ALPHA, color="C0")

    l0dmu = loci.ln_ld0_mu(the_d, mu=mu)
    l1dmu = loci.ln_ld1_mu(the_d, mu=mu)
    pdggmu = loci.ln_gg_mu(the_ggmu, mu=mu)
    b.plot(the_d, l0dmu, color=COLOR_DECENTRALIZED)
    b.plot(the_d, l1dmu, color=COLOR_DECENTRALIZED)
    b.plot(the_ggmu, pdggmu, color=COLOR_DECENTRALIZED, linestyle=LINESTYLE_SELECTION, linewidth=2)

    b.axvline(1, ymax=0.95, linestyle=LINESTYLE_THRESHOLD, color="black")

    fill_between_sorted(b, the_d, l0dmu, l1dmu, the_d > cv12, alpha=REGION_ALPHA, color="C3")
    fill_between_sorted(b, the_d, l1dmu, l0dmu, the_d < cv12, alpha=REGION_ALPHA, color="C3")

    b.set_title(r"b: $\mu=1,\tau=0$", fontsize=15)
    common_labels(b, fontsize=12)
    style_axes(b)

    # ---- panel c: mu=0, tau=1 ----
    cax = ax[1, 0]
    cax.set_xlim(0.8, 2.15)
    cax.set_ylim(-1.6, 4)

    cax.plot(the_1, l01, color=COLOR_PLANNER_BLACK)
    cax.plot(the_1, l11, color=COLOR_PLANNER_BLACK)
    fill_between_sorted(cax, the_1, l01, l11, np.ones_like(the_1, bool), alpha=REGION_ALPHA, color="C0")

    l0dtau = loci.ln_ld0(the_1, tau=tau)
    l1dtau = loci.ln_ld1(the_1, tau=tau)
    cax.plot(the_1, l0dtau, color=COLOR_DECENTRALIZED)
    cax.plot(the_1, l1dtau, color=COLOR_DECENTRALIZED)

    cax.plot(the_r1, ps, linestyle=LINESTYLE_SELECTION, color=COLOR_PLANNER_BLUE, linewidth=2)
    cax.plot(the_r2, ps0, linestyle=LINESTYLE_SELECTION, color=COLOR_PLANNER_BLUE, linewidth=2)
    cax.plot(the_r2, ps1, linestyle=LINESTYLE_SELECTION, color=COLOR_PLANNER_BLUE, linewidth=2)

    cax.axvline(CV, ymax=0.95, linestyle=LINESTYLE_THRESHOLD, color="black")
    cax.axvline(1, ymax=0.95, linestyle=LINESTYLE_THRESHOLD, color="black")

    fill_between_sorted(cax, the_1, l0dtau, l1dtau, the_1 > cv12, alpha=REGION_ALPHA, color="C3")
    fill_between_sorted(cax, the_1, l1dtau, l0dtau, the_1 < cv12, alpha=REGION_ALPHA, color="C3")

    cax.set_title(r"c: $\mu=0,\tau=1$", fontsize=15)
    common_labels(cax, fontsize=12)
    style_axes(cax)

    # ---- panel d: mu=1, tau=1 -- PLACEHOLDER, see docstring ----
    d = ax[1, 1]
    d.set_xlim(0.8, 2.15)

    d.plot(the_1, l01, color=COLOR_PLANNER_BLACK)
    d.plot(the_1, l11, color=COLOR_PLANNER_BLACK)
    fill_between_sorted(d, the_1, l01, l11, np.ones_like(the_1, bool), alpha=REGION_ALPHA, color="C0")
    fill_between_sorted(d, the_1, l01, l11, np.ones_like(the_1, bool), alpha=REGION_ALPHA, color="C3")

    d.axvline(1, ymax=0.95, linestyle=LINESTYLE_THRESHOLD, color="black")

    d.set_title(r"d: $\mu=1,\tau=1$", fontsize=15)
    common_labels(d, fontsize=12)
    style_axes(d)

    return fig, ax


# ---------------------------------------------------------------------------
# trajectories.png -- ported from generate_trajectories_figure.py, which was already
# well-designed (named, eq-tagged loci, sanity_checks()); adapted only to call
# `enclose.loci` instead of its own inline copies of the same formulas.
# ---------------------------------------------------------------------------

_TRAJ_YLIM = (-1.8, 4.4)
_TRAJ_XLIM = (0.74, 2.34)
_TRAJ_HATCH_CAP = 3.6
_TRAJ_THETA_TAU = loci.THETA_TAU

_ARROW = dict(arrowstyle="-|>", linewidth=2.2, color="black", shrinkA=0, shrinkB=0, mutation_scale=18)
_WBOX = dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1.2)
_ARROW_LEN = 1.6


def _traj_base_panel(ax):
    """The Figure-5-style canvas: first-best band, second-best loci, decentralized loci,
    over/under-enclosure hatching, dotted verticals. Returns the low-TFP theta grid."""
    th_lo = np.linspace(0.82, CV - 1e-6, 500)
    th_hi = np.linspace(CV, 2.1, 500)
    th_fb = np.linspace(1.1, 2.1, 500)
    th_s = np.linspace(1.02, CV, 500)

    ax.plot(th_fb, loci.ln_l01(th_fb), color=COLOR_PLANNER_BLUE, alpha=0.54)
    ax.plot(th_fb, loci.ln_l11(th_fb), color=COLOR_PLANNER_BLUE, alpha=0.54)
    ax.fill_between(th_fb, loci.ln_l01(th_fb), loci.ln_l11(th_fb), alpha=0.05, color="C0")

    ax.plot(th_s, loci.ln_ls(th_s), color=COLOR_PLANNER_BLUE, linestyle=LINESTYLE_SELECTION, linewidth=2)
    ax.plot(th_hi, loci.ln_lc0(th_hi), color=COLOR_PLANNER_BLUE, linestyle=LINESTYLE_SELECTION)
    ax.plot(th_hi, loci.ln_ld1(th_hi) + COMPARISON_VISUAL_SHIFT, color=COLOR_PLANNER_BLUE, linestyle=LINESTYLE_SELECTION)

    ax.plot(th_hi, loci.ln_ld0(th_hi), color=COLOR_DECENTRALIZED)
    ax.plot(th_hi, loci.ln_ld1(th_hi), color=COLOR_DECENTRALIZED, linewidth=2)

    upper = np.where(th_lo > 1.001, loci.ln_ls(np.maximum(th_lo, 1.001)), np.inf)
    upper = np.minimum(upper, _TRAJ_HATCH_CAP)
    ax.fill_between(th_lo, loci.ln_gg(th_lo), upper, alpha=0.75, hatch=".",
                     color="none", linewidth=0.0, edgecolor="red")

    ax.fill_between(th_hi, loci.ln_lc0(th_hi), loci.ln_ld0(th_hi), alpha=0.5, hatch="...",
                     color="none", linewidth=0.0, edgecolor="blue")
    ax.fill_between(th_hi, loci.ln_ld0(th_hi), loci.ln_ld1(th_hi), alpha=0.5, hatch="..",
                     color="none", linewidth=0.0, edgecolor="blue")

    ax.axvline(CV, ymax=0.95, linestyle=LINESTYLE_THRESHOLD, color="black")
    ax.axvline(1, ymax=0.95, linestyle=LINESTYLE_THRESHOLD, color="black")
    ax.text(1, _TRAJ_YLIM[0] + 0.06, r"$1$", fontsize=14, ha="center")
    ax.text(CV, _TRAJ_YLIM[0] + 0.06, r"$\theta_H=\frac{1}{\alpha}$", fontsize=14, ha="center")

    ep = 2.115
    ax.text(ep, loci.ln_l01(np.array([2.1]))[0], r"$\bar l^1_0$", fontsize=13)
    ax.text(ep, loci.ln_l11(np.array([2.1]))[0] + 0.05, r"$\bar l^1_1$", fontsize=13)
    ax.text(ep, loci.ln_lc0(np.array([2.1]))[0], r"$\bar l^s_0$", fontsize=13)
    ax.text(ep, loci.ln_ld1(np.array([2.1]))[0] - 0.07, r"$\bar l^s_1, \bar l^d_1$", fontsize=13)
    ax.text(ep, loci.ln_ld0(np.array([2.1]))[0] + 0.16, r"$\bar l^d_0$", fontsize=13)
    ax.text(1.075, 4.05, r"$\bar l^s$", fontsize=13)

    style_axes(ax)
    ax.set_xlim(*_TRAJ_XLIM)
    ax.set_ylim(*_TRAJ_YLIM)
    xlbl = ax.set_xlabel(r"$\theta$", fontsize=18)
    xpos = list(xlbl.get_position())
    ax.xaxis.set_label_coords(xpos[0] + 0.44, xpos[1] - 0.02)
    ax.set_ylabel(r"$\ln(\overline{l})$", fontsize=16)

    return th_lo


def _traj_panel_a(ax):
    """Movements in fundamentals against loci fixed at mu = tau = 0."""
    th_lo = _traj_base_panel(ax)
    ax.plot(th_lo, loci.ln_gg(th_lo), color=COLOR_DECENTRALIZED, linestyle=LINESTYLE_SELECTION, linewidth=2)
    ax.text(th_lo[0] - 0.055, loci.ln_gg(th_lo[:1])[0] + 0.04, r"$\bar l^d_{gg}$", fontsize=13)
    ax.set_title(r"(a) Fundamentals: shocks to $\bar l$ and $c/A$  (loci fixed, $\mu=\tau=0$)", fontsize=13.5)

    ax.scatter(1.0, 0.9, s=45, color="black", zorder=5, clip_on=False)
    ax.text(1.0, 0.55, "Weitzman–Samuelson", fontsize=11, ha="center", va="top", bbox=_WBOX)

    x = 2.0
    y0 = -1.30
    ax.annotate("", xy=(x, y0 + _ARROW_LEN), xytext=(x, y0), arrowprops=_ARROW)
    ax.text(x + 0.03, y0 + 0.12, "Boserup", fontsize=11, ha="left", bbox=_WBOX)
    cross = loci.ln_ld0(np.array([x]))[0]
    ax.scatter(x, cross, s=48, facecolor="white", edgecolor="black", zorder=6, linewidth=1.4)
    ax.text(x - 0.05, cross + 0.04, "smooth expansion", fontsize=10, ha="right", style="italic", bbox=_WBOX)

    x = 1.2
    y0 = 0.70
    ax.annotate("", xy=(x, y0 + _ARROW_LEN), xytext=(x, y0), arrowprops=_ARROW)
    ax.text(x - 0.035, 1.45, "Barbed wire /\ncheap titling", fontsize=11, ha="right", va="center", bbox=_WBOX)
    cross = loci.ln_gg(np.array([x]))[0]
    ax.scatter(x, cross, s=48, facecolor="white", edgecolor="black", zorder=6, linewidth=1.4)
    ax.text(x + 0.045, cross - 0.06, "tipping point", fontsize=10, ha="left", style="italic", bbox=_WBOX)

    ax.text(0.86, 3.0, "over-enclosure", fontsize=10, style="italic", color="darkred", rotation=-22, bbox=_WBOX)
    ax.text(1.72, 0.12, "under-enclosure", fontsize=10, style="italic", color="darkblue", rotation=-13, bbox=_WBOX)

    ax.text(_TRAJ_XLIM[0] + 0.04, _TRAJ_YLIM[0] + 0.32,
            r"Vertical arrows: rise in $\bar l$ or equal-sized fall in $c/A$"
            "\n" r"(all loci scale as $(c/A)^{1/\alpha}$).",
            fontsize=9.5, style="italic", va="bottom")


def _traj_panel_b(ax):
    """Movements in institutions (tau, mu) with the economy's point fixed."""
    th_lo = _traj_base_panel(ax)
    ax.set_title(r"(b) Institutions: shifts in $\tau$ and $\mu$  (economy fixed)", fontsize=13.5)

    ax.plot(th_lo, loci.ln_gg(th_lo), color=COLOR_DECENTRALIZED, linewidth=2)
    ax.text(0.775, 2.55, r"$\bar l^d_{gg}(\tau\!=\!0)$", fontsize=12, ha="left", bbox=_WBOX)

    th_tau = np.linspace(_TRAJ_THETA_TAU + 1e-4, CV - 1e-6, 800)
    ax.plot(th_tau, loci.ln_gg(th_tau, tau=1.0), color="darkred", linewidth=2)
    ax.text(1.515, 2.85, r"$\bar l^d_{gg}(\tau\!=\!1)$", fontsize=13, ha="left", color="darkred", bbox=_WBOX)
    ax.text(1.245, 3.82, r"$\to\infty$: no raid pays for" "\n" r"$\theta<\alpha^{-\alpha}$ when $\tau=1$",
            fontsize=9, ha="center", va="center", style="italic", color="darkred", bbox=_WBOX)

    x = 1.46
    ax.annotate("", xy=(x, loci.ln_gg(np.array([x]))[0] + 0.12),
                xytext=(x, loci.ln_gg(np.array([x]), tau=1.0)[0] - 0.10),
                arrowprops=dict(arrowstyle="-|>", linewidth=2.0, color="darkred", mutation_scale=16))
    ax.text(x + 0.02, 2.15, r"$\tau: 1\to 0$", fontsize=11, ha="left", color="darkred", bbox=_WBOX)

    ax.scatter(1.1, 2.7, s=45, color="black", zorder=6)
    ax.text(1.085, 2.98, "Marx / Brenner", fontsize=11, ha="right", bbox=_WBOX)

    ax.annotate("", xy=(1.04, -1.35), xytext=(1.49, -1.35), arrowprops=_ARROW)
    ax.text(1.265, -1.12,
            r"$\mu\!\uparrow$:  $\theta_H^\mu=\frac{1}{\alpha}-\mu\frac{1-\alpha}{\alpha}\;\to\;1$",
            fontsize=11, ha="center", bbox=_WBOX)

    ax.scatter(1.9, -0.24, s=45, color="black", zorder=6)
    ax.text(1.9, -0.62, "De Janvry", fontsize=11, ha="center", bbox=_WBOX)


def trajectories():
    """trajectories.png -- the new RESTUD-revision figure (editor item iii).

    Source: generate_trajectories_figure.py, ported to call `enclose.loci` instead of its
    own (numerically identical, cross-checked) inline locus definitions.
    """
    fig, (axa, axb) = plt.subplots(1, 2, figsize=(16, 7))
    _traj_panel_a(axa)
    _traj_panel_b(axb)
    fig.tight_layout(w_pad=3.0)
    return fig, (axa, axb)
