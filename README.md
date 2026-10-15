# Gaidai Eats

A review site for the places to eat and drink near Kansai Gaidai, in the style of Tabelog. Every
restaurant, café and fast-food place within 5 km of the Nakamiya and Gotenyama campuses, and
reviews written by the people who went. Anyone can read it; to write a review, you sign up.

It is built in Django, and it starts small on purpose. [`FEATURES.md`](FEATURES.md) lists what
to build next. [`DESIGN.md`](DESIGN.md) says how it works and why, and
[`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md) says how it looks.

*A student project. Not run by Kansai Gaidai University.*

## Get your own copy

Your copy is a **private** repository on your own GitHub account. You make it in four steps:
clone this one, make an empty repository of your own, push to it, and add your teacher.

**1. Clone this repository.** In a terminal, in the folder where you keep your projects:

```bash
git clone https://github.com/kreativitea/anyone-can-build-eats.git
cd anyone-can-build-eats
```

**2. Make an empty repository on GitHub.** On <https://github.com>, press **+** at the top right,
then **New repository**.

- **Repository name:** `anyone-can-build-eats`
- Choose **Private**.
- Leave **Add a README**, **.gitignore** and **license** turned off. The repository must be
  empty, or the push in step 3 is refused.

Press **Create repository**.

**3. Push your copy to it.** Put your GitHub name where it says `YOUR-NAME`:

```bash
git remote rename origin upstream
git remote add origin https://github.com/YOUR-NAME/anyone-can-build-eats.git
git push -u origin main
```

The first line keeps the original repository under the name `upstream`. The second makes your new
repository `origin`, the one `git push` sends to from now on. You never push to `upstream`.

If git asks you to log in, run `gh auth login` and try the push again.

**4. Add your teacher as a collaborator.** In your new repository on GitHub, open **Settings**,
then **Collaborators**, then **Add people**, and add
[**kreativitea**](https://github.com/kreativitea) (Michael Omoto).

**Check:** reload your repository's page on GitHub. It says **Private** next to its name, it has
all the files, and **Settings → Collaborators** shows kreativitea, as invited or added.

Your pull requests now open in your own repository, with your own `main` as the base.

## Your prompts are written down

Every prompt you type into Claude Code in this repository is saved, word for word, in
`docs/prompts/`, by a hook in `.claude/settings.json`. **Commit those files with your work**, and
never change what is already in them. Only your words are saved, not the AI's answers.
[`docs/prompts/README.md`](docs/prompts/README.md) has the details, and what to do if you use a
different AI tool.

The first time you open Claude Code in this folder, it asks whether you trust it. Say yes, or the
hook does not run.

## Run it on your laptop

**1. Install uv, once.** uv installs Python and this project's packages for you.

Mac:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close the terminal and open a new one, then check with `uv --version`.

**2. Set it up.** This installs the packages, creates the database, loads the places and turns on
the commit checks:

```bash
make setup
```

Without `make` (on Windows), the same is:

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py load_places
uv run pre-commit install
```

**3. Start the server.**

```bash
make run
```

Open <http://127.0.0.1:8000/>. You see the places nearest the Nakamiya campus. Press **Sign up**
to make an account, so you can write a review. Press `Ctrl+C` in the terminal to stop the server.
Without `make`: `uv run python manage.py runserver`.

**4. Run the tests.**

```bash
make test
```

You should see `OK`, then one line for each level of tests, like `Unit: 8 passed`. **Write down
the count**: every feature you add should make it go up. Without `make`:
`uv run python manage.py test`.

`make help` lists every command.

## Build a feature

1. Pick a feature from [`FEATURES.md`](FEATURES.md). You build five of its ten.
2. Write its plan in `docs/plans/<feature>.md`, from `docs/plans/TEMPLATE.md`. Three plans are
   already there, for features not on the list. They have not been reviewed: review them before
   you build any of them.
3. Have the plan reviewed (`docs/reviewer.md`, in a new session), build it on its own branch
   (`make worktree BRANCH=<feature>`), have the result reviewed, and check it in the browser.
4. Open a pull request in your repository, in your own words, with the plan and the prompts in it.
   Merge it when `make check` passes and you can explain every change.

## Checks

| Command | What it does |
|---|---|
| `make lint` | Finds mistakes and bad habits in the Python code (Ruff) |
| `make format` | Rewrites the Python code in the standard style (Ruff) |
| `make check` | Every commit check on every file, a check for missing migrations, then every test |

The commit checks run by themselves on every `git commit`. If a check fails because it fixed a
file for you, look at the change, `git add` the file, and commit again.

## The data

The places are from **OpenStreetMap**: © OpenStreetMap contributors, under the
[Open Database License](https://opendatacommons.org/licenses/odbl/1-0/). They are a snapshot,
in `data/places.json`, so the site never calls a map service while it runs. The snapshot stays
under the ODbL wherever it is copied; your code does not.

The places are real businesses. **Never write a made-up review of a real place**, in a test, a
screenshot or a demo: tests make up their own places.
