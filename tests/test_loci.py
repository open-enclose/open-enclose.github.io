"""Tests for enclose.loci.

Two kinds of check:
1. loci.py vs enclose.model agreement -- each locus is *defined* as the lbar where some
   model.py equilibrium condition holds (e.g. ln_ld0(th) is where req(0,...)=c); verifying
   that directly is a genuine cross-check between the two independently-written layers.
2. Ported/extended versions of generate_trajectories_figure.py's own sanity_checks(),
   plus fresh (not loci-internal) re-derivations of the mu/tau unification established
   during the Phase 1 migration -- see loci.py's module docstring.
"""
import inspect
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from enclose import loci, model  # noqa: E402

ALP, C, CV = loci.ALP, loci.C, loci.CV
TH = np.array([1.2, 1.4, 1.6, 1.8])


# ---------------------------------------------------------------------------
# Second-best loci extended by governance (mu)
#
# These were derived for the interactive wedge panel and are not in the appendix, so they
# are checked two ways: against the existing mu=0 forms, and against a fresh numerical
# differentiation of the second-best objective rather than against the algebra that
# produced them.
# ---------------------------------------------------------------------------

def _z0_mu(te, th, alp, mu, lbar=1.0):
    """Second-best objective under governance mu, built straight from its definition:
    output at the *decentralized* labor allocation l_e^mu. Deliberately not a rearranged
    closed form -- the point is to check the closed forms against something independent."""
    le = model.le(te, th, alp, mu)
    return (th * te**(1 - alp) * le**alp
            + (1 - te)**(1 - alp) * (1 - le)**alp) * lbar**alp


@pytest.mark.parametrize("mu", [0.0, 0.25, 0.5, 0.75, 1.0])
def test_second_best_loci_solve_the_numerically_differentiated_objective(mu):
    """ln_ls0_mu and ln_ls1_mu are where dz_0^mu/dt_e equals c at t_e=0 and t_e=1.

    Checked by finite-differencing `_z0_mu`, which is written from the definition. If the
    hand-derivation in either docstring is wrong, this fails.
    """
    h = 1e-6
    for th in (1.6, 1.9, 2.2):
        for locus, te in ((loci.ln_ls0_mu, 0.0), (loci.ln_ls1_mu, 1.0)):
            lbar = np.exp(locus(np.array([th]), mu=mu))[0]
            if not np.isfinite(lbar):
                continue
            lo, hi = (te, te + h) if te == 0.0 else (te - h, te)
            slope = (_z0_mu(hi, th, ALP, mu, lbar) - _z0_mu(lo, th, ALP, mu, lbar)) / h
            assert slope == pytest.approx(C, rel=1e-3), f"mu={mu} th={th} te={te}"


def test_second_best_mu_loci_reduce_to_the_published_forms_at_mu_zero():
    """The mu-extended loci must not perturb the mu=0 case the paper's figures already use."""
    th = np.linspace(1.45, 2.1, 200)
    assert np.allclose(loci.ln_ls0_mu(th, mu=0.0), loci.ln_lc0(th), equal_nan=True)
    assert np.allclose(loci.ln_ls1_mu(th, mu=0.0), loci.ln_ld1(th), equal_nan=True)


def test_low_tfp_second_best_locus_is_invariant_to_mu():
    """Eq. (18) compares t_e=0 with t_e=1, and governance acts only at interior t_e:
    z_0^mu(0)=lbar^alpha and z_0^mu(1)=theta*lbar^alpha, neither carrying Lambda_mu."""
    for mu in (0.0, 0.5, 1.0):
        assert _z0_mu(1e-9, 1.6, ALP, mu) == pytest.approx(1.0, rel=1e-4)
        assert _z0_mu(1 - 1e-9, 1.6, ALP, mu) == pytest.approx(1.6, rel=1e-4)


