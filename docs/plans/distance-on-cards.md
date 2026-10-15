# Plan: distance on each card

Status: draft, not yet reviewed.

*No real person's name or data in a plan or a prompt.*

## 1. The idea

- **The problem:** a student choosing where to eat cannot tell from the list how far a place is.
  The list is sorted nearest first, but the order does not say whether the tenth place is 400 m
  away or 3 km.
- **What it costs:** they open places one by one, or check a map app, or give up and go to the
  one they already know.
- **The change:** each card says how far the place is from the Nakamiya campus, like *1.2 km*.
- **What gets better:** a reader can see at a glance whether a place is a walk or a bus ride, and
  picks from the list itself.
- **Checked with a real person:** not yet.

## 2. Files it touches

| File | Function or section | Add or change |
|---|---|---|
| `places/models.py` | `Place.distance_label` | add: the distance as words for the page |
| `places/templates/places/_card.html` | the `meta` line | change: show `distance_label` after the cuisine |
| `places/tests/unit/test_models.py` | `DistanceLabelTests` | add |
| `places/tests/integration/test_place_list.py` | `PlaceListTests` | add: the card shows the distance |

No migration: `km_from_campus` is already worked out when the places are loaded.

## 3. Done when

- When a place is 1.234 km from campus, its card should read *1.2 km*.
- When a place is 0.125 km from campus, its card should read *0.1 km*.
- When a place is 0.04 km from campus, its card should read *under 0.1 km*, never *0.0 km*.
- When a place is 4.96 km from campus, its card should read *5.0 km*.
- The place page does not change.
- Test count before: 27. Test count when done: at least 32.

## 4. Not in this plan

- Distance from Gotenyama, or a choice of campus (feature 1 in `FEATURES.md`).
- Walking time. A straight line is not the walk, and the page should not pretend it is.
- Metres for short distances (*130 m*). One unit everywhere is easier to compare.
- A new sort. The list is already nearest first.

## 5. Decisions for me

1. **Kilometres always, or metres under 1 km?** Metres read more naturally for a place next door,
   but two units on one list are harder to compare. *Recommendation: kilometres, one decimal.*
2. **What does a place closer than 0.1 km show?** *0.0 km* looks like a mistake. *Recommendation:
   under 0.1 km.*
3. **Should the card say it is a straight line?** Some readers will take *1.2 km* as the walk.
   *Recommendation: no extra words on the card, but a `title` on the number, "straight-line
   distance from the Nakamiya campus", which a screen reader also reads.*

After the review, each objection, *accept* or *reject*, and *why*:

-
