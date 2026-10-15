# Plan: edit your own review

Status: draft, not yet reviewed.

*No real person's name or data in a plan or a prompt.*

## 1. The idea

- **The problem:** a person who wrote a review cannot change it: not a typo, not the stars after a
  second visit.
- **What it costs:** reviews stay wrong or out of date, and the only fix is to write a second one,
  which counts twice in the place's rating.
- **The change:** an **Edit** link under your own reviews on the place page. You can change the
  stars or the text, and the review then shows *edited*, so readers know it is not the first
  version.
- **What gets better:** reviews stay accurate, and nobody writes a second review just to correct
  the first.
- **Checked with a real person:** a classmate who writes reviews on a map app said they change the
  stars after a second visit.

## 2. Files it touches

| File | Function or section | Add or change |
|---|---|---|
| `reviews/models.py` | `Review.edited_at` | add: a date and time, empty until the first edit |
| `reviews/migrations/0002_review_edited_at.py` | | add, made by `makemigrations` |
| `reviews/views.py` | `review_edit` | add: `@login_required`; finds the review with `get_object_or_404(Review, pk=pk)`; `GET` shows the form filled in, `POST` saves it, sets `edited_at`, and goes back to the place |
| `reviews/urls.py` | `reviews/<int:pk>/edit/` | add |
| `reviews/templates/reviews/form.html` | the heading and the button | change: *Edit your review* and **Save** when editing |
| `places/templates/places/detail.html` | each review | change: an **Edit** link only under the logged-in person's own reviews (`{% if review.author == user %}`), so nobody else can reach the edit page; *edited* after the date |
| `reviews/tests/integration/test_review_edit.py` | | add |

The form is the same `ReviewForm` a new review uses, so the rules (1 to 5 stars, text not empty,
at most 2,000 characters) are checked the same way.

## 3. Done when

- When the author changes a review from 3 stars to 5, the place page should show 5 stars, and the
  place's rating should change with it.
- When the author saves an edit, the review should show *edited*, and keep its place in the list.
- When a visitor who is not logged in opens the edit address, they should be sent to log in, and
  nothing should change.
- When the edit breaks a rule (0 stars, empty text), the form should show again with the message,
  and the review should not change.
- The **Edit** link should appear only under the logged-in person's own reviews.
- Test count before: 27. Test count when done: at least 33.

## 4. Not in this plan

- Deleting a review (feature 4 in `FEATURES.md`).
- A history of earlier versions. *edited* says that it changed, not what it was.
- Staff editing other people's reviews. Staff use the admin.
- Moving an edited review to the top of the list.

## 5. Decisions for me

1. **Does an edited review move to the top?** The list is newest first. If an edit moved a review
   up, editing would become a way to stay at the top. *Recommendation: no, it keeps its place.*
2. **Does saving with no change count as an edit?** Pressing **Save** by accident would mark it
   *edited*. *Recommendation: only mark it when the stars or the text really changed.*
3. **Show when it was edited, or only that it was?** *edited 3 Nov 2026* says more; *edited* is
   shorter on a phone. *Recommendation: only *edited*, with the date in a `title`.*

After the review, each objection, *accept* or *reject*, and *why*:

-
