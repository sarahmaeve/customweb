"""Project configuration for the KARTAS segment index.

Everything site- or segment-specific lives here, so re-pointing the tools at a
different Ken-and-Robin recurring segment (or another WordPress tag archive with
the same theme) is a config edit, not a code change.
"""

# --- source site --------------------------------------------------------------
SITE = "https://www.kenandrobintalkaboutstuff.com"
SITE_LABEL = "Ken and Robin Talk About Stuff"
TAG_SLUG = "consulting-occultist"
TAG_LABEL = "Consulting Occultist"

# Regex used to find the paragraph that describes the segment. Kept deliberately
# loose ("Occ") so it still matches the show-notes typo "Occulist" and the early
# short form "Consulting Occult".
SEGMENT_MARKER = r"Consulting Occ"

# --- rendered page ------------------------------------------------------------
OUTPUT_HTML = "knrconsulting.html"
PAGE_TITLE = "The Consulting Occultist — a reading record"
KICKER = "Ken and Robin Talk About Stuff · a reading record"
HEADLINE_HTML = "The <em>Consulting Occultist</em>"  # raw HTML; <em> gets the gilt marker
SEARCH_PLACEHOLDER = "Search a subject or title — Dee, geomancy, chess…"

NO_SEGMENT_NOTE = f"[No {TAG_LABEL} segment written up in this episode's show notes.]"

# Episodes whose notes name the segment differently, or omit a write-up entirely.
# Keyed by permalink; the value replaces the auto-extracted segment text.
OVERRIDES = {
    f"{SITE}/index.php/episode-630-live-at-dragonmeet-2024/": NO_SEGMENT_NOTE,
    f"{SITE}/index.php/episode-534-manimal-utopia/": NO_SEGMENT_NOTE,
    f"{SITE}/index.php/episode-320-ghost-rationing-policy/":
        "Our survey of Belle Epoque weirdness ducks into the Eliptony Hut with a "
        "profile of early parapsychologist Albert de Rochas.",
}


def tag_url() -> str:
    return f"{SITE}/index.php/tag/{TAG_SLUG}/"


def page_url(n: int) -> str:
    """Archive page URL. Page 1 has no /page/ suffix on this theme."""
    return tag_url() if n == 1 else f"{tag_url()}page/{n}/"
