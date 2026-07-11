# customweb

Minor LLM-built custom web tools.

---

## The Consulting Occultist — a reading record

A single-page, searchable index of every episode of the podcast
[*Ken and Robin Talk About Stuff*](https://www.kenandrobintalkaboutstuff.com/)
tagged **[Consulting Occultist](https://www.kenandrobintalkaboutstuff.com/index.php/tag/consulting-occultist/)**
— 201 episodes — each with the date it aired and the subject Ken took up in that
episode's occult segment. The page filters as you type (with a violet
highlighter over matches), narrows by date range, and flips newest/oldest.

Open **`html/knrconsulting.html`** in a browser. It loads `styles.css` and
`app.js` from the same folder — no build step or server needed to view it.

### Layout

```
html/
  knrconsulting.html   generated page (open this)
  styles.css           styling — the "Glossa notebook" design language
  app.js               search / date-filter / sort behaviour
  posts.json           the extracted data (source of truth for the page)
tools/
  config.py            site, tag, segment marker, per-episode overrides
  kartas.py            pure extraction + rendering helpers (unit-tested)
  build_data.py        scrape the tag archive  -> html/posts.json
  build_html.py        render html/posts.json  -> html/knrconsulting.html
  test_kartas.py       Python unit tests
  test_app.js          Node unit tests for app.js's pure helpers
design/
  glossa-notebook.md   the design language and where it departs from stock Glossa
```

### Rebuilding

Two independent steps. Rendering needs only `posts.json`, so you can restyle
without re-scraping.

```sh
python3 tools/build_data.py   # re-scrape the archive -> html/posts.json
python3 tools/build_html.py   # re-render the page    -> html/knrconsulting.html
```

`build_data.py` caches each fetched archive page under `tools/.cache/`
(gitignored). Delete a cached page to refetch it, or the whole directory to
rescrape from scratch. It walks pagination until the archive ends and is polite
(one request/second) on live fetches.

### Tests

```sh
python3 -m unittest discover -s tools   # extraction + rendering helpers
node tools/test_app.js                  # app.js pure helpers
```

Requirements: Python 3 standard library only (no pip packages); Node for the JS
test. The page itself is plain HTML/CSS/JS.

### Data notes

Segment subjects are quoted verbatim from each episode's show notes. Four
episodes are special-cased in `tools/config.py`:

- **#320** — the segment is written up under the "Eliptony Hut" name (a de Rochas
  profile), so its subject is supplied as an override.
- **#175** and **#11** are handled automatically by a deliberately loose marker
  (`Consulting Occ`) that catches the show-notes typo "Occulist" and the early
  short form "Occult".
- **#630** and **#534** are tagged but their notes never summarise the segment;
  they render as an oxblood-marked, italic placeholder line.

Each entry also carries **Wikipedia links** for the specific subject(s) its
segment covers, rendered as chips beneath the segment text. These are curated by
hand in the `WIKI` table in `tools/config.py` (keyed by episode number); only
specific named subjects — people, works, groups, named events — are linked,
while broad practices (tarot, ley lines, chaos magick) are left bare. The table
is independent of the scrape, so rebuilding `posts.json` never disturbs it.

To point these tools at a different Ken-and-Robin recurring segment, edit
`tools/config.py` (tag slug, label, segment marker, overrides, Wikipedia links)
and rebuild.

### Provenance & credit

Data compiled from the public tag archive at kenandrobintalkaboutstuff.com.
Styling adapts **Glossa**, a reading-record design language exported from
Katagami; see `design/glossa-notebook.md` for the palette, type, and the
project-specific deviations.
