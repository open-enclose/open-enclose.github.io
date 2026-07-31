r"""Named, equation-tagged boundary loci in (theta, ln l_bar) space.

Every locus below has the form $\ln\bar l = \frac{1}{\alpha}\ln[\text{expr}(\theta)]$,
so a single theta grid carries every curve if `expr` is masked through
`enclose.numerics.safe_log_power` rather than hand-sliced per branch.

These were previously duplicated by hand, with independent drift, across `enclose.py`'s
`allpart`/`threeplots` and six cells of `Model_Construction.ipynb` (26, 36, 45, 47, 65, 91).
This module consolidates them, cross-checked in `sanity_checks()` and in
`tests/test_loci.py` against `enclose.model`'s decentralized-equilibrium functions and
against `enclosure_book/notebooks/generate_trajectories_figure.py`, the one place this math
was already done carefully.

Equation numbers refer to `enclosure_book/docs/online_appendix.md`. `ALP`/`C` are the
paper's benchmark calibration (also `generate_trajectories_figure.py`'s hardcoded values),
used here as defaults so every function reproduces the paper's figures when called with no
keyword arguments, while remaining fully parameterized for other calibrations.
"""

import numpy as np

from . import model
from .numerics import safe_log_power

ALP = 2 / 3                  # paper's benchmark alpha
# C is the paper's c/A, not c: A never appears alone in any locus, because every threshold
# solves "marginal benefit = marginal cost" and the A in the benefit cancels against the c
# in the cost. Hence the paper's own "drawn for c/A = 1". See the package README note on
# what this means if the model is ever extended to output or welfare *levels*.
C = 1.0
CV = model.theta_H(ALP)      # theta_H at mu=0 = 1/alpha, eq. (24)
# Asymptote of the tau=1, mu=0 global-games locus. Kept as a constant because
# figures.trajectories draws exactly that curve; the general boundary is `theta_tau()`.
THETA_TAU = ALP**(-ALP)


def lam_mu(th, alp=ALP, mu=0.0):
    r"""$\Lambda_\mu$, eq. (23) — a defaults-carrying wrapper over `enclose.model.Lambda`,
    which holds the one definition. At $\mu=1$ this is $\Lambda_o = \theta^{1/(1-\alpha)}$.
    """
    return model.Lambda(th, alp, mu)


def lam0(th, alp=ALP):
    r"""$\Lambda$ at $\mu=0$: $(\alpha\theta)^{1/(1-\alpha)}$."""
    return lam_mu(th, alp, mu=0.0)


# ---------------------------------------------------------------------------
# First-best (planner) loci
# ---------------------------------------------------------------------------

def ln_l01(th, alp=ALP, c=C):
    """First-best no-enclosure locus, eq. (6)."""
    lam_o = th**(1 / (1 - alp))
    return (1 / alp) * np.log(c / ((lam_o - 1) * (1 - alp)))


def ln_l11(th, alp=ALP, c=C):
    r"""First-best full-enclosure locus, eq. (7): $\bar l_1^1 = \Lambda_o \cdot \bar l_0^1$."""
    return ln_l01(th, alp, c) + (1 / (1 - alp)) * np.log(th)


# ---------------------------------------------------------------------------
# Decentralized loci, jointly extended by governance (mu) and compensation (tau)
#
# Both take the general form of eq. (27)'s enclosure condition
#   r_mu^e(t_e) - tau * r_mu^c(t_e) - c >= 0
# solved at the two boundaries t_e = 0 and t_e = 1, with Lambda_mu (eq. 23) in place of
# Lambda. Valid above theta_H^mu = 1/alpha - mu(1-alpha)/alpha (eq. 24); below that the
# strategic-complements branch applies instead (`ln_gg`, mu=0 only -- see its docstring).
# ---------------------------------------------------------------------------

