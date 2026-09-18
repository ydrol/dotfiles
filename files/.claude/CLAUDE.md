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

## Don't re-verify what I assert

When I state a fact, a measurement, or the value a change should take, treat it
as already checked. **Ask before probing, querying a live system, running an
experiment, or searching the web to confirm it.** A one-line question costs
nothing; a probe run costs tokens and wall-clock to re-derive what I already
know. Assume I've done the homework — I rarely raise something on a whim.

- This covers work undertaken *to confirm a claim of mine*: live-instance
  probes, exploratory test runs, doc lookups. Reading code to find the places a
  change has to touch is ordinary implementation work — do that without asking.
- If you think verification is genuinely worth it — you suspect I'm wrong, or
  the change is hard to reverse — say in one sentence what you'd check and why,
  then wait for my answer.
- If you think I'm wrong, argue it from what you already know rather than
  proving it empirically. State the contradiction and let me respond.

## Plan format

When re-displaying a plan in response to a follow-up prompt or question (i.e. a
plan that has already been shown), do BOTH:

1. **Amend the body** of the plan in place so it reads as one coherent, current
   plan.
2. **Restate the changes at the end** in a section titled **`## Plan
   Amendments`**, newest first (reverse chronological — each new revision's
   delta goes at the top of that section). Each entry is the delta for one
   revision: what changed and why, not a re-description of the whole plan.

Keep this section only while the plan is a living document; drop it once the
plan is finalised into a committed doc.

## Project documentation artefacts

My projects carry a standard documentation set — `README.md`, `AGENTS.md` (with
`CLAUDE.md` symlinked to it), `decisions/D###-slug.md` ADRs with a generated
index, `documentation/` reference files, `BACKLOG.md` — each with a defined
format. **`~/.claude/project-artefacts.md` is the master specification.**

Read it before: creating or restructuring a project doc, writing or citing an
ADR, recording open work, initialising a new repo's docs, or auditing an
existing repo against the standard. Don't invent a structure or a frontmatter
field when that file already defines one, and don't restate its rules inside a
project — cite it.

## Writing style

These rules govern narrative and argument wherever they appear: chat, the prose
sections of documents, commit messages, client deliverables. Structured
reference material is exempt and should stay structured.

- **BLUF is structural, not syntactic.** BLUF governs the order of information —
  lead with the conclusion. It does not mean compressed sentence construction.
  Write in connected, flowing paragraphs, not clipped, minute-taking style.
- **Concision is a property of the response, not the sentence.** Cut whole
  paragraphs that do not earn their place; do not buy brevity by stripping the
  words that hold a sentence together. Flowing prose is not a licence to pad.
- **Protect connective tissue.** Do not strip function words ("that", "which",
  "who is") for density. Name the actor: prefer the active voice, and where a
  passive or reduced clause is used, say who performs the action.
- **Vary the mechanics.** Vary sentence length deliberately. Avoid consecutive
  sentences opening with the same subject-verb pattern unless the repetition is
  deliberate.
- **Cohesion through grammar, not adverbs.** Connect related statements with
  subordinate clauses and conjunctions rather than stacking short sentences
  glued together with "However" or "Notably". Do not use a definite noun phrase
  ("the codes", "the room") for something not yet introduced.
- **Bullet discipline.** Bullets are for parallel items a reader will scan or
  look up: options, checks, inventories, cases. They are not for reasoning.
  Where the connection between two statements is the point, whether cause,
  exception, dependency or sequence, grammar has to carry it, and a bullet
  severs it. This applies by passage, not by document. A reference table belongs
  in a client report, and an argument broken into six bullets is wrong in a
  design doc.
- **Register.** Maintain a formal professional tone. Flowing prose does not mean
  conversational prose.
- **Endings still land.** Stopping once the information is delivered means
  adding no summary and no wrap-up, not ending mid-cadence.

## Code comments

Comments in deliverable code are succinct and elegant, or absent. The failure mode to avoid is the
**tutorial comment** — the dominant style in training data, and never what I want.

- **Never restate the code.** If the line below says what the comment says, delete the comment.
- **Rename before commenting.** A comment explaining what a variable holds is a variable with the
  wrong name. Fix the name and the comment has nothing left to say.
- **No project-internal references.** Decision ids, ticket numbers, doc section numbers, internal
  filenames — none of it means anything to someone reading the code. Rationale belongs in the
  commit message or the design doc, not the source.
- **Plain English, standard domain terms.** Prefer the word the wider industry uses over one this
  codebase invented.
- **Length is a smell.** If it takes a paragraph to make a block clear, the block is not clear.
  Refactor until the code is the comment, then delete the comment.

What survives the cut is a *why* the code genuinely cannot express: a non-obvious external
constraint, a workaround for someone else's behaviour, an ordering that looks arbitrary and is not.

**Never touch a comment you were not asked to touch.** Comment edits are in scope only when:

- the code is new;
- the comment sits on code the change actually modifies; or
- the task *is* a comment cleanup or refactor, asked for as such.

Everything else is unsolicited churn. A tidied comment three functions away turns a one-line change
into an unreviewable diff, and the separation a careful commit history gives you is lost the moment
the reviewer reads the deployed artefact rather than the repo — deployment records the push, not
the commit.

## Deleting files

**Never `rm -rf` a path you have not just enumerated.** Not as cleanup, not for a directory you
believe you created, not because it is "obviously" safe.

The sequence is always: `ls -Rl <path>` and read the output; `rm` the individual files; then
`rmdir` each directory from the leaves up. `rmdir` refuses a non-empty directory, which is the
point — it fails closed when the enumeration missed something.

A wrong path expands silently and there is nothing to undo.
