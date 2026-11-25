"""Repo check for the weekly-review agent (v2).

Checks that every notebook in work/notebooks/ on GitHub is committed and executed:
filled code cells must have outputs and no cell may hold an error.
Skeleton placeholder cells ("# This cell is for CODE ...") and empty cells are ignored.

Usage:
    python work/agent/check_notebooks.py                 # checks the public repo on GitHub
    python work/agent/check_notebooks.py path/to/x.ipynb # checks local files (used in the eval)
"""
import json
import sys
import urllib.request

REPO = "h0pi/flyrank-ml-intenrship"
PLACEHOLDER = "# This cell is for CODE"


def check(nb):
    filled = [c for c in nb["cells"] if c["cell_type"] == "code"
              and "".join(c["source"]).strip() and not "".join(c["source"]).lstrip().startswith(PLACEHOLDER)]
    no_output = sum(1 for c in filled if not c.get("outputs"))
    errors = sum(1 for c in filled for o in c.get("outputs", []) if o.get("output_type") == "error")
    status = "OK" if filled and not no_output and not errors else "PROBLEM"
    if not filled:
        status = "EMPTY"
    return status, len(filled), no_output, errors


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "weekly-review-agent"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def main(paths):
    if paths:
        items = [(p, json.load(open(p, encoding="utf-8"))) for p in paths]
    else:
        listing = fetch(f"https://api.github.com/repos/{REPO}/contents/work/notebooks")
        items = [(f["name"], fetch(f["download_url"])) for f in listing if f["name"].endswith(".ipynb")]
    print(f"{'notebook':38} {'status':8} {'filled':>6} {'no output':>9} {'errors':>6}")
    bad = empty = 0
    for name, nb in items:
        status, filled, no_out, err = check(nb)
        bad += status == "PROBLEM"
        empty += status == "EMPTY"
        print(f"{name.split('/')[-1]:38} {status:8} {filled:>6} {no_out:>9} {err:>6}")
    print(f"\n{len(items)} notebooks: {bad} with problems, {empty} unused skeletons (EMPTY)")


if __name__ == "__main__":
    main(sys.argv[1:])
