---
name: session-handoff
version: 1.0.0
description: >
  Write a HANDOFF-YYYY-MM-DD-HHMM.md capturing everything a cold session (or a human returning in three
  months) needs to pick up this work: the project's purpose and how its understanding has evolved, what was
  accomplished, the architecture decisions and their rationale, mistakes made and lessons learned, remaining
  TODOs, problems visible on the horizon, the docs and skills touched, and a candid read on how the user has
  been responding to the work. Use whenever the user asks for a handoff, a handover, a session summary to
  carry forward, a "write up where we got to", or says they are stopping and want the context preserved.
  Also appropriate unprompted when a long session is clearly ending and context is about to be lost.
---

# Session handoff documents

A handoff is written for **someone who was not here**. That is the only test that matters. A new session
starts with the repo, the git log, and this file — nothing else. Every sentence has to survive that.

## Where the file goes

`HANDOFF-YYYY-MM-DD-HHMM.md` in the project root, unless the user names somewhere else or the repo already
has a `handoffs/` or `docs/handoffs/` directory — use it if it exists.

**Get the timestamp from the system, never from memory:**

```bash
date +%Y-%m-%d-%H%M
```

Model knowledge of the current date is unreliable and a wrong timestamp makes the file sort wrongly against
its siblings forever.

## The nine sections

Write them in this order. Keep the headings stable across handoffs so a reader who has seen one can navigate
the next.

### 1. Project understanding — purpose, evolution, future

Three things, and keep them distinct:

- **What it is and what it was originally for.** State the problem it solves, not the implementation.
- **How that has evolved, with rationale.** The interesting part. What did the project turn out to be that it
  was not at the start? What forced each shift — a discovered constraint, a client need, a wrong assumption
  that broke? A reader who knows only the current code cannot recover this, which is exactly why it belongs
  here.
- **Where it goes next, split in two:**
  - **From the user's perspective** — what they have actually said they want. Quote or paraphrase their own
    framing. Do not extrapolate into this subsection.
  - **Blue sky (your own view)** — what you would do with it given no constraints, clearly labelled as your
    opinion. This is the one place in the document where speculation is invited. Say what the project could
    become, what it is structurally close to that nobody has named yet, and what you would stop doing. Be
    concrete enough to disagree with.

### 2. Work accomplished

What actually landed. Commit SHAs and titles, files touched, tests added, before/after numbers where they
exist. Distinguish **shipped and verified** from **shipped but unverified** from **started and abandoned** —
a reader will otherwise assume everything listed is solid.

### 3. Architecture decisions and rationale

Each decision: what was chosen, what was rejected, and **why** — including the argument for the losing
option, so it does not get re-proposed on Monday. If the repo has an ADR log, cite the entries rather than
restating them, and record here only what the ADR does not carry (usually: the discussion that surrounded it).

### 4. Mistakes made and lessons learned

**Write this section honestly or do not write it at all.** It is the highest-value part of the document and
the easiest to hollow out into nothing.

Include: things asserted that turned out to be wrong, verification that looked sound and was not, work done
in the wrong order, things missed that a reviewer or the user caught. For each: what the error was, how it was
caught, and what would catch it next time. Name your own errors plainly — a handoff that reads as though the
session went perfectly is a handoff nobody trusts.

### 5. TODO items remaining

Ranked, with enough context to start each without re-deriving it. Mark anything blocked and say what unblocks
it. If the repo tracks a backlog, point at it rather than duplicating — but pull forward the two or three
items that matter *now*.

### 6. Potential issues on the horizon

Things not yet broken. Accumulating debt, a design decision that will not survive the next feature, an
external dependency that is drifting, a scaling limit approaching. Say what the early warning sign would be,
so the next session can recognise it.

### 7. Docs and skills used or updated

Every doc file touched and what changed in it. Every skill invoked and whether it was accurate — a skill that
taught something stale is a defect worth recording. Include external references (vendor docs, tickets, URLs)
that were consulted and would be needed again.

### 8. Subjective read on the user's mood

Candid, evidence-based, and short. What is the user's disposition toward the work — trusting, checking
closely, frustrated, energised? What have they pushed back on, and were they right? What do they clearly value
(rigour, speed, brevity, being challenged) and what visibly annoys them?

**Cite behaviour, not vibes.** "Pushed back on the sys_id uniqueness claim and was right, then asked for the
reasoning to be re-verified before commit" is useful. "Seemed happy" is not. If the user corrected you
repeatedly, say so; if they accepted work without scrutiny, say that too — it tells the next session how much
independent verification to carry.

Do not flatter the user and do not flatter yourself. If the session was rough, the next session needs to know.

### 9. State at handoff

Close with the mechanical facts: current branch, HEAD SHA, whether it is pushed, working-tree cleanliness,
any uncommitted or untracked files and whether they matter, and how to run the tests.

## How to write it

- **Verify before asserting.** A handoff is read as ground truth by a session with no way to check it. If you
  did not confirm something, write "unverified" or "believed, not checked". A confident wrong sentence here
  costs more than a missing one.
- **Cite `file:line`, commit SHAs, and ADR identifiers** so claims are followable.
- **No "as discussed above" or "we decided earlier"** — there is no above and no we. Restate.
- **Prefer specifics over summary.** "2384 → 2394 tests, 6 pinning the JOIN-veto strings" beats "improved test
  coverage".
- **Match the repo's writing conventions** if it has them (check `CLAUDE.md` / `AGENTS.md` / a style section).
- Length follows the session. A one-hour session gets a page; a long, dense one gets several. Do not pad thin
  sessions to fill nine headings — write "nothing of note" and move on.

## After writing

Tell the user the path and give a two-line summary of what it covers. Do not commit it unless asked — a
handoff is often deliberately kept out of the repo.
