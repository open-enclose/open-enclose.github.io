r"""Check the figure table in `content/02-figures.md` against the paper's `main.tex`.

The site claims a figure number, a `\label` and a section for each of the paper's figures.
Nothing enforced those claims, and they were wrong: `trajectories.png` was listed among the
paper's figures with a section attribution although it appears nowhere in `main.tex`, and
two genuine paper figures (Figs. 3 and 4) were carried without numbers.

**Figure numbers come from source order.** LaTeX numbers floats in the order their
environments appear in the source, so the nth `\begin{figure}` in `main.tex` is Figure n.
That is what this script relies on, and it is why moving a figure silently renumbers
everything after it — the failure mode the `\label` column exists to survive.

The paper lives in a sibling repository that CI does not check out, so this is a script
rather than a test. `tests/test_figures.py` runs it when the paper is present and skips
otherwise.

    python scripts/check_figure_map.py [--tex PATH]
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEX = ROOT.parent / "enclosure_paper" / "main.tex"
PAGE = ROOT / "content" / "02-figures.md"


def paper_figures(tex_path):
    r"""[(number, filename, label)] in source order — i.e. in printed-number order."""
    lines = tex_path.read_text(encoding="utf8", errors="replace").splitlines()
    out, start = [], None
    for i, ln in enumerate(lines):
        if re.search(r"\\begin\{figure\*?\}", ln):
            start = i
        elif re.search(r"\\end\{figure\*?\}", ln) and start is not None:
            body = "\n".join(lines[start:i])
            g = re.search(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}", body)
            lab = re.search(r"\\label\{([^}]*)\}", body)
            if g:
                out.append((len(out) + 1, g.group(1).split("/")[-1],
                            lab.group(1) if lab else None))
            start = None
    return out


def site_table():
    """[(number, label, png)] parsed out of the page's figure table."""
    rows = []
    for ln in PAGE.read_text(encoding="utf8").splitlines():
        m = re.match(r"\|\s*Fig\.\s*(\d+)\s*\|\s*`([^`]+)`\s*\|[^|]*\|\s*`([^`]+)`", ln)
        if m:
            rows.append((int(m.group(1)), m.group(2), m.group(3)))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex", type=Path, default=DEFAULT_TEX)
    args = ap.parse_args()

    if not args.tex.is_file():
        print(f"paper not found at {args.tex} -- nothing to check against")
        return 0

    paper = paper_figures(args.tex)
    site = site_table()
    problems = []

    by_num = {n: (png, lab) for n, png, lab in paper}
    for num, label, png in site:
        if num not in by_num:
            problems.append(f"site claims Fig. {num}, paper has only {len(paper)} figures")
            continue
        p_png, p_lab = by_num[num]
        if png != p_png:
            problems.append(f"Fig. {num}: site says {png}, main.tex includes {p_png}")
        if label != p_lab:
            problems.append(f"Fig. {num}: site label `{label}`, main.tex `{p_lab}`")

    claimed = {png for _, _, png in site}
    for n, png, lab in paper:
        if png not in claimed:
            problems.append(f"main.tex Figure {n} ({png}, \\label{{{lab}}}) is missing "
                            f"from the site table")

    # The reverse error that was actually present: a site-only figure presented as the
    # paper's. Anything in the paper-figure table must really be in main.tex.
    in_paper = {png for _, png, _ in paper}
    for num, label, png in site:
        if png not in in_paper:
            problems.append(f"site lists {png} as Fig. {num}, but main.tex never includes it")

    print(f"paper: {len(paper)} figures    site table: {len(site)} rows\n")
    for n, png, lab in paper:
        mark = "ok " if any(s[0] == n and s[2] == png for s in site) else "MISSING"
        print(f"  {mark}  Figure {n}: {png:<26} \\label{{{lab}}}")

    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("\nfigure map agrees with main.tex")
    return 0


if __name__ == "__main__":
    sys.exit(main())
