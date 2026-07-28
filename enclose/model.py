r"""Pure economics for the enclosure model. Numpy only — no matplotlib, no widgets.

Ported from `enclosure_book/notebooks/enclose.py`. Density convention: every function
takes `lbar`, population density $\bar l = \bar L / \bar T$, matching the paper. Factor
prices scale as $r \propto \bar l^{\alpha}$ and $w \propto \bar l^{\alpha-1}$.

$\tau$ (compensation to villages) does not enter here — it is a locus-layer concept only,
see `enclose.loci`.
"""

import numpy as np

DEFAULT_TBAR = 100
DEFAULT_LBAR = 100


def f(T, L, a=0.5, th=1.0):
    r"""Production technology.

    $$f(T, L) = \theta \cdot T^{1-\alpha}L^{\alpha}$$
    """
    return th * T**(1 - a) * L**a


def mple(te, le, a=0.5, th=1.0, lbar=DEFAULT_LBAR / DEFAULT_TBAR):
    r"""Marginal product of labor on enclosed land.

    $$MPL(t_e, l_e) = \alpha \cdot \frac{f(t_e, l_e)}{l_e} \bar l^{\alpha-1}$$
    Since for a Cobb-Douglas, $$MPL = \alpha \cdot APL$$.
    """
    return a * f(te, le, a, th) / le * lbar**(a - 1)


def aple(te, le, a=0.5, th=1.0, lbar=DEFAULT_LBAR / DEFAULT_TBAR):
    r"""Average product of labor.

    $$APL(t_e, l_e) = \frac{f(T_e, L_e)}{L_e} = \frac{f(t_e, l_e)}{l_e} \cdot \bar l^{\alpha-1}$$
    """
    return f(te, le, a, th) / le * lbar**(a - 1)


def mpt(te, le, a=0.5, th=1.0, lbar=DEFAULT_LBAR / DEFAULT_TBAR):
    r"""Marginal product of land on enclosed land.

    $$MPT(t_e, l_e) = (1-\alpha) \cdot \frac{f(t_e, l_e)}{t_e} \bar l^\alpha$$
    Evaluated at the equilibrium $l_e(t_e)$ this is the rental `req`.
    """
    return (1 - a) * f(te, le, a, th) / te * lbar**a


def mplu(te, le, a=0.5, th=1.0, lbar=DEFAULT_LBAR / DEFAULT_TBAR):
    """Marginal product of labor on unenclosed land (same technology)."""
    return mple(te, le, a, th, lbar)


def aplu(te, le, a=0.5, th=1.0, lbar=DEFAULT_LBAR / DEFAULT_TBAR):
    """Average product of labor on unenclosed land."""
    return aple(te, le, a, th, lbar)


def Lambda(th, alp, mu):
    r"""Key pivot term, eq. (23). The single definition of $\Lambda_\mu$ in this package —
    `enclose.loci.lam_mu` delegates here rather than re-deriving it.

    $$\Lambda_\mu = \left(\frac{\alpha\theta}{1-\mu(1-\alpha)}\right)^{\frac{1}{1-\alpha}}$$

    $$\mu = 0 \rightarrow \Lambda = (\alpha \theta)^\frac{1}{1-\alpha}$$
    $$\mu = 1 \rightarrow \Lambda_o = \theta^\frac{1}{1-\alpha}$$

    The denominator is spelled as the appendix writes it, $1-\mu(1-\alpha)$; earlier code
    carried three algebraically-equal spellings of this same quantity across three modules.
    """
    return ((alp * th) / (1 - mu * (1 - alp)))**(1 / (1 - alp))


def theta_H(alp, mu=0.0):
    r"""High-TFP threshold separating strategic complements from substitutes, eq. (24).

    $$\theta_H^\mu = \frac{1}{\alpha} - \mu \cdot \frac{1-\alpha}{\alpha}$$

    Equivalently the $\theta$ at which $\Lambda_\mu = 1$. At $\mu=0$ this is $1/\alpha$;
    at $\mu=1$ it is $1$. Single definition — `tepvt`, `tepvt_g` and the figure layer all
    call this rather than re-spelling it.
    """
    return 1 / alp - mu * (1 - alp) / alp


