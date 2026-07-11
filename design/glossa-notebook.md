# Glossa Notebook — design language

The styling for the Consulting Occultist index. It is a **customised version of
"Glossa"**, a reading-record design language exported from Katagami. This file
records the palette, type, and rules the page actually uses, and calls out where
it departs from the source so the look can be reproduced or extended.

> A commonplace book kept by lamplight: knowledge accrues down a single ruled
> column; the outer margin keeps the dates and the ink-blots. Warm-dark walnut
> ground, ink-light text, one violet ink for every action. Emphasis is something
> you can feel.

## Colours

| Token | Value | Role |
|-------|-------|------|
| `bg` | `#16120E` | lamplit walnut desk (page ground) |
| `surface` | `#1F1A14` | inputs, the walnut leaf |
| `surface2` | `#262019` | inset gloss panel |
| `text` | `#F3EAD9` | parchment ink (body) |
| `muted` | `#A9997F` | secondary text |
| `faint` | `#6E614C` | tertiary / oldest date-tick |
| `accent` | `#B79CE8` | **violet — every action**: links, focus, primary data |
| `accent-deep` | `#9B7AD4` | violet underlines, focus rings |
| `gilt` | `#E0B250` | emphasis marker only: folio stamps, citation, newest date-tick |
| `oxblood` | `#C25B4E` | emphasis marker only: the one line argued with |

Contrast: parchment on walnut clears WCAG AA comfortably (>11:1). Marker colour is
always paired with weight or an underline, never colour alone.

## Type

- **Display** — Fraunces, 600–700. Headline and the folio hierarchy.
- **Body** — Spectral, 400–500. The reading column.
- **Label** — Spline Sans Mono, 500–600. Folio stamps, dates, kickers, controls.

Fonts load from Google Fonts with `Georgia` / `ui-monospace` fallbacks, so the
page degrades gracefully offline. The root is scaled `calc(100% + 5.33px)`
(≈ +4pt) and everything else is expressed in `rem`, so one line resizes the page.

## Layout

- A single centred reading column (max ~1180px) with a **margin rail** down the
  inner edge of each entry: a hairline vertical rule carrying the folio stamp and
  the date gloss. An opening violet ink-blot sits at the top of the hero.
- Sections are divided by whitespace and hairline rules — never boxes.
- Rounded corners are `0`, `16`, `24`, or full only. Controls that read as
  ledger fields (selects, folio stamps, the sort stamp) use `0`; the search
  field uses `16`.
- Responsive: below 640px the rail collapses to a horizontal date strip above
  each entry and everything stacks to one column. No horizontal overflow.

## Signature elements

- **Folio stamp** — the episode number as a rotated (~-2°) monospace label in a
  hairline gilt rectangle with a near-flat stamp shadow.
- **Date gloss-tick** — a small vertical tick coloured on a *temperature* scale:
  cool `faint` for the oldest year through warm `gilt` for the newest.
- **Highlighter** — search matches are wrapped in a translucent violet `<mark>`
  that overshoots the word (`box-decoration-break: clone`) — emphasis you feel.
- **Oxblood blot** — precedes the italic placeholder line for an episode whose
  notes never wrote up the segment: "the one argued with."

## Deviations from stock Glossa

Recorded so this stays honest about what was changed:

- **Newest entries first**, not append-only newest-at-foot. This is a reference
  index, so recency-first reading beats journal order. (A sort toggle restores
  oldest-first on demand.)
- **External stylesheet + script**, not a single hand-kept page — the index is
  generated, so styling and behaviour are shared static assets.
- **+4pt base scale** applied globally via the root font-size.
- Temperature ticks are keyed to the **publication year**, standing in for
  Glossa's "day's temperature."

## Do / Don't

- **Do** run the rail down each entry; hang the folio stamp and date-tick on it.
- **Do** use violet for every action and keep gilt/oxblood as emphasis only.
- **Do** pair any marker emphasis with weight or an underline.
- **Don't** flood a region with marker ink — emphasis is translucent and local.
- **Don't** add heavy drop shadows, pill navigation, or nested cards.
- **Don't** use in-between border radii.

---

*Derived from "Glossa" (Katagami design-language export). Palette and type tokens
follow the source; the deviations above are specific to this project.*
