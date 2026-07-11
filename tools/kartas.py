"""Pure extraction and rendering helpers for the KARTAS segment index.

No I/O and no globals — every function takes its inputs and returns a value — so
the parsing and formatting logic is directly unit-testable (see test_kartas.py).
The scripts that touch the network and filesystem are build_data.py (scrape +
parse) and build_html.py (render).
"""

import html as _html
import re

_MONTHS = {m: i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"], 1)}
_MON3 = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

_HEADER_RE = re.compile(
    r'<h3 id="post-\d+"><a href="([^"]+)"[^>]*rel="bookmark"[^>]*>(.*?)</a></h3>', re.S)
_DATE_RE = re.compile(r'<p class="date">\s*(.*?)\s*(?:\||</p>)', re.S)
_AUTHOR_RE = re.compile(r'<p class="date">[^|<]*\|\s*([^<]+?)\s*</p>')


# --- extraction ---------------------------------------------------------------

def strip_tags(s: str) -> str:
    """Drop HTML tags and unescape entities, collapsing surrounding whitespace."""
    return _html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def normalize_date(raw: str):
    """'June 26th, 2026' -> ('2026-06-26', '2026'). ('', '') if unparseable."""
    m = re.match(r"([A-Za-z]+)\s+(\d{1,2})[a-z]{2},\s+(\d{4})", raw or "")
    if not m:
        return "", ""
    mo = _MONTHS.get(m.group(1), 0)
    if not mo:
        return "", ""
    return f"{int(m.group(3)):04d}-{mo:02d}-{int(m.group(2)):02d}", m.group(3)


def extract_segment(block: str, marker: str = r"Consulting Occ"):
    """Text of the first paragraph in `block` that names the segment, or None.

    Handles the show-notes variants seen in the wild: plain <p>, <p class="...">,
    and text not wrapped in <p> at all. `block` runs from a post's <h3> header to
    the next post (the postTags div bounds the content region).
    """
    cstart = block.find("</h3>")
    cend = block.find('<div class="postTags"')
    content = block[cstart + 5: cend if cend != -1 else len(block)]
    for chunk in re.split(r"</?p\b[^>]*>", content):
        if re.search(marker, chunk):
            text = strip_tags(chunk)
            if text:
                return text
    return None


def parse_page(html_text: str, marker: str = r"Consulting Occ"):
    """Extract every episode post on one archive page (overrides not applied)."""
    posts = []
    for block in re.split(r'(?=<h3 id="post-\d+")', html_text):
        m = _HEADER_RE.search(block)
        if not m:
            continue
        dm = _DATE_RE.search(block)
        date_raw = strip_tags(dm.group(1)) if dm else ""
        am = _AUTHOR_RE.search(block)
        iso, year = normalize_date(date_raw)
        posts.append({
            "url": m.group(1),
            "title": strip_tags(m.group(2)),
            "segment": extract_segment(block, marker),
            "date": date_raw,
            "iso": iso,
            "year": year,
            "author": strip_tags(am.group(1)) if am else "",
        })
    return posts


# --- rendering ----------------------------------------------------------------

def episode_number(title: str) -> str:
    m = re.search(r"Episode\s+(\d+)", title)
    return m.group(1) if m else "—"  # em dash when a title lacks a number


def refs_html(links) -> str:
    """Render curated Wikipedia links as a chip row, or '' when there are none.

    `links` is a list of (label, url) pairs. The row is emitted as a sibling of
    the segment paragraph so the live-search highlighter (which rewrites the
    segment's innerHTML on every keystroke) never disturbs it.
    """
    if not links:
        return ""
    chips = "".join(
        '<a class="ref" href="{}" target="_blank" rel="noopener">{}</a>'.format(
            _html.escape(url, quote=True), _html.escape(label))
        for label, url in links)
    return f'\n        <p class="refs">{chips}</p>'


def lerp_hex(a: str, b: str, t: float) -> str:
    """Linear interpolate between two #rrggbb colors; t in [0, 1]."""
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(ca[i] + (cb[i] - ca[i]) * t) for i in range(3))


def temp_color(year, ymin: int, ymax: int,
               cool: str = "#6E614C", warm: str = "#E0B250") -> str:
    """Date gloss-tick color: cool (faint) for the oldest year, warm (gilt) newest."""
    if not year:
        return cool
    t = (int(year) - ymin) / max(1, (ymax - ymin))
    return lerp_hex(cool, warm, t)


def short_date(iso: str) -> str:
    """'2026-06-26' -> '26 Jun 2026'. '' for an empty/unknown date."""
    if not iso:
        return ""
    y, m, d = iso.split("-")
    return f"{int(d)} {_MON3[int(m) - 1]} {y}"
