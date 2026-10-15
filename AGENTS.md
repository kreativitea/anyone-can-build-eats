# AGENTS.md — for the AI agent working in this repository

The person asking you may be new to programming, and may read English as a second language.
Explain in short, plain sentences, and define a technical word the first time you use it. When you
change code, say which file changed and why.

## What this is

Gaidai Eats: a review site, in the style of Tabelog, for the places to eat and drink within 5 km of
Kansai Gaidai's two campuses. Anyone can read every page; only writing a review needs an account.
The places are real, from an OpenStreetMap snapshot in `data/places.json`. `DESIGN.md` says how it
works and why; `DESIGN-SYSTEM.md` says how it looks; `FEATURES.md` lists what to build next.

## What each file does

| File | Its one job |
|---|---|
| `config/settings.py` | Settings for the whole project. Secrets come from environment variables on a live server. `TIME_ZONE` is `Asia/Tokyo`. |
| `config/urls.py` | Sends `/admin/`, the log-in, log-out and sign-up pages, and then `reviews/urls.py` and `places/urls.py`. |
| `places/models.py` | `Place`: one place to eat. `display_name` (English first), `local_name` (the sign's name under it), `cuisine_label`, `osm_url`. `Place.objects.with_ratings()` adds `rating` (the average, `None` with no reviews) and `review_count`, worked out by the database; `daytime()` leaves out bars and pubs. |
| `places/management/commands/load_places.py` | `python manage.py load_places`: adds or updates every place in `data/places.json` by its `osm_id`, and works out `km_from_campus`. Safe to run again. |
| `places/views.py` | `place_list`: the home page; search (`q`), `category`, `bars`, `page`; nearest first, 20 to a page. Asked by htmx (`HX-Request`), it sends only `_browse.html`. `place_detail`: one place and its reviews, newest first. |
| `places/templates/places/` | `list.html` (the page and the filter form), `_browse.html` (the part htmx swaps: filters, count, cards, pages), `_card.html`, `_rating.html` (stars, number and count, or *No reviews yet*), `detail.html`. |
| `reviews/models.py` | `Review`: `place`, `author`, `rating` (1 to 5), `text` (at most 2,000 characters), `created_at`. |
| `reviews/forms.py` | `ReviewForm`: only `rating` and `text`, with the messages a person sees. |
| `reviews/views.py` | `review_create`: `@login_required`; sets `place` and `author` itself; a form with a mistake comes back with status 400 and what was typed kept. |
| `accounts/views.py` | `signup`: Django's `UserCreationForm`, then logs the person in and sends them back to `next` if it is on this site. |
| `templates/base.html` | The frame of every page: header, messages, footer with *© OpenStreetMap contributors*. |
| `templates/registration/` | The log-in and sign-up pages. |
| `static/eats.css` | The design system. `docs/design-system.html` shows every part of it. |
| `static/htmx.min.js` | htmx 2.0.11, unchanged. Never edit it. |
| `*/tests/unit/`, `*/tests/integration/`, `tests/cuj/` | The three levels of tests (see Rules). |
| `places/tests/helpers.py` | `make_place`, `make_user`, `card_names`, `TEST_PASSWORD`. |
| `docs/plans/` | One plan per feature. `TEMPLATE.md` is the empty one. |
| `docs/prompts/` | The prompt log, written by `.claude/hooks/log_prompt.py`. Never edit it. |

## Commands

Run every Python command through `uv run`, so it uses this project's packages.

- `make setup` — install, create the database, load the places, turn on the commit checks
- `make run` — start the server at <http://127.0.0.1:8000>
- `make test` — every test, with a count for each level
- `make lint` / `make format` — Ruff
- `make check` — every commit check, a check that no migration is missing, then every test

Add a package with `uv add <name>`, never with `pip install`. After changing a model, run
`uv run python manage.py makemigrations` and then `uv run python manage.py migrate`.

## Rules

- **Run `make check` before every commit.**
- **Never write a review, in a test, a fixture, a screenshot or a demo, of a real place.** The
  places in `data/places.json` are real businesses. Tests make their own places with `make_place`,
  with made-up names.
- **The author of anything is the person logged in, set by the view.** Never a form field.
- **A view that changes data needs `@login_required` and `POST`.** A `GET` only reads.
- **A person can only change their own things.** Look the object up through its owner, for
  example `get_object_or_404(Review, pk=pk, author=request.user)`, so anyone else gets a 404.
  Hiding a link is not a check.
- **The server checks every rule**, even when the page also checks it.
- **Averages and counts are worked out by the database** (`with_ratings`), never stored.
- **A query with `with_ratings()` needs its own `order_by`.** Django drops the model's default
  ordering from a query that works out an average.
- **An htmx view also works without htmx.** Every htmx control is a normal link or form too.
- **Use the design system.** New styles go in `static/eats.css`, use its tokens, and are shown on
  `docs/design-system.html`. Read `DESIGN-SYSTEM.md` first.
- **Never change `data/places.json` by hand.** It is a snapshot from OpenStreetMap, under the ODbL.
- **Never edit or delete anything in `docs/prompts/`.**
- **Every migration can be reversed**, and never edit a migration by hand.
- **Put a test in the lowest level that can catch the bug.** Its folder sets the level: `unit`
  (one piece alone), `integration` (a request through Django's test client), `cuj` (a whole
  journey a person takes).
- **Add or change a test with every change in behaviour**, and show the person the test failing
  before the fix and passing after.
