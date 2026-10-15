# Plan: helpful votes

Status: draft, not yet reviewed.

*No real person's name or data in a plan or a prompt.*

## 1. The idea

- **The problem:** on a busy place, the newest review is at the top, whether it is useful or
  three words long.
- **What it costs:** a reader scrolls past short reviews to find one that says what to order and
  how long the wait is, or leaves without finding it.
- **The change:** under each review, a **Helpful** button and a count: *12 people found this
  helpful*. A logged-in person can press it once per review, but not on their own. The place page
  shows the most helpful reviews first.
- **What gets better:** the useful reviews rise to the top, and writing a useful review is
  rewarded.
- **Checked with a real person:** not yet.

## 2. Files it touches

| File | Function or section | Add or change |
|---|---|---|
| `reviews/models.py` | `Review.helpful_count` | add: a whole number, starting at 0 |
| `reviews/migrations/0002_review_helpful_count.py` | | add, made by `makemigrations` |
| `reviews/views.py` | `review_helpful` | add: `@login_required`, `POST` only; adds 1 to the review's `helpful_count` with an `F()` expression, so two presses at the same moment both count; refuses the author's own review with 403; answers htmx with just the button and the new count |
| `reviews/urls.py` | `reviews/<int:pk>/helpful/` | add |
| `reviews/templates/reviews/_helpful.html` | | add: the button and the count. After a press, htmx swaps in the button greyed out (`disabled`), so the same person cannot press it again |
| `places/templates/places/detail.html` | each review | change: include `_helpful.html`; a **Most helpful** / **Newest** choice above the list, *Most helpful* chosen |
| `places/views.py` | `place_detail` | change: reviews order by `-helpful_count`, then newest; `?sort=newest` orders by newest only |
| `reviews/tests/integration/test_helpful.py` | | add |

## 3. Done when

- When a logged-in person presses **Helpful** on someone else's review, the count should go up by
  one, and the button should come back disabled.
- When the author presses **Helpful** on their own review, the server should answer 403 and the
  count should not change.
- When a visitor who is not logged in presses it, they should be sent to log in, and the count
  should not change.
- A `GET` to the helpful address should change nothing.
- On a place's page, a review with 3 votes should come before one with 1 vote, even when it is
  older. With `?sort=newest`, the newest comes first.
- Test count before: 27. Test count when done: at least 32.

## 4. Not in this plan

- Taking a vote back.
- *Not helpful* votes.
- Showing who voted.
- Hiding reviews with few votes.

## 5. Decisions for me

1. **Can a visitor see the count?** The count helps everyone; only voting needs an account.
   *Recommendation: everyone sees it, only logged-in people can press.*
2. **Default sort on the place page: newest or most helpful?** The reason for the feature is to
   put the useful reviews where a reader sees them first. *Recommendation: most helpful is the
   default; newest is one press away.*
3. **Wording when the count is 0.** *0 people found this helpful* reads as a judgement.
   *Recommendation: show only the button until the first vote.*

After the review, each objection, *accept* or *reject*, and *why*:

-
