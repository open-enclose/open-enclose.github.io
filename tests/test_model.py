"""Tests for enclose.model, ported from enclosure_book/tests/test_enclose.py.

Everything here is about one thing: every function takes `lbar`, population density
$\\bar l = \\bar L / \\bar T$. See `enclose.model`'s module docstring.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from enclose import model as e  # noqa: E402

TE_ALL = np.array([0.0, 0.2, 0.5, 0.8, 1.0])
# the MPT/MPL identities are stated at interior t_e: at t_e=0 both l_e and t_e
# are zero and the per-unit marginal products are 0/0, though req/weq stay finite
TE = np.array([0.2, 0.4, 0.5, 0.8, 0.99])
TH, ALP = 2.2, 0.5


# ---------------------------------------------------------------------------
# Compensation (tau) in the private enclosure decision
#
# tau lived only in the locus layer until 2026-07-29; `model.py`'s docstring said so
# explicitly. These pin the new model-layer implementation against (a) the tau=0 behaviour it
# replaced and (b) the locus layer, which derived the same margin independently.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("mu", [0.0, 0.5, 1.0])
def test_commons_rental_carries_no_theta(mu):
    """Commons land is unenclosed, so it runs the baseline technology. r^c and r^e differ by
    exactly the enclosure productivity factor theta*Lambda_mu^alpha."""
    lam = e.Lambda(TH, ALP, mu)
    np.testing.assert_allclose(
        e.req(TE_ALL, TH, ALP, 1.0, mu),
        TH * lam**ALP * e.rcom(TE_ALL, TH, ALP, 1.0, mu),
    )


@pytest.mark.parametrize("mu", [0.0, 0.5, 1.0])
@pytest.mark.parametrize("tau", [0.0, 0.4, 1.0])
def test_req_net_is_rental_minus_compensation(mu, tau):
    """`req_net` is exactly eq. (27)'s margin, not an independent re-derivation."""
    np.testing.assert_allclose(
        e.req_net(TE_ALL, TH, ALP, 1.0, mu, tau),
        e.req(TE_ALL, TH, ALP, 1.0, mu) - tau * e.rcom(TE_ALL, TH, ALP, 1.0, mu),
    )


@pytest.mark.parametrize("mu", [0.0, 0.5])
@pytest.mark.parametrize("tau", [0.0, 0.3, 0.8])
def test_req_net_corners_reproduce_the_loci(mu, tau):
    """The density at which the margin equals c, at te=0 and te=1, is `ln_ld0`/`ln_ld1`.

    This is the cross-layer check: `model.req_net` and `loci.ln_ld0`/`ln_ld1` were derived
    separately, and must agree or one of them is wrong.
    """
    from enclose import loci
    for th in (1.2, 1.8, 2.2):
        for te, locus in ((0.0, loci.ln_ld0), (1.0, loci.ln_ld1)):
            lbar = float(np.exp(locus(np.array([th]), alp=ALP, c=loci.C, tau=tau, mu=mu))[0])
            if not np.isfinite(lbar):
                continue
            assert e.req_net(te, th, ALP, lbar, mu, tau) == pytest.approx(loci.C, rel=1e-9)


def test_tau_zero_reproduces_the_uncompensated_enclosure_rate():
    """Regression guard: adding tau must not perturb any tau=0 result. The old closed form
    was lbar*(lam/(lam-1))*(th*(1-alp)/c)**(1/alp) - 1/(lam-1); the general one reduces to it
    because (Lambda^alpha)**(1/alpha) = Lambda."""
    for th in (1.1, 1.4, 1.6, 1.9, 2.4):
        for lnl in (-0.5, 0.5, 1.5, 2.5):
            lbar, lam = np.exp(lnl), e.Lambda(th, ALP, 0.0)
            if abs(lam - 1) < 1e-9:      # theta_H exactly: both forms divide by zero
                continue
            old = (lbar * (lam / (lam - 1)) * (th * (1 - ALP) / 1.0)**(1 / ALP)
                   - 1 / (lam - 1))
            got = e.tepvt(th, ALP, 1.0, lbar, 0.0, tau=0.0)
            # only compare where the old formula's interior branch was the operative one
            if 0.0 < got < 1.0:
                assert got == pytest.approx(old, rel=1e-12)


@pytest.mark.parametrize("mu", [0.0, 0.5])
def test_compensation_weakly_deters_enclosure(mu):
    """Raising tau cannot raise the private enclosure rate -- that is what compensation is
    for. Checked across the plane rather than at a point."""
    taus = [0.0, 0.25, 0.5, 0.75, 1.0]
    for th in (1.1, 1.3, 1.7, 2.1):
        for lnl in (-0.5, 0.5, 1.0, 2.0, 3.0):
            rates = [e.tepvt(th, ALP, 1.0, np.exp(lnl), mu, t) for t in taus]
            assert all(b <= a + 1e-12 for a, b in zip(rates, rates[1:])), \
                f"tepvt rose with tau at th={th}, ln lbar={lnl}, mu={mu}: {rates}"