def req(te, th=1.0, alp=0.5, lbar=1.0, mu=0.0):
    r"""Decentralized equilibrium rental given $t_e$.

    $$r(t_e) = \theta f_T(t_e, l_e(t_e)) \cdot \bar l^\alpha$$
    $$r(t_e) = \frac{(1-\alpha) \theta \Lambda_{\mu}^\alpha}{(1+(\Lambda_{\mu}-1)t_e)^\alpha} \cdot \bar l^\alpha$$
    """
    lam = Lambda(th, alp, mu)
    return (1 - alp) * th * lam**alp * (1 + (lam - 1) * te)**(-alp) * (lbar)**(alp)


def weq(te, th=1.0, alp=0.5, lbar=1.0, mu=0.0):
    r"""Decentralized equilibrium wage.

    $$w(t_e) = \left(1+(\Lambda_{\mu}-1)t_e\right)^{1-\alpha} \cdot \bar l^{\alpha-1}$$
    At $\mu=0$ this equals $MP_L^e$ evaluated at $l_e(t_e)$; for $\mu>0$ it is that
    marginal product scaled by $(1-\mu+\alpha\mu)$.
    """
    lam = Lambda(th, alp, mu)
    return (1 + (lam - 1) * te)**(1 - alp) * (lbar)**(alp - 1)


def le(te, th, alp, mu):
    r"""Private equilibrium labor share on enclosed land for given $t_e$.

    Solves $(1-\mu+\alpha\mu) \cdot APL = MPL$:
    $\mu=0$: $APL^c=MPL^e$, $l_e^*$ in the paper.
    $\mu=1$: $MPL^c=MPL^e$, $l_e^o$ in the paper.
    $\mu \in (0,1)$: partly secure.
    """
    lam = Lambda(th, alp, mu)
    return (lam * te) / (1 + (lam - 1) * te)


def dlete(te, th, alp, mu):
    """d l_e / d t_e."""
    lam = Lambda(th, alp, mu)
    return lam / (1 + (lam - 1) * te)**2


def leo(te, th, alp):
    """Optimal labor allocation (from MPLe = MPLu) given enclosed land share te."""
    return le(te, th, alp, mu=1)


def totalq(te, th, alp, lbar, mu):
    """Total output in the economy given te and mu. Enclosure costs not subtracted."""
    leq = le(te, th, alp, mu)
    return (th * f(te, leq, alp, 1.0) + f(1 - te, 1 - leq, alp, 1.0)) * lbar**alp


def z(te, th, alp, lbar):
    r"""Output per unit land, net of enclosure cost, at the first-best allocation.

    $$z(t_e) = \bar l^\alpha \left(1+(\Lambda_o-1)t_e\right)^{1-\alpha}$$
    """
    lam = th**(1 / (1 - alp))
    return lbar**alp * (1 + (lam - 1) * te)**(1 - alp)


def zpv(te, th, alp, lbar):
    r"""Output per unit land, net of enclosure cost, at the decentralized (mu=0) allocation.

    $$z_d(t_e) = \bar l^\alpha \cdot \frac{1+(\theta\Lambda^{\alpha-1}-1)t_e}{(1+(\Lambda-1)t_e)^\alpha}$$
    """
    lam = Lambda(th, alp, mu=0)
    return lbar**alp * (th * te * lam**alp + (1 - te)) / (1 + (lam - 1) * te)**alp


def zprime(te, th, alp, lbar, mu=1.0):
    r"""Derivative of the planner's z(t_e) function.

    $$z'(t_e) = \bar l^\alpha \cdot (1-\alpha)(\Lambda_o -1) \left(1+(\Lambda_o-1)t_e \right)^{-\alpha}$$
    """
    lam = Lambda(th, alp, mu)
    return (1 - alp) * (lam - 1) * lbar**alp * (1 + (lam - 1) * te)**(-alp)


