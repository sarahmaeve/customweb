#!/usr/bin/env python3
"""Scrape the tag archive and write html/posts.json.

Walks the paginated WordPress tag archive, extracts each episode's segment
subject, applies the manual overrides from config, and writes the data file the
page is built from. Pages are cached under tools/.cache (gitignored); delete a
cached page to force a refetch, or delete the whole directory to rescrape.

    python3 tools/build_data.py
"""

import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402
import kartas  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
HTML_DIR = REPO / "html"
CACHE = Path(__file__).resolve().parent / ".cache"
MAX_PAGES = 500  # safety valve against a pagination bug looping forever

HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"),
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}


def load_or_fetch(n: int) -> str:
    """Return page n's HTML, from cache when present, otherwise over the network."""
    CACHE.mkdir(exist_ok=True)
    cached = CACHE / f"{config.TAG_SLUG}-p{n}.html"
    if cached.exists():
        return cached.read_text(encoding="utf-8", errors="replace")
    req = urllib.request.Request(config.page_url(n), headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        text = resp.read().decode("utf-8", "replace")
    cached.write_text(text, encoding="utf-8")
    time.sleep(1)  # be polite between live fetches
    return text


def scrape():
    posts, seen = [], set()
    for n in range(1, MAX_PAGES + 1):
        try:
            text = load_or_fetch(n)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                break  # ran off the end of the archive
            if posts:
                print(f"warning: page {n} -> HTTP {e.code}; stopping here", file=sys.stderr)
                break
            raise
        except urllib.error.URLError as e:
            if posts:
                print(f"warning: page {n} unreachable ({e.reason}); stopping here", file=sys.stderr)
                break
            raise
        page_posts = kartas.parse_page(text, config.SEGMENT_MARKER)
        if not page_posts:
            break  # a page with no episode posts marks the end
        for p in page_posts:
            if p["url"] not in seen:
                seen.add(p["url"])
                posts.append(p)
    for p in posts:
        if p["url"] in config.OVERRIDES:
            p["segment"] = config.OVERRIDES[p["url"]]
    return posts


def main():
    posts = scrape()
    HTML_DIR.mkdir(exist_ok=True)
    out = HTML_DIR / "posts.json"
    out.write_text(json.dumps(posts, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    missing = [p for p in posts if not p["segment"]]
    print(f"{len(posts)} episodes -> {out.relative_to(REPO)}")
    if missing:
        print(f"{len(missing)} without a segment subject (consider a config override):")
        for p in missing:
            print("  ", p["url"])


if __name__ == "__main__":
    main()
