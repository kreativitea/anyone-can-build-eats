"""Write down every prompt you type into Claude Code, in docs/prompts/.

Claude Code runs this file each time you send a prompt (see .claude/settings.json). It adds what
you typed, word for word, to a file for this session: docs/prompts/<date>-<session>.md, in the
folder you are working in. A session that runs in a worktree writes into that worktree, so the
prompts are committed on the same branch as the work they asked for.

It writes only your words, never the AI's answers. Anything that looks like a secret key is
replaced with [REDACTED] before it is written. It never stops your prompt: if anything goes
wrong, it says so and lets the prompt through.

Standard library only, so it runs before `uv sync`.
"""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SECRETS = [
    re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),  # OpenAI and Anthropic keys
    re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}"),  # GitHub
    re.compile(r"AKIA[0-9A-Z]{16}"),  # AWS
    re.compile(
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S
    ),
]


def git(cwd, *args):
    result = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=False
    )
    return result.stdout.strip()


def fenced(text):
    """Put the prompt in a code block, longer than any backtick run inside it."""
    longest = max((len(run) for run in re.findall(r"`+", text)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}text\n{text}\n{fence}"


def main():
    event = json.load(sys.stdin)
    prompt = event.get("prompt", "")
    if not prompt.strip():
        return
    for pattern in SECRETS:
        prompt = pattern.sub("[REDACTED]", prompt)

    cwd = event.get("cwd") or "."
    root = Path(git(cwd, "rev-parse", "--show-toplevel") or cwd)
    branch = git(cwd, "rev-parse", "--abbrev-ref", "HEAD") or "unknown"
    session = (event.get("session_id") or "nosession")[:8]
    now = datetime.now().astimezone()

    folder = root / "docs" / "prompts"
    folder.mkdir(parents=True, exist_ok=True)
    log = folder / f"{now:%Y-%m-%d}-{session}.md"
    if not log.exists():
        log.write_text(
            f"# Prompts — session {session}, {now:%Y-%m-%d}\n\n"
            "Written by `.claude/hooks/log_prompt.py`: every prompt typed in this session, "
            "word for word. Add to this file; never change what is already in it.\n",
            encoding="utf-8",
        )
    with log.open("a", encoding="utf-8") as f:
        f.write(f"\n## {now:%H:%M} · branch `{branch}`\n\n{fenced(prompt)}\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:  # never block a prompt because the log failed
        print(f"log_prompt.py could not write the prompt log: {error}", file=sys.stderr)
    sys.exit(0)
