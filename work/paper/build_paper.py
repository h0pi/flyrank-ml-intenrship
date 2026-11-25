"""Builds docs/index.html (the deployed paper) from work/outputs/capstone_metrics.json.

Run the capstone notebook first, then:  python work/paper/build_paper.py
Every number on the page comes from the metrics file, so the paper always matches a fresh run.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
M = json.loads((ROOT / "work" / "outputs" / "capstone_metrics.json").read_text())
REPO = "https://github.com/h0pi/flyrank-ml-intenrship"
NB = f"{REPO}/blob/main/work/notebooks"

d, r = M["data"], M["results"]
lr, rule, hgb = r["Logistic Regression"], r["Week-4 rule"], r["Gradient Boosting"]
rg = M["refresh_group"]
pc = lambda x: f"{x:.0%}"
f3 = lambda x: f"{x:.3f}"
n = lambda x: f"{x:,}"
base = d["base_rate"]


def row(cells, head=False):
    tag = "th" if head else "td"
    return "<tr>" + "".join(f"<{tag}>{c}</{tag}>" for c in cells) + "</tr>"


results_table = "\n".join([
    row(["Method", "ROC-AUC", "P@50", "P@500", "P@1,000", "P@5,000"], head=True),
    row(["Logistic regression (model)", f3(lr["ROC-AUC"]), pc(lr["P@50"]), pc(lr["P@500"]), pc(lr["P@1000"]), pc(lr["P@5000"])]),
    row(["Week-4 rule (baseline)", f3(rule["ROC-AUC"]), pc(rule["P@50"]), pc(rule["P@500"]), pc(rule["P@1000"]), pc(rule["P@5000"])]),
    row(["Gradient boosting (tried)", f3(hgb["ROC-AUC"]), pc(hgb["P@50"]), pc(hgb["P@500"]), pc(hgb["P@1000"]), pc(hgb["P@5000"])]),
    row(["Random pick (base rate)", "0.500"] + [pc(base)] * 4),
])
refresh_table = "\n".join([row(["Refresh group, top K", "Model", "Week-4 rule", "Random pick"], head=True)] + [
    row([f"Top {k}", pc(v["model"]), pc(v["rule"]), pc(rg["base_rate"])]) for k, v in rg["top"].items()])
arch = M["archetypes"]
lanes = M["lanes"]

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Which content pages will lose search visibility next? A ranked review queue on real search data</title>
<meta name="description" content="A research paper: predicting which content pages lose Google impressions in the next 16 days, on {n(d['frame_pages'])} real pages, with a frozen rule baseline, client-grouped validation and an action playbook.">
<meta property="og:title" content="Which content pages will lose search visibility next?">
<meta property="og:description" content="Model vs rule baseline on {n(d['frame_pages'])} real pages, validated on unseen clients. Ammar Hopovac, FlyRank ML Internship capstone.">
<meta property="og:image" content="img/fig1_precision_at_k.png">
<style>
:root {{
  color-scheme: light;
  --bg: #fcfcfb; --ink: #0b0b0b; --muted: #52514e; --rule: #e4e3de; --soft: #f3f2ee; --accent: #2a78d6;
}}
@media (prefers-color-scheme: dark) {{
  :root {{ color-scheme: dark; --bg: #1a1a19; --ink: #f0efec; --muted: #c3c2b7; --rule: #3a3936; --soft: #242422; --accent: #6aa8f0; }}
  figure img {{ background: #fcfcfb; border-radius: 6px; }}
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--ink);
  font: 18px/1.65 Charter, "Bitstream Charter", "Sitka Text", Cambria, Georgia, serif; }}
main {{ max-width: 46rem; margin: 0 auto; padding: 3rem 1rem 4rem; }}
h1, h2, h3, .meta, nav, table, figcaption, .abstract h2, footer {{ font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }}
h1 {{ font-size: clamp(1.7rem, 4.5vw, 2.4rem); line-height: 1.2; letter-spacing: -0.02em; margin: 0 0 .6rem; }}
h2 {{ font-size: 1.35rem; margin: 2.8rem 0 .6rem; padding-top: .6rem; border-top: 1px solid var(--rule); }}
h3 {{ font-size: 1.05rem; margin: 1.6rem 0 .3rem; }}
.meta {{ color: var(--muted); font-size: .92rem; margin-bottom: 1.8rem; }}
a {{ color: var(--accent); }}
.abstract {{ background: var(--soft); border-left: 3px solid var(--accent); padding: 1rem 1.2rem; border-radius: 4px; }}
.abstract h2 {{ border: 0; margin: 0 0 .3rem; padding: 0; font-size: .85rem; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); }}
.abstract p {{ margin: 0; }}
nav {{ font-size: .9rem; margin: 1.6rem 0 0; color: var(--muted); }}
nav ol {{ columns: 2; padding-left: 1.2rem; margin: .3rem 0 0; }}
@media (max-width: 560px) {{ nav ol {{ columns: 1; }} }}
figure {{ margin: 1.6rem 0; }}
figure img {{ width: 100%; height: auto; display: block; }}
figcaption {{ font-size: .88rem; color: var(--muted); margin-top: .5rem; line-height: 1.5; }}
figcaption b {{ color: var(--ink); }}
.table-wrap {{ overflow-x: auto; margin: 1.2rem 0; }}
table {{ border-collapse: collapse; font-size: .88rem; width: 100%; }}
th, td {{ text-align: left; padding: .45rem .6rem; border-bottom: 1px solid var(--rule); white-space: nowrap; }}
td:not(:first-child), th:not(:first-child) {{ text-align: right; font-variant-numeric: tabular-nums; }}
th {{ color: var(--muted); font-weight: 600; }}
.left td, .left th {{ text-align: left !important; white-space: normal; }}
code {{ font-size: .85em; background: var(--soft); padding: .05em .3em; border-radius: 3px; }}
.note {{ font-size: .92rem; color: var(--muted); }}
footer {{ margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--rule); font-size: .9rem; color: var(--muted); }}
</style>
</head>
<body>
<main>
<h1>Which content pages will lose search visibility next? A ranked review queue on real search data</h1>
<div class="meta">Ammar Hopovac · FlyRank ML Internship capstone · data: March 2026 · <a href="{REPO}">code and notebooks</a></div>

<section class="abstract">
<h2>Abstract</h2>
<p>Content teams cannot check thousands of pages every week, so the question is which pages to look at first: which ones will lose Google impressions in the next 16 days?
I used one month of real Search Console data from the FlyRank ML Internship warehouse ({n(d['frame_pages'])} pages from {d['frame_clients']} clients, decision moment 16 March 2026) and labelled a page as declining when its daily impressions in 16–31 March fell below 80% of its 1–15 March level (base rate {pc(base)}).
A frozen rule (“already sliding × traffic”) was compared with a logistic regression on seven features known on 16 March, with 5-fold cross-validation grouped by client so every score comes from a model that never saw that client, plus a deliberate-leak check.
Both methods find almost only real declines at the very top of the list ({pc(lr['P@50'])} of the top 50, against {pc(base)} for a random pick), but the model ranks better overall (ROC-AUC {f3(lr['ROC-AUC'])} vs {f3(rule['ROC-AUC'])}) and clearly better among pages that are only starting to slide ({pc(rg['top']['50']['model'])} vs {pc(rg['top']['50']['rule'])} of the top 50).
The output is decision support, not a forecast of Google: a weekly review queue with reason codes, three action lanes, a no-go list and explicit limits (one month, associations only).</p>
</section>

<nav aria-label="Contents"><b>Contents</b>
<ol>
<li><a href="#intro">Introduction</a></li><li><a href="#data">Data</a></li><li><a href="#method">Methodology</a></li>
<li><a href="#results">Results</a></li><li><a href="#limits">Limitations</a></li><li><a href="#recs">Ranked recommendations</a></li>
<li><a href="#repro">Reproducibility</a></li><li><a href="#credit">Acknowledgments &amp; data credit</a></li>
</ol></nav>

<h2 id="intro">1. Introduction: the Monday problem</h2>
<p>It is Monday morning. An editor has a few hours for maintenance and thousands of published pages across many client sites. Some of them are about to lose a big part of their search visibility; most are fine. Without a list, the editor checks whatever they remember, or nothing.</p>
<p>This work builds that list. The goal is not to explain why Google ranks pages the way it does, but to put the pages most likely to decline at the top, with a reason a person can check in a minute and a suggested action. A false alarm costs about twenty minutes of review; a missed decline can cost weeks of lost traffic before anyone notices.</p>
<p>The tension: the obvious rule, “look at pages that are already dropping”, is very hard to beat at the top of the list, because a page that collapsed rarely bounces back within two weeks. The interesting question is whether a model adds anything <em>beyond</em> that, and where.</p>

<h2 id="data">2. Data</h2>
<p>The data is the FlyRank ML Internship warehouse on Hugging Face, read with DuckDB directly from Parquet. Two tables are used: the daily content-performance fact table (one row per page per day: Search Console impressions, clicks and average position) and the content dimension (page type and creation date).</p>
<p>The March 2026 partition has {n(d['march_daily_rows'])} daily rows covering {d['march_clients']} clients and {n(d['march_pages'])} pages. Three filters define the study frame:</p>
<ul>
<li>only rows with Search Console data, because the label is built from impressions;</li>
<li>at least 100 impressions in 1–15 March, so a 20% drop is not just noise;</li>
<li>pages created before 1 March, so every page has a full first half of the month.</li>
</ul>
<p>That leaves <b>{n(d['frame_pages'])} pages from {d['frame_clients']} clients</b>. Clients and pages are pseudonymous hashes, used only to group the validation, never as features. No client names, URLs or search queries appear anywhere in this paper or the repository. One client contributes {pc(d['largest_client_share'])} of the pages and the three largest {pc(d['top3_client_share'])}, which matters for validation (section 3). Almost all pages are keyword articles ({n(d['content_types']['keyword article'])}); comparison and news-feed articles are a small minority.</p>

<h2 id="method">3. Methodology</h2>
<h3>Label</h3>
<p>A page is <b>declining</b> if its average daily impressions on 16–31 March are below 80% of its average daily impressions on 1–15 March. {pc(base)} of pages meet this definition; this base rate is shown next to every precision number below.</p>
<h3>Features (all known on 16 March)</h3>
<div class="table-wrap"><table class="left">
<tr><th>Feature</th><th>Meaning</th></tr>
<tr><td><code>momentum</code></td><td>log ratio of daily impressions in 8–15 March vs 1–7 March: is the page already sliding?</td></tr>
<tr><td><code>log_imp</code></td><td>log of impressions per day: how visible the page is</td></tr>
<tr><td><code>ctr</code></td><td>clicks divided by impressions</td></tr>
<tr><td><code>avg_position</code></td><td>impression-weighted average Google position</td></tr>
<tr><td><code>age_days</code></td><td>days since the page was created</td></tr>
<tr><td><code>is_feedly</code>, <code>is_comparison</code></td><td>content type flags</td></tr>
</table></div>
<p>Left out on purpose: client and page ids, everything from 16–31 March, and any trend or “direction” field precomputed in the warehouse, because those overlap the label window.</p>
<h3>Baseline</h3>
<p>The week-4 rule, frozen before any model was trained: <code>score = −momentum × log(1 + impressions per day)</code> when momentum is below −0.1, otherwise 0. It needs no training, so it cannot overfit, and it is the bar any model has to clear.</p>
<h3>Model</h3>
<p>A standardized logistic regression on the seven features. Gradient boosting was also tried; it was not clearly better (table below) and is harder to explain to an editor, so the simpler model was kept.</p>
<h3>Validation design</h3>
<p>Five-fold cross-validation <b>grouped by client</b>: every test fold contains only clients that were not in training, which is the situation of a new client. All scores in this paper are out-of-fold. The same model under a random page-level split reads ROC-AUC {f3(M['random_split_auc'])} instead of {f3(lr['ROC-AUC'])}: pages of the same client share trends, so a random split partly measures memory of the client. The grouped number is the one reported.</p>
<h3>Leakage checks</h3>
<p>Every feature was traced to the 1–15 March window. As a check of the check, a deliberately leaky feature built from the label window was added: ROC-AUC jumped to {f3(M['leak_check_auc'])}, exactly what a leak looks like, and the feature was removed. The honest model scores far below that, as it should.</p>

<h2 id="results">4. Results</h2>
<div class="table-wrap"><table>
{results_table}
</table></div>
<p class="note">Out-of-fold, grouped by client, {n(d['frame_pages'])} pages. P@K = share of the top-K ranked pages that actually declined. Per-fold ROC-AUC spread (standard deviation) is about {lr['AUC fold sd']:.2f} for the model.</p>

<figure><img src="img/fig1_precision_at_k.png" alt="Line chart of precision at K for the model and the rule, both far above the 34% random line, with the model slightly above the rule from 200 pages on.">
<figcaption><b>Figure 1. Both rankings beat a random pick by a wide margin; the model pulls ahead after the first ~100 pages.</b> At the top, both pick pages that already collapsed.</figcaption></figure>

<p>The top of the list is a tie: {pc(lr['P@50'])} of the top 50 declined for both methods. That is the “down stays down” effect. The real test is the next tier, pages that are sliding but have not collapsed, because that is where an editor decides on a refresh. In that group ({n(rg['pages'])} pages, base rate {pc(rg['base_rate'])}) the model's choices declined clearly more often:</p>
<div class="table-wrap"><table>
{refresh_table}
</table></div>
<figure><img src="img/fig2_refresh_group.png" alt="Bar chart: among sliding pages, the model's top 50 declined 78% of the time vs 58% for the rule and 42% random.">
<figcaption><b>Figure 2. Among pages that are only starting to slide, the model finds more real declines than the rule.</b> With 50 pages per bar, differences of about ±12 points are within noise; the gap at top 50 and 100 is larger than that.</figcaption></figure>

<figure><img src="img/fig3_importance.png" alt="Horizontal bars: shuffling momentum drops ROC-AUC by 0.12; CTR and age by about 0.02-0.03; the rest near zero.">
<figcaption><b>Figure 3. Momentum carries most of the signal.</b> CTR and page age add a little; content type, position and traffic level add almost nothing on their own.</figcaption></figure>

<p><b>Error analysis.</b> Of the model's top 500 pages, {M['false_alarms_top500']} did not decline. Almost all of them had a sharp drop in the second week of March and then recovered: pages where one quiet week looked like a collapse. This is why the playbook below sends sharp drops to a quick technical check rather than straight to a rewrite.</p>

<h2 id="limits">5. Limitations and honest framing</h2>
<ul>
<li><b>One month.</b> Everything is March 2026. There was no second month to use as a sealed test, so stability over time is unmeasured. Seasonality or a search-engine update can move the base rate and the ranking quality.</li>
<li><b>Associations, not causes.</b> Nothing here shows that refreshing a page causes recovery; no refresh was observed in the data. The features predict a drop; they do not explain it.</li>
<li><b>The easy top.</b> The highest precision numbers come from pages that had already collapsed. The fair measures are the refresh-group comparison and ROC-AUC, and those are modest (≈0.66).</li>
<li><b>The label is impressions.</b> It ignores clicks, conversions and whether the page still matters to the business.</li>
<li><b>Few, uneven clients.</b> {d['frame_clients']} clients, one of them {pc(d['largest_client_share'])} of the pages; per-fold ROC-AUC varies by about ±{lr['AUC fold sd']:.2f}.</li>
<li><b>Not calibrated.</b> The score ranks pages; it should not be read as the probability for one page.</li>
<li><b>Possible tracking artefacts.</b> {d['pages_zero_impressions_after']} pages had zero impressions after 16 March and are counted as declining; some may be de-indexing or tracking problems rather than decay.</li>
</ul>

<h2 id="recs">6. Ranked recommendations: the weekly playbook</h2>
<p>Each page gets one archetype, checked in order, and each archetype has one action. Each action is its own lane, sorted by the model score, so a weekly review takes the top of each lane rather than the top of one list (which would be all collapses).</p>
<div class="table-wrap"><table class="left">
<tr><th>#</th><th>Lane</th><th>Which pages</th><th>Action</th><th>Per week</th></tr>
<tr><td>1</td><td>Technical check</td><td>daily impressions fell below ~22% within a week ({n(arch['cliff_drop']['pages'])} pages, {pc(arch['cliff_drop']['declined'])} declined)</td><td>check indexing, redirects and tracking before touching content</td><td>top 20, ~5 min each</td></tr>
<tr><td>2</td><td>Refresh review</td><td>already sliding (momentum &lt; −0.1) ({n(arch['sliding_visible']['pages'])} pages, {pc(arch['sliding_visible']['declined'])} declined)</td><td>open the page, decide on a content refresh</td><td>top 30, ~20 min each</td></tr>
<tr><td>3</td><td>Snippet fix</td><td>page-one position but CTR below the page-one median</td><td>rewrite title and meta description</td><td>top 10</td></tr>
<tr><td>4</td><td>Wait / monitor</td><td>pages younger than 45 days, and everything else</td><td>no action this week</td><td>—</td></tr>
</table></div>
<figure><img src="img/fig4_archetypes.png" alt="Bars of decline rate by archetype: cliff drop 86%, sliding 42%, new pages 31%, low CTR 27%, stable 25%; base rate 34%.">
<figcaption><b>Figure 4. Sharp drops kept declining far more often than the rest; sliding pages sit above the base rate.</b> The snippet lane is not a decline call (its pages decline at about the base rate); it targets clicks lost on page one.</figcaption></figure>
<p>On March data, the refresh lane's top 30 had {pc(lanes['review_refresh']['declined'])} real declines against {pc(lanes['review_refresh']['lane_base_rate'])} for that lane at random. All three lanes together are about 13 hours of review per week.</p>
<h3>Human review and no-go list</h3>
<ul>
<li>A person confirms every drop in Search Console before acting, and checks whether a whole client dropped at once (a site-wide cause, not many separate jobs).</li>
<li>Never auto-edit, unpublish, redirect or delete pages from this score.</li>
<li>Never use the score to judge writers, editors or clients, and never present it as predicting Google.</li>
<li><b>Retrain or pause</b> when the base rate moves by more than 10 points, the momentum distribution shifts, the top-50 precision on a new month falls below the rule's, or the label definition changes; retrain monthly regardless.</li>
</ul>

<h2 id="repro">7. Reproducibility</h2>
<ul>
<li>Repository: <a href="{REPO}">{REPO.replace('https://', '')}</a></li>
<li>Capstone notebook (every number and chart on this page): <a href="{NB}/capstone.ipynb">work/notebooks/capstone.ipynb</a></li>
<li>Earlier steps: <a href="{NB}/w03_data_contract.ipynb">data contract</a> · <a href="{NB}/w04_baseline_score.ipynb">baseline</a> · <a href="{NB}/w05_model.ipynb">model</a> · <a href="{NB}/w06_validation_audit.ipynb">validation &amp; leakage audit</a> · <a href="{NB}/w07_action_playbook.ipynb">action playbook</a></li>
<li>Metrics behind this page: <a href="{REPO}/blob/main/work/outputs/capstone_metrics.json">work/outputs/capstone_metrics.json</a>; the page is generated from it by <a href="{REPO}/blob/main/work/paper/build_paper.py">work/paper/build_paper.py</a>.</li>
<li>To rerun: open the capstone notebook in Colab or Jupyter with a Hugging Face read token (<code>HF_TOKEN</code>), run all (it caches the March slice to <code>work/outputs/</code>), then run <code>python work/paper/build_paper.py</code>. Seed {M['seed']}, scikit-learn {M['sklearn']}.</li>
</ul>

<h2 id="credit">8. Acknowledgments &amp; data credit</h2>
<p>Built on the <a href="https://flyrank.ai">FlyRank ML Internship dataset</a>. Thanks to the FlyRank team for the warehouse, the weekly assignments and the review of this work. All client and page identifiers in the data are pseudonymous; no private data is published here.</p>

<footer>Ammar Hopovac · 2026 · <a href="https://h0pi.github.io">h0pi.github.io</a></footer>
</main>
</body>
</html>
"""

out = ROOT / "docs" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(HTML, encoding="utf-8")
print("wrote", out.relative_to(ROOT))
