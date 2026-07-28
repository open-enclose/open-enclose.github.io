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
