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

from . import loci, model
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

    Source: Model_Construction.ipynb cell 91, with panel (d) rebuilt (see below).

    **Panel (d) now computes a real combined mu-and-tau locus.** The source cell had a
    placeholder here — it drew the planner band twice in two fill colors, never computing
    a decentralized curve at all. `online_appendix.md` eqs. 26-27 do close the loop: they
    generalize the tau-only condition by replacing Lambda with Lambda_mu (eq. 23), giving
    `ln_ld0`/`ln_ld1`'s joint (mu, tau) form.

    At mu=1, tau=1 those loci coincide *exactly* with the planner's — Lambda_mu becomes
    Lambda_o and the identity theta*Lambda_o^alpha = Lambda_o collapses the decentralized
    denominator to the planner's. That is the paper's Key Result (online_appendix.md 5.3,
    "the wedge closes when mu=1 AND tau=1") made concrete, and it is asserted in
    `loci.sanity_checks()` and `tests/test_loci.py`. So the panel looks much as it did
    before — but now because the two loci are computed and demonstrably equal, rather than
    because the same band was drawn twice.

    Domain note: `the_1` (1.1-2.1) sits entirely above theta_H^{mu=1} = 1 (eq. 24), so only
    the boundary conditions of eq. 27 are needed. Extending below theta=1 would require a
    combined-(mu, tau) global-games threshold, which is derived nowhere in the appendix or
    the codebase — see `ln_gg`, which is tau-extended but mu=0 only.
    """
    start, finish, step = 1.1, 2.1, 0.01
    cv12 = model.theta_H(ALP, mu)   # theta_H^mu, eq. (24)

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

    # ---- panel d: mu=1, tau=1 ----
    # The decentralized loci here are computed, not faked. They provably coincide with the
    # planner's (see the docstring and loci.sanity_checks()), so the red curves land exactly
    # on the black ones -- which is the panel's whole point: the wedge has closed.
    d = ax[1, 1]
    d.set_xlim(0.8, 2.15)

    d.plot(the_1, l01, color=COLOR_PLANNER_BLACK)
    d.plot(the_1, l11, color=COLOR_PLANNER_BLACK)
    fill_between_sorted(d, the_1, l01, l11, np.ones_like(the_1, bool), alpha=REGION_ALPHA, color="C0")

    l0dmutau = loci.ln_ld0(the_1, tau=tau, mu=mu)
    l1dmutau = loci.ln_ld1(the_1, tau=tau, mu=mu)
    # Dashed, unlike the solid decentralized loci in panels (a)-(c): at mu=tau=1 these sit
    # exactly on the black planner curves, and a solid red line would hide them entirely --
    # leaving a reader unable to see the coincidence that is the panel's whole point. The
    # dashes let the black show through. (No gg locus is drawn in this panel, so there is
    # no clash with the dashed-red gg convention used elsewhere in the figure.)
    d.plot(the_1, l0dmutau, color=COLOR_DECENTRALIZED, linestyle=(0, (6, 6)), linewidth=2)
    d.plot(the_1, l1dmutau, color=COLOR_DECENTRALIZED, linestyle=(0, (6, 6)), linewidth=2)
    fill_between_sorted(d, the_1, l0dmutau, l1dmutau, np.ones_like(the_1, bool),
                        alpha=REGION_ALPHA, color="C3")

    d.axvline(1, ymax=0.95, linestyle=LINESTYLE_THRESHOLD, color="black")

    d.set_title(r"d: $\mu=1,\tau=1$", fontsize=15)
    common_labels(d, fontsize=12)
    style_axes(d)

    return fig, ax


# Fixed for `wedge_panel` so the axes do not rescale as mu and tau move. Under a slider a
# self-scaling panel is unreadable -- the curves stay put and the frame jumps around, which
# reads as the loci moving when they have not. Chosen to contain panels (a)-(d) of
# `combined_4x4` at every (mu, tau), so the single panel is directly comparable to the 2x2.
_WEDGE_XLIM = (0.8, 2.15)
_WEDGE_YLIM = (-1.6, 4.0)


def wedge_panel(mu=0.0, tau=0.0, ax=None, second_best=True, figsize=(7.5, 6)):
    r"""One panel of `combined_4x4`, for *any* $(\mu, \tau)$ rather than the four corners.

    `combined_4x4` hard-codes $(\mu,\tau) \in \{0,1\}^2$ across four axes. This draws the
    same content on a single axis with both parameters continuous, which is what makes the
    wedge legible under a slider: the black planner band is fixed, and the red decentralized
    band moves toward it as governance ($\mu$) and compensation ($\tau$) rise. At
    $\mu=\tau=1$ the two coincide exactly -- the paper's Key Result (§5.3, "the wedge
    closes"), here reached continuously instead of in one jump between panels.

    **The global-games locus is drawn only where it exists.** `ln_gg` is $\tau$-extended but
    $\mu=0$ only; `ln_gg_mu` is $\mu$-extended but $\tau=0$ only. A combined $(\mu,\tau)$
    risk-dominance threshold is derived nowhere in the appendix or this codebase, so when
    both are non-zero this panel omits the dashed selection curve and says so on the axis
    rather than interpolating something underived. Do not "fix" that by drawing either
    one-sided locus in the interior; they are not the same object.

    **The blue second-best loci move with $\mu$ and not with $\tau$.** The constrained
    planner respects the decentralized labor allocation, which governance shifts; but
    compensation is a transfer and cancels out of any output objective. Two of the three
    move: eq. (19) and eq. (20) generalize, while eq. (18) is $\mu$-invariant because it
    compares $t_e=0$ with $t_e=1$ and governance bites only in between. `second_best=False`
    drops them.
    """
    # Matches the other single-panel figures, which is what the site's default body column
    # fits. `figsize` is exposed for anyone rendering this somewhere wider; ignored when
    # `ax` is supplied.
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    th_H = model.theta_H(ALP, mu)          # theta_H^mu, eq. (24)

    the_1 = np.arange(1.1, 2.1, 0.005)     # planner band domain, as in combined_4x4
    the_d = np.arange(0.8, 2.1, 0.005)     # decentralized loci extend below theta=1

    # ---- planner band (black): independent of mu and tau, the fixed reference ----
    l01, l11 = loci.ln_l01(the_1), loci.ln_l11(the_1)
    ax.plot(the_1, l01, color=COLOR_PLANNER_BLACK)
    ax.plot(the_1, l11, color=COLOR_PLANNER_BLACK)
    fill_between_sorted(ax, the_1, l01, l11, np.ones_like(the_1, bool),
                        alpha=REGION_ALPHA, color="C0")

    # ---- decentralized band (red): the part that moves ----
    l0d = loci.ln_ld0(the_d, tau=tau, mu=mu)
    l1d = loci.ln_ld1(the_d, tau=tau, mu=mu)
    ax.plot(the_d, l0d, color=COLOR_DECENTRALIZED)
    ax.plot(the_d, l1d, color=COLOR_DECENTRALIZED)
    # The two loci swap order at theta_H^mu, so the fill is split there -- otherwise
    # fill_between draws the bowtie across the crossing.
    fill_between_sorted(ax, the_d, l0d, l1d, the_d > th_H, alpha=REGION_ALPHA, color="C3")
    fill_between_sorted(ax, the_d, l1d, l0d, the_d < th_H, alpha=REGION_ALPHA, color="C3")

    # ---- global-games selection locus, drawn on its actual domain ----
    # Appendix (27a) gives the joint (mu, tau) form, so this is no longer restricted to the
    # two edges. It lives on theta_tau < theta < theta_H^mu, squeezed from the left by
    # compensation and from the right by governance, and the two edges mean different
    # things. At theta_H^mu the multiplicity region itself ends. theta_tau is not a
    # property of the selection problem at all: the factor (theta*Lam^alpha - tau) sits in
    # ln_ld0 and ln_ld1 too, so all three decentralized loci vanish together below it.
    # There, enclosure earns less than the compensation it owes, at any density -- both
    # rents scale with lbar^alpha, so density cancels out of the sign.
    # `ln_gg` returns +inf outside the interval, which matplotlib skips.
    th_tau = loci.theta_tau(ALP, mu, tau)
    if th_tau < th_H:
        the_gg = np.arange(max(0.8, th_tau), th_H, 0.002)
        ax.plot(the_gg, loci.ln_gg(the_gg, tau=tau, mu=mu), color=COLOR_DECENTRALIZED,
                linestyle=LINESTYLE_SELECTION, linewidth=2)
        # Mark the left edge only when compensation is what creates it, i.e. when it sits
        # inside the plotted range rather than at theta_tau = 0.
        if tau > 0 and th_tau > _WEDGE_XLIM[0]:
            ax.axvline(th_tau, color=COLOR_DECENTRALIZED, linestyle=":", linewidth=1,
                       alpha=0.7)
            # Not "no raid pays": the paper reserves *raid* for the uncompensated tau=0
            # taking, and at tau>0 every enclosure above theta_tau is a partly-compensated
            # one. What fails below theta_tau is profitability, not the transfer.
            gg_note = (rf"$\theta_\tau={th_tau:.2f}$: below this, enclosure earns" "\n"
                       "less than the compensation it owes, at any density")
        else:
            gg_note = None
    else:
        # theta_tau has overtaken theta_H^mu -- the interval is empty and the coordination
        # problem is gone entirely. Happens only at mu = tau = 1, where both are 1.
        gg_note = ("no multiplicity region:\n"
                   r"$\theta_\tau \geq \theta_H^\mu$")

    # ---- second-best loci (blue, dashed): move with mu, but not with tau ----
    # The constrained planner respects the *decentralized* labor allocation, which is
    # governed by mu -- so these are not static context, they shift as governance improves.
    # tau is absent by derivation, not by oversight: it is a transfer, so it nets out of the
    # planner's output margin. See the `ln_ls0_mu` / `ln_ls1_mu` docstrings.
    #
    # The regime split is at theta_H^mu, not the fixed 1/alpha -- the boundary between the
    # convex and concave branches of z_0 moves with mu along with the loci themselves.
    if second_best:
        # The eq.(19)/(20) arguments go negative on the wrong side of theta_H^mu; masked
        # immediately after, so the NaNs there are expected rather than a bug.
        with np.errstate(invalid="ignore"):
            ls = np.where(the_1 < th_H, loci.ln_ls(the_1), np.nan)
            ls0 = np.where(the_1 > th_H, loci.ln_ls0_mu(the_1, mu=mu), np.nan)
            ls1 = np.where(the_1 > th_H, loci.ln_ls1_mu(the_1, mu=mu), np.nan)
        for curve in (ls, ls0, ls1):
            ax.plot(the_1, curve, linestyle=LINESTYLE_SELECTION,
                    color=COLOR_PLANNER_BLUE, linewidth=2)

    ax.axvline(1, ymax=0.95, linestyle=LINESTYLE_THRESHOLD, color="black")
    ax.axvline(th_H, ymax=0.95, linestyle=LINESTYLE_THRESHOLD, color="black")

    ax.set_xlim(*_WEDGE_XLIM)
    ax.set_ylim(*_WEDGE_YLIM)
    ax.set_title(rf"$\mu={mu:.2f}$,  $\tau={tau:.2f}$"
                 rf"    ($\theta_H^\mu={th_H:.2f}$)", fontsize=15)
    common_labels(ax, fontsize=12)
    style_axes(ax)

    if gg_note is not None:
        ax.annotate(gg_note, xy=(0.03, 0.03), xycoords="axes fraction", fontsize=9,
                    style="italic", color="grey", va="bottom")

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
    # "no raid" would be exactly backwards here: tau=1 is *full* compensation, so nothing
    # is being taken. Enclosure simply does not cover what it must pay.
    ax.text(1.245, 3.82, r"$\to\infty$: enclosure never covers $\tau$" "\n" r"for $\theta<\alpha^{-\alpha}$ when $\tau=1$",
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


# ---------------------------------------------------------------------------
# Explanatory figures for the online appendix -- not in the paper's set of 8.
# These fill placeholders the appendix already numbers but never had generators for.
# Ported from enclosure_book/notebooks/enclose.py (plotle, plotmpts).
# ---------------------------------------------------------------------------

def labor_reaction(te=0.5, th=1.0, alp=0.5, mu=0.5, ax=None):
    r"""Appendix Figure 5: the labor reaction function $l_e(t_e)$ under varying $\mu$.

    The single most useful explanatory graph for the extended model: it shows what
    $\Lambda_\mu$ actually *does*. The 45-degree line is $l_e = t_e$ (labor and land
    enclosed in equal proportion); a curve above it means the enclosed sector is
    labor-intensive relative to the economy, below it means labor-extensive.

    Three curves are drawn — open access ($\mu=0$), planner ($\mu=1$), and the chosen
    intermediate $\mu$ — with the allocation at the given `te` marked on each, so the
    governance wedge is visible as the vertical gap.

    Source: `plotle` in the old enclose.py, restructured to accept `ax` for composition.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6))
    else:
        fig = ax.figure

    tte = np.linspace(0, 1, 200)
    leq = model.le(te, th, alp, mu=0)      # open access
    leop = model.le(te, th, alp, mu=1)     # planner
    lemu = model.le(te, th, alp, mu)       # chosen mu

    ax.plot(tte, model.le(tte, th, alp, mu=0), linewidth=2, color="b")
    ax.plot(tte, model.le(tte, th, alp, mu=1), linewidth=2, color="r")
    ax.plot(tte, model.le(tte, th, alp, mu), linewidth=2, color="g")
    ax.plot([0, 1], [0, 1], linestyle=":", color="grey")

    ax.scatter(te, leop, color="r", zorder=5, label=r"Planner, $\mu=1$")
    ax.scatter(te, leq, color="b", zorder=5, label=r"Open access, $\mu=0$")
    ax.scatter(te, lemu, color="g", zorder=5,
               label=r"Regulated commons, $\mu$" + f"={mu}")

    for y in (leq, leop):
        ax.plot([0, te], [y, y], linestyle=":", color="grey", linewidth=1)
    ax.plot([te, te], [0, max(leq, leop)], linestyle=":", color="grey", linewidth=1)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal", "box")
    ax.set_title(r"Labor reaction $l_e(t_e)$"
                 + f"   ($\\theta$={th}, $\\alpha$={alp})", fontsize=12)
    ax.set_xlabel(r"$t_e$", fontsize=15)
    ax.set_ylabel(r"$l_e$", fontsize=15)
    ax.legend(loc="upper left", fontsize=9)
    return fig, ax