def teopt(th, alp, c, lbar):
    r"""Planner's optimal enclosure rate.

    $$t_e^o = \frac{\bar l}{(\Lambda_o - 1)} \left[\frac{(1-\alpha)(\Lambda_o - 1)}{c}\right]^\frac{1}{\alpha} - \frac{1}{(\Lambda_o - 1)}$$
    """
    lam = th**(1 / (1 - alp))

    if zprime(0, th, alp, lbar, mu=1) < c:
        teopt_val = 0.0
    elif zprime(1, th, alp, lbar, mu=1) > c:
        teopt_val = 1.0
    else:
        teopt_val = (lbar * (((1 - alp) * (lam - 1)) / c)**(1 / alp) - 1) / (lam - 1)
    return teopt_val


def tepvt(th, alp, c, lbar, mu):
    """Private enclosure rate.

    req(te) = rental rate. r(0)<c: no enclosure. r(1)>c: full enclosure.
    r(0)>c and r(1)<c: partial enclosure, solved from the FOC.
    """
    thresh = theta_H(alp, mu)
    lam = Lambda(th, alp, mu)
    r0 = req(0, th, alp, lbar, mu)
    r1 = req(1, th, alp, lbar, mu)
    if th < thresh:  # r slopes up
        if r0 >= c:
            tep = 1.0
        elif r1 < c:
            tep = 0.0
        else:
            tep = lbar * (lam / (lam - 1)) * (th * (1 - alp) / c)**(1 / alp) - (1 / (lam - 1))
    else:  # r slopes down
        if r1 >= c:
            tep = 1.0
        elif r0 < c:
            tep = 0.0
        else:
            tep = lbar * (lam / (lam - 1)) * (th * (1 - alp) / c)**(1 / alp) - (1 / (lam - 1))

    return tep


def tepvt_g(th, alp, c, lbar, mu):
    """Private enclosure rate under the global-games refinement.

    Like `tepvt` but adjusted for the global game: if theta < theta_hi, the refinement
    says enclose fully if tep (from `tepvt`) <= 0.5, else no enclosure.

    `mu` is threaded through to `tepvt` (a prior version hardcoded `mu=0` here regardless
    of the caller's `mu`, silently discarding it whenever `mu != 0`).
    """
    thresh = theta_H(alp, mu)
    tep = tepvt(th, alp, c, lbar, mu)

    tepg = tep
    if (tep == 1) or (tep == 0):
        tepg = tep
    elif th < thresh:
        if tep > 0.5:
            tepg = 0.0
        elif tep <= 0.5:
            tepg = 1.0

    return tepg


def dwl(th, alp, c, lbar):
    """Deadweight-loss comparison: first-best z minus decentralized (global-games) z, at mu=0."""
    teo = teopt(th, alp, c, lbar)
    teg = tepvt_g(th, alp, c, lbar, mu=0)

    zo = z(teo, th, alp, lbar) - c * teo
    zg = zpv(teg, th, alp, lbar) - c * teg
    return zo, zg


def dwlpct(th, alp, c, lbar):
    """Actual/potential output ratio, at mu=0."""
    teo = teopt(th, alp, c, lbar)
    if th > (1 / alp):
        tep = tepvt(th, alp, c, lbar, mu=0)
    else:
        tep = tepvt_g(th, alp, c, lbar, mu=0)

    zo = z(teo, th, alp, lbar) - c * teo
    zg = zpv(tep, th, alp, lbar) - c * tep
    return zg / zo


def decomp(te, th, alp, mu, lbar):
    """Decomposition of the marginal social benefit of enclosure. Not finished — see notes."""
    lam = Lambda(th, alp, mu)
    FTe = (1 - alp) * th * lam**alp * (1 + (lam - 1) * te)**(-alp)
    FTc = (1 - alp) * th * (1 + (lam - 1) * te)**(-alp)
    return lam, FTe, FTc
