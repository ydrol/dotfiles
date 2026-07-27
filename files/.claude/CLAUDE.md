# Global instructions

## Shell command style

The Bash tool runs under bash (`defaultShell: "bash"`); the interactive login
shell is zsh. Write commands that are correct in both, and that match existing
permission allow-rules so they don't re-prompt:

- **Don't rely on implicit word-splitting.** `S="python3 x.py"; $S` is wrong in
  every shell — bash only fails to punish it, zsh errors outright. Inline the
  command, or use an array: `cmd=(python3 x.py); "${cmd[@]}"`.
- **Invoke interpreters/tools by bare token** (`python3`, `node`, `git`), never
  an absolute pyenv-shim path. Bare tokens match `Bash(python3 *)`-style
  allow-rules; absolute paths (`/home/.../.pyenv/shims/python3`) don't, and
  re-prompt every time. Bare `python3` already resolves to the pyenv shim here.
- **Prefer atomic single commands** over `export …; …; for …; done | …` chains.
  Compound strings can't match prefix allow-rules, so each one re-prompts and a
  "don't ask again" choice never carries over to the next.
- **Push nontrivial logic into a script file** and invoke it trivially
  (`python3 scan.py`) rather than cramming loops/heredocs into a one-liner —
  it avoids quoting bugs and matches allow-rules cleanly.
