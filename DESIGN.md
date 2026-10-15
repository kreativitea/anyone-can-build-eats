# Design doc — Gaidai Eats

*The places are real, from OpenStreetMap. Every person, review and example row here is made up.*

---

*The product spec*

## 1. The problem

A student new to Hirakata wants to know where to eat near campus, and which places are worth
the walk. Map apps list the places but say little about them, and review sites are mostly in
Japanese. Gaidai Eats is a review site in the style of Tabelog: every place to eat or drink within
5 km of the Nakamiya and Gotenyama campuses, and reviews written by the people who went there.
Anyone can read it. To write a review, you sign up.

It starts small on purpose. It does the basic things well, and leaves a list of features
(`FEATURES.md`) for whoever extends it.

## 2. Not in this version

- **No photos.** A photo needs file storage, size limits and moderation: a design of its own.
- **No editing or deleting a review**, and no limit of one review per person per place.
- **A review is stars and text.** Nothing else is attached to it.
- **No map.** Each place links out to OpenStreetMap instead. Map tiles come from a service with
  usage rules of their own.
- **No distances shown.** The distance from campus is worked out when the places are loaded,
  and not yet shown on the page.
- **No live map data.** The places are a snapshot, loaded once; nothing calls a map service while
  the site runs.
- **No sample reviews.** The places are real businesses, and a made-up review of a real shop is
  not fair to it. The site starts with every place unreviewed.
- **No password reset.** It needs email.
- **No Docker**, and no deploy set up yet.

## 3. Screens

