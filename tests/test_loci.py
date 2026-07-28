"""Tests for enclose.loci.

Two kinds of check:
1. loci.py vs enclose.model agreement -- each locus is *defined* as the lbar where some
   model.py equilibrium condition holds (e.g. ln_ld0(th) is where req(0,...)=c); verifying
   that directly is a genuine cross-check between the two independently-written layers.
2. Ported/extended versions of generate_trajectories_figure.py's own sanity_checks(),
   plus fresh (not loci-internal) re-derivations of the mu/tau unification established
   during the Phase 1 migration -- see loci.py's module docstring.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from enclose import loci, model  # noqa: E402

ALP, C, CV = loci.ALP, loci.C, loci.CV
TH = np.array([1.2, 1.4, 1.6, 1.8])


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


def test_ld0_mu_reduces_to_ld0_at_mu_zero():
    th = np.linspace(0.85, CV - 1e-6, 50)
    np.testing.assert_allclose(loci.ln_ld0_mu(th, mu=0.0), loci.ln_ld0(th))


def test_gg_mu_reduces_to_gg_at_mu_zero():
    th = np.linspace(0.85, CV - 1e-6, 50)
    np.testing.assert_allclose(loci.ln_gg_mu(th, mu=0.0), loci.ln_gg(th))


def test_ld1_mu_is_invariant_to_mu():
    """The r(1)=c condition doesn't involve the governance wedge -- ln_ld1_mu should be
    flat in mu (source: cell 91 sets ln_l1dmu = ln_l1d.copy())."""
    th = np.linspace(0.85, CV - 1e-6, 50)
    base = loci.ln_ld1_mu(th, mu=0.0)
    for mu in (0.3, 0.6, 1.0):
        np.testing.assert_allclose(loci.ln_ld1_mu(th, mu=mu), base)


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