def test_compensation_above_the_gross_return_stops_enclosure_entirely():
    """If tau exceeds theta*Lambda_mu^alpha the margin is negative at every te, so no density
    makes enclosure worthwhile -- and the interior formula must not be reached, since it would
    take a fractional power of a negative number."""
    th, mu = 1.5, 0.0
    gross = th * e.Lambda(th, ALP, mu)**ALP
    for lbar in (0.5, 5.0, 50.0):
        assert e.tepvt(th, ALP, 1.0, lbar, mu, tau=gross + 0.5) == 0.0
        assert e.tepvt_g(th, ALP, 1.0, lbar, mu, tau=gross + 0.5) == 0.0


@pytest.mark.parametrize("mu", [0.0, 0.5, 1.0])
@pytest.mark.parametrize("lbar", [0.25, 1.0, 4.0])
def test_rental_equals_marginal_product_of_land(mu, lbar):
    """r(t_e) is MPT evaluated at the equilibrium labor allocation l_e(t_e)."""
    le = e.le(TE, TH, ALP, mu)
    np.testing.assert_allclose(
        e.req(TE, TH, ALP, lbar, mu),
        e.mpt(TE, le, ALP, TH, lbar),
    )


@pytest.mark.parametrize("lbar", [0.25, 1.0, 4.0])
def test_wage_equals_marginal_product_of_labor_at_mu_zero(lbar):
    """At mu=0 the wage is MPL on enclosed land at l_e(t_e)."""
    le = e.le(TE, TH, ALP, mu=0.0)
    np.testing.assert_allclose(
        e.weq(TE, TH, ALP, lbar, mu=0.0),
        e.mple(TE, le, ALP, TH, lbar),
    )


@pytest.mark.parametrize("mu", [0.25, 0.5, 1.0])
def test_wage_scales_by_security_wedge_for_positive_mu(mu):
    """For mu>0, weq is that same marginal product scaled by (1-mu+alp*mu)."""
    le = e.le(TE, TH, ALP, mu)
    np.testing.assert_allclose(
        e.weq(TE, TH, ALP, 2.0, mu) * (1 - mu + ALP * mu),
        e.mple(TE, le, ALP, TH, 2.0),
    )


def test_factor_prices_scale_with_density_in_opposite_directions():
    """r ~ lbar**alp, w ~ lbar**(alp-1)."""
    k = 4.0
    np.testing.assert_allclose(
        e.req(TE_ALL, TH, ALP, lbar=k), k**ALP * e.req(TE_ALL, TH, ALP, lbar=1.0)
    )
    np.testing.assert_allclose(
        e.weq(TE_ALL, TH, ALP, lbar=k), k**(ALP - 1) * e.weq(TE_ALL, TH, ALP, lbar=1.0)
    )


def test_mpl_is_alpha_times_apl():
    """Cobb-Douglas identity."""
    np.testing.assert_allclose(
        e.mple(0.4, 0.6, ALP, TH, lbar=3.0),
        ALP * e.aple(0.4, 0.6, ALP, TH, lbar=3.0),
    )


@pytest.mark.parametrize("lbar", [0.25, 1.0, 4.0])
def test_totalq_matches_closed_form_z_at_mu_one(lbar):
    """At mu=1, l_e is the first-best allocation, so totalq must equal z(t_e)."""
    np.testing.assert_allclose(
        e.totalq(TE, TH, ALP, lbar, mu=1.0),
        e.z(TE, TH, ALP, lbar),
    )


@pytest.mark.parametrize("mu", [0.0, 0.25, 0.5, 1.0])
def test_lambda_matches_appendix_eq23(mu):
    """Lambda_mu is spelled as online_appendix.md eq. (23) writes it.

    Guards against the drift this replaced: three algebraically-equal spellings of this
    same denominator had accumulated across three modules.
    """
    th = np.array([1.2, 1.5, 2.0])
    expected = ((ALP * th) / (1 - mu * (1 - ALP)))**(1 / (1 - ALP))
    np.testing.assert_allclose(e.Lambda(th, ALP, mu), expected)


@pytest.mark.parametrize("mu", [0.0, 0.25, 0.5, 1.0])
def test_theta_H_matches_appendix_eq24(mu):
    """theta_H^mu = 1/alpha - mu(1-alpha)/alpha, eq. (24)."""
    assert e.theta_H(ALP, mu) == pytest.approx(1 / ALP - mu * (1 - ALP) / ALP)


def test_theta_H_is_where_lambda_equals_one():
    """Cross-check tying eq. (24) back to eq. (23): theta_H^mu is by definition the theta
    at which Lambda_mu = 1. Verifying that is stronger than restating the formula."""
    for mu in (0.0, 0.4, 1.0):
        assert e.Lambda(e.theta_H(ALP, mu), ALP, mu) == pytest.approx(1.0)


def test_tepvt_g_threads_mu_through():
    """Regression guard: tepvt_g must use its own mu, not hardcode mu=0 internally.

    At these parameters the global-games refinement decision itself flips between
    mu=0 and mu=0.8 -- not just a numeric nudge, a different corner solution.
    """
    th, alp, c, lbar = 1.85, 0.5, 0.9, 1.0
    assert e.tepvt_g(th, alp, c, lbar, mu=0.0) != e.tepvt_g(th, alp, c, lbar, mu=0.8)
    # and it must agree with tepvt at the same mu, not tepvt(mu=0)
    assert e.tepvt_g(th, alp, c, lbar, mu=0.8) in (
        0.0, 1.0, e.tepvt(th, alp, c, lbar, mu=0.8)
    )
