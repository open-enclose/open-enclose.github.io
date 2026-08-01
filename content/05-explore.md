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
resp = await pyfetch(WHEEL_URL)
if resp.status != 200:
    raise RuntimeError(f"HTTP {resp.status} fetching {WHEEL_URL}")
with open(WHEEL_NAME, "wb") as fh:
    fh.write(await resp.bytes())

# `emfs:` means "a wheel already sitting in the Emscripten virtual filesystem".
await micropip.install(f"emfs:{WHEEL_NAME}", deps=False)

print("installed from", WHEEL_URL)
```

```{code-cell} python
:tags: [hide-input]
import numpy as np
import matplotlib.pyplot as plt

from enclose import figures, loci, model

print("enclose", __import__("enclose").__version__, "loaded in the browser")
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

Push both sliders to 1 and the red band lands exactly on the black one. That coincidence is
the paper's Key Result (§5.3) — the wedge closes only when commons governance and
compensation are *both* complete. Neither alone suffices, which you can check by pushing one
slider to 1 while leaving the other at 0.

```{code-cell} python
:tags: [hide-input]
from ipywidgets import interact, FloatSlider

def wedge(mu=0.0, tau=0.0):
    fig, ax = figures.wedge_panel(mu=mu, tau=tau)
    plt.show()

interact(
    wedge,
    mu=FloatSlider(value=0.0, min=0.0, max=1.0, step=0.05,
                   description=r"$\mu$ (governance)", style={"description_width": "initial"}),
    tau=FloatSlider(value=0.0, min=0.0, max=1.0, step=0.05,
                    description=r"$\tau$ (compensation)", style={"description_width": "initial"}),
);
```

The four corners, side by side, are the paper's Figure 6:

```{code-cell} python
:tags: [hide-input]
fig, ax = figures.combined_4x4()
```

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

The wheel is committed at `pyodide/enclose-0.1.0-py3-none-any.whl`, rebuilt by CI ahead of the
test suite, and byte-compared against the source by `tests/test_wheel.py` — so what runs here
cannot lag what the tests pass against. If a result here still disagrees with the
[figures page](02-figures.md),
[open an issue](https://github.com/open-enclose/open-enclose.github.io/issues).