Five screens, built for a phone first. The look follows Tabelog, in Kansai Gaidai's colours: the
university's navy for the site, one warm colour for ratings, each place as a card with its name,
its category and its rating. [`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md) has the details.

- **Places** (the home page). A search box (name, in English or Japanese), a row of category
  filters (restaurant · café · fast food · ice cream), and a **Show bars and pubs** switch, off by
  default. The list changes as you type or press a filter, without the page reloading, and the
  address changes with it, so a search can be shared or bookmarked. Below them, the places as cards, 20 to a page, nearest the Nakamiya campus first. Each
  card shows the name, the category, the cuisine when it is known, the average rating as stars
  with the number beside it (*3.7*), and how many reviews (*12 reviews*), or *No reviews yet*.
  Its one job: help you pick a place.
- **A place.** The name large, in English when OpenStreetMap has an English name and in Japanese
  under it; the category and cuisine; the rating and the number of reviews; a link, *See it on
  OpenStreetMap*. Below, its reviews, newest first: the reviewer's name, the stars, the date, the
  text. A **Write a review** button. Its one job: show what people thought of this place.
- **Write a review.** Stars from 1 to 5, and the text. Only for someone logged in; a visitor who
  presses the button is sent to log in first, then back here.
- **Log in** and **Sign up.** A username and a password.

Every page ends with *© OpenStreetMap contributors*, which the map data's licence requires, and
*A student project. Not run by Kansai Gaidai University.*

---

*The engineering design*

## 4. The three parts

```
the browser                     the server                              the store
HTML pages, CSS        ──  Django: urls → views → templates   ──  db.sqlite3
   "show me places near campus" ▶     "the places, their averages" ▶
   ◀ a finished HTML page             ◀ the rows
```

| Part | What it is |
|---|---|
| **Frontend** (runs on the user's device) | HTML pages that the server builds from templates; one CSS file, `static/eats.css`, the design system; and **htmx**, one JavaScript file in `static/`, which lets a part of a page update without loading the whole page again. |
| **Backend** (runs on the server) | Django 5.2, in three apps, one per part of the product: `places`, `reviews` and `accounts`. Each has its own models, views, templates and tests. |
| **Data** (runs on the server) | `db.sqlite3`, one SQLite file. The places come from `data/places.json`, loaded by a command. |

**Technologies, and why each one.**

- **Django.** One framework gives the database models, the forms and their checks, log-in, the
  admin and the test client, so the code in this repository is only the product.
- **htmx, for the parts that react.** The server builds every page, as Django does. Where a part
  of a page should change by itself (the list as you type a search, a filter, later a *helpful*
  vote or a *save* button), htmx asks the server for just that part and swaps it in. The server
  still decides everything and still sends HTML, so the app stays one program in one language,
  and every test is a Django test. Each htmx control is also an ordinary link or form, so the page
  still works when JavaScript is off. htmx is one file, kept in `static/`, so there is nothing to
  install.
- **Three Django apps.** A feature usually belongs to one part of the product, so it changes one
  app's files and makes migrations in one app. Two people working on different parts do not edit
  the same files.
- **SQLite.** One file, no database server of its own.
- **uv** installs Python and the packages, at the versions in `uv.lock`. **Ruff** finds mistakes
  and formats the code (in the same style as Black). **pre-commit** runs both on every commit.
- **The places as a committed snapshot.** Every copy of the repository holds the same places, and
  the site never waits on a map service.

**The addresses.**

| Address | What it does |
|---|---|
| `GET /` | The places page. Takes `?q=` (search), `?category=`, `?bars=1`, `?page=`. Asked by htmx (the `HX-Request` header), it sends only the list, not the whole page |
| `GET /places/<id>/` | One place and its reviews |
| `GET /places/<id>/review/` · `POST` | The review form · save it, then back to the place (log-in needed) |
| `/accounts/login/` · `/accounts/signup/` · `POST /accounts/logout/` | Django's own log-in pages, and a sign-up page |
| `/admin/` | Django's admin, for staff |

**The rules.** A rating is a whole number from 1 to 5. The text is not empty after trimming, and is
at most 2,000 characters. Only a logged-in person can write a review, and the reviewer is always
the person logged in: it is never a field in the form. Every page can be read without logging in.

## 5. The data model

Three tables, and Django's own `User`.

| `places.Place` | |
|---|---|
| `id` | integer, primary key |
| `osm_id` | text, unique: where the place is in OpenStreetMap, like `node/14146066463` |
| `name` | text, as it is on the sign, usually Japanese |
| `name_en` | text, the English name, `""` when OpenStreetMap has none |
| `category` | one of `restaurant`, `cafe`, `fast_food`, `ice_cream`, `bar`, `pub` |
| `cuisine` | text, OpenStreetMap's tag, like `ramen` or `sushi;japanese`, `""` when unknown |
| `opening_hours` | text, OpenStreetMap's format, like `Mo-Fr 11:00-22:00`, `""` when unknown |
| `brand` | text, a chain's name, `""` for an independent place |
| `lat`, `lon` | decimal, where it is |
| `km_from_campus` | decimal, straight-line distance from the Nakamiya campus, worked out when loaded |

| `reviews.Review` | |
|---|---|
| `id` | integer, primary key |
| `place` | foreign key to `Place`; deleting a place deletes its reviews |
| `author` | foreign key to `User`; deleting a user deletes their reviews |
| `rating` | integer, 1 to 5 |
| `text` | text, at most 2,000 characters |
| `created_at` | date and time |

A place's average rating and number of reviews are **not stored**. They are worked out from
`Review` when a page asks, so they can never disagree with the reviews.

`python manage.py load_places` reads `data/places.json` and adds or updates each place by its
`osm_id`. Running it twice changes nothing; running it on a newer snapshot updates the places and
keeps their reviews.

Example rows: `Place` `1 · node/14146066463 · スターバックス · Starbucks · cafe · · · Starbucks ·
34.8236441 · 135.6635768 · 0.13` · `Review` `1 · 1 · aiko · 4 · Quiet in the morning, busy after
third period. · 2026-10-20 09:12`.

## 6. How I will know it works

1. When a visitor opens the home page, they should see places nearest the Nakamiya campus first,
   20 to a page, with no bar or pub unless they turn the switch on.
2. When a visitor searches *starbucks* or *スターバックス*, they should see the same place. When
   the search comes from htmx, the server should send only the list, and the same places.
3. When a logged-in person writes a review, it should appear first on that place's page, and the
   place's average and number of reviews should change on the place page and on its card.
4. When a place has reviews of 4, 4 and 5 stars, its rating should read *4.3*.
5. **And when it goes wrong:** a rating of 0, 6 or *great*, or an empty review, should be refused
   with a message saying which rule it broke. A visitor who tries to write a review should be sent
   to log in, and nothing should be saved. Someone who changes the form to name another person as
   the author should still be saved as themselves.

`make test` checks all of these: unit tests for the models and the loader, integration tests for
each address through Django's test client, and CUJ tests for two whole journeys (a visitor finds a
place; a new person signs up and reviews it). How the pages look, and that the list changes as
you type, is checked by eye, in a browser.

---

## 7. Adversarial review

| Objection | About | Decision | Why | What changed |
|---|---|---|---|---|
| Sample reviews would make the site look alive. | product | reject | The places are real businesses. A made-up review of a real shop, in a public repository, is unfair to it and looks real. | No sample reviews; tests make their own. |
| Ask OpenStreetMap for the places live, so they are always up to date. | design | reject | The public servers are often busy, and every copy should hold the same places. | A committed snapshot and a loader that can be run again. |
| Bars and pubs do not belong on a site for students. | product | accept in part | They are part of the area, and many students are over 20; some are not. | Hidden by default, one switch away. |
| Store the average on the place, so the list is fast. | design | reject | About 1,200 places and a database query can work it out. A stored copy can go out of date. | Worked out by the query; worth revisiting if it is ever slow. |
| Most names are in Japanese only, and most readers cannot read them. | product | accept | It is the biggest problem the data has. | English first when there is one; search finds either. |
| Two people adding fields in one app both make migration `0002`. | design | accept | Django sees the clash and refuses to run. | Three apps, so different parts do not clash. Within one app, `makemigrations --merge` joins them, and `make check` catches it. |
| Require log-in for every page, as a private app would. | product | reject | A review site is public. Reading should cost nothing. | Only writing needs log-in. |
| Build the frontend in React, with Django as an API. | design | reject | Two programs in two languages, a Node toolchain to install, and an API between them. Most features would change both sides, so twice the files and twice the clashes, and two kinds of tests. | htmx: the reactive parts, with the server still deciding and sending HTML. A move to React later is a project of its own. |
| Add Black as well as Ruff. | design | reject | Ruff's formatter writes Black's style. Two formatters on one file disagree about details and undo each other. | Ruff only, for both checks and formatting. |

## 8. Build or borrow

- **Built:** the pages, the three apps, the loader.
- **Borrowed:** Django (its models, forms, log-in, admin and test client), htmx 2.0 (Zero-Clause
  BSD licence, so no credit is required), SQLite, uv, Ruff, pre-commit, and the place data, from **OpenStreetMap** — © OpenStreetMap contributors, under the
  Open Database License (ODbL). The snapshot in `data/places.json` stays under the ODbL wherever
  it is copied. The code is not covered by the ODbL.

---

## 9. Features to add

[`FEATURES.md`](FEATURES.md) lists ten features to build next, each small enough for one plan,
one branch and one pull request. `docs/plans/` holds three more plans, for features not on that
list, drafted and not yet reviewed.