def ln_ld0(th, alp=ALP, c=C, tau=0.0, mu=0.0):
    r"""Decentralized r(0)=c locus, eq. (14), extended by $\mu$ and $\tau$ (eqs. 23, 26-27).

    $$\bar l_0 = \left[\frac{c}{(1-\alpha)(\theta\Lambda_\mu^\alpha - \tau)}\right]^{1/\alpha}$$

    Reduces to the separately-derived special cases already in the codebase: to
    `generate_trajectories_figure.py`'s `ln_ld0` and `Model_Construction.ipynb` cell 91's
    `expr_pd0nu` at $\mu=0$, and to cell 91's `expr_pd0mu` at $\tau=0$ — see
    `tests/test_loci.py`.
    """
    lam = lam_mu(th, alp, mu)
    expr = c / ((1 - alp) * (th * lam**alp - tau))
    return safe_log_power(expr, power=1 / alp)


def ln_ld1(th, alp=ALP, c=C, tau=0.0, mu=0.0):
    r"""Decentralized r(1)=c locus, eq. (15), extended by $\mu$ and $\tau$.

    $$\bar l_1 = \left[\frac{c\,\Lambda_\mu^\alpha}{(1-\alpha)(\theta\Lambda_\mu^\alpha - \tau)}\right]^{1/\alpha}$$
    """
    lam = lam_mu(th, alp, mu)
    expr = c * lam**alp / ((1 - alp) * (th * lam**alp - tau))
    return safe_log_power(expr, power=1 / alp)


def theta_tau(alp=ALP, mu=0.0, tau=0.0):
    r"""Lower edge of the global-games domain, appendix eq. (27a).

    $$\theta_\tau(\mu,\tau) = \tau^{1-\alpha}\left(\frac{A_\mu}{\alpha}\right)^{\alpha},
      \qquad A_\mu = 1-\mu(1-\alpha)$$

    Below this, $\theta\Lambda_\mu^\alpha < \tau$ and the expected return to a raid is
    negative **at every density** — both rents scale with $\bar l^\alpha$, so density
    cancels out of the sign and cannot rescue it. The threshold does not move out of view;
    it ceases to exist. Contrast the enclosure cost $c$, a level charge that density always
    eventually outruns, which is why every other locus is finite everywhere.

    At $\mu=0,\tau=1$ this is $\alpha^{-\alpha}$. At $\tau=0$ it is $0$ — no restriction.
    """
    A_mu = 1 - mu * (1 - alp)
    return tau**(1 - alp) * (A_mu / alp)**alp


def ln_gg(th, alp=ALP, c=C, tau=0.0, mu=0.0):
    r"""Global-games risk-dominance locus, appendix eq. (15) and its $(\mu,\tau)$
    extension (27a): $E[r_\mu^e - \tau r_\mu^c - c] = 0$ over $t_e \in [0,1]$.

    $$\bar l_{gg}^d(\mu,\tau) = \left[\frac{c\,(\Lambda_\mu-1)}
      {(\theta\Lambda_\mu^{\alpha}-\tau)(\Lambda_\mu^{1-\alpha}-1)}\right]^{1/\alpha}$$

    Defined on the interval $\theta_\tau(\mu,\tau) < \theta < \theta_H^\mu$ — squeezed from
    the left by compensation and from the right by governance — and $+\infty$ outside it.
    The two edges mean different things: at $\theta_H^\mu$ the multiplicity region itself
    ends, while below $\theta_\tau$ no density makes a raid pay (see `theta_tau`).

    The governance wedge $A_\mu$ does not appear separately: with
    $\Lambda_\mu^{1-\alpha} = \alpha\theta/A_\mu$ it enters numerator and denominator alike
    and cancels, so $\mu$ acts only through $\Lambda_\mu$. That is specific to this locus —
    in the labor-market conditions of appendix §5.1, $A_\mu$ sets the *level* of what labor
    takes home and does not cancel.
    """
    th = np.asarray(th, dtype=float)
    lam = lam_mu(th, alp, mu)
    margin = th * lam**alp - tau
    out = np.full_like(th, np.inf)
    ok = (margin > 0) & (th < model.theta_H(alp, mu))
    with np.errstate(divide="ignore", invalid="ignore"):
        out[ok] = (1 / alp) * np.log(
            c * (lam[ok] - 1) / (margin[ok] * (lam[ok]**(1 - alp) - 1))
        )
    return out


