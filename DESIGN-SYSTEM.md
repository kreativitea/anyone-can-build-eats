# Design system — Gaidai Eats

How every page looks, and the rules for adding to it. The styles are in one file,
[`static/eats.css`](static/eats.css). Every part is shown on one page,
[`docs/design-system.html`](docs/design-system.html): open it in a browser, and press **Light /
dark** to see both themes.

## The idea

A review site in the style of Tabelog, in Kansai Gaidai's colours: a calm page, the university's
navy for everything that is the site, and one warm colour for everything that is a rating. Places
are cards. The page is built for a phone first and widens to two or three columns.

The site is a student project, not the university's: it uses the university's colours, never its
name as the site's author or its logo, and the footer says *Not run by Kansai Gaidai University*.

## Colour

The colours are Kansai Gaidai University's, read from `kansaigaidai.ac.jp` (2026-10-15).

| Token | Light | Dark | Used for |
|---|---|---|---|
| `--brand` | navy `#020b4a` | `#0b1340` | the header, the primary button |
| `--ink` | navy `#020b4a` | `#eef2f7` | text, headings |
| `--ink-2` | `#4a5468` | `#a7b3c9` | details: dates, counts, distances |
| `--link`, `--focus` | blue `#095181` | `#8fc1ea` | links, the focus ring |
| `--star` | `#b85a14` | `#f2a65e` | stars and the rating number, **and nothing else** |
| `--bg`, `--surface` | `#f5f8fa`, white | `#030829`, `#0b1340` | the page, and the cards on it |
| `--chip` | mist `#e1e9ef` | `#121c52` | filters, avatars |
| `--danger` | `#b42318` | `#f59e8b` | errors, delete |

The category tags use the university's tile colours: coral for restaurants, orange for cafés, teal
for fast food. The star colour is the university's orange (`#ea9b59`) darkened, because the orange
itself is too light to see on white.

**Every text colour passes WCAG AA** (4.5:1) on every background it sits on, in both themes; the
stars pass 3:1. A new colour is checked the same way before it is used.

**Components use the tokens on the left, never a colour written out**, and never the `--kgu-`
names directly. Then the dark theme works by itself.

## Type

One family, the device's own sans-serif, with a Japanese face named after it, so a Japanese name
and an English one sit on one line at the same weight. No font is downloaded. Six sizes, from
`--text-xs` (12px) to `--text-2xl` (32px); body text is 16px with a line height of 1.6. Ratings use
`tabular-nums`, so *3.7* and *4.1* line up.

## Space and shape

Space comes in seven steps (`--space-1`, 4px, to `--space-7`, 48px). Corners are rounded: 8px for
small things, 12px for cards and boxes, 20px for large panels, and fully round for buttons and
filters. Cards have a soft shadow and lift a little under the mouse.

## Components

| Component | Class | Rule |
|---|---|---|
| Header | `.site-header` | The wordmark, the search, the account links. Stays at the top. |
| Search | `.search` | One box. Finds a name in English or Japanese. |
| Row | `.row` | Things side by side that wrap on a phone, like a box and its button. |
| Filters | `.chips`, `.chip` | A checkbox or a link. On is navy. |
| Switch | `.switch` | One on/off choice, like *Show bars and pubs*. A real checkbox. |
| Place card | `.cards`, `.card` | The whole card is one link. Name, local name, tag, details, rating. |
| Category tag | `.tag .tag--<category>` | One per place, in its category's colour. |
| Rating | `.rating`, `.stars` | Stars, the number and the count, always together; or *No reviews yet*. The stars take `style="--rating: 3.7"` and an `aria-label`. |
| Place header | `.hero` | The top of a place's page. |
| Review | `.reviews`, `.review` | Newest first, a line between them. |
| Form | `.form`, `.field` | A label above every box, the help under it, the error under that. |
| Star picker | `.star-picker` | Five radio buttons drawn as stars, written 5 to 1. |
| Button | `.btn--primary`, `--secondary`, `--ghost`, `--danger` | **At most one primary button on a page.** |
| Message | `.message`, `.message--error` | What just happened. |
| Empty state | `.empty` | Says that nothing is there, and what to do about it. |
| Pages | `.pagination` | Previous, *Page 2 of 49*, Next. |
| Footer | `.site-footer` | *© OpenStreetMap contributors*, always. |

## Modern touches

Each one makes the site better where a browser has it, and changes nothing where it does not.

- **Dark theme** by the device's setting (`prefers-color-scheme`), in the university's navy.
- **Page-to-page fades** (`@view-transition`), turned off for anyone who asks their device for
  less motion.
- **`:has()`** for styling a filter or a field from the input inside it, so no JavaScript is needed
  for how a control looks.
- **htmx swaps fade in.** Whatever htmx replaces carries the class `swap`: it dims while the
  request is on its way, and fades in when the new part arrives, so the list does not jump.
- **`color-mix()`** for tints, so a tag's background comes from its one colour.
- Cards in a **grid that fills the width**, one column on a phone and three on a wide screen.

## Rules for adding to it

1. **Use a token, not a value.** A new colour, size or space goes in the tokens first.
2. **A new component goes in `eats.css` and on `docs/design-system.html`**, with a line in the
   table above.
3. **Every control works with the keyboard alone** and shows the focus ring.
4. **Never colour alone.** A rating has its number; an error has its words.
5. **Check both themes and a phone width** before calling a page done.
6. **No made-up reviews of real places**, in the design-system page or anywhere else. Examples use
   made-up places.
