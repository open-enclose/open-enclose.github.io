# Handoff — 2026-07-29

**Read `CLAUDE.md` first.** It holds the invariants; this file holds only *where things stand
right now*. When this handoff goes stale, delete it — `CLAUDE.md` is the durable document.

Written to start a **fresh conversation** for site and code work, rather than continuing one
whose context predates a large reorganisation.

## State

All four repositories are committed and in sync with their remotes. **184 tests pass.**

| Repo | HEAD | |
|---|---|---|
| `open-enclose.github.io` | `7af3a64` | this one — code, site, appendix |
| `enclosure_paper` (private) | `09d49bd` | Jonathan's working repo; its `README.md` maps the project |
| `enclosure_notebooks` (private) | `e105dd6` | **Matt's. Do not touch.** |
| `enclosure_book` | `4c4c849` | retired; serves a redirect only |

## What just changed here

- `8aa9545` — the mathematical appendix gained §6.4 in full, equations (37)–(43): the
  governance wedge $A_\mu$, the manufacturing margin, the equilibrium share, the planner's
  enclosure margin, three regimes, the compensation threshold. `content/03-manufacturing.md`
  lost a re-derivation that duplicated it.
- `7af3a64` — `CLAUDE.md` added.
- `enclose/` and `tests/` are **unchanged** since `bdecce6`.

Outside this repo: the appendix's second copy in `enclosure_book` is now a stub, that site is
retired behind a redirect, and roughly 260 files of research material moved from
`enclosure_book` into `enclosure_paper`.

## Phase 4: interactivity — built 2026-07-29, **not yet verified in a browser**

An explore page now exists and the whole pipeline is wired. Read the verification gap below
before trusting it. Nothing in this section is committed.

### What was built

- `enclose/numerics.py` — `safe_log_power` moved here out of `style.py`. This was the recorded
  blocker: `loci.py` imported it from `style.py`, which imports `matplotlib.patches`, so
  evaluating any locus pulled in the whole plotting stack.
- `tests/test_imports.py` — subprocess-based guard that `enclose`, `enclose.numerics`,
  `enclose.model` and `enclose.loci` leave matplotlib/scipy/sympy out of `sys.modules`, plus
  two converse tests so it cannot pass vacuously. **190 tests pass** (184 + 6).
- `myst.yml` — `project.jupyter.lite: true` and `project.static_files: [pyodide]`.
- `pyodide/enclose-0.1.0-py3-none-any.whl` — committed wheel, served at
  `/pyodide/enclose-0.1.0-py3-none-any.whl`.
- `content/05-explore.md` — added to the toc. Setup cell, one live figure, two `interact`
  slider sections, an open-ended cell.
- `deploy.yml` — MyST CLI pinned to `mystmd@^1.10`.

### Corrections to what this handoff previously said

- **"JupyterLite would be a separate build artifact, not a change to this flow" was wrong.**
  It is three lines in `myst.yml`. mystmd ships `thebe-lite`, which bundles a JupyterLite
  server and Pyodide into the static page. The build emits `thebe-core.min.js` /
  `thebe-lite.min.js` and nothing else changes — still no `--execute` in CI.
- **The scipy question resolves in favour of the browser.** scipy is in the Pyodide
  distribution, so `enclose.manufacturing` and its `brentq` solve can run live. Manufacturing
  figures do not need pre-rendering.
- **The "reported, not verified" claim about `interact`-readiness is now verified.** Every
  figure function takes keyword arguments with defaults; the single-panel ones take `ax=None`.

### New findings

- **`project.static_files` requires mystmd ≥ 1.10.** 1.9.1 logs
  `'config.project' extra key ignored: static_files` and builds a site where the wheel is
  simply missing — a silent failure that surfaces only as a runtime 404. The local `ecopy` env
  was on 1.9.1; CI was unpinned (`npm install -g mystmd`) and so happened to work. Now pinned
  to `^1.10`, with the reason recorded in `deploy.yml`.
- **Pyodide is fetched from `cdn.jsdelivr.net/pyodide/v0.27.0/full/`, not bundled.** The
  explore page therefore depends on a third-party CDN at runtime. Documented on the page.