# ---------------------------------------------------------------------------
# Second-best loci
# ---------------------------------------------------------------------------

def ln_ls(th, alp=ALP, c=C):
    r"""Second-best full-vs-none locus (low-TFP side), eq. (18).

    **Invariant to $\mu$, and that is a result rather than an omission.** The comparison is
    $z_0^\mu(1) - c \ge z_0^\mu(0)$, and both endpoints are free of $\Lambda_\mu$:
    $z_0^\mu(0) = \bar l^\alpha$ (no land enclosed, so the commons carries everything and
    the allocation problem is trivial) and $z_0^\mu(1) = \bar l^\alpha\theta$ (all land
    enclosed, so there is no commons left for governance to act on). Governance only bites
    at interior $t_e$, and this locus compares the two corners. Hence no `mu` argument.
    """
    return (1 / alp) * np.log(c / (th - 1))


def ln_lc0(th, alp=ALP, c=C):
    """Second-best no-enclosure locus (high-TFP side), eq. (19). Fixed at mu=0 --
    `ln_ls0_mu` is the governance-extended form and reduces to this at mu=0."""
    lam = lam0(th, alp)
    return (1 / alp) * np.log(alp * c / ((lam * (1 + alp) - alp) * (1 - alp)))


# ---------------------------------------------------------------------------
# Second-best loci, extended by governance (mu)
#
# The constrained planner "respects the labor allocation that emerges from decentralized
# labor markets but can control t_e" (appendix 4.1). Under governance mu that allocation is
# l_e^mu, so Lambda -> Lambda_mu throughout the objective, which becomes
#
#     z_0^mu(t_e) = lbar^alpha * [theta*Lambda_mu^alpha*t_e + (1-t_e)]
#                              / (1 + (Lambda_mu - 1)*t_e)^alpha
#
# reducing to eq. (17) at mu=0 via the identity theta*Lambda^alpha = Lambda/alpha (eq. 12).
#
# **tau does not appear and must not be added.** Compensation is a transfer from encloser
# to commoners; it nets out of total output, so it cannot shift a locus derived from the
# planner's output margin. It moves the *private* loci (`ln_ld0`, `ln_ld1`) only. The
# paper's own Figure 6 says the same thing: panel (c) is mu=0, tau=1 and draws exactly the
# second-best curves of panel (a), tau=0.
# ---------------------------------------------------------------------------

def ln_ls0_mu(th, alp=ALP, c=C, mu=0.0):
    r"""Second-best no-enclosure locus, eq. (19) extended by $\mu$.

    From $z_0^{\mu\prime}(0) \ge c$ with $u = 1 + (\theta\Lambda_\mu^\alpha - 1)t_e$ and
    $v = (1+(\Lambda_\mu-1)t_e)^\alpha$, both evaluated at $t_e = 0$:

    $$z_0^{\mu\prime}(0) = \bar l^\alpha\left[\theta\Lambda_\mu^\alpha - 1
                                              - \alpha(\Lambda_\mu - 1)\right]$$

    $$\bar l_0^{s,\mu} = \left[\frac{c}{\theta\Lambda_\mu^\alpha - 1
                                        - \alpha(\Lambda_\mu-1)}\right]^{1/\alpha}$$

    At $\mu=0$, $\theta\Lambda^\alpha = \Lambda/\alpha$ turns the denominator into
    $(1-\alpha)(\Lambda(1+\alpha)-\alpha)/\alpha$, i.e. exactly `ln_lc0` — asserted in
    `tests/test_loci.py` rather than left to inspection.
    """
    lam = lam_mu(th, alp, mu)
    expr = c / (th * lam**alp - 1 - alp * (lam - 1))
    return safe_log_power(expr, power=1 / alp)


