# Prompts

Every prompt you type into Claude Code in this repository is written here, word for word, by
`.claude/hooks/log_prompt.py`. There is one file per session, named by its date and session:
`2026-10-31-1a2b3c4d.md`. Each prompt is under the time and the branch it was typed on.

- **Commit these files with your work.** A session in a worktree writes into that worktree, so its
  prompts go in the same pull request as the change they asked for.
- **Add to them; never change what is already in them.** The git history shows any change.
- **Only your words are written, not the AI's answers.** Anything that looks like a secret key is
  replaced with `[REDACTED]`, but do not paste passwords, keys or anyone's personal details into
  a prompt in the first place.
- **Using a different AI tool** (Codex, a chat in the browser)? It has no hook. Copy what you typed
  into a file here yourself, in the same shape, before you commit.
