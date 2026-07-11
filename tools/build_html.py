#!/usr/bin/env python3
"""Render html/posts.json into the static page (links styles.css + app.js).

    python3 tools/build_html.py

Only the markup is generated here; the styling lives in html/styles.css and the
interactivity in html/app.js, both hand-maintained static assets.
"""

import datetime
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402
import kartas  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
HTML_DIR = REPO / "html"
NBSP = " "


def esc(s, attr=False):
    return html.escape(str(s), quote=attr)


def entry_li(p, ymin, ymax):
    seg = p["segment"] or ""
    placeholder = seg.startswith("[")
    tick = kartas.temp_color(p["year"], ymin, ymax)
    date_disp = (kartas.short_date(p["iso"]) or p["date"]).replace(" ", NBSP)
    search_blob = f'{p["title"]} {seg} {p["date"]}'.lower()
    return f'''    <li class="entry" data-iso="{esc(p["iso"], True)}" data-text="{esc(search_blob, True)}">
      <div class="rail">
        <span class="folio">No.&nbsp;{esc(kartas.episode_number(p["title"]))}</span>
        <time class="gloss" datetime="{esc(p["iso"], True)}" title="{esc(p["date"], True)}"><span class="tick" style="background:{tick}"></span>{esc(date_disp)}</time>
      </div>
      <div class="col">
        <a class="title" href="{esc(p["url"], True)}">{esc(p["title"])}</a>
        <p class="seg{' none' if placeholder else ''}" data-raw="{esc(seg, True)}">{esc(seg)}</p>
      </div>
    </li>'''


def build(posts):
    years = [int(p["year"]) for p in posts if p["year"]]
    ymin, ymax = min(years), max(years)
    rows = "\n".join(entry_li(p, ymin, ymax) for p in posts)
    year_opts = "".join(f'<option value="{y}">{y}</option>' for y in range(ymin, ymax + 1))
    newest, oldest = posts[0], posts[-1]
    built = datetime.date.today().strftime("%-d %B %Y")
    domain = config.SITE.split("://", 1)[-1]
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(config.PAGE_TITLE)}</title>
<link rel="stylesheet" href="styles.css">
</head>
<body>
<header class="hero">
  <span class="blot" aria-hidden="true"></span>
  <p class="kicker">{esc(config.KICKER)}</p>
  <h1>{config.HEADLINE_HTML}</h1>
  <p class="lede">Every episode of <a href="{esc(config.SITE, True)}/">{esc(config.SITE_LABEL)}</a>
     tagged <a href="{esc(config.tag_url(), True)}">{esc(config.TAG_LABEL)}</a> &mdash;
     {len(posts)} in all, from Episode&nbsp;{esc(kartas.episode_number(newest["title"]))}
     back to Episode&nbsp;{esc(kartas.episode_number(oldest["title"]))} &mdash;
     each with the date it aired and the subject of that episode's {esc(config.TAG_LABEL)} segment.</p>
  <div class="tools">
    <label class="field">
      <input id="q" type="search" placeholder="{esc(config.SEARCH_PLACEHOLDER, True)}" autocomplete="off" spellcheck="false">
    </label>
    <button class="sort" id="sort" type="button" aria-label="Reverse the order"><span class="arw" aria-hidden="true">&darr;</span>Newest first</button>
  </div>
  <div class="filters">
    <span class="flabel">Aired</span>
    <div class="presets" id="presets">
      <button type="button" data-preset="all" class="on">All</button>
      <button type="button" data-preset="month">Past month</button>
      <button type="button" data-preset="year">Past year</button>
    </div>
    <span class="sep" aria-hidden="true">|</span>
    <span class="yr">
      <span class="flabel">Years</span>
      <select id="from" aria-label="From year"><option value="">{ymin}</option>{year_opts}</select>
      <span class="dash" aria-hidden="true">&ndash;</span>
      <select id="to" aria-label="To year"><option value="">{ymax}</option>{year_opts}</select>
    </span>
    <span class="count" id="count">{len(posts)} entries</span>
  </div>
</header>

<main>
  <hr class="rule">
  <ol id="list">
{rows}
  </ol>
  <p class="empty" id="empty">Nothing in the ledger matches that.</p>
</main>

<footer>
  Compiled {built} from the public tag archive at
  <a href="{esc(config.tag_url(), True)}">{esc(domain)}</a>.
  Subjects are quoted from each episode's show notes; an oxblood-marked, italic line means those notes
  don't summarise the {esc(config.TAG_LABEL)} segment. Newest entries first.
  Styling follows the notebook design language in <code>design/</code>.
</footer>

<script src="app.js"></script>
</body>
</html>
'''


def main():
    posts = json.loads((HTML_DIR / "posts.json").read_text(encoding="utf-8"))
    out = HTML_DIR / config.OUTPUT_HTML
    out.write_text(build(posts), encoding="utf-8")
    print(f"{len(posts)} entries -> {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
