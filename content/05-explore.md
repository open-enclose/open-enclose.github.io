---
title: Explore the Model in Your Browser
short_title: Explore
kernelspec:
  name: python3
  display_name: Python 3
---

# Explore the Model in Your Browser

Every other page on this site shows figures that were rendered ahead of time. This one does
not. The cells below run **in your browser** — no server, no account, no install — and they
call the same [`enclose`](https://github.com/open-enclose/open-enclose.github.io/tree/main/enclose)
package that generates the paper's figures. Nothing here is a second implementation of the
model; that is the whole point of the package existing.

The source of each cell is collapsed. Use the toggle on a cell to read or edit it.

:::{warning} First load is slow, and needs a CDN
Starting the kernel downloads a Python runtime and the scientific stack — tens of megabytes.
Expect roughly half a minute the first time, then near-instant afterwards while the page stays
open. Once the model is loaded, evaluation is genuinely fast: every locus is closed-form numpy.

The runtime itself comes from `cdn.jsdelivr.net`, not from this site — that is where
`thebe-lite` fetches Pyodide from. On a network that blocks jsDelivr, this page will not
start. Nothing else on this site depends on it.
:::

## How this works

The site is static HTML on GitHub Pages. It gains a Python kernel through
[JupyterLite](https://jupyterlite.readthedocs.io/), which runs CPython compiled to
WebAssembly ([Pyodide](https://pyodide.org/)) inside the browser tab. MyST wires this up with
three lines in `myst.yml`:

```yaml
project:
  jupyter:
    lite: true
```

The one thing that is not automatic is `enclose` itself — it is not on PyPI, and Pyodide only
knows about packages in its own distribution. So the build ships a wheel as a static asset and
the first cell installs it from this site.

## Setup

```{code-cell} python
:tags: [hide-input, hide-output]
import micropip
import js
from pyodide.http import pyfetch

# Resolved against wherever this page is served from, so the same cell works on the deployed
# site and under a local `myst start`. `/pyodide/` is a `static_files` entry in myst.yml,
# copied to the site root at build time.
#
# `js.location`, not `js.window.location`: the JupyterLite kernel runs in a Web Worker, where
# there is no `window` and the global is a WorkerGlobalScope. Same origin either way.
BASE = js.location.origin
WHEEL_NAME = "enclose-0.1.0-py3-none-any.whl"
WHEEL_URL = f"{BASE}/pyodide/{WHEEL_NAME}"

# numpy and matplotlib ship with Pyodide, so micropip resolves them from its own lockfile
# rather than PyPI. Two of `enclose`'s four dependencies are deliberately left out, because
# nothing on this page reaches the modules that need them:
#   sympy -- `enclose.symbolic`, which re-derives every locus from its objective and checks
#            the numeric layer against it. That check belongs in the test suite.
#   scipy -- `enclose.manufacturing`, whose three-sector equilibrium is transcendental and
#            needs `brentq`. Add "scipy" below to explore that extension here.
#
# ipywidgets is NOT preinstalled and the major version is not free to choose. thebe bundles
# the browser half of the widget protocol, and its `@jupyter-widgets/controls` is 2.0.0 --
# the ipywidgets 8 protocol. Pair it with ipywidgets 7 and the sliders render as blank space
# with no error, because the front end cannot resolve the model. Check `CONTROLS_VERSION` in
# `thebe-core.min.js` before changing this pin.
await micropip.install(["numpy", "matplotlib", "ipywidgets>=8,<9"])

# Fetch the wheel ourselves rather than handing micropip the URL. Given a URL together with
# deps=False, micropip can reach its install step with nothing downloaded and raise
# "Micropip internal error: attempted to install wheel before downloading it?". Fetching
# explicitly also means a bad path fails here, with a status code you can read, instead of
# surfacing as an internal error several frames deep in micropip.
#
# cache="no-store" is load-bearing. The wheel's filename never changes, so every deploy
# replaces a URL the browser may already hold, and GitHub Pages serves it with
# `Cache-Control: max-age=600`. Without this a reader gets up to ten minutes of the previous
# build's model code while the surrounding page is current -- which is not a hypothetical:
# it shipped a heatmap with white gridlines and no axis labels after both had been fixed,
# deployed and verified on the server. There is no build step here to hash the filename
# with, so the fetch declines the cache instead.
resp = await pyfetch(WHEEL_URL, cache="no-store")
if resp.status != 200:
    raise RuntimeError(f"HTTP {resp.status} fetching {WHEEL_URL}")
wheel_bytes = await resp.bytes()
with open(WHEEL_NAME, "wb") as fh:
    fh.write(wheel_bytes)

# `emfs:` means "a wheel already sitting in the Emscripten virtual filesystem".
await micropip.install(f"emfs:{WHEEL_NAME}", deps=False)

# Fingerprint what actually got installed, reported by the next cell (this one's output is
# hidden, and micropip is noisy). If a figure here ever disagrees with the source on GitHub,
# this is the first thing to check.
import hashlib

WHEEL_SHA = hashlib.sha256(wheel_bytes).hexdigest()[:12]
WHEEL_SIZE = len(wheel_bytes)
print("installed from", WHEEL_URL)
```

```{code-cell} python
:tags: [hide-input]
import numpy as np
import matplotlib.pyplot as plt

from enclose import figures, loci, model, welfare

print("enclose", __import__("enclose").__version__, "loaded in the browser")
print(f"wheel {WHEEL_SIZE:,} bytes, sha256 {WHEEL_SHA}")
```

## A figure, rendered here rather than shipped

The same call that produces `social_opt_cond.png` in the paper. If this renders, the whole
path works: wheel delivery, Pyodide, matplotlib, and the package's own figure code.

```{code-cell} python
:tags: [hide-input]
fig, ax = figures.social_optimum(cond_opt=True)
```

## Closing the wedge: $\mu$ and $\tau$ on one panel

This is the figure the site exists to make interactive.

Figure 6 of the paper shows four panels at the corners of the $(\mu, \tau)$ square —
$(0,0)$, $(1,0)$, $(0,1)$, $(1,1)$ — and asks you to interpolate between them in your head.
Here both parameters are continuous on a single panel, so you can watch the interpolation
instead.

- **Black** is the first-best band. It does not move: $\mu$ and $\tau$ are institutions, and
  the first-best is defined without reference to them.
- **Red** is the decentralized band. It moves with both sliders.
- **Dashed blue** are the second-best loci — the constrained planner, who takes the
  decentralized labor allocation as given but chooses $t_e$. These move with $\mu$ **only**.
- The dotted verticals are $\theta = 1$ and $\theta_H^\mu$. The second one moves with $\mu$:
  it is $1/\alpha - \mu(1-\alpha)/\alpha$, and it is also where the second-best objective
  switches from convex to concave.

Push $\mu$ and $\tau$ to 1 and the red band lands exactly on the black one. That coincidence is
the paper's Key Result (§5.3) — the wedge closes only when commons governance and
compensation are *both* complete. Neither alone suffices, which you can check by pushing one
slider to 1 while leaving the other at 0.

:::{note} What $\alpha$ does, and why it is not like the other two
$\mu$ and $\tau$ are *institutions*: they move the decentralized loci across a fixed canvas.
$\alpha$ is **technology**, and it rescales the canvas itself — which is why the axes move
when you drag it and not when you drag the others.

Its main role is that it sets the upper threshold outright:

$$\theta_H = \frac{1}{\alpha}, \qquad \theta_H^\mu = \frac{1}{\alpha} - \mu\frac{1-\alpha}{\alpha}$$

Raising $\alpha$ pulls $\theta_H$ down toward 1 and **shrinks the strategic-complements
region** — the band below $\theta_H$ where enclosure decisions reinforce one another,
equilibrium is multiple, and the outcome is selected rather than determined. A labor-intensive
technology ($\alpha \to 1$) leaves almost no room for that: nearly every economy sits above
$\theta_H$, where the private enclosure rate is unique and moves smoothly. A land-intensive
one ($\alpha$ small) makes the coordination region wide, and races the dominant failure.

Two further consequences are worth watching for as you drag it:

- **Steepness.** Every locus scales as $(c/A)^{1/\alpha}$, so $\alpha$ sets how sharply the
  thresholds respond to density. Low $\alpha$ stretches the picture vertically: small changes
  in $\bar l$ swing the enclosure decision much further.
- **The size of the labor wedge.** The gap between private and planner labor intensity is
  $\Lambda_o/\Lambda_\mu = (A_\mu/\alpha)^{1/(1-\alpha)}$, which at $\mu=0$ is
  $\alpha^{-1/(1-\alpha)}$ — the open-access distortion is *worse* the more land-intensive
  production is, because that is when the possession rent commoners capture is largest.

At $\alpha=1$ land would earn nothing and the model has nothing to be about; the slider stops
at 0.9.
:::

```{code-cell} python
:tags: [hide-input]
from ipywidgets import interact, FloatSlider

def wedge(mu=0.0, tau=0.0, alp=2/3):
    fig, ax = figures.wedge_panel(mu=mu, tau=tau, alp=alp)
    plt.show()

interact(
    wedge,
    mu=FloatSlider(value=0.0, min=0.0, max=1.0, step=0.05,
                   description=r"$\mu$ (governance)", style={"description_width": "initial"}),
    tau=FloatSlider(value=0.0, min=0.0, max=1.0, step=0.05,
                    description=r"$\tau$ (compensation)", style={"description_width": "initial"}),
    # alpha rescales the axes, so unlike mu and tau it moves the canvas as well as the
    # curves -- see `figures._wedge_window`.
    alp=FloatSlider(value=2/3, min=0.45, max=0.9, step=0.01,
                    description=r"$\alpha$ (labor share)", readout_format=".2f",
                    style={"description_width": "initial"}),
);
```

The four corners, side by side, are the paper's Figure 6:

```{code-cell} python
:tags: [hide-input]
fig, ax = figures.combined_4x4()
```

## How much output is actually lost

:::{warning} Exploratory, and not reviewed by both authors
Everything above this heading is the published paper. This section is not: it is work in
progress, computed and tested but not yet reviewed by both co-authors. Treat the *shapes* as
findings and the numbers as provisional.
:::

The loci say *where* private and social enclosure decisions diverge. They do not say by how
much. `enclose.welfare` answers that by comparing three economies at every point of the same
$(\theta, \ln\bar l)$ plane — each a pair of a labor rule and an enclosure rate:

| regime | labor allocated by | enclosure rate $t_e$ |
|:---|:---|:---|
| **First-best** $W^{FB}$ | $\Lambda_o$ — marginal products equated | maximizes $z$ |
| **Second-best** $W^{SB}$ | $\Lambda_\mu$ — the *decentralized* rule, taken as given | maximizes $z_0^\mu$ |
| **Private** $W^{P}$ | $\Lambda_\mu$ | $t_e^d$ where $r(t_e)=c$, global-games selected |

The second-best planner is what makes the exercise work: it **inherits the labor distortion
it cannot fix** but chooses enclosure freely. That separates the two failures, so net output
$W^k = Y^k - c\,t_e^k$ splits exactly:

$$\underbrace{W^{FB} - W^{P}}_{\text{total foregone}}
  = \underbrace{W^{FB} - W^{SB}}_{\text{labor misallocation}}
  + \underbrace{W^{SB} - W^{P}}_{\text{enclosure error}}$$

Both terms are non-negative by construction, not by luck, and `build_grid` asserts the
orderings and the identity at every grid point rather than taking them on trust.

```{code-cell} python
:tags: [hide-input]
from ipywidgets import Dropdown

def losses(mu=0.0, tau=0.0, component="total", normalize="ratio", n=121):
    figures.loss_panel(mu=mu, tau=tau, component=component, normalize=normalize, n=n)
    plt.show()

# continuous_update=False: each redraw is a full grid solve, so recompute on release rather
# than on every pixel of the drag. Drop `grid` to 61 if that still feels slow -- cost is
# quadratic in it, and no conclusion on this page depends on the resolution.
interact(
    losses,
    mu=FloatSlider(value=0.0, min=0.0, max=1.0, step=0.05, continuous_update=False,
                   description=r"$\mu$ (governance)", style={"description_width": "initial"}),
    tau=FloatSlider(value=0.0, min=0.0, max=1.0, step=0.05, continuous_update=False,
                    description=r"$\tau$ (compensation)", style={"description_width": "initial"}),
    component=Dropdown(options=list(welfare.COMP_LABEL), value="total",
                       description="component", style={"description_width": "initial"}),
    normalize=Dropdown(options=list(welfare.NORM_LABEL), value="ratio",
                       description="normalize", style={"description_width": "initial"}),
    n=Dropdown(options=[61, 91, 121, 161], value=121,
               description="grid", style={"description_width": "initial"}),
);
```

Three things are worth looking for.

**The losses live in a band, and its edges are curves the paper already draws.** Everything
outside is flat zero. At low density nobody encloses; at high density everybody does; both
are right. Inefficiency is a *transitional* phenomenon, confined to where the decision is
genuinely close — which is why the overlaid loci are not decoration. The paper's diagrams
turn out to be the boundaries of this surface rather than separate objects.

**The enclosure error dominates the misallocation.** Switch `component` between the two. The
open-access labor distortion — the classic tragedy-of-the-commons story — tops out near 5% of
first-best. Getting the *enclosure decision* wrong costs several times that. The misallocation
wedge also vanishes at both corners by construction, since with all land in one state there is
nothing to misallocate between, so it is intrinsically an interior, second-order effect.

**Below $\theta = 1$, enclosure has no productivity rationale and happens anyway.** Both
planners enclose nothing there. Private agents enclose fully once density passes a threshold,
because enclosure captures rents that open access was dissipating — with a misallocation
component of exactly zero. Redistribution dressed as improvement, triggered by *density*, not
by any change in technology.

:::{note} Why the three normalizations disagree
They are not rescalings of one another. Output per unit land scales as $\bar l^{\alpha}$, so
output per worker scales as $\bar l^{\alpha-1}$ and *falls* in density. Switching to
`per_worker` therefore upweights sparse economies hard enough to move the worst-affected
economy to the opposite corner of the plane — from poor-and-crowded to
productive-and-land-abundant. The `ratio` is the default because it is the only one invariant
to the choice.
:::

### Does either reform work alone?

The Key Result is stated in locus terms — at $\mu=\tau=1$ the decentralized loci become
*identical* to the planner's. In output terms it becomes quantitative, and stronger:

```{code-cell} python
:tags: [hide-input]
grid = [0.0, 0.25, 0.5, 0.75, 1.0]

print("mean total loss, % of first-best")
print("        " + "".join(f"  tau={t:<5.2f}" for t in grid))
for mu in grid:
    row = ""
    for tau in grid:
        _, _, S = welfare.build_grid(n_th=31, n_l=31, mu=mu, tau=tau)
        # Clamped: non-negative by theorem, but at mu=tau=1 the two objectives coincide
        # exactly and the mean lands a few times 1e-16 below zero. Printing "-0.00" there
        # would read as a bug rather than as the exact-zero result it is.
        row += f"{max(0.0, 100 * S['total'].mean()):9.2f}"
    print(f"  mu={mu:4.2f}" + row)
```

The diagonal falls monotonically to zero: joint reform works, and works smoothly. But **both
axes are U-shaped, and both end worse than doing nothing** — unilateral reform is not merely
insufficient, it is counterproductive at the limit. Raising $\mu$ alone fixes the smaller
wedge while widening the gap between private and social enclosure incentives, because a
well-run commons has value that enclosers still do not pay for. Raising $\tau$ alone converts
over-enclosure into under-enclosure; set `component` to `over_enclosure` and then
`under_enclosure` and sweep $\tau$ to watch the trade.

Read the means as shape, not level: they are unweighted averages over an arbitrary rectangle
of $(\theta, \ln\bar l)$, not a welfare criterion, and the minimizing $\tau$ moves with the
window.

## Going further

Every locus is a plain function of $\theta$, so anything on this page can be rebuilt from
parts. Edit the cell below and re-run it.

```{code-cell} python
:tags: [hide-input]
theta = np.linspace(1.01, 2.5, 300)

fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(theta, loci.ln_l01(theta), label=r"first-best, no enclosure  (eq. 6)")
ax.plot(theta, loci.ln_ld0(theta), label=r"decentralized, $\tau=0$")
ax.plot(theta, loci.ln_ld0(theta, tau=1.0), label=r"decentralized, $\tau=1$")
ax.set_xlabel(r"$\theta$ (rel. TFP)")
ax.set_ylabel(r"$\ln(\overline{l})$ (log population density)")
ax.legend()
plt.show()
```

:::{note} The parameters
The paper's diagrams are drawn at $\alpha = 2/3$ and $c/A = 1$, which the loci carry as
defaults. `loci.C` is the paper's $c/A$, not $c$ — see the note on the
[figures page](02-figures.md). Welfare and output *levels* are therefore in units of $A$;
thresholds and ratios are not affected.
:::

## If something here is broken

Three things can fail independently:

- **The kernel never starts.** Pyodide is fetched from `cdn.jsdelivr.net`; check the network
  tab for a blocked or failed request there.
- **The setup cell errors.** The wheel did not load — look for a 404 or a CORS refusal on
  `/pyodide/enclose-0.1.0-py3-none-any.whl`. That path is produced by `project.static_files`
  in `myst.yml`, which **mystmd 1.9 and earlier silently ignore**, so a build on an old CLI
  produces a site whose wheel is simply absent. CI pins `mystmd@^1.10` for this reason.
- **The sliders render but do nothing.** That is the `ipywidgets`↔JupyterLite pairing, not
  the model — the figures above the sliders will still be correct.

- **A figure looks like an older version of itself.** The wheel's filename is fixed, so each
  deploy replaces a URL your browser may already hold. The setup cell fetches with
  `cache="no-store"` to prevent that, but a kernel already running from a previous visit has
  `enclose` imported and will not re-import it. Reload the page, which restarts the kernel.
  The sha256 printed by the second cell tells you which build you are on: compare it against
  a clone with

  ```bash
  python -c "import hashlib;print(hashlib.sha256(open('pyodide/enclose-0.1.0-py3-none-any.whl','rb').read()).hexdigest()[:12])"
  ```

The wheel is committed at `pyodide/enclose-0.1.0-py3-none-any.whl`, rebuilt by CI ahead of the
test suite, and byte-compared against the source by `tests/test_wheel.py` — so what the *site
serves* cannot lag what the tests pass against. Caching is a separate matter, handled above.
If a result here still disagrees with the [figures page](02-figures.md) once the fingerprints
match, [open an issue](https://github.com/open-enclose/open-enclose.github.io/issues).