def labor_misallocation(te=0.5, alp=0.5, th=1.0, lbar=1.0, mu=0.0, ax=None):
    r"""Appendix Figure 4: MPL/APL and the labor misallocation wedge.

    Labor on the commons enters until the *average* product equals the wage, not the
    marginal product, so $MP_L^c$ sits below $MP_L^e$ and the hatched area between them is
    the efficiency loss. Points A, C, E mark the open-access allocation, the commons wage,
    and the efficient allocation.

    Source: `plotmpts` in the old enclose.py, which carried
    `TODO: not yet working for mu different from 0` — that caveat still stands and is
    carried over rather than quietly dropped. `mu` shifts the decentralized allocation
    `leam`, but the commons curves (`aplu`/`mplu`) take no `mu` argument, so the wage and
    intersection geometry are only right at `mu=0`. Left as the default; a correct
    `mu > 0` version is derivation work, not a port.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    else:
        fig = ax.figure

    ll = np.linspace(0.0001, 0.9999, 400)
    leop = model.leo(te, th, alp)          # efficient
    leam = model.le(te, th, alp, mu)       # decentralized
    we = model.weq(te, th, alp, lbar)
    wo = model.mple(te, leop, alp, th, lbar)
    wc = model.mplu(1 - te, 1 - leam, alp, 1, lbar)

    ax.plot(ll, model.mple(te, ll, alp, th, lbar), linewidth=2, color="k")
    ax.plot(ll, model.aplu(1 - te, 1 - ll, alp, 1, lbar), linewidth=2, color="k")
    ax.plot(ll, model.mplu(1 - te, 1 - ll, alp, 1, lbar), linewidth=2, color="k")

    ax.fill_between(ll, model.mple(te, ll, alp, th, lbar),
                    model.mplu(1 - te, 1 - ll, alp, 1, lbar),
                    where=(ll >= leam) & (ll <= leop),
                    hatch="//", color="none", edgecolor="k")

    ax.vlines(x=leam, ymin=0, ymax=we, linestyle=":")
    ax.vlines(x=leop, ymin=0, ymax=wo, linestyle=":")
    ax.axhline(we, linestyle=":")
    ax.axhline(wc, linestyle=":")

    ax.set_ylim(0, 1.5)
    ax.set_xlim(0, 1)
    ax.spines["top"].set_visible(False)
    ax.annotate(r"$MP_L^c$", xy=(0.85, model.mplu(1 - te, 0.15, alp, 1, lbar)),
                textcoords="offset points", xytext=(-30, 20), fontsize=14)
    ax.annotate(r"$AP_L^c$", xy=(0.65, model.aplu(1 - te, 0.35, alp, 1, lbar)),
                textcoords="offset points", xytext=(-24, 15), fontsize=14)
    ax.annotate(r"$MP_L^e$", xy=(0.8, model.mple(te, 0.8, alp, th, lbar)),
                textcoords="offset points", xytext=(20, -20), fontsize=14)

    ax.set_xticks([0, leam, leop, 1],
                  ["0", r"$l_e^*(t_e)$", r"$l_e^o(t_e)$", "1"], fontsize=13)

    for x, y, lab in zip([leam, leam, leop], [wc, we, wo], ["A", "  C", "  E"]):
        ax.scatter(x, y, marker="o", s=30, c="k", clip_on=False, zorder=5)
        ax.annotate(lab, (x, y), textcoords="offset points", xytext=(-5, 7),
                    ha="center", fontsize=12)
    return fig, ax


# ---------------------------------------------------------------------------
# Manufacturing / structural transformation (content/03-manufacturing.md)
# ---------------------------------------------------------------------------

def manufacturing_equilibrium(te_values=(0.0, 1.0), th=1.0, alp=0.4, b=0.7,
                              tbar=1.0, kb=1.0, p=1.0):
    r"""Labor market equilibrium with a manufacturing sector, before and after enclosure.

    One panel per value of `te`. In each, $MPL_m$ falls in $l_m$ while $MPL_a$ rises, so
    they cross exactly once — that single crossing is what makes the equilibrium unique and
    the bracketed solve safe.

    Both the open-access ($\mu=0$) and planner ($\mu=1$) agricultural curves are drawn, each
    with its *own* equilibrium marked. The source notebook's `pl()` drew one agricultural
    curve at the chosen $\mu$ but marked the $\mu=0$ and $\mu=1$ equilibria on it, so at
    intermediate $\mu$ the marked points did not lie on the drawn curve; drawing both curves
    is the reading that makes the private-vs-planner comparison consistent.
    """
    from . import manufacturing as mfg

    n = len(te_values)
    fig, axes = plt.subplots(1, n, figsize=(6 * n, 5), squeeze=False)
    lm = np.linspace(0.005, 0.995, 400)

    for ax, te in zip(axes[0], te_values):
        ax.plot(lm, mfg.mpl_m(lm, p, kb, b), color="k", linewidth=2, label=r"$MPL_m$")
        # At te=0 the two agricultural curves stand in the ratio alpha (open access pays
        # the average product, the planner the marginal product); at te=1 there is no
        # commons and they coincide exactly, so mu=1 is dashed to keep it visible there.
        for mu, colour, dash, name in (
            (0.0, COLOR_DECENTRALIZED, "-", r"$w_a$, open access $\mu=0$"),
            (1.0, COLOR_PLANNER_BLUE, (0, (6, 4)), r"$w_a$, planner $\mu=1$"),
        ):
            ax.plot(lm, mfg.mpl_a(lm, te, tbar, alp, th, mu), color=colour,
                    linewidth=2, linestyle=dash, label=name)
            star = mfg.labor_share(te, b=b, alp=alp, th=th, tbar=tbar, kb=kb, p=p, mu=mu)
            w = mfg.mpl_m(star, p, kb, b)
            ax.scatter(star, w, color=colour, zorder=6, s=45)
            ax.vlines(star, 0, w, color=colour, linestyle=":", linewidth=1)
            # Label beside the marker rather than on the axis, where the two values would
            # collide with each other and with the tick labels when the equilibria are close.
            ax.annotate(rf"$l_m={star:.2f}$", (star, w), textcoords="offset points",
                        xytext=(10, 8), ha="left", fontsize=10, color=colour)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 2)
        ax.set_xlabel(r"$l_m$  (labor share in manufacturing)", fontsize=12)
        ax.set_ylabel(r"wage / $MPL$", fontsize=12)
        ax.set_title(rf"$t_e={te:g}$", fontsize=13)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(fontsize=9, loc="upper right", framealpha=0.95)

    fig.tight_layout()
    return fig, axes[0]


def structural_transformation(alp=0.5, mu=0.0, b=0.5, tbar=1.0, kb=1.0, p=1.0):
    r"""How enclosure shifts labor into or out of manufacturing — and where it reverses.

    $MPL_a$ carries $\left(1+(\Lambda_\mu-1)t_e\right)^{1-\alpha}$, so the sign of
    $\partial l_m/\partial t_e$ is the sign of $(1-\Lambda_\mu)$ (the equilibrium condition
    inverts it: $l_m$ rises when the agricultural constant falls) — and $\Lambda_\mu=1$
    exactly at $\theta_H^\mu$. Below that threshold enclosure releases labor to
    manufacturing; above it, labor is pulled back into agriculture; at it, enclosure moves
    no labor at all.
    """
    from . import manufacturing as mfg

    th_H = model.theta_H(alp, mu)
    thetas = [th_H - 0.8, th_H - 0.2, th_H, th_H + 0.5, th_H + 1.5]
    te = np.linspace(0, 1, 60)

    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    cmap = plt.get_cmap("coolwarm")
    for i, th in enumerate(thetas):
        shares = [mfg.labor_share(t, b=b, alp=alp, th=th, tbar=tbar, kb=kb, p=p, mu=mu)
                  for t in te]
        at_threshold = np.isclose(th, th_H)
        ax.plot(te, shares,
                color="k" if at_threshold else cmap(i / (len(thetas) - 1)),
                linewidth=3 if at_threshold else 2,
                linestyle="--" if at_threshold else "-",
                label=rf"$\theta={th:.1f}$" + (r"  $=\theta_H$" if at_threshold else ""))

    ax.set_xlim(0, 1)
    ax.set_xlabel(r"$t_e$  (share of land enclosed)", fontsize=12)
    ax.set_ylabel(r"$l_m$  (labor share in manufacturing)", fontsize=12)
    ax.set_title(r"Enclosure and structural transformation: the effect reverses at "
                 rf"$\theta_H={th_H:g}$", fontsize=12)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(fontsize=10, loc="best")
    # Annotation colours match the curves they describe: the coolwarm map puts the low-theta
    # (rising) curves at the blue end and the high-theta (falling) ones at the red end.
    ax.annotate(r"$\theta<\theta_H$: enclosure releases" "\n" "labor to manufacturing",
                xy=(0.70, 0.90), xycoords="axes fraction", ha="center", fontsize=10,
                style="italic", color="darkblue")
    ax.annotate(r"$\theta>\theta_H$: enclosure pulls" "\n" "labor back to agriculture",
                xy=(0.70, 0.12), xycoords="axes fraction", ha="center", fontsize=10,
                style="italic", color="darkred")
    fig.tight_layout()
    return fig, ax
