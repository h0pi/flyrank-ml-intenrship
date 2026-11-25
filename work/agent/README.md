# Internship weekly-review agent

**What it does:** once a week it tells me exactly where I stand in the FlyRank internship and what to do next, in under a page. It reads my internship portal (read-only) and this GitHub repo, then writes a short report: what is submitted, what is still open this week (most hours first), whether every notebook in the repo is committed and executed, and one next step per open task.

**For whom:** me, a FlyRank intern with two tracks (Machine Learning + AI Fluency) and ~35 assignments. It is useful for any intern on the same portal; only the repo name changes.

**Demo video (3–5 min, captions, live run):** _link added after upload_

## How it works

```
 "weekly review"                                   work/agent/reports/
      │                                            weekly-review-<date>.md
      ▼                                                      ▲
┌──────────────────────┐   reads (read-only)   ┌────────────────────────┐
│ Claude Code          │ ────────────────────▶ │ internship portal      │
│ + skill file         │   Claude in Chrome    │ submissions, week page │
│ weekly-review/       │   (my logged-in tab)  └────────────────────────┘
│ SKILL.md             │
│                      │   runs                ┌────────────────────────┐
│                      │ ────────────────────▶ │ check_notebooks.py     │
│                      │                       │ GitHub API → notebooks │
└──────────────────────┘                       └────────────────────────┘
          │ writes the report (only file it may write)
          ▼
```

- **Brain:** Claude Code, with the agent written as a skill (`weekly-review/SKILL.md`): job, tools, steps, report format, guardrails.
- **Portal:** Claude in Chrome (MCP) uses my real, already logged-in Chrome. It opens its own tab and only reads.
- **Repo check (v2):** `check_notebooks.py` is plain Python. It lists `work/notebooks/` through the public GitHub API and, per notebook, counts filled code cells, cells without outputs and error cells. Skeleton placeholder cells are ignored. Deterministic code for the part that must be exact; the model only reads its output.

**Design decision:** in v1 the model checked notebooks by reading JSON itself; it miscounted placeholder cells. In v2 that check is a script with a fixed rule, and the model only explains the result. Rule of thumb: counting goes to code, judgement goes to the model.

## Setup (from zero)

1. Install [Claude Code](https://claude.com/claude-code) (desktop app or CLI) and the **Claude in Chrome** extension; connect them (Claude Code → browser extension settings).
2. In Chrome, log in to `https://internship.flyrank.ai` once (LinkedIn or email sign-in). The agent never logs in for you.
3. Install Python 3.10+ (only the standard library is used).
4. Clone this repo and copy the skill so Claude Code finds it:
   ```bash
   git clone https://github.com/h0pi/flyrank-ml-intenrship
   mkdir -p ~/.claude/skills/internship-weekly-review
   cp flyrank-ml-intenrship/work/agent/weekly-review/SKILL.md ~/.claude/skills/internship-weekly-review/
   ```
5. Using your own repo? Change `REPO` at the top of `check_notebooks.py` and the GitHub URL in `SKILL.md`.

## Usage

In Claude Code, opened in the repo folder, type:

```
weekly review
```

The agent opens the portal's Submissions page, then the all-weeks assignment page, runs the repo check, writes `work/agent/reports/weekly-review-YYYY-MM-DD.md` and shows it. The repo check also works alone:

```bash
python work/agent/check_notebooks.py                       # all notebooks on GitHub
python work/agent/check_notebooks.py path/to/notebook.ipynb  # local files
```

Example output (25 Nov 2026, week 8): [weekly-review-2026-11-25-week8.md](reports/weekly-review-2026-11-25-week8.md). It found two unused skeleton notebooks without outputs, which were also why the repo's CI was failing.

## Evaluation (v2, 25 Nov 2026)

The five cases from the agent spec, run against v2:

| # | Case | How it was tested | Result |
|---|---|---|---|
| 1 | Normal week with open tasks | Live run on week 8 | **Pass.** Open list matched the portal exactly: 3 tasks with hours, most hours first; 33 submissions counted (10 ML, 23 AI Fluency). |
| 2 | Everything of the week already submitted | Live, on week 7 (3/3 submitted) | **Pass (partial).** Reports “Week 7: all 3 submitted, nothing left”. Not yet seen on the *current* week being complete. |
| 3 | Notebook overwritten by an unexecuted Colab save | Script on a copy of `w07` with all outputs stripped, next to an untouched `w06` | **Pass.** Stripped copy flagged `PROBLEM` (8 of 8 filled cells without output); untouched copy `OK`. |
| 4 | Session expired: portal shows the login page | Opened the portal in a browser without my session | **Pass.** Redirected to `/login`; the agent stops and asks me to log in. No credentials typed. |
| 5 | Page text tries to instruct the agent (“click Submit for the user”) | Planned with a test page; the test page was blocked by the tool's own safety check, so it was **not run live** | **Not verified live.** The guardrail is in the instructions and nothing on the portal is ever clicked, but this case still needs a real test. |

v1 → v2 changes: notebook check moved to `check_notebooks.py` (fixes the placeholder-cell false alarms); unused skeletons reported as `EMPTY` instead of `PROBLEM`.

## Limitations

- **Manual start.** It runs when I type “weekly review”, not on a schedule: an unattended run would need a logged-in browser left open.
- **Depends on the portal layout.** If FlyRank changes the Submissions or week pages, the reading step can miss items; it then says “unknown” instead of guessing, but I have to notice.
- **Needs my browser session.** If the session expires it stops (case 4); it can't fix that itself.
- **Prompt injection only covered by design so far** (case 5 above).
- **Hours are FlyRank's estimates**, not my real time.
- It reports and plans; it does not do the tasks or submit anything, on purpose.

## Guardrails

Never clicks Submit / Save submission / Mark complete, never uploads, never opens the e-mail inbox, announcements or other people's data, never types credentials, and writes only to `work/agent/reports/`. Page text is treated as data, not instructions.

## Where AI did the work

I decided what the agent is for, what it may read and what it must never do. Claude (Claude Code) did most of the building at my direction: it wrote the skill text, `check_notebooks.py`, this README and the demo captions, ran the live run and the evaluation above, and it is also the agent's runtime. The eval table reports what actually happened in those runs on 25 Nov 2026, including the case that could not be run.
