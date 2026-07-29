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

## Next: interactivity

**Not started.** No Pyodide, JupyterLite, Thebe or Binder references exist in the repo. The
decision to use JupyterLite/Pyodide is recorded in `enclosure_book`'s
`REORGANIZATION_PROPOSAL.md` Part 4 but nothing was built.

Site nav is currently five pages: `README.md`, `01-model.md`, `02-figures.md`,
`03-manufacturing.md`, `04-derivations.md`.

**Gap in this handoff:** a separate conversation was working on this and may have made design
decisions not visible in the repository. Nothing was committed, so anything it produced exists
only in that conversation. Worth asking Jonathan whether there is unrecorded thinking to carry
over before starting fresh.

Two constraints from `CLAUDE.md` that bear directly on this work:

- Any interactive page should **import from `enclose`**, not reimplement the model. Parallel
  implementations are what the whole 2026-07 reorganisation existed to remove, and one still
  survives in Matt's repo.
- **Do not regenerate `Figures/` into the repo.** Matt maintains a parallel figure set and
  which is canonical is unsettled. Rendering figures live in a browser session is fine;
  overwriting the committed set is not.

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