def test_full_enclosure_coincidence_holds_at_mu_zero_and_breaks_above_it():
    """Appendix eq. (20)'s note that the second-best and private full-enclosure thresholds
    coincide is a mu=0 statement. `ln_ld1` at tau=0 is mu-invariant; `ln_ls1_mu` is not.

    Scoped to tau=0 and theta >= theta_H^{mu=0} = 1/alpha deliberately: off the tau=0 edge
    the private locus moves for an unrelated reason, and below theta_H the eq. (20) margin is
    not the operative condition. See `test_tau_does_not_move_the_second_best_locus`.
    """
    th = np.linspace(1.5, 2.1, 100)
    assert np.allclose(loci.ln_ls1_mu(th, mu=0.0), loci.ln_ld1(th, mu=0.0), equal_nan=True)
    assert not np.allclose(loci.ln_ls1_mu(th, mu=0.6), loci.ln_ld1(th, mu=0.6), equal_nan=True)


def test_tau_does_not_move_the_second_best_locus():
    """Compensation is a transfer, so it cancels out of the planner's output margin -- the
    second-best loci take no `tau` at all. The private locus they are compared against does
    move with it, which is why the eq. (20) coincidence is only readable at tau=0.
    """
    for fn in (loci.ln_ls0_mu, loci.ln_ls1_mu):
        assert "tau" not in inspect.signature(fn).parameters, f"{fn.__name__} grew a tau"
    th = np.linspace(1.55, 2.1, 50)
    assert not np.allclose(loci.ln_ld1(th, tau=0.0), loci.ln_ld1(th, tau=0.5), equal_nan=True)


# ---------------------------------------------------------------------------
# loci.py vs model.py agreement
# ---------------------------------------------------------------------------

def test_ld0_is_where_rental_equals_c_at_te_zero():
    """ln_ld0(th) is, by construction, the lbar where model.req(0,...) = c."""
    lbar = np.exp(loci.ln_ld0(TH))
    r0 = model.req(np.zeros_like(TH), TH, ALP, lbar, mu=0.0)
    np.testing.assert_allclose(r0, C, rtol=1e-6)


def test_ld1_is_where_rental_equals_c_at_te_one():
    """ln_ld1(th) is the lbar where model.req(1,...) = c."""
    lbar = np.exp(loci.ln_ld1(TH))
    r1 = model.req(np.ones_like(TH), TH, ALP, lbar, mu=0.0)
    np.testing.assert_allclose(r1, C, rtol=1e-6)


def test_l01_is_where_planner_marginal_benefit_equals_c_at_te_zero():
    """ln_l01(th) is the lbar where model.zprime(0, ..., mu=1) = c."""
    lbar = np.exp(loci.ln_l01(TH))
    zp0 = model.zprime(np.zeros_like(TH), TH, ALP, lbar, mu=1.0)
    np.testing.assert_allclose(zp0, C, rtol=1e-6)


def test_l11_is_where_planner_marginal_benefit_equals_c_at_te_one():
    """ln_l11(th) is the lbar where model.zprime(1, ..., mu=1) = c."""
    lbar = np.exp(loci.ln_l11(TH))
    zp1 = model.zprime(np.ones_like(TH), TH, ALP, lbar, mu=1.0)
    np.testing.assert_allclose(zp1, C, rtol=1e-6)


# ---------------------------------------------------------------------------
# tau/mu unification, established during the Phase 1 migration (see loci.py docstring)
# ---------------------------------------------------------------------------

def test_ld0_tau_matches_independent_nu_derivation():
    """ln_ld0's tau parameter matches Model_Construction.ipynb cell 91's independently
    hand-derived `nu`-parameterized formula, at multiple tau values including tau=0.

    This is a fresh re-derivation (not a call into loci.ln_ld0), so it's a genuine
    cross-check rather than a tautology.
    """
    th = np.linspace(1.02, CV - 1e-6, 50)
    lam = loci.lam0(th)
    for tau in (0.0, 0.3, 0.6):
        nu_expr = C / (1 - ALP) * (1 / (th * lam**ALP - tau))
        with np.errstate(invalid="ignore"):
            nu_ld0 = np.log(nu_expr) / ALP
        np.testing.assert_allclose(loci.ln_ld0(th, tau=tau), nu_ld0, equal_nan=True)