def ln_ls1_mu(th, alp=ALP, c=C, mu=0.0):
    r"""Second-best full-enclosure locus, eq. (20) extended by $\mu$.

    From $z_0^{\mu\prime}(1) \ge c$. Using $A_\mu\Lambda_\mu^{1-\alpha} = \alpha\theta$ and
    $1 - A_\mu = \mu(1-\alpha)$, the derivative at $t_e=1$ collapses to

    $$z_0^{\mu\prime}(1) = \bar l^\alpha (1-\alpha)
                           \left[\theta - \mu\Lambda_\mu^{-\alpha}\right]$$

    $$\bar l_1^{s,\mu} = \left[\frac{c}{(1-\alpha)
                                \left(\theta - \mu\Lambda_\mu^{-\alpha}\right)}\right]^{1/\alpha}$$

    **This breaks a coincidence the appendix records.** Appendix eq. (20) notes that the
    second-best and private full-enclosure thresholds are equal — $\bar l_1^s = \bar l_1^d$
    of eq. (14). That holds at $\mu = 0$, where this reduces to
    $[c/((1-\alpha)\theta)]^{1/\alpha}$. It does **not** survive $\mu > 0$: `ln_ld1` at
    $\tau=0$ is invariant to $\mu$ (its $\Lambda_\mu^\alpha$ cancels top and bottom), while
    this locus is not. So the two curves separate as governance improves.

    Both scopes are load-bearing. The coincidence is a $\tau=0$ statement — with $\tau>0$ the
    private locus moves for an unrelated reason, and lands *above* this one. And it is a
    $\theta > \theta_H^\mu$ statement: below that, $z_0$ is convex, so the optimum is a corner
    rather than a tangency and eq. (18)'s full-versus-none comparison governs instead — this
    locus does not apply there and `enclose.figures.wedge_panel` masks it out. That separation is
    derived here and is **not** in the appendix — treat it as a claim to check, not as
    settled, before it goes anywhere near the manuscript. Written up, with the intuition and
    the policy reading, in `enclosure_paper/REVISION_IDEAS.md` section 1 (private repo,
    deliberately: this has not been reviewed by the co-author).
    """
    lam = lam_mu(th, alp, mu)
    expr = c / ((1 - alp) * (th - mu * lam**(-alp)))
    return safe_log_power(expr, power=1 / alp)


# ---------------------------------------------------------------------------
# mu-only convenience wrappers (partial commons governance, eq. 23/24)
#
# These now delegate to the jointly-extended ln_ld0/ln_ld1 above rather than carrying
# their own copy of the algebra; kept as named entry points because the mu-only case is
# what panel (b) of the 2x2 figure plots. Cross-checked against Model_Construction.ipynb
# cell 91's independently-derived forms in tests/test_loci.py.
# ---------------------------------------------------------------------------

def ln_ld0_mu(th, alp=ALP, c=C, mu=0.0):
    """Decentralized r(0)=c locus under partial commons governance mu."""
    return ln_ld0(th, alp, c, tau=0.0, mu=mu)


def ln_ld1_mu(th, alp=ALP, c=C, mu=0.0):
    r"""Decentralized r(1)=c locus under governance mu — invariant to mu.

    The invariance is not asserted by hand here; it falls out of the algebra. At $\tau=0$
    the general form's $\Lambda_\mu^\alpha$ cancels top and bottom, leaving
    $\bar l_1 = [c/((1-\alpha)\theta)]^{1/\alpha}$ with no $\mu$ in it — which is why
    `Model_Construction.ipynb` cell 91 could legitimately write `ln_l1dmu = ln_l1d.copy()`.
    """
    return ln_ld1(th, alp, c, tau=0.0, mu=mu)


def ln_gg_mu(th, alp=ALP, c=C, mu=0.0):
    """Global-games locus under governance mu alone — a named entry point for the tau=0
    edge, delegating to the joint form rather than carrying its own algebra."""
    return ln_gg(th, alp, c, tau=0.0, mu=mu)


