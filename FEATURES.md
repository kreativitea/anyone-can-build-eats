# Features to add

Gaidai Eats starts small. These are ten features it could have next. Each one is small enough for
one plan, one branch and one pull request, and each one is something a real review site does.

**Build five of them**, in any order. Which five, and why those, is your decision. **Write a plan
for each one first**, in `docs/plans/<feature>.md`, from the template in `docs/plans/TEMPLATE.md`,
starting with the idea loop: the problem, what it costs, the change, what gets better. The three
plans already in `docs/plans/` are for features that are not on this list; read them, and have
them reviewed, before you build them.

## How to read the table

- **App** is the part of the code the feature changes most: `places`, `reviews` or `accounts`.
  Two features in **different apps** rarely touch the same files, so they can be built at the same
  time, on two branches, by two people or two agents.
- **Migration** says whether the feature changes a table. Two branches that both add a migration
  to the **same app** clash: both make a migration with the same number, and Django refuses to run
  until they are joined with `uv run python manage.py makemigrations --merge`. Build those one
  after the other, or expect to join them.
- **Size**: **S** is a few lines and a test or two. **M** changes a model, a view and a page.
  **L** needs a decision about the product before it can be built, and the plan should say what
  you decided and why.

## The features

| # | Feature | App | Migration | Size |
|---|---|---|---|---|
| 1 | **Choose the campus.** Measure distance from Nakamiya or Gotenyama, and sort by the one chosen. | places | yes | M |
| 2 | **Chains or independents.** Show or hide chain shops (`brand`), so the independent places can be found. | places | no | S |
| 3 | **Rankings.** The top ten in each category. Decide how many reviews a place needs before it can be ranked. | places | no | M |
| 4 | **Delete your own review.** | reviews | no | S |
| 5 | **One review per person per place.** Writing again opens the first one to edit. Decide what happens to people who already wrote two. | reviews | yes | L |
| 6 | **Sub-ratings,** as Tabelog has: food, service, atmosphere, value for money, drinks. Each optional; each place shows its averages. | reviews | yes | M |
| 7 | **Lunch or dinner, and what you spent,** in bands (*under ¥1,000*, *¥1,000–1,999* …). The place shows its usual price for each. | reviews | yes | M |
| 8 | **The date you went.** It cannot be in the future. | reviews | yes | S |
| 9 | **Star breakdown.** On the place page, how many reviews gave each number of stars, as bars. | reviews | no | S |
| 10 | **A profile page.** A person's reviews, newest first, and how many they have written. Every reviewer's name links to it. | accounts | no | S |