def test_ld1_tau_matches_independent_nu_derivation():
    th = np.linspace(1.02, CV - 1e-6, 50)
    lam = loci.lam0(th)
    for tau in (0.0, 0.3, 0.6):
        nu_expr = (C * lam**ALP / (1 - ALP)) * (1 / (th * lam**ALP - tau))
        with np.errstate(invalid="ignore"):
            nu_ld1 = np.log(nu_expr) / ALP
        np.testing.assert_allclose(loci.ln_ld1(th, tau=tau), nu_ld1, equal_nan=True)


def test_ld0_mu_matches_independent_cell91_derivation():
    """ln_ld0's mu parameter matches Model_Construction.ipynb cell 91's independently
    hand-derived `expr_pd0mu`, transcribed fresh here.

    Note cell 91 writes this in an asymmetric form (Lambda_mu outside the 1/alpha power,
    the rest inside) and applies power=1.0; that is algebraically the same as the
    consolidated form, and this test is what pins that down.
    """
    th = np.linspace(0.85, CV - 1e-6, 50)
    for mu in (0.0, 0.4, 1.0):
        mu_denom = (1 - mu) * (1 - ALP) + ALP
        expr = (1 / (ALP * th / mu_denom)**(1 / (1 - ALP))) * (C / th * 1 / (1 - ALP))**(1 / ALP)
        np.testing.assert_allclose(loci.ln_ld0_mu(th, mu=mu), np.log(expr))


def test_gg_mu_reduces_to_gg_at_mu_zero():
    th = np.linspace(0.85, CV - 1e-6, 50)
    np.testing.assert_allclose(loci.ln_gg_mu(th, mu=0.0), loci.ln_gg(th))


def test_ld1_is_invariant_to_mu_at_tau_zero():
    """At tau=0 the general form's Lambda_mu^alpha cancels top and bottom, leaving no mu --
    which is why cell 91 could legitimately write `ln_l1dmu = ln_l1d.copy()`."""
    th = np.linspace(0.85, CV - 1e-6, 50)
    base = loci.ln_ld1(th, tau=0.0, mu=0.0)
    for mu in (0.3, 0.6, 1.0):
        np.testing.assert_allclose(loci.ln_ld1(th, tau=0.0, mu=mu), base)


def test_ld1_is_not_invariant_to_mu_when_tau_positive():
    """Guard against over-reading the tau=0 invariance above: once tau>0 the cancellation
    no longer happens and mu genuinely moves the locus."""
    th = np.linspace(1.2, 2.0, 50)
    a = loci.ln_ld1(th, tau=0.5, mu=0.0)
    b = loci.ln_ld1(th, tau=0.5, mu=1.0)
    assert not np.allclose(a, b, equal_nan=True)


def test_wedge_closes_exactly_at_mu_one_tau_one():
    """The paper's Key Result (online_appendix.md 5.3): at mu=1 AND tau=1 the decentralized
    loci don't merely approach the planner's -- they coincide exactly.

    At mu=1, Lambda_mu = theta^(1/(1-alpha)) = Lambda_o, and theta*Lambda_o^alpha =
    Lambda_o collapses the decentralized denominator (1-alpha)(theta*Lambda_mu^alpha - tau)
    to the planner's (Lambda_o - 1)(1-alpha). This is what panel (d) of new_comp_fig4x4.png
    now actually plots, instead of drawing the planner band twice.
    """
    th = np.linspace(1.1, 2.1, 200)
    np.testing.assert_allclose(loci.ln_ld0(th, tau=1.0, mu=1.0), loci.ln_l01(th))
    np.testing.assert_allclose(loci.ln_ld1(th, tau=1.0, mu=1.0), loci.ln_l11(th))