# ---------------------------------------------------------------------------
# Monopoly loci (cell 45)
# ---------------------------------------------------------------------------

def ln_lm0(th, alp=ALP, c=C):
    """Monopolist's locus, low-TFP side."""
    return (1 / alp) * np.log(c / ((1 - alp) * th))


def ln_lm1(th, alp=ALP, c=C):
    """Monopolist's locus, high-TFP side. (The monopolist's *other* high-TFP locus
    coincides with `ln_ld0` up to the visual-separation shift — see `enclose.figures`.)"""
    lam = lam0(th, alp)
    expr = c * alp * lam**alp / ((1 - alp) * (lam * (1 - alp) + alp))
    return safe_log_power(expr, power=1 / alp)


def sanity_checks():
    """Assertions mirroring `generate_trajectories_figure.py`'s own checks, extended to the
    consolidated mu/tau loci. Raises AssertionError on failure; prints on success."""
    th = np.linspace(THETA_TAU + 1e-3, CV - 1e-3, 400)
    g0, g1 = ln_gg(th, tau=0.0), ln_gg(th, tau=1.0)
    assert np.all(g1 > g0), "tau=1 gg locus must lie above tau=0 locus"
    print(f"OK: gg(tau=1) > gg(tau=0) on ({th[0]:.3f}, {th[-1]:.3f}); "
          f"min gap {np.min(g1 - g0):.3f} (ln units)")

    th2 = np.linspace(0.85, CV - 1e-6, 300)
    assert np.allclose(ln_ld0_mu(th2, mu=0.0), ln_ld0(th2)), "ld0_mu(mu=0) must match ld0"
    assert np.allclose(ln_gg_mu(th2, mu=0.0), ln_gg(th2)), "gg_mu(mu=0) must match gg"
    print("OK: mu-extended loci reduce to the mu=0 loci at mu=0")

    th3 = np.linspace(1.02, CV - 1e-6, 300)
    for tau in (0.0, 0.3, 0.6):
        lam = lam0(th3)
        nu_expr0 = C / (1 - ALP) * (1 / (th3 * lam**ALP - tau))
        nu_ld0 = safe_log_power(nu_expr0, power=1 / ALP)
        # equal_nan=True: both sides correctly mask the theta where the denominator
        # crosses zero (the tau-dependent singularity); that's agreement, not a mismatch.
        assert np.allclose(ln_ld0(th3, tau=tau), nu_ld0, equal_nan=True), f"ld0(tau={tau}) mismatch"
    print("OK: ln_ld0's tau parameterization matches the independent nu-derivation at tau=0,0.3,0.6")

    ws_gg = ln_gg(np.array([1.0]))[0]
    assert 0.9 < ws_gg, "Weitzman-Samuelson point must lie below lbar_gg^d"
    print("OK: annotation reference points verified against their loci")

    # The paper's Key Result (online_appendix.md 5.3): the decentralized-vs-planner wedge
    # closes when mu=1 AND tau=1. At mu=1, Lambda_mu = theta^(1/(1-alpha)) = Lambda_o, and
    # the identity theta*Lambda_o^alpha = Lambda_o collapses the decentralized denominator
    # to the planner's -- so the two loci don't merely converge, they coincide exactly.
    th4 = np.linspace(1.1, 2.1, 300)
    assert np.allclose(ln_ld0(th4, tau=1.0, mu=1.0), ln_l01(th4)), \
        "at mu=tau=1 the decentralized r(0)=c locus must equal the planner's"
    assert np.allclose(ln_ld1(th4, tau=1.0, mu=1.0), ln_l11(th4)), \
        "at mu=tau=1 the decentralized r(1)=c locus must equal the planner's"
    print("OK: mu=1, tau=1 decentralized loci coincide exactly with the planner's "
          "(the wedge closes -- online_appendix.md 5.3)")


if __name__ == "__main__":
    sanity_checks()
