"""Unit tests for the pure extraction/rendering helpers in kartas.py.

    python3 -m unittest discover -s tools
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import kartas  # noqa: E402


def block(header_title, body):
    """Wrap body text in the minimal post structure extract_segment expects."""
    return (f'<h3 id="post-1"><a href="u" rel="bookmark">{header_title}</a></h3>'
            f'{body}<div class="postTags">Tags: ...</div>')


class StripTags(unittest.TestCase):
    def test_removes_tags_and_unescapes(self):
        self.assertEqual(kartas.strip_tags("<p>a &amp; <strong>b</strong></p>"), "a & b")


class NormalizeDate(unittest.TestCase):
    def test_ordinals(self):
        self.assertEqual(kartas.normalize_date("June 26th, 2026"), ("2026-06-26", "2026"))
        self.assertEqual(kartas.normalize_date("August 3rd, 2012"), ("2012-08-03", "2012"))
        self.assertEqual(kartas.normalize_date("January 1st, 2015"), ("2015-01-01", "2015"))

    def test_unparseable(self):
        self.assertEqual(kartas.normalize_date(""), ("", ""))
        self.assertEqual(kartas.normalize_date("sometime"), ("", ""))
        self.assertEqual(kartas.normalize_date("Smarch 5th, 2020"), ("", ""))


class ExtractSegment(unittest.TestCase):
    def test_plain_paragraph(self):
        b = block("Ep", "<p>Intro.</p><p>Finally the <strong>Consulting Occultist </strong>profiles X.</p>")
        self.assertEqual(kartas.extract_segment(b), "Finally the Consulting Occultist profiles X.")

    def test_wp_block_paragraph_attr(self):
        b = block("Ep", '<p class="wp-block-paragraph">Finally the Consulting Occultist covers etymomancy.</p>')
        self.assertEqual(kartas.extract_segment(b), "Finally the Consulting Occultist covers etymomancy.")

    def test_not_wrapped_in_p(self):
        b = block("Ep", "Finally the <strong>Consulting Occultist</strong> blows the lid off Buenos Aires.")
        self.assertEqual(kartas.extract_segment(b),
                         "Finally the Consulting Occultist blows the lid off Buenos Aires.")

    def test_typo_occulist(self):
        b = block("Ep", "<p>the Consulting Occulist recounts Tom Driberg.</p>")
        self.assertEqual(kartas.extract_segment(b), "the Consulting Occulist recounts Tom Driberg.")

    def test_short_form_occult(self):
        b = block("Ep", "<p>the Consulting Occult, as Ken gives us the 101 on John Dee.</p>")
        self.assertEqual(kartas.extract_segment(b), "the Consulting Occult, as Ken gives us the 101 on John Dee.")

    def test_absent_returns_none(self):
        b = block("Ep", "<p>The Gaming Hut vamps for time.</p><p>The Cinema Hut reaches the sound era.</p>")
        self.assertIsNone(kartas.extract_segment(b))


class ParsePage(unittest.TestCase):
    PAGE = (
        '<h3 id="post-2"><a href="https://x/ep-2/" rel="bookmark" title="Permanent Link to Episode 2: Two">Episode 2: Two</a></h3>'
        '<p class="date">June 26th, 2026 | Robin</p>'
        '<p>Finally the <strong>Consulting Occultist </strong>profiles Alpha.</p>'
        '<div class="postTags">Tags: x</div>'
        '<h3 id="post-1"><a href="https://x/ep-1/" rel="bookmark" title="Permanent Link to Episode 1: One">Episode 1: One</a></h3>'
        '<p class="date">August 3rd, 2012 | Robin</p>'
        '<p>Then the Consulting Occultist covers Beta.</p>'
        '<div class="postTags">Tags: y</div>'
    )

    def test_extracts_both_posts(self):
        posts = kartas.parse_page(self.PAGE)
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0]["url"], "https://x/ep-2/")
        self.assertEqual(posts[0]["title"], "Episode 2: Two")
        self.assertEqual(posts[0]["iso"], "2026-06-26")
        self.assertEqual(posts[0]["segment"], "Finally the Consulting Occultist profiles Alpha.")
        self.assertEqual(posts[0]["author"], "Robin")
        self.assertEqual(posts[1]["iso"], "2012-08-03")


class RenderHelpers(unittest.TestCase):
    def test_episode_number(self):
        self.assertEqual(kartas.episode_number("Episode 705: A Real Science"), "705")
        self.assertEqual(kartas.episode_number("Episode 691 – From Such Triangles"), "691")
        self.assertEqual(kartas.episode_number("A title with no number"), "—")

    def test_lerp_hex_endpoints_and_mid(self):
        self.assertEqual(kartas.lerp_hex("#000000", "#ffffff", 0), "#000000")
        self.assertEqual(kartas.lerp_hex("#000000", "#ffffff", 1), "#ffffff")
        self.assertEqual(kartas.lerp_hex("#000000", "#ffffff", 0.5), "#808080")

    def test_temp_color_bounds(self):
        self.assertEqual(kartas.temp_color("2012", 2012, 2026), "#6e614c")
        self.assertEqual(kartas.temp_color("2026", 2012, 2026), "#e0b250")
        self.assertEqual(kartas.temp_color("", 2012, 2026), "#6E614C")

    def test_short_date(self):
        self.assertEqual(kartas.short_date("2026-06-26"), "26 Jun 2026")
        self.assertEqual(kartas.short_date(""), "")


if __name__ == "__main__":
    unittest.main()