def test_wedge_is_open_when_only_one_of_mu_tau_is_one():
    """The closure is genuinely joint -- neither mu=1 alone nor tau=1 alone suffices.
    Without this, the test above would pass for the wrong reason."""
    th = np.linspace(1.2, 2.0, 50)
    planner = loci.ln_l01(th)
    assert not np.allclose(loci.ln_ld0(th, tau=0.0, mu=1.0), planner, equal_nan=True)
    assert not np.allclose(loci.ln_ld0(th, tau=1.0, mu=0.0), planner, equal_nan=True)


def test_monopoly_locus_matches_source_cell():
    """ln_lm0/ln_lm1 match Model_Construction.ipynb cell 45's formulas directly
    transcribed here, independent of loci.py's own implementation."""
    the_gg = np.arange(0.8, CV, 0.01)
    the_r2 = np.arange(CV, 2.1, 0.01)
    lam = (ALP * the_r2)**(1 / (1 - ALP))

    ln_pm_orig = np.log((C / ((1 - ALP) * the_gg))**(1 / ALP))
    ln_pm1_orig = np.log((C * ALP * lam**ALP / ((1 - ALP) * (lam * (1 - ALP) + ALP)))**(1 / ALP))

    np.testing.assert_allclose(loci.ln_lm0(the_gg), ln_pm_orig)
    np.testing.assert_allclose(loci.ln_lm1(the_r2), ln_pm1_orig)


# ---------------------------------------------------------------------------
# Ported from generate_trajectories_figure.py's sanity_checks()
# ---------------------------------------------------------------------------

def test_gg_locus_rises_with_tau():
    th = np.linspace(loci.THETA_TAU + 1e-3, CV - 1e-3, 400)
    g0, g1 = loci.ln_gg(th, tau=0.0), loci.ln_gg(th, tau=1.0)
    assert np.all(g1 > g0), "tau=1 gg locus must lie above tau=0 locus"


def test_gg_tau1_asymptote():
    assert loci.THETA_TAU == pytest.approx(ALP**(-ALP))


def test_weitzman_samuelson_point_below_gg_locus():
    ws_gg = loci.ln_gg(np.array([1.0]))[0]
    assert 0.9 < ws_gg


def test_marx_brenner_point_between_gg_and_ls():
    mx_gg = loci.ln_gg(np.array([1.1]))[0]
    mx_ls = loci.ln_ls(np.array([1.1]))[0]
    assert mx_gg < 2.7 < mx_ls


def test_de_janvry_point_between_lc0_and_ld0():
    dj_lo = loci.ln_lc0(np.array([1.9]))[0]
    dj_hi = loci.ln_ld0(np.array([1.9]))[0]
    assert dj_lo < -0.24 < dj_hi


def test_loci_sanity_checks_function_runs_clean():
    """loci.py's own sanity_checks() (mirrors these tests, kept for parity with
    generate_trajectories_figure.py's convention) must not raise."""
    loci.sanity_checks()


# ---------------------------------------------------------------------------
# theta_tau bounds the whole decentralized family, not just the selection locus
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("mu,tau", [(0.0, 1.0), (0.35, 0.35), (0.65, 0.5), (0.5, 0.9)])
def test_theta_tau_truncates_all_three_decentralized_loci(mu, tau):
    """theta_tau is easy to mistake for a property of the coordination problem, because it
    is the left edge of the region ln_gg is drawn on. It is not: the factor
    (theta*Lambda_mu^alpha - tau) sits in eq. (14) and eq. (15) too, so ln_ld0 and ln_ld1
    go undefined at exactly the same theta. A figure or docstring that attributes the edge
    to selection alone is wrong, and this pins that down."""
    tt = loci.theta_tau(loci.ALP, mu, tau)
    assert tt > 0.5, "pick parameters where the boundary actually binds"

    below, above = np.array([tt - 1e-3]), np.array([tt + 1e-3])
    for name in ("ln_ld0", "ln_ld1", "ln_gg"):
        f = getattr(loci, name)
        assert not np.isfinite(f(below, tau=tau, mu=mu)[0]), f"{name} defined below theta_tau"
        assert np.isfinite(f(above, tau=tau, mu=mu)[0]), f"{name} undefined above theta_tau"


