---
title: Mathematical Appendix
short_title: Appendix
---

## A Model of Enclosures: Coordination, Conflict, and Efficiency in the Transformation of Land Property Rights

**Matthew J. Baker and Jonathan Conning**
Hunter College and the Graduate Center, City University of New York

---

## Overview

This online appendix provides complete mathematical derivations for all numbered equations in the main paper. The appendix is organized to mirror the structure of the paper, presenting step-by-step derivations, highlighting key mathematical techniques, and referencing computational implementations for verification.

**Contents:**
- Section 3: Benchmark Model (Equations 1-15)
- Section 4: Social Efficiency Analysis (Equations 16-21)
- Section 5: Extended Model with Institutions (Equations 22-27)
- Section 6: Applications and Extensions (Equations 28-43)
- Appendix G: Computational Verification

## Notation

The paper's symbol table, with a column added for the corresponding name in the
[`enclose`](https://github.com/open-enclose/open-enclose.github.io/tree/main/enclose)
package — so a symbol here can be traced to the code that computes it.

| Symbol | Meaning | Effect of an increase | Key thresholds | In code |
|---|---|---|---|---|
| $\theta$ | TFP gain on enclosed land ($\theta = A_e/A_c$) | Raises the return to enclosing; crossing $\theta_H^\mu$ switches decisions from complements to substitutes, and the risk from over- to under-enclosure | $\theta_H = 1/\alpha$; $\theta = 1$ separates progressive from regressive enclosure | `th` |
| $A$ | Baseline TFP | Enters only as $c/A$: shifts every locus down by the same vertical distance | — | *(absent — see below)* |
| $\alpha$ | Labor share (Cobb–Douglas) | Lowers $\theta_H = 1/\alpha$, shrinking the race-prone complements region | — | `alp`, default `loci.ALP` |
| $\bar l = \bar L/\bar T$ | Population density | Smooth $t_e \uparrow$ if $\theta > \theta_H$; a jump at $\bar l_{gg}^d$ if $\theta < \theta_H$ | Loci $\bar l_0^1, \bar l_1^1, \bar l_0^d, \bar l_1^d, \bar l_{gg}^d, \bar l^s, \dots$ | `lbar`; loci return $\ln\bar l$ |
| $c$ | Enclosure cost per unit land | Shifts every locus up by the same vertical distance — geometrically identical to the economy's point moving down | Enters all loci as $c/A$, each scaling as $(c/A)^{1/\alpha}$ | `c`, default `loci.C` |
| $t_e,\ l_e$ | Shares of land, labor in the enclosed sector | — | — | `te`, `model.le` |
| $\mu \in [0,1]$ | Community capacity to regulate commons access | Shrinks labor misallocation and moves $\theta_H^\mu$ left toward 1; under-enclosure shrinks, but over-enclosure expands if $\tau = 0$ | $\mu=1$: no misallocation; $\theta_H^\mu = \frac{1}{\alpha} - \mu\frac{1-\alpha}{\alpha}$ | `mu` |
| $\tau \in [0,1]$ | Compensation/resistance power of customary users | Raises the density needed before enclosure pays; over-enclosure shrinks, under-enclosure expands | $\tau=1$: "trade"; $\tau=0$: "raid" | `tau` |

:::{note} One fixed canvas
Every locus has the form

$$\ln \bar l = \frac{1}{\alpha}\ln(c/A) + g(\theta)$$

so $\bar l$, $c$ and $A$ never change the shape of the picture — they are the same vertical
movement on one fixed canvas, and only $\mu$ and $\tau$ (through $g$) move the loci
themselves. This is checked rather than asserted: scaling $c/A$ by $k$ shifts
`ln_l01`, `ln_l11`, `ln_ld0`, `ln_ld1`, `ln_gg` and `ln_lm0` by
$\tfrac{1}{\alpha}\ln k$ apiece, agreeing across $\theta$ to $10^{-15}$.

It is also why the package carries no separate `A`: since $c$ and $A$ appear only as the
ratio, `loci.C` **is** the paper's $c/A$. Output and welfare *levels* are consequently in
units of $A$; thresholds and ratios are unaffected.
:::

**Also used in this appendix**, beyond the paper's table:

| Symbol | Meaning | In code |
|---|---|---|
| $\Lambda_\mu = \left(\alpha\theta/A_\mu\right)^{1/(1-\alpha)}$ | Enclosed-to-commons labor intensity; $\Lambda_o = \theta^{1/(1-\alpha)}$ is the planner's | `model.Lambda(th, alp, mu)`, `loci.lam_mu` |
| $A_\mu = 1-\mu(1-\alpha)$ | Share of the commons average product labor retains, eq. (37) | `manufacturing.commons_wedge` |
| $\theta_H^\mu$ | Where $\Lambda_\mu = 1$: enclosure switches labor-extensive to labor-intensive | `model.theta_H(alp, mu)` |
| $\theta_\tau = \tau^{1-\alpha}(A_\mu/\alpha)^{\alpha}$ | Below it enclosure earns less than the compensation owed, at any density — eq. (27b) | `loci.theta_tau(alp, mu, tau)` |
| $\bar T,\ \bar L,\ \bar K$ | Total land, labor, capital endowments; $\bar t = \bar T/\bar L$, $\bar k = \bar K/\bar L$ | `tbar`, `lbar`, `kb` |
| $l_c,\ l_m$ | Labor shares in the commons and in manufacturing (§6.4) | `manufacturing.labor_share` |
| $\beta \in (0,1)$, $p > 0$ | Manufacturing labor share and relative price (§6.4) | `b`, `p` |

:::{note} On $\Lambda$, and its correspondence with the paper's notation
This appendix carries the composite

$$\Lambda_\mu = \left(\frac{\alpha\theta}{A_\mu}\right)^{\frac{1}{1-\alpha}},
\qquad \Lambda_0 = (\alpha\theta)^{\frac{1}{1-\alpha}},
\qquad \Lambda_1 = \Lambda_o = \theta^{\frac{1}{1-\alpha}}$$

throughout, because every equilibrium object is a function of it and the closed forms are
unreadable without it. **The main paper deliberately avoids $\Lambda$**, writing the same
expressions in terms of $\alpha$ and $\theta$ directly. The two are related by

$$\Lambda_\mu^{1-\alpha} = \frac{\alpha\theta}{A_\mu},
\qquad\text{so at } \mu=0: \quad \Lambda^{1-\alpha} = \alpha\theta$$

which is the substitution that turns any expression here into the paper's form. Two
consequences are worth keeping in view when moving between the documents:

- A factor written $(1-\alpha\theta)$ in the paper appears here as
  $-(\Lambda^{1-\alpha}-1)$. Both vanish at $\theta_H = 1/\alpha$; the paper's form reads
  more directly as *distance from the threshold*, which is why it is preferred there.
- The $\Lambda$ form is what generalizes. Writing $\alpha\theta$ silently fixes $\mu=0$,
  because in general $\Lambda_\mu^{1-\alpha} = \alpha\theta/A_\mu$. Extensions to $\mu$
  should be done in the $\Lambda_\mu$ form and simplified afterwards, not the reverse —
  the governance wedge is easy to lose otherwise.
:::

---

## Section 3: Benchmark Model

### 3.1 Technology and Resources

We begin by establishing the production technology and key relationships. Production in both enclosed and unenclosed sectors follows Cobb-Douglas technology:

**Unenclosed sector:**
$$F(T_c, L_c) = T_c^{1-\alpha}L_c^\alpha$$

**Enclosed sector:**
$$G(T_e, L_e) = \theta \cdot T_e^{1-\alpha}L_e^\alpha$$

where $\theta \geq 1$ captures potential productivity gains from enclosure.

#### Key Property: Homogeneity of Production

For Cobb-Douglas production with constant returns to scale, we have the useful property:

$$F(t_e\bar{T}, l_e\bar{L}) = (t_e\bar{T})^{1-\alpha}(l_e\bar{L})^\alpha = t_e^{1-\alpha}\bar{T}^{1-\alpha} \cdot l_e^\alpha\bar{L}^\alpha = F(t_e, l_e) \cdot F(\bar{T}, \bar{L})$$

This allows us to factor out the scale $F(\bar{T}, \bar{L})$ and work with shares.

#### Potential Output per Unit Land

We define:
$$A\bar{l}^\alpha = A \cdot \frac{F(\bar{T}, \bar{L})}{\bar{T}} = A \cdot \frac{\bar{T}^{1-\alpha}\bar{L}^\alpha}{\bar{T}} = A\left(\frac{\bar{L}}{\bar{T}}\right)^\alpha = A\bar{l}^\alpha$$

This represents potential output per unit land using the base technology, and serves as a convenient normalization throughout.

---

### 3.2 First-Best Labor Allocation and Enclosure

#### Equation (1): Social Planner's Objective

The social planner maximizes total output net of enclosure costs:

$$\max_{t_e, l_e} A\left[\theta F(t_e\bar{T}, l_e\bar{L}) + F((1-t_e)\bar{T}, (1-l_e)\bar{L})\right] - ct_e\bar{T} \qquad (1)$$

**Derivation:**
- Total output = output from enclosed sector + output from unenclosed sector
- Enclosed sector produces: $A\theta F(t_e\bar{T}, l_e\bar{L})$
- Unenclosed sector produces: $AF((1-t_e)\bar{T}, (1-l_e)\bar{L})$
- Cost of enclosing share $t_e$ of total land $\bar{T}$: $ct_e\bar{T}$

---

#### Equation (2): Normalized Planner's Objective

Using the homogeneity property, we can rewrite (1) as:

$$\max_{t_e, l_e} \left[\theta F(t_e, l_e) + F(1-t_e, 1-l_e)\right] \cdot A\bar{l}^\alpha - c \cdot t_e \qquad (2)$$

**Derivation:**
Starting from (1):
$$A\left[\theta F(t_e\bar{T}, l_e\bar{L}) + F((1-t_e)\bar{T}, (1-l_e)\bar{L})\right] - ct_e\bar{T}$$

Factor out $F(\bar{T}, \bar{L})$ from each production term:
$$= A\left[\theta F(t_e, l_e) \cdot F(\bar{T}, \bar{L}) + F(1-t_e, 1-l_e) \cdot F(\bar{T}, \bar{L})\right] - ct_e\bar{T}$$

$$= A F(\bar{T}, \bar{L})\left[\theta F(t_e, l_e) + F(1-t_e, 1-l_e)\right] - ct_e\bar{T}$$

Divide the objective by $\bar{T}$ (which doesn't affect the maximizing choices):
$$= \frac{AF(\bar{T}, \bar{L})}{\bar{T}}\left[\theta F(t_e, l_e) + F(1-t_e, 1-l_e)\right] - ct_e$$

$$= A\bar{l}^\alpha\left[\theta F(t_e, l_e) + F(1-t_e, 1-l_e)\right] - ct_e$$

This formulation isolates the allocation problem (choosing $t_e, l_e$) from scale effects.

---

#### Equation (3): Marginal Product Equalization

The first-order condition with respect to $l_e$ yields:

$$\theta \alpha A\left(\frac{t_e}{l_e}\right)^{1-\alpha} = \alpha A\left(\frac{1-t_e}{1-l_e}\right)^{1-\alpha} \qquad (3)$$

**Derivation:**
From (2), the objective is:
$$\left[\theta t_e^{1-\alpha}l_e^\alpha + (1-t_e)^{1-\alpha}(1-l_e)^\alpha\right] \cdot A\bar{l}^\alpha - ct_e$$

Take the derivative with respect to $l_e$:
$$\frac{\partial}{\partial l_e}\left[\theta t_e^{1-\alpha}l_e^\alpha + (1-t_e)^{1-\alpha}(1-l_e)^\alpha\right] \cdot A\bar{l}^\alpha = 0$$

Apply the power rule:
$$\left[\theta t_e^{1-\alpha} \cdot \alpha l_e^{\alpha-1} + (1-t_e)^{1-\alpha} \cdot \alpha(1-l_e)^{\alpha-1} \cdot (-1)\right] \cdot A\bar{l}^\alpha = 0$$

Simplify:
$$\theta \alpha t_e^{1-\alpha}l_e^{\alpha-1} = \alpha(1-t_e)^{1-\alpha}(1-l_e)^{\alpha-1}$$

Divide both sides by $\alpha$ and rearrange:
$$\theta t_e^{1-\alpha}l_e^{\alpha-1} = (1-t_e)^{1-\alpha}(1-l_e)^{\alpha-1}$$

Rewrite as:
$$\theta \left(\frac{t_e}{l_e}\right)^{1-\alpha} = \left(\frac{1-t_e}{1-l_e}\right)^{1-\alpha}$$

This states that the planner equalizes the marginal product of labor across sectors.

---

#### Equation (4): First-Best Labor Allocation Function

Solving (3) for $l_e$ as a function of $t_e$:

$$l_e^1(t_e) = \frac{\theta^{\frac{1}{1-\alpha}}t_e}{1+\left(\theta^{\frac{1}{1-\alpha}}-1\right)t_e} \qquad (4)$$

**Derivation:**
Starting from (3):
$$\theta \left(\frac{t_e}{l_e}\right)^{1-\alpha} = \left(\frac{1-t_e}{1-l_e}\right)^{1-\alpha}$$

Take both sides to the power $\frac{1}{1-\alpha}$:
$$\theta^{\frac{1}{1-\alpha}} \cdot \frac{t_e}{l_e} = \frac{1-t_e}{1-l_e}$$

**Define** $\Lambda_o = \theta^{\frac{1}{1-\alpha}}$ for convenience. Then:
$$\Lambda_o \cdot \frac{t_e}{l_e} = \frac{1-t_e}{1-l_e}$$

Cross-multiply:
$$\Lambda_o t_e(1-l_e) = l_e(1-t_e)$$

Expand:
$$\Lambda_o t_e - \Lambda_o t_e l_e = l_e - l_e t_e$$

Collect terms with $l_e$ on the left:
$$\Lambda_o t_e = l_e + \Lambda_o t_e l_e - l_e t_e$$

$$\Lambda_o t_e = l_e(1 + \Lambda_o t_e - t_e)$$

$$\Lambda_o t_e = l_e(1 + (\Lambda_o - 1)t_e)$$

Solve for $l_e$:
$$l_e = \frac{\Lambda_o t_e}{1+(\Lambda_o-1)t_e}$$

This is the planner's optimal labor allocation function, showing how labor should be distributed for any given enclosure rate $t_e$.

---

#### Equation (5): Simplified Planner's Objective

Substituting $l_e^1(t_e)$ into the objective (2) yields:

$$\max_{t_e} z_1(t_e) - c \cdot t_e$$

where
$$z_1(t_e) = \left[1+\left(\theta^{\frac{1}{1-\alpha}}-1\right)t_e\right]^{1-\alpha} \cdot A\bar{l}^\alpha \qquad (5)$$

**Derivation:**
This is a crucial simplification. Starting from (2) with $l_e = l_e^1(t_e) = \frac{\Lambda_o t_e}{1+(\Lambda_o-1)t_e}$:

$$z_1(t_e) = \left[\theta t_e^{1-\alpha}l_e^\alpha + (1-t_e)^{1-\alpha}(1-l_e)^\alpha\right] \cdot A\bar{l}^\alpha$$

Let's break this into two terms: $A = \theta t_e^{1-\alpha}l_e^\alpha$ and $B = (1-t_e)^{1-\alpha}(1-l_e)^\alpha$.

**Term A:**
$$A = \theta t_e^{1-\alpha}\left(\frac{\Lambda_o t_e}{1+(\Lambda_o-1)t_e}\right)^\alpha$$

$$= \theta t_e^{1-\alpha} \cdot \frac{(\Lambda_o t_e)^\alpha}{(1+(\Lambda_o-1)t_e)^\alpha}$$

$$= \theta \cdot \frac{t_e^{1-\alpha} \cdot t_e^\alpha \cdot \Lambda_o^\alpha}{(1+(\Lambda_o-1)t_e)^\alpha}$$

$$= \theta \cdot \frac{t_e \cdot \Lambda_o^\alpha}{(1+(\Lambda_o-1)t_e)^\alpha}$$

**Key Mathematical Trick:** Note that $\theta \cdot \Lambda_o^\alpha = \theta \cdot (\theta^{\frac{1}{1-\alpha}})^\alpha = \theta \cdot \theta^{\frac{\alpha}{1-\alpha}} = \theta^{1+\frac{\alpha}{1-\alpha}} = \theta^{\frac{1-\alpha+\alpha}{1-\alpha}} = \theta^{\frac{1}{1-\alpha}} = \Lambda_o$

Therefore:
$$A = \frac{\Lambda_o t_e}{(1+(\Lambda_o-1)t_e)^\alpha}$$

**Term B:**
First note that:
$$1-l_e = 1 - \frac{\Lambda_o t_e}{1+(\Lambda_o-1)t_e} = \frac{1+(\Lambda_o-1)t_e - \Lambda_o t_e}{1+(\Lambda_o-1)t_e} = \frac{1-t_e}{1+(\Lambda_o-1)t_e}$$

Thus:
$$B = (1-t_e)^{1-\alpha}\left(\frac{1-t_e}{1+(\Lambda_o-1)t_e}\right)^\alpha$$

$$= \frac{(1-t_e)^{1-\alpha}(1-t_e)^\alpha}{(1+(\Lambda_o-1)t_e)^\alpha}$$

$$= \frac{1-t_e}{(1+(\Lambda_o-1)t_e)^\alpha}$$

**Combining A and B:**
$$A + B = \frac{\Lambda_o t_e + (1-t_e)}{(1+(\Lambda_o-1)t_e)^\alpha}$$

$$= \frac{1 + (\Lambda_o-1)t_e}{(1+(\Lambda_o-1)t_e)^\alpha}$$

$$= (1+(\Lambda_o-1)t_e)^{1-\alpha}$$

Therefore:
$$z_1(t_e) = (1+(\Lambda_o-1)t_e)^{1-\alpha} \cdot A\bar{l}^\alpha$$

This elegant closed form shows that output is increasing and concave in $t_e$ when $\theta > 1$ (so $\Lambda_o > 1$).

---

#### Equation (6): No-Enclosure Threshold

The planner chooses no enclosure when:

$$z_1'(0) \leq c \Leftrightarrow \bar{l} \leq \left[\frac{1}{(1-\alpha)\left(\theta^{\frac{1}{1-\alpha}}-1\right)} \cdot \frac{c}{A}\right]^{\frac{1}{\alpha}} = \bar{l}_0^1(\theta) \qquad (6)$$

**Derivation:**
First, compute $z_1'(t_e)$:
$$z_1(t_e) = A\bar{l}^\alpha \cdot (1+(\Lambda_o-1)t_e)^{1-\alpha}$$

$$z_1'(t_e) = A\bar{l}^\alpha \cdot (1-\alpha)(1+(\Lambda_o-1)t_e)^{-\alpha} \cdot (\Lambda_o-1)$$

$$= (1-\alpha)(\Lambda_o-1) \cdot A\bar{l}^\alpha \cdot (1+(\Lambda_o-1)t_e)^{-\alpha}$$

Evaluate at $t_e = 0$:
$$z_1'(0) = (1-\alpha)(\Lambda_o-1) \cdot A\bar{l}^\alpha$$

For no enclosure to be optimal, we need $z_1'(0) \leq c$:
$$(1-\alpha)(\Lambda_o-1) \cdot A\bar{l}^\alpha \leq c$$

Solve for $\bar{l}$:
$$\bar{l}^\alpha \leq \frac{c}{(1-\alpha)(\Lambda_o-1)A}$$

$$\bar{l} \leq \left[\frac{c}{(1-\alpha)(\Lambda_o-1)A}\right]^{\frac{1}{\alpha}}$$

Substituting $\Lambda_o = \theta^{\frac{1}{1-\alpha}}$:
$$\bar{l}_0^1(\theta) = \left[\frac{1}{(1-\alpha)(\theta^{\frac{1}{1-\alpha}}-1)} \cdot \frac{c}{A}\right]^{\frac{1}{\alpha}}$$

This defines a threshold population density below which enclosure is not worthwhile.

---

#### Equation (7): Full-Enclosure Threshold

The planner chooses full enclosure when:

$$z_1'(1) \geq c \Leftrightarrow \bar{l} \geq \theta^{\frac{1}{1-\alpha}} \cdot \bar{l}_0^1(\theta) = \bar{l}_1^1(\theta) \qquad (7)$$

**Derivation:**
Evaluate $z_1'(t_e)$ at $t_e = 1$:
$$z_1'(1) = (1-\alpha)(\Lambda_o-1) \cdot A\bar{l}^\alpha \cdot (1+(\Lambda_o-1))^{-\alpha}$$

$$= (1-\alpha)(\Lambda_o-1) \cdot A\bar{l}^\alpha \cdot \Lambda_o^{-\alpha}$$

For full enclosure to be optimal, we need $z_1'(1) \geq c$:
$$(1-\alpha)(\Lambda_o-1) \cdot A\bar{l}^\alpha \cdot \Lambda_o^{-\alpha} \geq c$$

$$\bar{l}^\alpha \geq \frac{c \cdot \Lambda_o^\alpha}{(1-\alpha)(\Lambda_o-1)A}$$

$$\bar{l} \geq \left[\frac{c \cdot \Lambda_o^\alpha}{(1-\alpha)(\Lambda_o-1)A}\right]^{\frac{1}{\alpha}}$$

Note that this can be written as:
$$\bar{l}_1^1 = \Lambda_o \cdot \left[\frac{c}{(1-\alpha)(\Lambda_o-1)A}\right]^{\frac{1}{\alpha}} = \Lambda_o \cdot \bar{l}_0^1 = \theta^{\frac{1}{1-\alpha}} \cdot \bar{l}_0^1(\theta)$$

This shows that the full enclosure threshold is exactly $\Lambda_o$ times the no-enclosure threshold.

**Summary of First-Best:** The planner chooses:
- No enclosure if $\bar{l} \leq \bar{l}_0^1$
- Partial enclosure if $\bar{l}_0^1 < \bar{l} < \bar{l}_1^1$ (where $z_1'(t_e^*) = c$)
- Full enclosure if $\bar{l} \geq \bar{l}_1^1$

```{figure} ../Figures/social_opt_cond.png
:name: appendix-fig-1
:width: 90%

Socially efficient enclosure regions.
```

---

### 3.3 Decentralized Enclosure Processes

#### Equation (8): Average Product Decomposition

By Euler's theorem for homogeneous functions:

$$AP_L^c = MP_L^c + MP_T^c \cdot \frac{T_c}{L_c} \qquad (8)$$

**Derivation:**
For a homogeneous function of degree one (constant returns to scale), Euler's theorem states:
$$F(T, L) = T \cdot F_T + L \cdot F_L$$

where $F_T = \frac{\partial F}{\partial T}$ and $F_L = \frac{\partial F}{\partial L}$.

Divide both sides by $L$:
$$\frac{F(T,L)}{L} = \frac{T}{L} \cdot F_T + F_L$$

In other notation:
$$AP_L = MP_L + MP_T \cdot \frac{T}{L}$$

This decomposition is crucial: it shows that average product exceeds marginal product by the amount $MP_T \cdot (T/L)$, which represents the **possession rent** that labor captures under open access when it must occupy land.

---

#### Equation (9): Labor Market Equilibrium (Decentralized)

Under open access to unenclosed land, labor equilibrium requires:

$$\theta \alpha A\left(\frac{t_e}{l_e}\right)^{1-\alpha} = A\left(\frac{1-t_e}{1-l_e}\right)^{1-\alpha} \qquad (9)$$

**Derivation:**
In the enclosed sector, competitive firms pay labor its marginal product:
$$w_e = MP_L^e = \theta \alpha A\left(\frac{t_e}{l_e}\right)^{1-\alpha} \cdot \bar{l}^\alpha$$

In the unenclosed (common) sector under open access, labor captures the **average product** (not marginal product) because workers must possess land to produce:
$$w_c = AP_L^c = A\frac{F(1-t_e, 1-l_e)}{1-l_e} \cdot \bar{l}^\alpha = A\left(\frac{1-t_e}{1-l_e}\right)^{1-\alpha} \cdot \bar{l}^\alpha$$

Labor mobility requires $w_e = w_c$:
$$\theta \alpha A\left(\frac{t_e}{l_e}\right)^{1-\alpha} \cdot \bar{l}^\alpha = A\left(\frac{1-t_e}{1-l_e}\right)^{1-\alpha} \cdot \bar{l}^\alpha$$

Cancel $A\bar{l}^\alpha$ to get (9).

The key difference from (3) is the $\alpha$ multiplier on the left-hand side, reflecting that labor earns only its marginal product in the enclosed sector but captures the average product in the commons.

---

#### Equation (10): Labor Reaction Function (Decentralized)

Solving (9) for $l_e$ yields:

$$l_e^0(t_e) = \frac{(\alpha\theta)^{\frac{1}{1-\alpha}}t_e}{1+\left((\alpha\theta)^{\frac{1}{1-\alpha}}-1\right)t_e} \qquad (10)$$

**Derivation:**
From (9):
$$\theta \alpha \left(\frac{t_e}{l_e}\right)^{1-\alpha} = \left(\frac{1-t_e}{1-l_e}\right)^{1-\alpha}$$

Raise both sides to power $\frac{1}{1-\alpha}$:
$$(\alpha\theta)^{\frac{1}{1-\alpha}} \cdot \frac{t_e}{l_e} = \frac{1-t_e}{1-l_e}$$

**Define** $\Lambda = (\alpha\theta)^{\frac{1}{1-\alpha}}$ (note: different from $\Lambda_o = \theta^{\frac{1}{1-\alpha}}$!).

Then following identical algebraic steps to equation (4):
$$\Lambda \cdot \frac{t_e}{l_e} = \frac{1-t_e}{1-l_e}$$

Cross-multiply and solve:
$$l_e = \frac{\Lambda t_e}{1+(\Lambda-1)t_e}$$

**Critical Distinction:** Under decentralized enclosure with open-access commons, $\Lambda = (\alpha\theta)^{\frac{1}{1-\alpha}}$ whereas the planner uses $\Lambda_o = \theta^{\frac{1}{1-\alpha}}$. Since $\alpha < 1$, we have $\Lambda < \Lambda_o$, meaning the decentralized economy allocates **less labor to enclosed land** than is socially optimal (for any given $t_e$). This is the labor misallocation at the heart of the inefficiency.

---

#### Equation (11): Private Return to Enclosure (General Form)

A private encloser's return is:

$$r(t_e) = \theta \cdot AF_T(t_e\bar{T}, l_e^0(t_e)\bar{L}) \qquad (11)$$

**Derivation:**
An encloser captures the marginal product of land in the enclosed sector. For Cobb-Douglas:
$$F_T = (1-\alpha) \cdot \frac{F(T,L)}{T} = (1-\alpha)T^{-\alpha}L^\alpha$$

Therefore:
$$r(t_e) = \theta A(1-\alpha)(t_e\bar{T})^{-\alpha}(l_e^0(t_e)\bar{L})^\alpha$$

$$= \theta A(1-\alpha) \cdot t_e^{-\alpha}\bar{T}^{-\alpha} \cdot l_e^\alpha\bar{L}^\alpha$$

$$= \theta A(1-\alpha) \cdot \left(\frac{l_e}{t_e}\right)^\alpha \cdot \bar{l}^\alpha$$

This is the rental rate per unit enclosed land, which depends on the labor intensity $l_e/t_e$.

---

#### Equation (12): Private Return to Enclosure (Closed Form)

Substituting $l_e^0(t_e)$ from (10):

$$r(t_e) = \theta(1-\alpha)A\bar{l}^\alpha \cdot \left(\frac{(\alpha\theta)^{\frac{1}{1-\alpha}}}{1+\left((\alpha\theta)^{\frac{1}{1-\alpha}}-1\right)t_e}\right)^\alpha \qquad (12)$$

**Derivation:**
From (11):
$$r(t_e) = \theta A(1-\alpha) \cdot \left(\frac{l_e^0(t_e)}{t_e}\right)^\alpha \cdot \bar{l}^\alpha$$

From (10), we have:
$$\frac{l_e^0(t_e)}{t_e} = \frac{\Lambda}{1+(\Lambda-1)t_e}$$

where $\Lambda = (\alpha\theta)^{\frac{1}{1-\alpha}}$.

Substitute:
$$r(t_e) = \theta A(1-\alpha) \cdot \left(\frac{\Lambda}{1+(\Lambda-1)t_e}\right)^\alpha \cdot \bar{l}^\alpha$$

**Alternative form using mathematical trick:**
Note that $\theta \cdot \Lambda^\alpha = \theta \cdot [(\alpha\theta)^{\frac{1}{1-\alpha}}]^\alpha = \theta \cdot (\alpha\theta)^{\frac{\alpha}{1-\alpha}}$

$$= \theta^{1+\frac{\alpha}{1-\alpha}} \cdot \alpha^{\frac{\alpha}{1-\alpha}} = \theta^{\frac{1}{1-\alpha}} \cdot \alpha^{\frac{\alpha}{1-\alpha}}$$

Actually, more directly:
$$\theta \cdot \Lambda^\alpha = \theta \cdot (\alpha\theta)^{\frac{\alpha}{1-\alpha}} = \alpha^{\frac{\alpha}{1-\alpha}} \cdot \theta^{1+\frac{\alpha}{1-\alpha}} = \alpha^{\frac{\alpha}{1-\alpha}} \cdot \theta^{\frac{1}{1-\alpha}}$$

$$= \frac{1}{\alpha} \cdot \alpha^{\frac{\alpha}{1-\alpha}+1} \cdot \theta^{\frac{1}{1-\alpha}} = \frac{1}{\alpha} \cdot \alpha^{\frac{1}{1-\alpha}} \cdot \theta^{\frac{1}{1-\alpha}} = \frac{\Lambda}{\alpha}$$

So we can write:
$$r(t_e) = (1-\alpha)A\bar{l}^\alpha \cdot \frac{\Lambda}{\alpha} \cdot \frac{\Lambda^{\alpha-1}}{(1+(\Lambda-1)t_e)^\alpha}$$

This simplifies to the form in (12).

**Key Properties:**
- When $\theta \geq \theta_H = 1/\alpha$ (so $\Lambda \geq 1$), we have $r'(t_e) < 0$: enclosure decisions are **strategic substitutes**
- When $\theta < \theta_H$, we have $r'(t_e) > 0$: enclosure decisions are **strategic complements**

---

#### Equation (13): No-Enclosure Threshold (Decentralized)

Private enclosers begin enclosing when:

$$r(0) \geq c \Leftrightarrow \bar{l} \geq \frac{1}{(\alpha\theta)^{\frac{1}{1-\alpha}}} \left[\frac{c}{\theta A(1-\alpha)}\right]^{\frac{1}{\alpha}} = \bar{l}_0^d \qquad (13)$$

**Derivation:**
Evaluate $r(t_e)$ at $t_e = 0$:
$$r(0) = \theta(1-\alpha)A\bar{l}^\alpha \cdot \Lambda^\alpha$$

where $\Lambda = (\alpha\theta)^{\frac{1}{1-\alpha}}$.

Set $r(0) = c$:
$$\theta(1-\alpha)A\bar{l}^\alpha \cdot \Lambda^\alpha = c$$

Solve for $\bar{l}$:
$$\bar{l}^\alpha = \frac{c}{\theta(1-\alpha)A \cdot \Lambda^\alpha}$$

$$\bar{l} = \left[\frac{c}{\theta(1-\alpha)A \cdot \Lambda^\alpha}\right]^{\frac{1}{\alpha}}$$

$$= \Lambda^{-1} \cdot \left[\frac{c}{\theta(1-\alpha)A}\right]^{\frac{1}{\alpha}}$$

$$= \frac{1}{(\alpha\theta)^{\frac{1}{1-\alpha}}} \left[\frac{c}{\theta(1-\alpha)A}\right]^{\frac{1}{\alpha}}$$

---

#### Equation (14): Full-Enclosure Threshold (Decentralized)

Private enclosers fully enclose when:

$$r(1) \geq c \Leftrightarrow \bar{l} \geq \left[\frac{c}{\theta A(1-\alpha)}\right]^{\frac{1}{\alpha}} = \bar{l}_1^d \qquad (14)$$

**Derivation:**
Evaluate $r(t_e)$ at $t_e = 1$:
$$r(1) = \theta(1-\alpha)A\bar{l}^\alpha \cdot \left(\frac{\Lambda}{1+(\Lambda-1)}\right)^\alpha = \theta(1-\alpha)A\bar{l}^\alpha \cdot \frac{\Lambda^\alpha}{\Lambda^\alpha} = \theta(1-\alpha)A\bar{l}^\alpha$$

Set $r(1) = c$:
$$\theta(1-\alpha)A\bar{l}^\alpha = c$$

$$\bar{l} = \left[\frac{c}{\theta(1-\alpha)A}\right]^{\frac{1}{\alpha}}$$

**Note:** $\bar{l}_1^d = \Lambda \cdot \bar{l}_0^d$, similar to the first-best relationship.

```{figure} ../Figures/nash_so_comp.png
:name: appendix-fig-2
:width: 90%

Decentralized enclosure regions, including the multiplicity region.
```

---

#### Equation (15): Global Games Threshold (Risk-Dominant Equilibrium)

In the multiplicity region where $\theta < \theta_H$, the unique risk-dominant equilibrium involves full enclosure when:

$$E[r(t_e) - c] \geq 0 \Leftrightarrow \bar{l} \geq \bar{l}_{gg}^d \qquad (15)$$

**Derivation:**
The global games refinement (Morris and Shin 2003) selects the equilibrium where the expected return to enclosure equals the cost:

$$\int_0^1 r(t_e) dt_e = c$$

Substituting $r(t_e)$ from (12):
$$\int_0^1 \theta(1-\alpha)A\bar{l}^\alpha \cdot \left(\frac{\Lambda}{1+(\Lambda-1)t_e}\right)^\alpha dt_e = c$$

Only the bracket depends on $t_e$. The substitution $u = 1+(\Lambda-1)t_e$ reduces the integral to a power rule:

$$\int_0^1\left(1+(\Lambda-1)t_e\right)^{-\alpha}dt_e
= \frac{1}{\Lambda-1}\int_1^{\Lambda}u^{-\alpha}\,du
= \frac{\Lambda^{1-\alpha}-1}{(1-\alpha)(\Lambda-1)}$$

The factor $(1-\alpha)$ cancels, and solving for population density gives the threshold in closed form:

$$\bar{l}_{gg}^d = \left[\frac{(c/A)\left(\Lambda-1\right)}
{\theta\Lambda^{\alpha}\left(\Lambda^{1-\alpha}-1\right)}\right]^{\frac{1}{\alpha}}$$

Since $\Lambda^{1-\alpha} = \alpha\theta$ by construction of $\Lambda$, this is equivalently

$$\bar{l}_{gg}^d = \left[\frac{(c/A)(1-\Lambda)}{\theta\Lambda^{\alpha}\,(1-\alpha\theta)}\right]^{\frac{1}{\alpha}}$$

which is the form used in the code. In the multiplicity region $\Lambda<1$ and $\alpha\theta<1$, so both the numerator and the denominator are positive.

**Note:** No special functions are needed — the integrand is a power of a linear function of $t_e$. (Earlier versions of this appendix stated that the evaluation involves a beta function and requires numerical integration. Both were incorrect; the closed form above is elementary, and is what the accompanying code has always used.)

*[End of Section 3]*

---

## Section 4: Social Efficiency of Private Enclosure Decisions

### 4.1 Are Decentralized Enclosures Second-Best?

We now ask whether decentralized enclosure decisions are at least "second-best" efficient—that is, optimal given the constraint that labor is misallocated due to open access. A **second-best** (or constrained) planner respects the labor allocation $l_e^0(t_e)$ that emerges from decentralized labor markets but can control the enclosure rate $t_e$.

#### Equation (16): Second-Best Planner's Objective

The second-best planner maximizes:

$$z_0(t_e) = \left[\theta F(t_e, l_e^0(t_e)) + F(1-t_e, 1-l_e^0(t_e))\right] \cdot A\bar{l}^\alpha \qquad (16)$$

subject to the constraint that labor allocation follows $l_e^0(t_e)$ from equation (10), not the first-best $l_e^1(t_e)$.

**Comparison to First-Best:**
- First-best uses $l_e^1(t_e) = \frac{\Lambda_o t_e}{1+(\Lambda_o-1)t_e}$ where $\Lambda_o = \theta^{\frac{1}{1-\alpha}}$
- Second-best uses $l_e^0(t_e) = \frac{\Lambda t_e}{1+(\Lambda-1)t_e}$ where $\Lambda = (\alpha\theta)^{\frac{1}{1-\alpha}}$

Since $\Lambda < \Lambda_o$, the second-best involves labor misallocation toward the unenclosed sector.

---

#### Equation (17): Second-Best Objective (Closed Form)

Substituting $l_e^0(t_e)$ yields:

$$z_0(t_e) = \bar{l}^\alpha \cdot \frac{\theta(\alpha\theta)^{\frac{\alpha}{1-\alpha}}t_e + (1-t_e)}{\left(1+\left((\alpha\theta)^{\frac{1}{1-\alpha}}-1\right)t_e\right)^\alpha} \qquad (17)$$

or equivalently:
$$z_0(t_e) = \bar{l}^\alpha \cdot \frac{1+\left(\frac{\Lambda}{\alpha}-1\right)t_e}{(1+(\Lambda-1)t_e)^\alpha}$$

**Derivation:**
Following the same approach as equation (5), we substitute $l_e^0(t_e) = \frac{\Lambda t_e}{1+(\Lambda-1)t_e}$ into:

$$z_0(t_e) = \left[\theta t_e^{1-\alpha}(l_e^0)^\alpha + (1-t_e)^{1-\alpha}(1-l_e^0)^\alpha\right] \cdot A\bar{l}^\alpha$$

Break into terms $A = \theta t_e^{1-\alpha}(l_e^0)^\alpha$ and $B = (1-t_e)^{1-\alpha}(1-l_e^0)^\alpha$.

**Term A:**
$$A = \theta t_e^{1-\alpha}\left(\frac{\Lambda t_e}{1+(\Lambda-1)t_e}\right)^\alpha = \theta \cdot \frac{t_e \cdot \Lambda^\alpha}{(1+(\Lambda-1)t_e)^\alpha}$$

**Mathematical Trick:** Recall from equation (12) that:
$$\theta \cdot \Lambda^\alpha = \theta \cdot (\alpha\theta)^{\frac{\alpha}{1-\alpha}} = \frac{\Lambda}{\alpha}$$

(Proof: $\theta \cdot (\alpha\theta)^{\frac{\alpha}{1-\alpha}} = \theta^{1+\frac{\alpha}{1-\alpha}} \cdot \alpha^{\frac{\alpha}{1-\alpha}} = \theta^{\frac{1}{1-\alpha}} \cdot \alpha^{\frac{\alpha}{1-\alpha}} = (\alpha\theta)^{\frac{1}{1-\alpha}} \cdot \alpha^{-1} = \frac{\Lambda}{\alpha}$)

Therefore:
$$A = \frac{1}{\alpha} \cdot \frac{\Lambda t_e}{(1+(\Lambda-1)t_e)^\alpha}$$

**Term B:**
As before, $1-l_e^0 = \frac{1-t_e}{1+(\Lambda-1)t_e}$, so:
$$B = \frac{1-t_e}{(1+(\Lambda-1)t_e)^\alpha}$$

**Combining:**
$$A + B = \frac{\frac{\Lambda}{\alpha}t_e + (1-t_e)}{(1+(\Lambda-1)t_e)^\alpha} = \frac{1+(\frac{\Lambda}{\alpha}-1)t_e}{(1+(\Lambda-1)t_e)^\alpha}$$

Alternatively, using $\theta \Lambda^\alpha = \Lambda/\alpha$:
$$z_0(t_e) = \bar{l}^\alpha \cdot \frac{\theta \Lambda^\alpha t_e + (1-t_e)}{(1+(\Lambda-1)t_e)^\alpha}$$

**Note:** Unlike the first-best $z_1(t_e) = \bar{l}^\alpha(1+(\Lambda_o-1)t_e)^{1-\alpha}$ which is always concave, $z_0(t_e)$ can be either concave or convex depending on $\theta$ relative to $\theta_H = 1/\alpha$.

---

#### Equation (18): Second-Best Threshold (Low-TFP Region)

When $\theta < \theta_H = 1/\alpha$ (so $\Lambda < 1$), the objective $z_0(t_e)$ is convex. The second-best planner chooses full enclosure when:

$$z_0(1) - c \geq z_0(0) \Leftrightarrow \bar{l} \geq \left[\frac{c}{A(\theta-1)}\right]^{\frac{1}{\alpha}} = \bar{l}^s \qquad (18)$$

**Derivation:**
With convex objective, compare corner solutions.

**At $t_e = 0$:**
$$z_0(0) = \bar{l}^\alpha \cdot \frac{1}{1} = \bar{l}^\alpha$$

**At $t_e = 1$:**
$$z_0(1) = \bar{l}^\alpha \cdot \frac{1+(\frac{\Lambda}{\alpha}-1)}{\Lambda^\alpha} = \bar{l}^\alpha \cdot \frac{\frac{\Lambda}{\alpha}}{\Lambda^\alpha} = \bar{l}^\alpha \cdot \frac{1}{\alpha\Lambda^{\alpha-1}}$$

Actually, let's compute more carefully. At $t_e=1$:
- Numerator: $\theta \Lambda^\alpha \cdot 1 + (1-1) = \theta \Lambda^\alpha = \frac{\Lambda}{\alpha}$
- Denominator: $(1+(\Lambda-1) \cdot 1)^\alpha = \Lambda^\alpha$

$$z_0(1) = \bar{l}^\alpha \cdot \frac{\Lambda/\alpha}{\Lambda^\alpha} = \bar{l}^\alpha \cdot \frac{1}{\alpha \Lambda^{\alpha-1}}$$

Hmm, let me reconsider. Actually for Cobb-Douglas when all land is enclosed:
$$z_0(1) = A[\theta \cdot 1^{1-\alpha} \cdot 1^\alpha + 0] \cdot \bar{l}^\alpha = A\theta\bar{l}^\alpha$$

And at $t_e=0$:
$$z_0(0) = A[0 + 1^{1-\alpha} \cdot 1^\alpha] \cdot \bar{l}^\alpha = A\bar{l}^\alpha$$

For full enclosure to be preferred:
$$z_0(1) - c \geq z_0(0)$$
$$A\theta\bar{l}^\alpha - c \geq A\bar{l}^\alpha$$
$$A(\theta-1)\bar{l}^\alpha \geq c$$
$$\bar{l} \geq \left[\frac{c}{A(\theta-1)}\right]^{\frac{1}{\alpha}}$$

This is the threshold for full enclosure in the low-TFP region where strategic complementarities create potential for multiple equilibria.

---

#### Equation (19): Second-Best No-Enclosure Threshold (High-TFP)

When $\theta \geq \theta_H$ (so $\Lambda \geq 1$), $z_0(t_e)$ is concave. The second-best planner begins enclosing when:

$$z_0'(0) \geq c \Leftrightarrow \bar{l} \geq \left[\frac{c}{A\left((\alpha\theta)^{\frac{1}{1-\alpha}}(1+\alpha)-\alpha\right)} \cdot \frac{1}{(1-\alpha)}\right]^{\frac{1}{\alpha}} = \bar{l}_0^s \qquad (19)$$

**Derivation:**
We need to compute $z_0'(t_e)$ using the quotient rule on:
$$z_0(t_e) = \bar{l}^\alpha \cdot \frac{1+(\frac{\Lambda}{\alpha}-1)t_e}{(1+(\Lambda-1)t_e)^\alpha}$$

Let $u = 1+(\frac{\Lambda}{\alpha}-1)t_e$ and $v = (1+(\Lambda-1)t_e)^\alpha$.

Then:
$$\frac{d u}{dt_e} = \frac{\Lambda}{\alpha}-1$$

$$\frac{dv}{dt_e} = \alpha(1+(\Lambda-1)t_e)^{\alpha-1} \cdot (\Lambda-1)$$

By quotient rule:
$$z_0'(t_e) = \bar{l}^\alpha \cdot \frac{v \cdot u' - u \cdot v'}{v^2}$$

$$= \bar{l}^\alpha \cdot \frac{(1+(\Lambda-1)t_e)^\alpha \cdot (\frac{\Lambda}{\alpha}-1) - [1+(\frac{\Lambda}{\alpha}-1)t_e] \cdot \alpha(1+(\Lambda-1)t_e)^{\alpha-1}(\Lambda-1)}{(1+(\Lambda-1)t_e)^{2\alpha}}$$

Factor out $(1+(\Lambda-1)t_e)^{\alpha-1}$:

$$= \bar{l}^\alpha \cdot \frac{(1+(\Lambda-1)t_e)(\frac{\Lambda}{\alpha}-1) - [1+(\frac{\Lambda}{\alpha}-1)t_e] \cdot \alpha(\Lambda-1)}{(1+(\Lambda-1)t_e)^{\alpha+1}}$$

At $t_e = 0$:
$$z_0'(0) = \bar{l}^\alpha \cdot \frac{\frac{\Lambda}{\alpha}-1 - \alpha(\Lambda-1)}{1}$$

$$= \bar{l}^\alpha \cdot \left[\frac{\Lambda}{\alpha}-1 - \alpha\Lambda + \alpha\right]$$

$$= \bar{l}^\alpha \cdot \left[\frac{\Lambda}{\alpha} - \alpha\Lambda + \alpha - 1\right]$$

$$= \bar{l}^\alpha \cdot \left[\Lambda\left(\frac{1}{\alpha} - \alpha\right) + (\alpha-1)\right]$$

$$= \bar{l}^\alpha \cdot \left[\Lambda \cdot \frac{1-\alpha^2}{\alpha} - (1-\alpha)\right]$$

$$= \bar{l}^\alpha(1-\alpha) \cdot \left[\Lambda \cdot \frac{1+\alpha}{\alpha} - 1\right]$$

$$= \bar{l}^\alpha(1-\alpha) \cdot \left[\frac{\Lambda(1+\alpha) - \alpha}{\alpha}\right]$$

Set $z_0'(0) = c$:
$$\bar{l}^\alpha(1-\alpha) \cdot \frac{\Lambda(1+\alpha) - \alpha}{\alpha} = c$$

$$\bar{l}^\alpha = \frac{c\alpha}{(1-\alpha)[\Lambda(1+\alpha)-\alpha]}$$

$$\bar{l} = \left[\frac{c\alpha}{A(1-\alpha)[(\alpha\theta)^{\frac{1}{1-\alpha}}(1+\alpha)-\alpha]}\right]^{\frac{1}{\alpha}}$$

Rearranging:
$$\bar{l}_0^s = \left[\frac{c}{A\left((\alpha\theta)^{\frac{1}{1-\alpha}}(1+\alpha)-\alpha\right)} \cdot \frac{1}{(1-\alpha)}\right]^{\frac{1}{\alpha}}$$

---

#### Equation (20): Second-Best Full-Enclosure Threshold (High-TFP)

The second-best planner chooses full enclosure when:

$$z_0'(1) \geq c \Leftrightarrow \bar{l} \geq \left[\frac{c}{\theta A(1-\alpha)}\right]^{\frac{1}{\alpha}} = \bar{l}_1^s \qquad (20)$$

**Derivation:**
At $t_e = 1$, we evaluate the derivative. From the general formula:

$$z_0'(t_e) = \bar{l}^\alpha \cdot \frac{(1+(\Lambda-1)t_e)(\frac{\Lambda}{\alpha}-1) - [1+(\frac{\Lambda}{\alpha}-1)t_e] \cdot \alpha(\Lambda-1)}{(1+(\Lambda-1)t_e)^{\alpha+1}}$$

At $t_e = 1$:
- $(1+(\Lambda-1) \cdot 1) = \Lambda$
- $[1+(\frac{\Lambda}{\alpha}-1) \cdot 1] = \frac{\Lambda}{\alpha}$

$$z_0'(1) = \bar{l}^\alpha \cdot \frac{\Lambda(\frac{\Lambda}{\alpha}-1) - \frac{\Lambda}{\alpha} \cdot \alpha(\Lambda-1)}{\Lambda^{\alpha+1}}$$

$$= \bar{l}^\alpha \cdot \frac{\frac{\Lambda^2}{\alpha}-\Lambda - \Lambda(\Lambda-1)}{\Lambda^{\alpha+1}}$$

$$= \bar{l}^\alpha \cdot \frac{\frac{\Lambda^2}{\alpha}-\Lambda - \Lambda^2 + \Lambda}{\Lambda^{\alpha+1}}$$

$$= \bar{l}^\alpha \cdot \frac{\frac{\Lambda^2}{\alpha} - \Lambda^2}{\Lambda^{\alpha+1}}$$

$$= \bar{l}^\alpha \cdot \frac{\Lambda^2({\frac{1}{\alpha} - 1})}{\Lambda^{\alpha+1}}$$

$$= \bar{l}^\alpha \cdot \frac{\Lambda^2 \cdot \frac{1-\alpha}{\alpha}}{\Lambda^{\alpha+1}}$$

$$= \bar{l}^\alpha \cdot \frac{(1-\alpha)}{\alpha\Lambda^{\alpha-1}}$$

But recall $\Lambda = (\alpha\theta)^{\frac{1}{1-\alpha}}$, so $\Lambda^{\alpha-1} = (\alpha\theta)^{\frac{\alpha-1}{1-\alpha}} = (\alpha\theta)^{-1}$.

$$z_0'(1) = \bar{l}^\alpha \cdot \frac{(1-\alpha)}{\alpha} \cdot \alpha\theta = \bar{l}^\alpha \theta(1-\alpha)$$

Set $z_0'(1) = c$:
$$\bar{l}^\alpha \theta(1-\alpha) = c$$

$$\bar{l} = \left[\frac{c}{\theta A(1-\alpha)}\right]^{\frac{1}{\alpha}}$$

**Important Note:** This equals $\bar{l}_1^d$ from equation (14)! The second-best and private thresholds for full enclosure coincide.

```{figure} ../Figures/comparison.png
:name: appendix-fig-3
:width: 90%

First-best, second-best and private enclosure thresholds compared.
```

---

### 4.2 Sources of Inefficiency

#### Equation (21): Decomposition of Social Marginal Benefit

The derivative of the second-best objective can be decomposed as:

$$z_0'(t_e) - c = \underbrace{\theta F_T^e A\bar{l}^\alpha}_{\text{private return}} - \underbrace{F_T^c A\bar{l}^\alpha}_{\text{displaced rents}} + \underbrace{(\theta F_L^e - F_L^c)A\bar{l}^\alpha \cdot \frac{dl_e^0}{dt_e}}_{\text{labor reallocation effect}} - c \qquad (21)$$

**Derivation:**
Apply the chain rule to $z_0(t_e) = [\theta F(t_e, l_e^0(t_e)) + F(1-t_e, 1-l_e^0(t_e))] \cdot A\bar{l}^\alpha$:

$$z_0'(t_e) = \left[\theta F_T^e + \theta F_L^e \cdot \frac{dl_e^0}{dt_e} + F_T^c \cdot (-1) + F_L^c \cdot \left(-\frac{dl_e^0}{dt_e}\right)\right] \cdot A\bar{l}^\alpha$$

where we use the notation:
- $F_T^e = \frac{\partial F(t_e, l_e^0)}{\partial t_e}$
- $F_L^e = \frac{\partial F(t_e, l_e^0)}{\partial l_e}$
- $F_T^c = \frac{\partial F(1-t_e, 1-l_e^0)}{\partial (1-t_e)}$
- $F_L^c = \frac{\partial F(1-t_e, 1-l_e^0)}{\partial (1-l_e)}$

Rearranging:
$$z_0'(t_e) = \left[(\theta F_T^e - F_T^c) + (\theta F_L^e - F_L^c)\frac{dl_e^0}{dt_e}\right] \cdot A\bar{l}^\alpha$$

**Interpretation:**

1. **Private Return** ($\theta F_T^e A\bar{l}^\alpha$): The rental income captured by the encloser. This is what drives private enclosure decisions.

2. **Displaced Rents** ($-F_T^c A\bar{l}^\alpha$): The marginal product of land in the commons that is lost when a unit of land is enclosed. Private enclosers do not internalize this loss, creating a **negative externality** that leads to **over-enclosure**.

3. **Labor Reallocation Effect** ($(\theta F_L^e - F_L^c)A\bar{l}^\alpha \cdot \frac{dl_e^0}{dt_e}$): When land is enclosed, labor reallocates from the commons (where it earns average product) to the enclosed sector (where it earns marginal product). This reduces the efficiency cost of labor misallocation. Private enclosers don't capture this benefit, creating a **positive externality** that leads to **under-enclosure**.

**Supporting Calculations:**

For Cobb-Douglas, we can compute explicit expressions:

**Marginal Product of Land (Enclosed):**
$$F_T^e = (1-\alpha) \cdot \left(\frac{l_e^0(t_e)}{t_e}\right)^\alpha = (1-\alpha)\left(\frac{\Lambda}{1+(\Lambda-1)t_e}\right)^\alpha$$

**Marginal Product of Land (Commons):**
$$F_T^c = (1-\alpha) \cdot \left(\frac{1-l_e^0(t_e)}{1-t_e}\right)^\alpha = (1-\alpha)\left(\frac{1}{1+(\Lambda-1)t_e}\right)^\alpha$$

**Marginal Product of Labor (Enclosed):**
$$F_L^e = \alpha\theta(1+(\Lambda-1)t_e)^{1-\alpha}$$

**Marginal Product of Labor (Commons):**
$$F_L^c = \alpha(1+(\Lambda-1)t_e)^{1-\alpha}$$

**Derivative of Labor Allocation:**
$$\frac{dl_e^0}{dt_e} = \frac{\Lambda}{(1+(\Lambda-1)t_e)^2}$$

These expressions show precisely how the three effects vary with $t_e$ and parameters $(\theta, \alpha)$.

**Key Result:** The private enclosure decision ($r(t_e) = c$) ignores both the displaced rents term and the labor reallocation term. Depending on which effect dominates, private enclosure can be excessive or insufficient relative to the second-best.

```{figure} ../Figures/labor_misallocation.png
:name: appendix-fig-4
:width: 90%

MPL, APL and the labor misallocation wedge.
```

---

*[End of Section 4]*

---

## Section 5: The Extended Model

The baseline model assumes complete open access to unenclosed land ($\mu=0$) and no compensation for displacement ($\tau=0$). We now introduce institutional parameters to capture variations in governance quality and power relations.

### 5.1 The Regulated Commons

#### Equation (22): Labor Equilibrium with Governance

We generalize the labor market equilibrium to allow for partial regulation of the commons. Define $\mu \in [0,1]$ as a governance parameter where:
- $\mu = 0$: Complete open access (baseline case)
- $\mu = 1$: Perfect regulation/private property in commons
- $0 < \mu < 1$: Partial security/regulation

The labor equilibrium condition becomes:

$$w_e - w_c = (1-\mu) \cdot r_c \cdot \frac{T_c}{L_c} \qquad (22)$$

**Derivation:**
Under imperfect governance of the commons, a worker who moves to the enclosed sector gives up not only their labor income but also a fraction $(1-\mu)$ of the possession rents they were capturing in the commons.

The wage in the enclosed sector is the marginal product of labor:
$$w_e = \theta \alpha A\left(\frac{t_e}{l_e}\right)^{1-\alpha}\bar{l}^\alpha$$

The effective return in the commons is:
$$w_c = \alpha A\left(\frac{1-t_e}{1-l_e}\right)^{1-\alpha}\bar{l}^\alpha + (1-\mu) \cdot r_c \cdot \frac{T_c}{L_c}$$

where $r_c = (1-\alpha)A\left(\frac{1-l_e}{1-t_e}\right)^\alpha\bar{l}^\alpha$ is the marginal product of land in the commons.

Setting $w_e = w_c$ gives equation (22).

**Interpretation:**
- When $\mu = 0$: Workers must fully occupy land to produce, earning $AP_L^c$
- When $\mu = 1$: Perfect institutional enforcement; workers earn only $MP_L^c$
- When $0 < \mu < 1$: Workers lose fraction $(1-\mu)$ of possession rents when leaving

---

#### Equation (23): Modified Labor Reaction Function

With governance parameter $\mu$, the labor allocation function becomes:

$$l_e^\mu(t_e) = \frac{\Lambda_\mu t_e}{1+(\Lambda_\mu-1)t_e} \qquad (23)$$

where
$$\Lambda_\mu = \left(\frac{\alpha\theta}{1-\mu(1-\alpha)}\right)^{\frac{1}{1-\alpha}}$$

**Derivation:**
From the equilibrium condition (22), we can show:
$$\theta \alpha \left(\frac{t_e}{l_e}\right)^{1-\alpha} = [1-\mu(1-\alpha)]\left(\frac{1-t_e}{1-l_e}\right)^{1-\alpha}$$

Raise to power $\frac{1}{1-\alpha}$:
$$\left(\frac{\alpha\theta}{1-\mu(1-\alpha)}\right)^{\frac{1}{1-\alpha}} \cdot \frac{t_e}{l_e} = \frac{1-t_e}{1-l_e}$$

Defining $\Lambda_\mu$ as above and following the same algebraic steps as equations (4) and (10), we obtain equation (23).

**Key Properties:**
- When $\mu = 0$: $\Lambda_0 = (\alpha\theta)^{\frac{1}{1-\alpha}}$ (baseline case)
- When $\mu = 1$: $\Lambda_1 = \theta^{\frac{1}{1-\alpha}} = \Lambda_o$ (first-best allocation)
- As $\mu$ increases, $\Lambda_\mu$ increases, so more labor flows to the enclosed sector for any given $t_e$

---

#### Equation (24): Modified High-TFP Threshold

The threshold separating strategic complements from strategic substitutes shifts with $\mu$:

$$\theta_H^\mu = \frac{1}{\alpha} - \mu \cdot \frac{1-\alpha}{\alpha} \qquad (24)$$

**Derivation:**
The critical threshold occurs when $\Lambda_\mu = 1$:
$$\left(\frac{\alpha\theta}{1-\mu(1-\alpha)}\right)^{\frac{1}{1-\alpha}} = 1$$

$$\frac{\alpha\theta}{1-\mu(1-\alpha)} = 1$$

$$\alpha\theta = 1-\mu(1-\alpha)$$

$$\theta = \frac{1-\mu(1-\alpha)}{\alpha} = \frac{1}{\alpha} - \mu \cdot \frac{1-\alpha}{\alpha}$$

**Implications:**
- When $\mu = 0$: $\theta_H^0 = 1/\alpha$ (baseline threshold)
- When $\mu = 1$: $\theta_H^1 = 1$ (first-best threshold)
- As governance improves ($\mu$ increases), the strategic complements region shrinks

```{figure} ../Figures/labor_reaction.png
:name: appendix-fig-5
:width: 90%

Labor allocation curves $l_e^\mu(t_e)$ for different values of $\mu$.
```

---

### 5.2 Power and Compensation

#### Equation (25): Profitability with Compensation

Now introduce parameter $\tau \in [0,1]$ representing the fraction of displaced rents that enclosers must compensate. Private enclosure is profitable when:

$$\theta F_T^e A\bar{l}^\alpha - \tau \cdot F_T^c A\bar{l}^\alpha - c \geq 0 \qquad (25)$$

**Derivation:**
- Without compensation ($\tau = 0$): Encloser captures full rental return $\theta F_T^e A\bar{l}^\alpha$ (a "raid")
- With full compensation ($\tau = 1$): Encloser must pay displaced users $F_T^c A\bar{l}^\alpha$ (a "trade")

The net return is:
$$\pi_e = \theta F_T^e A\bar{l}^\alpha - \tau F_T^c A\bar{l}^\alpha - c$$

Enclosure occurs when $\pi_e \geq 0$, giving equation (25).

**Interpretation:**
- $\tau = 0$: "Raid" - coercive displacement, encloser internalizes no negative externality
- $\tau = 1$: "Trade" - negotiated transfer, encloser fully internalizes displaced rents
- $0 < \tau < 1$: Partial compensation reflecting partial bargaining power

---

### 5.3 The Extended Wedge: A Unified Framework

#### Equation (26): Combined Governance and Compensation Effects

The social return to enclosure with both institutional parameters is:

$$z_0'(t_e) = \theta F_T^e A\bar{l}^\alpha - (1-\tau)F_T^c A\bar{l}^\alpha + (1-\mu)F_T^c A\bar{l}^\alpha \frac{T_c}{L_c} \cdot \frac{dl_e^\mu}{dt_e} - c \qquad (26)$$

**Derivation:**
This extends equation (21) by:
1. Scaling the displaced rents term by $(1-\tau)$ - compensation internalizes fraction $\tau$
2. Scaling the labor reallocation term by $(1-\mu)$ - governance reduces misallocation

The labor reallocation effect now uses $l_e^\mu(t_e)$ instead of $l_e^0(t_e)$, and the magnitude of the effect is proportional to $(1-\mu)$ since better governance reduces the initial misallocation.

**Key Result:** The wedge between private and social returns closes when:
- $\mu = 1$ **AND** $\tau = 1$

With both parameters at 1, private incentives align with social optimum. However, improving only one dimension while holding the other fixed can worsen outcomes (second-best problem).

---

#### Equation (27): General Enclosure Decision

Private enclosure with both institutional parameters occurs when:

$$r_\mu^e(t_e) - \tau \cdot r_\mu^c(t_e) - c \geq 0 \qquad (27)$$

where:
$$r_\mu^e(t_e) = \theta(1-\alpha)A\bar{l}^\alpha \left(\frac{\Lambda_\mu}{1+(\Lambda_\mu-1)t_e}\right)^\alpha$$

$$r_\mu^c(t_e) = (1-\alpha)A\bar{l}^\alpha \left(\frac{1}{1+(\Lambda_\mu-1)t_e}\right)^\alpha$$

This generalizes equation (12) to allow for both governance quality ($\mu$) and compensation requirements ($\tau$).

```{figure} ../Figures/new_comp_fig4x4.png
:name: appendix-fig-6
:width: 90%

Effects of varying $\mu$ and $\tau$ on equilibrium outcomes.
```

---

#### Equation (27a): Global Games Threshold under Governance and Compensation

Equations (13)–(14) generalize to the extended model by substituting (27) for (12), and so
does the selection criterion of equation (15). The multiplicity region does not disappear
when $\mu$ or $\tau$ is positive — it is $\theta < \theta_H^\mu$, which is non-empty for
every $\mu \in [0,1]$ — so a risk-dominance threshold continues to exist there and can be
written down.

The two rents in (27) share the same dependence on $t_e$, so they combine before integrating:

$$r_\mu^e(t_e) - \tau\,r_\mu^c(t_e)
= (1-\alpha)A\bar{l}^{\alpha}\left(\theta\Lambda_\mu^{\alpha}-\tau\right)
\left(1+(\Lambda_\mu-1)t_e\right)^{-\alpha}$$

Applying the same substitution as in (15) gives

$$\bar{l}_{gg}^d(\mu,\tau) = \left[\frac{(c/A)\left(\Lambda_\mu-1\right)}
{\left(\theta\Lambda_\mu^{\alpha}-\tau\right)\left(\Lambda_\mu^{1-\alpha}-1\right)}
\right]^{\frac{1}{\alpha}} \qquad (27a)$$

**Properties:**

- At $\mu=\tau=0$ this is equation (15), since $\Lambda_0 = \Lambda$.
- It is defined where $\theta < \theta_H^\mu$ *and* $\theta\Lambda_\mu^{\alpha} > \tau$ —
  an interval, squeezed from the right by governance and from the left by compensation. The
  second edge is derived below and is substantive rather than technical.
- The governance wedge $A_\mu = 1-\mu(1-\alpha)$ of equations (22)–(23) does **not** appear
  as a separate factor here. Using $\Lambda_\mu^{1-\alpha} = \alpha\theta/A_\mu$, it enters
  numerator and denominator alike and cancels, leaving $\mu$ to act only through
  $\Lambda_\mu$. This is specific to this locus: in the labor-market conditions of §5.1,
  $A_\mu$ sets the *level* of what labor takes home and does not cancel.

**Comparative statics.** The two institutional parameters move the threshold in opposite
directions. Compensation raises it: $\tau$ enters only through $(\theta\Lambda_\mu^\alpha -
\tau)$, so a larger $\tau$ shrinks the expected return and a higher density is needed to
trigger the cascade. Governance *lowers* it. Raising $\mu$ reduces $A_\mu$, which raises
$\Lambda_\mu$ and hence the encloser's return $\theta\Lambda_\mu^{\alpha}$ — a regulated
commons pays labor its marginal rather than its average product, so the outside wage an
encloser must match is lower. At $\alpha=2/3$, $\theta=0.9$, $\tau=0$:

| $\mu$ | $A_\mu$ | $\Lambda_\mu$ | $\theta\Lambda_\mu^{\alpha}$ | $\ln \bar{l}_{gg}^d$ |
|---:|---:|---:|---:|---:|
| 0.0 | 1.000 | 0.216 | 0.324 | 2.700 |
| 0.3 | 0.900 | 0.296 | 0.400 | 2.495 |
| 0.6 | 0.800 | 0.422 | 0.506 | 2.279 |
| 1.0 | 0.667 | 0.729 | 0.729 | 1.970 |

Better commons governance therefore makes the enclosure race easier to trigger, at the same
time as it shrinks the region in which a race is possible at all, since $\theta_H^\mu$ falls
from $1/\alpha$ to $1$ over the same range. The two effects work against each other, and
which dominates is a quantitative question.

*Verification:* (27a) was checked against symbolic integration, against numerical quadrature
of the payoff, and by reduction to the two one-sided forms already implemented in the code —
equation (15) extended in $\tau$ at $\mu=0$, and the $\mu$-extended form at $\tau=0$.

---

#### Equation (27b): Where the Selection Threshold Ceases to Exist

The condition $\theta\Lambda_\mu^{\alpha} > \tau$ in (27a) has a closed-form boundary.
Setting the two equal and using $\Lambda_\mu^{1-\alpha} = \alpha\theta/A_\mu$:

$$\theta\left(\frac{\alpha\theta}{A_\mu}\right)^{\frac{\alpha}{1-\alpha}} = \tau
\qquad\Longrightarrow\qquad
\theta_\tau(\mu,\tau) = \tau^{1-\alpha}\left(\frac{A_\mu}{\alpha}\right)^{\alpha}
\qquad (27b)$$

At $\tau=0$ this is $0$, imposing nothing. At $\mu=0,\tau=1$ it is $\alpha^{-\alpha}$
($\approx 1.310$ at $\alpha=2/3$), the asymptote of the $\tau=1$ locus.

**Why this is a different kind of boundary.** Both rents in (27) carry the same factor
$\bar l^{\alpha}$, so it factors out of the comparison entirely:

$$r_\mu^e - \tau r_\mu^c = (1-\alpha)A\bar{l}^{\alpha}
\underbrace{\left(\theta\Lambda_\mu^{\alpha}-\tau\right)}_{\text{no } \bar l}
\left(1+(\Lambda_\mu-1)t_e\right)^{-\alpha}$$

Population density scales *both* the encloser's gross return and the compensation owed, so
it cannot change the sign of their difference. Below $\theta_\tau$ the expected net return
is negative at **every** density: the threshold does not move upward out of reach, it ceases
to exist.

This distinguishes the two obstacles to enclosure in the model:

| | how it enters | can density overcome it? |
|:---|:---|:---|
| Enclosure cost $c$ | a **level** charge per unit land | **Yes.** Rents scale with $\bar l^{\alpha}$ while $c$ does not, so some density always suffices. This is why every locus is downward-sloping and finite. |
| Compensation $\tau$ | a **proportional** claim on displaced rents | **No.** It scales with the thing it taxes, so the comparison is density-free. Below $\theta_\tau$ no density suffices. |

The distinction matters for the Boserupian reading of the model. Rising population density
is the mechanism that drives an economy through every other threshold in the paper —
$\bar l_0^1$, $\bar l_0^d$, $\bar l_{gg}^d$. Compensation is the one institution it cannot
push through. Cost-based protections for customary users — titling fees, registration
requirements, administrative friction — are eroded by population growth, because they are
levels. A compensation *requirement* is not, because it is a share.

**Closure at the corner.** Since $\theta_H^\mu = A_\mu/\alpha$ and
$\theta_\tau = \tau^{1-\alpha}(A_\mu/\alpha)^{\alpha}$, the interval
$(\theta_\tau, \theta_H^\mu)$ is non-empty whenever $\tau < 1$ or $\mu < 1$, and empty
exactly at $\mu=\tau=1$, where both equal $1$. So the coordination problem vanishes at
precisely the corner where the wedge closes: complete governance and complete compensation
not only align the decentralized loci with the planner's (§5.3), they eliminate the
multiplicity that made equilibrium selection necessary in the first place. Neither parameter
achieves this alone — at $\mu<1$ a multiplicity region survives even at $\tau=1$, since
$(A_\mu/\alpha)^{\alpha} < A_\mu/\alpha$ whenever $A_\mu/\alpha > 1$.

---

*[End of Section 5]*

---

## Section 6: Applications and Extensions

### 6.1 Labor Release and Wages

#### Equation (28): Total Labor Income (Access Fees Redistributed)

When access fees collected in the commons are redistributed to labor, total labor income is:

$$Y_L = AF(\bar{T}, \bar{L}) \cdot \frac{1+(\alpha\theta\Lambda_\mu-1)t_e}{(1+(\Lambda_\mu-1)t_e)^\alpha} \qquad (28)$$

**Derivation:**
Labor earns:
- In enclosed sector: $w_e \cdot L_e = \alpha\theta F(T_e, L_e)$
- In commons: Total output $F(T_c, L_c)$ if access fees are redistributed

Total labor income:
$$Y_L = \alpha\theta AF(T_e, L_e) + AF(T_c, L_c)$$

Factoring out $AF(\bar{T}, \bar{L})$ and expressing in shares:
$$Y_L = AF(\bar{T}, \bar{L})[\alpha\theta F(t_e, l_e^\mu) + F(1-t_e, 1-l_e^\mu)]$$

Substituting $l_e^\mu(t_e)$ and simplifying (similar to derivations in equations 5 and 17) yields equation (28).

**Result:** Labor benefits from enclosure when $\theta > \theta_H^\mu$, as the productivity gains outweigh the loss of commons access.

---

#### Equation (29): Total Labor Income (Access Fees Captured by Elites)

If elites capture the fraction $(1-\mu)$ of possession rents:

$$Y_L = (1-\mu(1-\alpha))AF(\bar{T}, \bar{L})(1+(\Lambda_\mu-1)t_e)^{1-\alpha} \qquad (29)$$

**Derivation:**
Labor now earns only:
- Marginal product in enclosed sector: $\alpha\theta F(T_e, L_e)$
- Marginal product in commons: $\alpha F(T_c, L_c)$
- Fraction $\mu$ of land rents in commons: $\mu(1-\alpha)F(T_c, L_c)$

Total:
$$Y_L = \alpha[\theta F(T_e, L_e) + F(T_c, L_c)] + \mu(1-\alpha)F(T_c, L_c)$$

After substitution and simplification, this leads to equation (29).

**Result:** With elite capture, labor's share of income is reduced by factor $(1-\mu(1-\alpha))$, highlighting distributional consequences of weak governance.

---

### 6.2 Power Shifts and Contested Claims

*(No new numbered equations - qualitative discussion)*

The framework can be applied to analyze:
- English enclosures: Regional variation in $\theta$, $\mu$, $\tau$ explaining different enclosure patterns
- American frontier: Variation in $\tau$ depending on Native American military capacity
- Modern land formalization: Trade-offs between improving $\mu$ vs. ensuring adequate $\tau$

---

### 6.3 Encompassing Interests and Frontier Colonization

#### Equation (30): Monopolistic Encloser's Profit

A monopolistic encloser (e.g., colonial authority, land syndicate) maximizes total profit:

$$\pi(t_e) = r(t_e) \cdot t_e - c \cdot t_e \qquad (30)$$

**Derivation:**
Unlike competitive enclosers who take $r(t_e)$ as given, a monopolist internalizes the effect of their enclosure decisions on the rental rate. Total profit is rental income minus enclosure costs.

---

#### Equations (31-34): Monopoly Thresholds

**Low-TFP Region:** Monopolist chooses full enclosure when:

$$\pi(1) > 0 \Leftrightarrow \bar{l} \geq \left[\frac{c}{\theta A(1-\alpha)}\right]^{\frac{1}{\alpha}} = \bar{l}^m \qquad (31)$$

This equals $\bar{l}_1^d$, but the monopolist jumps directly to full enclosure (Wakefield's "sufficient price").

**High-TFP Region:** Monopolist begins enclosing when:

$$\pi'(0) \geq 0 \Leftrightarrow \bar{l} \geq \bar{l}_0^m \qquad (32)$$

And fully encloses when:

$$\pi'(1) \geq 0 \Leftrightarrow \bar{l} \geq \bar{l}_1^m \qquad (33)$$

**Derivation:** From $\pi'(t_e) = r(t_e) + r'(t_e)t_e - c$, evaluate at boundaries. The monopolist restricts enclosure below competitive levels when $r'(t_e) < 0$ (high-TFP), as they internalize the rent-reducing effect of enclosure.

```{figure} ../Figures/monopoly.png
:name: appendix-fig-7
:width: 90%

Monopolist's enclosure decisions vs. competitive outcomes.
```

---

### 6.4 Structural Transformation and Manufacturing

#### Equation (35): Labor Market with Manufacturing

Extend to three sectors (enclosed agriculture, commons agriculture, manufacturing):

$$l_e + l_c + l_m = 1 \qquad (35)$$

where $l_m$ is labor share in manufacturing.

---

#### Equation (36): Modified Labor Allocation

The agricultural labor allocation becomes:

$$l_e^\mu(t_e) = \frac{\Lambda_\mu t_e}{1+(\Lambda_\mu-1)t_e} \cdot (1-l_m) \qquad (36)$$

**Derivation:** The intra-agricultural condition is unchanged — equation (22) equalizes returns between enclosed land and the commons whatever else the economy contains — so the only modification is that the agricultural labor force is $(1-l_m)$ rather than $1$. Following the steps of (23) with $(1-l_m)$ in place of $1$ gives (36). The same expression with $\Lambda_o$ in place of $\Lambda_\mu$ is the planner's allocation, since $\mu=1$ gives $\Lambda_1=\Lambda_o$.

Everything below is stated in intensive form with $\bar t = \bar T/\bar L$ and $\bar k = \bar K/\bar L$; factor-price levels carry the same density scaling as Section 3.

---

#### Equation (37): The Governance Wedge $A_\mu$

Labor in the commons takes home the fraction

$$A_\mu = 1 - \mu(1-\alpha), \qquad A_0 = 1, \quad A_1 = \alpha \qquad (37)$$

of the commons average product.

**Derivation:** From the Euler decomposition (8), $AP_L^c = MP_L^c + MP_T^c \cdot (T_c/L_c)$, with $MP_L^c = \alpha AP_L^c$ and hence $MP_T^c(T_c/L_c) = (1-\alpha)AP_L^c$. Equation (22) says a worker leaving the commons forfeits the fraction $\mu$ of those possession rents, retaining $(1-\mu)$. Total commons income per worker is therefore

$$w_c = \alpha AP_L^c + (1-\mu)(1-\alpha)AP_L^c = [1-\mu(1-\alpha)]\,AP_L^c$$

$\mu=0$ recovers open access, where labor captures the whole average product; $\mu=1$ gives the marginal product, which is the planner's valuation.

$A_\mu$ is stated separately from $\Lambda_\mu$ because the two are not substitutes: $\Lambda_\mu$ governs the *slope* of the labor allocation, $A_\mu$ the *level* of what labor earns, and they enter subsequent expressions independently. The distinction is invisible in the two-sector model, where the level cannot affect an allocation that is agricultural regardless.

---

#### Equation (38): The Manufacturing Margin

Labor moves between sectors until $p \cdot MP_L^m = \theta \cdot MP_L^e = w_c$. Substituting (36) into each side:

$$\underbrace{p\beta\bar k^{1-\beta}}_{C_m} \cdot l_m^{-(1-\beta)} \;=\; \underbrace{A_\mu\,\bar t^{1-\alpha}\left(1+(\Lambda_\mu-1)t_e\right)^{1-\alpha}}_{C_a} \cdot (1-l_m)^{-(1-\alpha)} \qquad (38)$$

**Derivation:** From (36), $1-l_m-l_e^\mu = (1-l_m)(1-t_e)/[1+(\Lambda_\mu-1)t_e]$, so

$$AP_L^c = \bar t^{1-\alpha}\left(\frac{1-t_e}{1-l_m-l_e^\mu}\right)^{1-\alpha} = \bar t^{1-\alpha}\left(\frac{1+(\Lambda_\mu-1)t_e}{1-l_m}\right)^{1-\alpha}$$

and $w_c = A_\mu \cdot AP_L^c$ by (37). Equivalently, working from the enclosed side, $\theta MP_L^e = \alpha\theta\,\bar t^{1-\alpha}(t_e/l_e^\mu)^{1-\alpha} = \alpha\theta\Lambda_\mu^{-(1-\alpha)}\bar t^{1-\alpha}(1+(\Lambda_\mu-1)t_e)^{1-\alpha}(1-l_m)^{-(1-\alpha)}$, and $\alpha\theta\Lambda_\mu^{-(1-\alpha)} = A_\mu$ by the definition of $\Lambda_\mu$ in (23). The two routes agree, as they must.

Note that at $\mu=0$ the prefactor equals exactly $1$, so the agricultural side can be written compactly as $\bar t^{1-\alpha}(t_e/l_e^0)^{1-\alpha}$. That shorthand does not survive to $\mu>0$, where the prefactor is $A_\mu$ and not $1$.

Two properties pin the level and serve as checks:

- At $t_e=0$, $\Lambda_\mu$ drops out and $C_a = A_\mu\bar t^{1-\alpha}$, so the planner's and open-access curves differ by exactly $\alpha$ — one pays labor its average product, the other its marginal product.
- At $t_e=1$ there is no commons, so $\mu$ cannot matter: $C_a = A_\mu\Lambda_\mu^{1-\alpha}\bar t^{1-\alpha} = \alpha\theta\,\bar t^{1-\alpha}$ for **every** $\mu$. Equivalently, full enclosure implements the planner's inter-sectoral labor allocation for any $\theta$ — conditional on $t_e$, a qualification equation (40) makes essential.

---

#### Equation (39): Equilibrium Manufacturing Share

Rearranging (38):

$$\frac{l_m^{1-\beta}}{(1-l_m)^{1-\alpha}} = \frac{C_m}{C_a} \qquad (39)$$

**Existence and uniqueness.** The left side is continuous and strictly increasing on $(0,1)$, from $0$ to $\infty$. Hence (39) has exactly one solution for any $C_m/C_a > 0$: the equilibrium exists and is unique for all admissible parameters, and a bracketed root-finder on $(0,1)$ is guaranteed to converge.

**Closed form when $\beta=\alpha$.** The exponents coincide and (39) becomes $\left(\frac{l_m}{1-l_m}\right)^{1-\alpha} = \frac{C_m}{C_a}$, so

$$l_m = \frac{R}{1+R}, \qquad R = \left(\frac{C_m}{C_a}\right)^{\frac{1}{1-\alpha}}$$

For $\beta\neq\alpha$ equation (39) is transcendental and has no elementary solution.

**Comparative static in $t_e$.** $\partial C_a/\partial t_e$ has the sign of $(\Lambda_\mu-1)$. Because the left side of (39) is *increasing* in $l_m$, the manufacturing share rises exactly when $C_a$ falls, so

$$\operatorname{sign}\left(\frac{\partial l_m}{\partial t_e}\right) = \operatorname{sign}(1-\Lambda_\mu)$$

— the opposite sign, an inversion easily lost. By (24), $\Lambda_\mu=1$ exactly at $\theta_H^\mu$, so enclosure accelerates structural transformation below that threshold, retards it above, and moves no labor at all at it. The knife-edge is exact. Equation (41) tabulates the consequences; note that $\theta_H^\mu$ is the same threshold that separates strategic complements from substitutes in (24), a coincidence taken up there.

---

#### Equation (40): The Planner's Enclosure Margin

Equations (36)–(39) condition on $t_e$. Restoring the planner's choice of $t_e$, and applying the envelope theorem — at the planner's allocation marginal products are already equal, so reallocating labor has no first-order effect and only the land-rent differential survives:

$$\frac{dY}{dt_e} = (1-\alpha)\,\bar t^{1-\alpha}(\Lambda_o-1)\left(\frac{1-l_m(t_e)}{1+(\Lambda_o-1)t_e}\right)^{\alpha} \qquad (40)$$

**Derivation:** $dY/dt_e = \theta F_T^e - F_T^c = (1-\alpha)\bar t^{1-\alpha}[\theta(l_e/t_e)^\alpha - (l_c/(1-t_e))^\alpha]$. Substituting (36) at $\mu=1$ gives $l_e/t_e = \Lambda_o(1-l_m)/D_o$ and $l_c/(1-t_e) = (1-l_m)/D_o$ with $D_o = 1+(\Lambda_o-1)t_e$, and $\theta\Lambda_o^\alpha = \Lambda_o^{1-\alpha}\Lambda_o^{\alpha} = \Lambda_o$.

This is exactly $z'(t_e)$ from Section 3 with the *agricultural* labor share $(1-l_m)$ in place of the whole labor force. **Manufacturing changes the level but not the sign.**

**Two thresholds, not one.** The sign of (40) is that of $(\Lambda_o - 1)$, i.e. of $(\theta-1)$ — note $\Lambda_o$, not $\Lambda_\mu$. This margin turns at $\theta=1$; the labor-allocation reversal of (39) turns at $\theta_H^\mu$. They answer different questions — *is enclosure worth doing* versus *which way does it push labor* — and must not be conflated. Below $\theta=1$ enclosure lowers output even at $c=0$; at $\theta=1$ (40) is identically zero; above it the planner encloses while (40) exceeds $c\,\bar t$.

So $t_e^o=0$ for every $c>0$ whenever $\theta\le1$, however misallocated the decentralized economy's labor is at $t_e=0$. That full enclosure reproduces the planner's *labor* allocation does not make full enclosure optimal. At $\theta=1$ in particular, the whole gain from enclosure is the repair of the commons distortion, which regulating the commons ($\mu\to1$) achieves at $t_e=0$ without incurring $c\bar T$.

---

#### Equation (41): Three Regimes

Since $\theta_H^\mu = [1-\mu(1-\alpha)]/\alpha$ from (24) and the enclosure margin turns at $\theta=1$,

$$\theta_H^\mu - 1 = \frac{(1-\alpha)(1-\mu)}{\alpha} \;\geq\; 0, \qquad \text{with equality iff } \mu=1 \qquad (41)$$

The two thresholds therefore bracket a band, and the parameter space divides into three regimes:

| Regime | Range | Enclosure socially desirable? | Effect on structural transformation | Enclosure game |
|:---|:---|:---|:---|:---|
| A | $\theta<1$ | No (at any $c>0$) | Releases labor to manufacturing | Complements |
| B | $1<\theta<\theta_H^\mu$ | Yes, if $c$ small enough | Releases labor to manufacturing | Complements |
| C | $\theta>\theta_H^\mu$ | Yes, if $c$ small enough | Draws labor back into agriculture | Substitutes |

Regime B is the configuration the conventional account of enclosure and industrialization presumes — enclosure both efficiency-improving and labor-releasing. By (41) its width is proportional to $(1-\mu)$, so **it exists only to the extent that the commons is poorly governed, and closes entirely at $\mu=1$.** It is also wider the larger is land's share $(1-\alpha)$. The conventional account is thus not a general property of enclosure but a feature of the open-access case, and one that yields an inverted comparative static: within B, the labor-release effect weakens as $\theta$ rises toward $\theta_H^\mu$, so enclosures delivering the *largest* productivity gains should release the *least* labor.

**The last column is not an additional assumption.** By (12), $r_\mu(t_e)$ is increasing in $t_e$ exactly when $\Lambda_\mu<1$ — the condition for strategic complementarity, and hence for the multiplicity that (15) resolves. By (39) that is *also* exactly the condition for enclosure to release labor. The two are the same inequality because both turn on whether enclosed land is more or less labor-hungry than the commons. Hence:

> Wherever enclosure accelerates structural transformation, the enclosure game admits multiple equilibria; wherever it retards structural transformation, the equilibrium is unique.

Regimes A and B lie entirely inside the strategic-complements region and C entirely outside it. The enclosures relevant to industrialization are therefore precisely those whose extent is not pinned down by fundamentals alone.

---

#### Equation (42): Private Enclosure with Manufacturing and Compensation

Equations (40)–(41) describe what the *planner* would do. Restoring the decentralized enclosure condition (27) in the presence of manufacturing:

$$r_\mu^e(t_e) - \tau\,r_\mu^c(t_e) = (1-\alpha)A\bar l^\alpha\left(\frac{1-l_m(t_e)}{1+(\Lambda_\mu-1)t_e}\right)^{\alpha}\Big[\theta\Lambda_\mu^{\alpha} - \tau\Big] \qquad (42)$$

**Derivation:** With manufacturing present, the enclosed and commons labor–land ratios are $L_e/T_e = \Lambda_\mu(1-l_m)\bar l/D_\mu$ and $L_c/T_c = (1-l_m)\bar l/D_\mu$, with $D_\mu = 1+(\Lambda_\mu-1)t_e$, by (36). Substituting into $r^e_\mu = \theta(1-\alpha)A(L_e/T_e)^\alpha$ and $r^c_\mu = (1-\alpha)A(L_c/T_c)^\alpha$ and collecting terms gives (42). The marginal encloser takes $l_m$ and the wage as given, so $l_m$ enters as a level, not through a strategic term.

The factorization is worth pausing on. **Manufacturing enters only through $(1-l_m)^\alpha$** — a scale factor common to both rentals, reflecting that a smaller agricultural labor force lowers the land–labor ratio and hence both rents equally. **$\tau$ enters only the bracket.** The planner's counterpart, from (40), is the bracket $[\Lambda_o-1]$; since $\theta\Lambda_\mu^\alpha = \Lambda_\mu$ when $\mu=1$, private and social margins coincide exactly at $\mu=1$ **and** $\tau=1$, which is the condition stated in §5.3.

---

#### Equation (43): The Compensation Threshold

From the bracket in (42), enclosure is privately profitable at some $c \geq 0$ if and only if

$$\tau < \tau^*(\theta,\mu) = \theta\,\Lambda_\mu^{\alpha} = \theta^{\frac{1}{1-\alpha}}\left(\frac{\alpha}{A_\mu}\right)^{\frac{\alpha}{1-\alpha}} \qquad (43)$$

$\tau^*$ is strictly increasing in both $\theta$ and $\mu$. The second is a second-best tension in its own right: better commons governance raises $\Lambda_\mu$ and hence the enclosed-land rent, so improving governance makes enclosure *harder* to deter by compensation, even as it makes deterrence more worthwhile.

Setting $\tau^*=1$ and solving gives the range over which full compensation binds at all:

$$\tau^*(\theta,\mu) \lessgtr 1 \iff \theta \lessgtr \left(\theta_H^\mu\right)^{\alpha}$$

Since $\theta_H^\mu \geq 1$ and $\alpha<1$, this lies strictly between $1$ and $\theta_H^\mu$ and collapses to $1$ at $\mu=1$. Above it no admissible $\tau$ prevents enclosure, and compensation is a pure transfer with no allocative consequence. This splits regime B of (41) at $(\theta_H^\mu)^\alpha$ into a sub-range where a compensation requirement blocks enclosure and one where it does not.

**$\tau$ moves neither threshold of (41).** Appearing in neither production nor the planner's objective, it cannot shift $\theta_H^\mu$ or the $\theta=1$ margin. Its role is to select *which $t_e$ is reached*, not what enclosure does once there: $\mu$ changes what enclosure would do, $\tau$ changes whether it happens.

Consequently the two instruments are complements rather than substitutes, and $\partial Y/\partial \tau$ changes sign with $\mu$. Requiring compensation without regulating the commons removes the repair of the labor misallocation that enclosure was accomplishing; requiring it with a regulated commons prevents enclosure that would merely expend $c$. This is the claim of §5.3, now with a second margin on which it operates. Worked numerical illustrations are in `enclose/manufacturing.py`.

*Caveat.* Any equilibrium $t_e$ computed from the marginal condition alone is incomplete for $\theta<\theta_H^\mu$, where (15)'s refinement is needed to select among multiple equilibria.

---

*[End of Section 6]*

*Interpretation of these results — the mapping from regimes to historical accounts of enclosure, the relation to dual-economy models, and the research agenda they suggest — is deliberately not developed here. See `notes/manuf_paper_ideas.md` in the project repository.*

---

## Appendix G: Computational Verification

All equations in this appendix have been implemented and can be verified using the Python module `enclose.py` located at `notebooks/enclose.py`.

### G.1 Code Overview

The `enclose.py` module provides a complete computational implementation of the model with functions for:

- Production functions and marginal products
- Labor allocation under different institutional regimes
- Rental rates and optimal enclosure decisions
- Parameter space partitioning and comparative statics
- Plotting functions for generating figures

**Standard Parameters Used Throughout:**
- $\alpha = 2/3$ (labor share)
- $c/A = 1.0$ (normalized enclosure cost)
- Various values of $\theta$ (productivity gain) and $\bar{l}$ (population density)

---

### G.2 Function-to-Equation Mapping

| Python Function | Equations | Purpose | Key Parameters |
|----------------|-----------|---------|----------------|
| `f(T, L, a, th)` | Production | Cobb-Douglas $F(T,L) = T^{1-\alpha}L^\alpha$ | α, θ |
| `Lambda(th, alp, mu)` | (4), (10), (23) | Compute $\Lambda$ parameter | θ, α, μ |
| `le(te, th, alp, mu)` | (4), (10), (23) | Labor reaction function $l_e(t_e)$ | θ, α, μ |
| `z(te, th, alp, lbar)` | (5) | First-best output $z_1(t_e)$ | θ, α, $\bar{l}$ |
| `zpv(te, th, alp, lbar)` | (17) | Second-best output $z_0(t_e)$ | θ, α, $\bar{l}$ |
| `req(te, th, alp, lbar, mu)` | (12), (27) | Rental rate $r(t_e)$ or $r_\mu(t_e)$ | θ, α, $\bar{l}$, μ |
| `weq(te, th, alp, lbar, mu)` | Labor equilibrium | Commons average product $AP_L^c(t_e)$. The **wage** is $A_\mu \cdot$ `weq`, per (37) — the two coincide only at $\mu=0$ | θ, α, $\bar{l}$, μ |
| `zprime(te, th, alp, lbar, mu)` | (6), (7), (19), (20) | Marginal benefit $z'(t_e)$ or $z_0'(t_e)$ | θ, α, $\bar{l}$, μ |
| `teopt(th, alp, c, lbar)` | Lemma 1 | Optimal enclosure rate (first-best) | θ, α, c, $\bar{l}$ |
| `tepvt(th, alp, c, lbar, mu)` | Props 2-3 | Private enclosure rate | θ, α, c, $\bar{l}$, μ |
| `tepvt_g(th, alp, c, lbar, mu)` | (15) | Global games refined equilibrium | θ, α, c, $\bar{l}$, μ |
| `mple(te, le, a, th, lbar)` | Supporting | Marginal product of labor (enclosed) | |
| `mpt(te, le, a, th, lbar)` | Supporting | Marginal product of land | |
| `totalq(te, th, alp, lbar, mu)` | Supporting | Total economy output | |

The three-sector extension of §6.4 lives in a separate module, `enclose/manufacturing.py`
in the `open-enclose.github.io` repository, with tests in `tests/test_manufacturing.py`:

| Python Function | Equations | Purpose | Key Parameters |
|----------------|-----------|---------|----------------|
| `commons_wedge(alp, mu)` | (37) | Governance wedge $A_\mu$ | α, μ |
| `mpl_m(lm, p, kb, b)` | (38) | $MP_L^m$, manufacturing side | p, $\bar k$, β |
| `mpl_a(lm, te, tbar, alp, th, mu)` | (38) | Agricultural return $A_\mu \cdot AP_L^c$ — a marginal product only at $\mu=1$ | α, θ, μ, $t_e$ |
| `labor_share(te, ...)` | (39) | Equilibrium $l_m$, bracketed solve | all |
| `labor_share_closed_form(te, ...)` | (39) | Exact $l_m$ at $\beta=\alpha$; used as a test oracle | all |
| `agricultural_labor(te, ...)` | (36) | $l_e^\mu(t_e)$ with manufacturing present | θ, α, μ |
| `total_output(te, ...)` | Supporting | $Y/\bar L$ at the equilibrium allocation, gross of $c$ | all |
| `planner_marginal_benefit(te, ...)` | (40) | $dY/dt_e$ at the planner's allocation | α, θ, β, p |
| `private_marginal_return(te, tau, ...)` | (42) | $r^e_\mu - \tau r^c_\mu$ with manufacturing | α, θ, β, μ, τ |
| `compensation_threshold(th, alp, mu)` | (43) | $\tau^*(\theta,\mu)$ | α, θ, μ |

Equation (37) is the correction most worth checking against: it was absent from earlier
drafts of this material, which stated the $\mu=0$ shorthand of (38) as though it held for
all $\mu$. `tests/test_manufacturing.py` pins it by verifying the planner's first-order
conditions against the primitive derivatives of the objective, independently of any
expression in §6.4.

---

### G.3 Figure References

All figures in the main paper were generated using the code and can be found in the `docs/Figures/` directory:

**Core Figures:**
- `Figure1.png` - First-best parameter space (equations 6-7)
- `Figure2.png` - Decentralized equilibrium regions (equations 13-15)
- `Figure3.png` - Comparison of first-best, second-best, and private thresholds
- `Figure4.png` - Labor misallocation and deadweight loss illustration

**Extended Model Figures:**
- `Figure5.png` - Labor allocation under different governance regimes (equation 23)
- `Figure6.png` - Four-panel comparative statics with μ and τ
- `Figure7.png` - Monopolistic enclosure decisions

**Note:** If specific figures are not found, placeholder references are provided. Figures can be regenerated using:

```python
import enclose as enc
import matplotlib.pyplot as plt

# Example: Plot rental rate function
te_vals = np.linspace(0, 1, 100)
r_vals = [enc.req(te, th=1.5, alp=2/3, ltbar=2.0, mu=0) for te in te_vals]
plt.plot(te_vals, r_vals)
plt.xlabel('$t_e$')
plt.ylabel('$r(t_e)$')
plt.title('Rental Rate Function')
plt.savefig('rental_rate.png')
```

---

### G.4 Verification Examples

#### Example 1: Verify Equation (5)

```python
import enclose as enc

# Parameters
th = 1.5
alp = 2/3
lbar = 2.0
te = 0.5

# Compute z_1(t_e) using closed form (equation 5)
Lambda_o = th**(1/(1-alp))
z1 = lbar**alp * (1 + (Lambda_o - 1) * te)**(1-alp)

# Verify using code
z1_code = enc.z(te, th, alp, lbar)

print(f"Equation (5): z_1({te}) = {z1:.6f}")
print(f"Code output: {z1_code:.6f}")
print(f"Match: {np.isclose(z1, z1_code)}")
```

#### Example 2: Verify Labor Allocation (Equation 10)

```python
# Compute labor allocation
Lambda = (alp * th)**(1/(1-alp))
le_formula = (Lambda * te) / (1 + (Lambda - 1) * te)

# Using code
le_code = enc.le(te, th, alp, mu=0)

print(f"Equation (10): l_e({te}) = {le_formula:.6f}")
print(f"Code output: {le_code:.6f}")
print(f"Match: {np.isclose(le_formula, le_code)}")
```

#### Example 3: Verify Thresholds (Equations 6-7, 13-14)

```python
# First-best thresholds
c = 1.0
A = 1.0

lbar0_1 = (c / (A * (1-alp) * (Lambda_o - 1)))**(1/alp)
lbar1_1 = Lambda_o * lbar0_1

# Decentralized thresholds
lbar0_d = (c / (th * A * (1-alp) * Lambda**alp))**(1/alp)
lbar1_d = (c / (th * A * (1-alp)))**(1/alp)

print(f"First-best: l̄₀¹ = {lbar0_1:.4f}, l̄₁¹ = {lbar1_1:.4f}")
print(f"Decentralized: l̄₀ᵈ = {lbar0_d:.4f}, l̄₁ᵈ = {lbar1_d:.4f}")
```

---

### G.5 Reproducing Main Results

The key propositions can be verified computationally:

**Proposition 1 (Strategic Interactions):**
```python
# Check sign of r'(t_e)
theta_H = 1 / alp  # Critical threshold
te_test = 0.5

# High-TFP case (strategic substitutes)
r_high_before = enc.req(te_test - 0.01, th=2.0, alp=alp, ltbar=lbar, mu=0)
r_high_after = enc.req(te_test + 0.01, th=2.0, alp=alp, ltbar=lbar, mu=0)
print(f"High-TFP: r'(t_e) < 0? {r_high_after < r_high_before}")

# Low-TFP case (strategic complements)
r_low_before = enc.req(te_test - 0.01, th=1.2, alp=alp, ltbar=lbar, mu=0)
r_low_after = enc.req(te_test + 0.01, th=1.2, alp=alp, ltbar=lbar, mu=0)
print(f"Low-TFP: r'(t_e) > 0? {r_low_after > r_low_before}")
```

**Proposition 4 (Second-Best Concavity):**
```python
# Check concavity of z_0(t_e)
te_vals = np.linspace(0, 1, 100)
z0_vals = [enc.zpv(te, th=1.5, alp=alp, lbar=lbar) for te in te_vals]
z0_second_diff = np.diff(np.diff(z0_vals))
print(f"z_0 concave (high-TFP)? {np.all(z0_second_diff < 1e-6)}")

z0_vals_low = [enc.zpv(te, th=1.2, alp=alp, lbar=lbar) for te in te_vals]
z0_second_diff_low = np.diff(np.diff(z0_vals_low))
print(f"z_0 convex (low-TFP)? {np.all(z0_second_diff_low > -1e-6)}")
```

---

## References for Computational Methods

- **Cobb-Douglas Properties**: All derivations exploit homogeneity and the relationship between marginal and average products
- **Closed-Form Integration**: The expectation in equation (15) — and its extension (27a) — integrates in closed form by the power rule; no quadrature or special functions are required
- **Root Finding**: Interior solutions (equations 6, 7, 13, 14, 19, 20) are found by setting derivatives equal to costs
- **Parameter Space Partitioning**: Threshold loci divide $(\theta, \ln\bar{l})$ space into regions

---

## Conclusion

This online appendix provides complete mathematical derivations for all equations in "A Model of Enclosures." The derivations show how:

1. **First-best outcomes** (Section 3.2) emerge from a social planner equalizing marginal products
2. **Decentralized decisions** (Section 3.3) lead to labor misallocation due to open access
3. **Efficiency losses** (Section 4) arise from two offsetting externalities
4. **Institutional parameters** (Section 5) can improve outcomes but require coordinated reform
5. **Applications** (Section 6) connect the framework to historical and contemporary settings

All results are computationally implemented and verified in the accompanying Python code at `notebooks/enclose.py`.

---

**Document Prepared:** February 2026
**For:** Submission to *Review of Economic Studies*
**Code repository:** https://github.com/open-enclose/open-enclose.github.io