- **The JupyterLite kernel runs in a Web Worker, so `js.window` does not exist.** The first
  draft used `js.window.location.origin` and failed with `AttributeError: window`. Confirmed
  against a real worker in this browser: `window` is `undefined`, `location.origin` is
  correct. The page now uses `js.location.origin`.

### The verification gap — read this

**The explore page has never been run end to end.** Confirmed:

- The site builds clean on mystmd 1.10.1 with no warnings.
- The wheel is served at the exact URL the page requests (HTTP 200, 30,974 bytes).
- `location.origin` resolves correctly inside a Web Worker in this browser.
- On one earlier run the kernel *did* boot, execute every cell, and fail only on the
  `js.window` line — so thebe-lite, the Pyodide boot and cell execution all work.

**Not** confirmed, because the browser automation stopped dispatching clicks to thebe's start
button after that first run:

- `micropip` actually installing the wheel from that URL.
- `enclose` importing under Pyodide's Python 3.12 / numpy 2.x.
- **`ipywidgets` sliders working under thebe-lite** — the version pairing this handoff
  flagged as historically finicky, and still the highest-risk item.

Someone should open the page in a real browser and click "start compute environment" before
this ships:

```bash
python -m http.server 8765 --directory _build/html
```

### Still true

- Any interactive page must **import from `enclose`**, not reimplement the model. Parallel
  implementations are what the reorganisation existed to remove, and one still survives in
  Matt's repo.
- **Do not regenerate `Figures/` into the repo.** Which figure set is canonical is unsettled.
- `myst.yml` uses an explicit `project.toc`; a page not listed there does not appear.
- `TODO.md` is gitignored and **badly stale** — it lists Phase 3 as pending although all four
  content pages ship and `Model_Construction.ipynb` is already in `archive/`, and it lists a
  `myst.yml` nav warning that can no longer occur (there is no `nav:` key). Rewrite or drop it.

### Local environment notes (this machine, 2026-07-29)

`CLAUDE.md` documents `mamba run -n ecopy python -m pytest tests/ -q`, but **mamba is not
installed here** — miniforge at `%LOCALAPPDATA%\miniforge3` ships only `conda.exe`, and it is
not on PATH. `ecopy` was also missing `pytest`, `python-build` and `nodejs`; all three were
installed from conda-forge, and `mystmd` was upgraded 1.9.1 → 1.10.1. Working invocation:

```bash
"$LOCALAPPDATA/miniforge3/envs/ecopy/python.exe" -m pytest tests/ -q
```

### Phase 5 is still untouched

`Figures/new_comp_fig.png`, the root `social_opt_cond.png`, `anaconda_projects/`, and retiring
`enclosure_book/notebooks/enclose.py` with its `enclose` name collision — all still present.
Phase 5 also removes that name collision, described as a latent trap.

## Also outstanding

- **Archive `enclosure_book`** once the revision clears — it is at conditional acceptance.
  Leave its `gh-pages` alone; older versions of the paper cite that URL.
- One item in `enclosure_paper/TASKS.md`: a sentence for the manuscript, to be added in
  Overleaf. Jonathan's, not an agent's.
- Jonathan is to speak with Matt about this repository. Until then the package is not
  established as canonical for figures.

## Working across two machines

`Y:\code\GitHub\` is a **Google Drive mirror of the same folder on both of Jonathan's
machines** — including `.git`. The repositories are not two clones; they are one set of files
seen from two places.

So there is **nothing to pull between machines** — but:

1. **Wait for Drive to finish syncing before working**, and before switching machines. Two
   machines writing git state simultaneously is how `.git/logs/HEAD[Conflict]` files got
   created in `enclosure_paper`, which broke `git gc` until they were removed.
2. If git reports `bad ref` or `invalid sha1 pointer`, look for `[Conflict]` files under
   `.git` first: `find .git -name "*\[Conflict\]*"`.
3. `enclosure_paper`'s `master`, `gh-pages` and `jc-edits` branches were **deleted** locally
   and on the remote on 2026-07-29; `main` is now the only branch and the GitHub default. If a
   stale checkout appears, `git fetch --prune && git switch main`.

Environment: `mamba run -n ecopy python -m pytest tests/ -q`.
