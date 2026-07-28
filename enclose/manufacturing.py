r"""Three-sector extension: enclosed agriculture, commons agriculture, manufacturing.

Eqs (35)-(36) of `online_appendix.md` §6.4 — the structural-transformation extension.
Manufacturing provides an outside option for labor, so the agricultural labor allocation
is scaled by $(1-l_m)$ and the enclosure margin shifts with manufacturing productivity.

Ported from `enclosure_book/notebooks/enclosure_manuf.ipynb`, which defined its own `mplm`,
`mpla` and `LM` in-notebook — a fourth parallel implementation of model code. Here they
reuse `enclose.model.Lambda` rather than recomputing it.

**Why this module needs a numerical solve.** Labor allocates until marginal products are
equal across sectors:

$$MPL_m = C_m\, l_m^{-(1-\beta)},\qquad
  MPL_a = C_a\, (1-l_m)^{-(1-\alpha)}$$

with $C_m = p\beta k^{1-\beta}$ and $C_a = \bar t^{1-\alpha}(1+(\Lambda_\mu-1)t_e)^{1-\alpha}$.
Setting them equal and rearranging gives

$$\frac{l_m^{1-\beta}}{(1-l_m)^{1-\alpha}} = \frac{C_m}{C_a}$$

which for $\alpha \neq \beta$ is transcendental — no elementary closed form, hence
`labor_share` solves it numerically. Two facts make that solve safe rather than a leap:

1. **The equilibrium is unique.** $MPL_m$ falls in $l_m$ and $MPL_a$ rises in it, so the
   residual crosses zero exactly once on $(0,1)$. `labor_share` therefore uses a *bracketed*
   root-finder (`brentq`), which is guaranteed to converge on a sign-changing bracket —
   unlike an initial-guess method, which can wander.
2. **There is an exact closed form when $\alpha=\beta$.** The exponents coincide and the
   condition collapses to $l_m = R/(1+R)$ with $R = (C_m/C_a)^{1/(1-\alpha)}$. That is not
   the production path; it is an independent oracle the numerical solver is tested against
   in `tests/test_manufacturing.py`.
"""

import numpy as np
from scipy.optimize import brentq

from .model import Lambda

#: Root-finder bracket. The residual diverges at both endpoints, so the bracket is opened
#: slightly rather than taken as exactly [0, 1].
_EPS = 1e-12


def mpl_m(lm, p=1.0, kb=1.0, b=0.5):
    r"""Marginal product of labor in manufacturing.

    $$MPL_m(l_m) = p\,\beta\,k^{1-\beta}\; l_m^{-(1-\beta)}$$

    Strictly decreasing in $l_m$: more labor in manufacturing lowers its marginal product.
    """
    return (p * b) * kb**(1 - b) * (1 / lm)**(1 - b)


def mpl_a(lm, te, tbar=1.0, alp=0.5, th=1.0, mu=1.0):
    r"""Marginal product of labor in agriculture, given manufacturing's labor share.

    $$MPL_a(l_m) = \bar t^{1-\alpha}\left(1+(\Lambda_\mu-1)t_e\right)^{1-\alpha}
                    (1-l_m)^{-(1-\alpha)}$$

    Strictly *increasing* in $l_m$: labor leaving agriculture raises the marginal product
    of those who remain. `mu` enters only through $\Lambda_\mu$ (eq. 23) — at `mu=0` the
    commons is unregulated, at `mu=1` labor is allocated as the planner would.
    """
    lam = Lambda(th, alp, mu)
    return tbar**(1 - alp) * (1 + (lam - 1) * te)**(1 - alp) * (1 / (1 - lm))**(1 - alp)


def _c_m(p, kb, b):
    """Manufacturing constant, the part of MPL_m independent of lm."""
    return p * b * kb**(1 - b)


def _c_a(te, tbar, alp, th, mu):
    """Agricultural constant, the part of MPL_a independent of lm."""
    lam = Lambda(th, alp, mu)
    return tbar**(1 - alp) * (1 + (lam - 1) * te)**(1 - alp)


def excess_mpl(lm, te, b=0.5, alp=0.5, th=1.0, tbar=1.0, kb=1.0, p=1.0, mu=0.0):
    """MPL_m - MPL_a. Zero at equilibrium; strictly decreasing in lm, so it has exactly one
    root on (0, 1)."""
    return (mpl_m(lm, p, kb, b) - mpl_a(lm, te, tbar, alp, th, mu))


def labor_share(te, b=0.5, alp=0.5, th=1.0, tbar=1.0, kb=1.0, p=1.0, mu=0.0):
    r"""Equilibrium labor share in manufacturing, $l_m$, solving $MPL_m = MPL_a$.

    Uses `brentq` on the open interval $(0,1)$. The bracket is valid by the single-crossing
    argument in the module docstring, so this converges for any admissible parameters
    rather than depending on a starting guess.
    """
    return brentq(excess_mpl, _EPS, 1 - _EPS,
                  args=(te, b, alp, th, tbar, kb, p, mu))


def labor_share_closed_form(te, alp=0.5, th=1.0, tbar=1.0, kb=1.0, p=1.0, mu=0.0):
    r"""Exact $l_m$ for the special case $\beta = \alpha$.

    When the two exponents coincide the equilibrium condition collapses to
    $\left(\frac{l_m}{1-l_m}\right)^{1-\alpha} = C_m/C_a$, giving

    $$l_m = \frac{R}{1+R}, \qquad R = \left(\frac{C_m}{C_a}\right)^{\frac{1}{1-\alpha}}$$

    Exists only at $\beta=\alpha$; `labor_share` is the general path. Kept because an
    independent closed form is the strongest available check on a numerical solver — see
    `tests/test_manufacturing.py`.
    """
    R = (_c_m(p, kb, alp) / _c_a(te, tbar, alp, th, mu))**(1 / (1 - alp))
    return R / (1 + R)


def agricultural_labor(te, th=1.0, alp=0.5, mu=0.0, **kw):
    r"""Agricultural labor share on enclosed land with manufacturing present, eq. (36).

    $$l_e^\mu(t_e) = \frac{\Lambda_\mu t_e}{1+(\Lambda_\mu-1)t_e}\cdot(1-l_m)$$

    i.e. the usual reaction function scaled by the labor that stays in agriculture.
    Extra keyword arguments are forwarded to `labor_share`.
    """
    lm = labor_share(te, alp=alp, th=th, mu=mu, **kw)
    lam = Lambda(th, alp, mu)
    return (lam * te) / (1 + (lam - 1) * te) * (1 - lm)
