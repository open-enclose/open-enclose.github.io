r"""Three-sector extension: enclosed agriculture, commons agriculture, manufacturing.

Eqs (35)-(36) of `online_appendix.md` §6.4 — the structural-transformation extension.
Manufacturing provides an outside option for labor, so the agricultural labor allocation
is scaled by $(1-l_m)$ and the enclosure margin shifts with manufacturing productivity.

Ported from `enclosure_book/notebooks/enclosure_manuf.ipynb`, which defined its own `mplm`,
`mpla` and `LM` in-notebook — a fourth parallel implementation of model code. Here they
reuse `enclose.model.Lambda` rather than recomputing it.

**Why this module needs a numerical solve.** Labor allocates until the return it earns in
manufacturing equals the return it earns in agriculture:

$$MPL_m = C_m\, l_m^{-(1-\beta)},\qquad
  w_a = C_a\, (1-l_m)^{-(1-\alpha)}$$

with $C_m = p\beta k^{1-\beta}$ and
$C_a = A_\mu\,\bar t^{1-\alpha}(1+(\Lambda_\mu-1)t_e)^{1-\alpha}$, where
$A_\mu = 1-\mu(1-\alpha)$ is the `commons_wedge`.
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

**The $A_\mu$ factor, and why it is easy to lose.** $\Lambda_\mu$ absorbs
$1-\mu(1-\alpha)$ into the *slope* of the agricultural labor allocation, but the same
wedge also sits on the *level* of what labor earns. `enclosure_manuf.md` writes the
agricultural return as $\bar t^{1-\alpha}(t_e/l_e^*)^{1-\alpha}$ — a shorthand that is
correct only at $\mu=0$, because $\alpha\theta\Lambda_0^{-(1-\alpha)} = 1$ there. In
general $\alpha\theta\Lambda_\mu^{-(1-\alpha)} = A_\mu$, which is $\alpha$ at $\mu=1$, not
$1$. An earlier version of this module carried the shorthand across to every $\mu$ and so
overstated the planner's agricultural labor demand by exactly $1/\alpha$.

Two properties pin the correct level, and both are tested:

* At $t_e=0$ the whole economy *is* the commons. Open access pays labor its average
  product, a planner its marginal product, so the two curves must differ by exactly
  $\alpha$ — not coincide.
* At $t_e=1$ there is no commons left, so $\mu$ cannot matter at all:
  $C_a = \alpha\theta\bar t^{1-\alpha}$ for every $\mu$. Equivalently, **full enclosure
  implements the planner's inter-sectoral allocation for any $\theta$.**

The sign result below is unaffected: $A_\mu$ carries no $t_e$ and no $l_m$, so
$\partial l_m/\partial t_e$ still takes the sign of $(1-\Lambda_\mu)$.

**Mind that sign.** The equilibrium condition
$l_m^{1-\beta}(1-l_m)^{-(1-\alpha)} = C_m/C_a$ has a left side that is strictly
*increasing* in $l_m$, so $l_m$ rises exactly when $C_a$ *falls* — one inversion. Since
$\partial C_a/\partial t_e$ has the sign of $(\Lambda_\mu-1)$, the effect on $l_m$ has the
opposite sign. Several docstrings and pages here previously stated it as
"$\operatorname{sign}(\Lambda_\mu-1)$", which is backwards; the accompanying descriptions
and every test were right. Note the *enclosure* margin in `planner_marginal_benefit` is
genuinely $\operatorname{sign}(\Lambda_o-1)$ — that one is not an error, and the two must
not be made to agree.
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


def commons_wedge(alp, mu):
    r"""The governance wedge $A_\mu = 1-\mu(1-\alpha)$, appendix eqs. (22)-(23).

    The share of the commons *average* product that labor actually takes home: its
    marginal product $\alpha\,APL$ plus the fraction $(1-\mu)$ of possession rents it
    retains, $(1-\mu)(1-\alpha)\,APL$. So $A_0 = 1$ (open access — labor captures the whole
    average product) and $A_1 = \alpha$ (perfect regulation — labor is paid its marginal
    product, as a planner would).

    Equivalently $A_\mu = \alpha\theta\,\Lambda_\mu^{-(1-\alpha)}$, which is the form in
    which it appears when $l_e^\mu(t_e)$ is substituted back into the agricultural return.
    Named and defined once here so it cannot be silently dropped again.
    """
    return 1 - mu * (1 - alp)


def mpl_a(lm, te, tbar=1.0, alp=0.5, th=1.0, mu=0.0):
    r"""What labor earns in agriculture, given manufacturing's labor share.

    $$w_a(l_m) = A_\mu\,\bar t^{1-\alpha}\left(1+(\Lambda_\mu-1)t_e\right)^{1-\alpha}
                    (1-l_m)^{-(1-\alpha)}$$

    Strictly *increasing* in $l_m$: labor leaving agriculture raises the product of those
    who remain. `mu` enters twice and in opposing directions — through $\Lambda_\mu$
    (eq. 23), which raises this curve, and through the `commons_wedge` $A_\mu$, which
    lowers it. At $t_e=0$ the second dominates outright (the first drops out); at $t_e=1$
    they cancel exactly and $\mu$ is irrelevant.

    Despite the name this is a *marginal* product only at $\mu=1$; at $\mu=0$ it is the
    commons average product, which is what open access pays. The name is kept because it
    is the agricultural labor-demand curve of the two-curve diagram, but see the module
    docstring — reading it as an MPL for every $\mu$ is exactly the error that put a
    spurious factor of $1/\alpha$ on the planner's curve.

    The default is `mu=0` (open access), matching `labor_share` and `excess_mpl`; it was
    previously `mu=1`, so the same call to two functions in this module meant two different
    economies.
    """
    lam = Lambda(th, alp, mu)
    return (commons_wedge(alp, mu) * tbar**(1 - alp)
            * (1 + (lam - 1) * te)**(1 - alp) * (1 / (1 - lm))**(1 - alp))


def _c_m(p, kb, b):
    """Manufacturing constant, the part of MPL_m independent of lm."""
    return p * b * kb**(1 - b)


def _c_a(te, tbar, alp, th, mu):
    """Agricultural constant, the part of the agricultural return independent of lm.

    Carries the `commons_wedge` as well as $\\Lambda_\\mu$ — see the module docstring.
    """
    lam = Lambda(th, alp, mu)
    return commons_wedge(alp, mu) * tbar**(1 - alp) * (1 + (lam - 1) * te)**(1 - alp)


def excess_mpl(lm, te, b=0.5, alp=0.5, th=1.0, tbar=1.0, kb=1.0, p=1.0, mu=0.0):
    """MPL_m - the agricultural return. Zero at equilibrium; strictly decreasing in lm, so
    it has exactly one root on (0, 1)."""
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


def total_output(te, b=0.5, alp=0.5, th=1.0, tbar=1.0, kb=1.0, p=1.0, mu=0.0):
    r"""Total output per worker at the equilibrium allocation for this $t_e$.

    $$Y/\bar L = \theta(t_e\bar t)^{1-\alpha}l_e^{\alpha}
                 + ((1-t_e)\bar t)^{1-\alpha}l_u^{\alpha}
                 + p\,\bar k^{1-\beta}l_m^{\beta}$$

    Gross — the enclosure cost $c$ is *not* netted off; see `planner_marginal_benefit`.
    At `mu=1` this is the planner's value function over $t_e$; at `mu=0` it is what the
    open-access economy actually produces, which is strictly lower except at $t_e=1$,
    where there is no commons left to misallocate labor.
    """
    lm = labor_share(te, b, alp, th, tbar, kb, p, mu)
    le = agricultural_labor(te, th, alp, mu, b=b, tbar=tbar, kb=kb, p=p)
    lu = (1 - lm) - le
    ag_e = th * (te * tbar)**(1 - alp) * le**alp if te > 0 else 0.0
    ag_u = ((1 - te) * tbar)**(1 - alp) * lu**alp if te < 1 else 0.0
    return ag_e + ag_u + p * kb**(1 - b) * lm**b


def planner_marginal_benefit(te, b=0.5, alp=0.5, th=1.0, tbar=1.0, kb=1.0, p=1.0):
    r"""Marginal social benefit of enclosure, $dY/dt_e$ per worker, at the planner's
    allocation. Compare against $c\,\bar t$ to get the planner's enclosure margin.

    By the envelope theorem the labor-reallocation terms drop out — the planner has already
    equalised marginal products, so shifting labor has no first-order effect — leaving only
    the land-rent differential $\theta F_T^e - F_T^u$:

    $$\frac{dY}{dt_e} = (1-\alpha)\,\bar t^{1-\alpha}(\Lambda_o-1)
        \left(\frac{1-l_m(t_e)}{1+(\Lambda_o-1)t_e}\right)^{\alpha}$$

    This is exactly the benchmark's `model.zprime` with the *agricultural* labor share
    $(1-l_m)$ in place of the whole labor force: manufacturing changes the level but not
    the structure, and in particular not the sign.

    **The sign is the sign of $(\Lambda_o - 1)$, i.e. of $(\theta - 1)$** — note $\Lambda_o$,
    not $\Lambda_\mu$, so the relevant threshold here is $\theta = 1$ and *not* the
    $\theta_H^\mu$ of the labor-allocation reversal. Consequences:

    * $\theta < 1$: enclosure lowers output even at $c=0$. The planner never encloses.
    * $\theta = 1$: exactly zero. Enclosure is output-neutral for a planner at every $t_e$,
      so with any $c>0$ the planner sets $t_e^o = 0$.
    * $\theta > 1$: positive, and the planner encloses while it exceeds $c\,\bar t$.

    So $t_e^o = 0$ for every $c>0$ whenever $\theta \le 1$, and full enclosure is first best
    only when $\theta > 1$ *and* $c$ is small. That the decentralized economy's labor
    allocation happens to coincide with the planner's at $t_e=1$ does not make $t_e=1$ the
    planner's choice — those are different margins.
    """
    lm = labor_share(te, b, alp, th, tbar, kb, p, mu=1.0)
    lam_o = Lambda(th, alp, 1.0)
    return ((1 - alp) * tbar**(1 - alp) * (lam_o - 1)
            * ((1 - lm) / (1 + (lam_o - 1) * te))**alp)


def private_marginal_return(te, tau=0.0, b=0.5, alp=0.5, th=1.0, tbar=1.0, kb=1.0,
                            p=1.0, mu=0.0):
    r"""Private marginal return to enclosure with manufacturing, eq. (42).

    $$r^e_\mu - \tau r^c_\mu = (1-\alpha)\,\bar t^{1-\alpha}
        \left(\frac{1-l_m(t_e)}{1+(\Lambda_\mu-1)t_e}\right)^{\alpha}
        \left[\theta\Lambda_\mu^{\alpha} - \tau\right]$$

    Compare against $c\,\bar t$ for the decentralized enclosure margin, as
    `planner_marginal_benefit` is compared for the social one.

    The factorization is the point: **manufacturing enters only through
    $(1-l_m)^\alpha$**, a scale factor common to both rentals, while **$\tau$ enters only
    the bracket**. Since $\theta\Lambda_\mu^\alpha = \Lambda_\mu$ at $\mu=1$, the bracket
    reduces to the planner's $[\Lambda_o-1]$ exactly when $\mu=1$ *and* $\tau=1$.

    The marginal encloser takes $l_m$ and the wage as given, so $l_m$ enters as a level
    rather than through a strategic term.

    Note this returns the marginal return only. For $\theta<\theta_H^\mu$ the enclosure
    game has strategic complementarities and multiple equilibria, so selecting the
    realised $t_e$ needs the global-games refinement (`model.tepvt_g`), not just the sign
    of this expression.
    """
    lm = labor_share(te, b, alp, th, tbar, kb, p, mu)
    lam = Lambda(th, alp, mu)
    return ((1 - alp) * tbar**(1 - alp) * ((1 - lm) / (1 + (lam - 1) * te))**alp
            * (th * lam**alp - tau))


def compensation_threshold(th=1.0, alp=0.5, mu=0.0):
    r"""Compensation rate above which enclosure is never privately profitable, eq. (43).

    $$\tau^*(\theta,\mu) = \theta\,\Lambda_\mu^{\alpha}$$

    Strictly increasing in both $\theta$ and $\mu$ — so better commons governance makes
    enclosure *harder* to deter by compensation, even as it makes deterrence more
    worthwhile.

    Full compensation binds only below a threshold with a clean closed form:

    $$\tau^*(\theta,\mu) \lessgtr 1 \iff \theta \lessgtr \left(\theta_H^\mu\right)^{\alpha}$$

    which lies strictly between $1$ and $\theta_H^\mu$ and collapses to $1$ at $\mu=1$.
    Above it no admissible $\tau$ prevents enclosure and compensation is a pure transfer.
    """
    return th * Lambda(th, alp, mu)**alp


def agricultural_labor(te, th=1.0, alp=0.5, mu=0.0, **kw):
    r"""Agricultural labor share on enclosed land with manufacturing present, eq. (36).

    $$l_e^\mu(t_e) = \frac{\Lambda_\mu t_e}{1+(\Lambda_\mu-1)t_e}\cdot(1-l_m)$$

    i.e. the usual reaction function scaled by the labor that stays in agriculture.
    Extra keyword arguments are forwarded to `labor_share`.
    """
    lm = labor_share(te, alp=alp, th=th, mu=mu, **kw)
    lam = Lambda(th, alp, mu)
    return (lam * te) / (1 + (lam - 1) * te) * (1 - lm)