@pytest.mark.parametrize("mu,tau", [(0.35, 0.35), (0.65, 0.5)])
def test_theta_tau_boundary_is_density_free(mu, tau):
    """Why no density rescues enclosure below theta_tau: the enclosure rent and the
    compensation owed both scale with lbar^alpha, so their ratio is theta*Lambda^alpha/tau
    with no lbar in it. Scaling density scales a negative number."""
    th = loci.theta_tau(loci.ALP, mu, tau) - 0.01
    lam = loci.lam_mu(np.array([th]), loci.ALP, mu)[0]
    ratios = []
    for lbar in (1.0, 1e3, 1e9):
        r_e = (1 - loci.ALP) * th * lam**loci.ALP * lbar**loci.ALP
        comp = tau * (1 - loci.ALP) * lbar**loci.ALP
        assert r_e - comp < 0, "should be unprofitable below theta_tau at every density"
        ratios.append(r_e / comp)
    assert np.allclose(ratios, ratios[0], rtol=1e-12), "ratio must not depend on lbar"
    assert ratios[0] == pytest.approx(th * lam**loci.ALP / tau, rel=1e-12)


# ---------------------------------------------------------------------------
# "One fixed canvas" -- the symbol table's note in content/04-derivations.md
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("k", [2.0, 0.25, 7.5])
def test_scaling_c_over_A_translates_every_locus_equally(k):
    r"""Every locus has the form ln(lbar) = (1/alpha)ln(c/A) + g(theta), so c and A cannot
    change the shape of the picture -- they move every curve by the same vertical distance,
    which is geometrically identical to the economy's own point moving the other way. The
    appendix's Notation section states this; this is what makes it a checked claim.

    The corollary is why the package carries no separate `A`: c and A appear only as the
    ratio, so `loci.C` is c/A."""
    th = np.linspace(1.05, 2.2, 40)
    predicted = np.log(k) / loci.ALP
    curves = {
        "ln_l01": lambda c: loci.ln_l01(th, loci.ALP, c),
        "ln_l11": lambda c: loci.ln_l11(th, loci.ALP, c),
        "ln_ld0": lambda c: loci.ln_ld0(th, loci.ALP, c, tau=0.3, mu=0.4),
        "ln_ld1": lambda c: loci.ln_ld1(th, loci.ALP, c, tau=0.3, mu=0.4),
        "ln_gg": lambda c: loci.ln_gg(th, loci.ALP, c, tau=0.3, mu=0.4),
        "ln_lm0": lambda c: loci.ln_lm0(th, loci.ALP, c),
    }
    for name, f in curves.items():
        d = f(loci.C * k) - f(loci.C)
        d = d[np.isfinite(d)]
        assert d.size, f"{name} produced no finite points to compare"
        assert np.allclose(d, predicted, rtol=0, atol=1e-11), (
            f"{name} did not translate by (1/alpha)ln({k}): "
            f"got {d.min():.6f}..{d.max():.6f}, expected {predicted:.6f}"
        )


def test_tau_deforms_rather_than_translates():
    """The converse half of the same claim: tau is not a vertical shift. Without this, a
    locus that ignored tau entirely would pass the test above and look like a fixed canvas."""
    th = np.linspace(1.05, 2.2, 40)
    d = (loci.ln_ld0(th, tau=0.5, mu=0.0) - loci.ln_ld0(th, tau=0.0, mu=0.0))
    d = d[np.isfinite(d)]
    assert d.max() - d.min() > 0.5, "tau should change the shape, not just the level"
