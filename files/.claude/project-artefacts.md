# Project documentation artefacts

The standard documentation set for my projects: which files exist, what each one holds, and the format rules
each one is written to. Read this before creating a project doc, adding a decision, recording open work,
initialising a new repo, or auditing an existing repo's docs against the standard.

**Reference implementation: `~/work/bitbucket/snowdrift`.** Every rule below is in use there — read the real file
when a rule needs an example. `snowdrift/decisions/README.md` and `snowdrift/AGENTS.md` are the two files to copy
from when seeding a new repo.

**This file is the master.** It lives at `~/bitbucket/dotfiles/files/.claude/project-artefacts.md`, symlinked to
`~/.claude/project-artefacts.md` and referenced from `~/.claude/CLAUDE.md`. Edit the dotfiles copy, never the
symlink target in `~/.claude`. Changes here apply to every project; a project that needs to deviate records the
deviation as its own ADR and says so in its `AGENTS.md`.

## The artefact set

| Path | Holds | Maintained |
|---|---|---|
| `README.md` | Repo root. Index + quickstart. The canonical voice all other generated prose matches. | Hand |
| `AGENTS.md` | Repo root. Working conventions for agents and the author: code layout, review rules, writing style, doc map. `CLAUDE.md` is a **symlink** to it — edit `AGENTS.md`. | Hand |
| `ONBOARDING.md` | Repo root. Cold-start orientation for a new contributor or session. Stays at the root: the share-guide flow only uploads it from there. | Hand |
| `CHANGELOG.md` | Repo root. User-facing changes per released version, each entry citing its ADR. Stays at the root: it is what the git host renders and what packaging tools look for. | Hand |
| `decisions/D###-slug.md` | One settled choice per file — adopted, rejected, or superseded. The reason a question is not re-litigated. | Hand |
| `decisions/README.md` | The ADR index, grouped by domain, **plus the canonical definition of the ADR frontmatter vocabulary**. | Generated (preamble hand) |
| `documentation/ARCHITECTURE.md` | How it works: execution flow, component roles, the models and schemes a reader must hold to change anything. | Hand |
| `documentation/FEATURES.md` | What it does today + the full interface reference. Terse entries pointing at depth elsewhere. Carries originator tags. | Hand |
| `documentation/CODEMAP.md` | Where code lives: module map, classes and functions by area, greppable anchors. | Generated |
| `documentation/BACKLOG.md` | Open work: known limitations, deferred items, back-burner proposals. The open counterpart to `decisions/`. | Hand |
| `documentation/REFACTOR_TRAIL.md` | The structural-refactor arc: what shipped, how behaviour-neutrality was proved, reusable harnesses, mistakes not to repeat, ranked remaining targets. | Hand |
| `documentation/BUILD.md` | Building and installing the deliverable. | Hand |
| `documentation/HANDOFF-YYYY-MM-DD-HHMM.md` | Session handoffs (the `session-handoff` skill writes these). | Generated |
| `documentation/STATUS.md` | The verification record: what is proven, by which spike or live run, on which instance. Optional — for projects whose claims must be measured rather than reasoned. | Hand |
| `agent-docs/` | Docs that **ship to a consumer** — the vendor-neutral agent reference, harness wrappers, a pasteable `CLAUDE.md` block. A separate tree from the internal docs, and a disclosure boundary. | Mixed |
| `reference/` | Code cited but not owned, verbatim, never edited. Indexed by `reference/README.md`. | Frozen |
| `resources/` | Cached source documents pulled from Drive or the web, with an index — see the **Reference Caching mechanism** section of `~/.claude/CLAUDE.md`. | Mixed |

Anything else — a masking reference, an MCP design, a performance note — is a subject file under `documentation/`,
named for its subject in `SCREAMING_SNAKE.md`, and listed in the `AGENTS.md` doc table with a "read it when…" line.

**Directory names.** `decisions/` sits at the repo root; the number-slug path `decisions/D###-slug.md` is written
into hundreds of citations and into the index generator, so nesting it buys nothing. Everything else goes under
`documentation/`. An existing repo already using `docs/` keeps that name — renaming a directory rewrites every
citation in the repo for no reader benefit. Pick one and do not churn it.

## Where each convention is defined

One definition, one place. When applying these rules to a repo, read the definition rather than restating it:

| Convention | Canonical definition |
|---|---|
| The artefact set and its formats (this document) | `~/.claude/project-artefacts.md` |
| ADR frontmatter fields and their vocabulary | That repo's `decisions/README.md` preamble |
| Originator tags, review rules, code conventions, writing style | That repo's `AGENTS.md` |
| The prose voice all generated docs match | That repo's `README.md` |
| Cached-source front matter and staleness | `~/.claude/CLAUDE.md`, "Reference Caching mechanism" |

A repo doc never restates a field definition that `decisions/README.md` already carries — it links to it. Two
copies of a vocabulary is two copies to drift.

## Decision log (ADRs)

**One file per decision, `decisions/D###-slug.md`.** A monolithic `DECISIONS.md` fails three ways at scale — the
topic grouping is abandoned, a single decision fragments across amendments filed far apart, and the record drifts
into unindexable free-prose statuses. See `D233-decision-log-one-file-per-adr` for the measurements that settled it.

### Frontmatter

```markdown
---
id: D042
title: "Address columns added to `UserLikeDefinition`"
status: adopted
domain: masking
originator: Author
raised_by: Andy
raised: 2026-08-19
decided: 2026-08-23
originator_note: "Author called the columns; AI derived the exclusion rule."
revises: [D020]
---

# D042 — Address columns added to `UserLikeDefinition`

<the argument, in prose>
```

| Field | Rule |
|---|---|
| `id` | `D###`, zero-padded, matching the filename prefix. Sequential, stable, never reused. |
| `title` | The decision in one line, quoted. Not a path, not a summary of the argument. |
| `status` | `adopted`, `rejected`, `superseded`, or `parked`. See the status vocabulary below. |
| `domain` | One of the domains the repo's index generator groups by. Add a domain to the generator, not ad hoc. |
| `originator` | `Author`, `AI`, or `Author+AI`. Default `Author` when the user raised it; `AI` only when the assistant originated it unprompted. |
| `raised_by` | The person who raised it, by name. Mandatory where a human did. Omitted on `originator: AI`. |
| `raised` | ISO date the requirement or question was raised. |
| `decided` | ISO date it was settled. Mandatory. The index sorts and dates from this. |
| `originator_note` | Optional, quoted. Who did which part, where `Author+AI` loses the detail. |
| `revisit` | Mandatory on `status: parked` — what would un-park it. |
| `supersedes` / `superseded_by` / `revises` / `revised_by` / `extends` / `extended_by` | ADR-id lists, `[D122, D130]`. |

**Provenance is the point of the first six fields.** A reader must be able to tell a requirement the author set
from an inference the tool made, without asking, because the two carry different authority: an AI-invented
constraint may be dropped, one of the author's may not. `raised_by` + `raised` carry the human half; `originator`
carries the split. Record it when the entry is written — it is unrecoverable later.

### Status vocabulary

| Status | Means | Consequence |
|---|---|---|
| `adopted` | Settled and in force. | — |
| `rejected` | Proposed, never adopted. Records *why*, so it stays rejected. | — |
| `superseded` | Adopted, then wholly replaced. | Carries `superseded_by`. Never deleted or rewritten. |
| `parked` | Adopted or drafted, then deliberately set aside with the reasoning kept. | Carries `revisit`: the measurement, threshold or event that reopens it. |

`rejected` and `parked` are different facts and the log must say which — a reader needs to know whether a thing was
tried and set aside or never adopted at all. A parked entry whose `revisit` condition cannot be stated is not
parked; it is open work, and belongs in `BACKLOG.md`.

### Relations are bidirectional at matching strength

Every relation is written in both directions, each spelled at the strength its own direction claims:

| Forward, on the new entry | Mirror, on the older entry | Claims |
|---|---|---|
| `supersedes: [D077]` | `superseded_by: [D117]` | **Total.** The old decision no longer stands. |
| `revises: [D092]` | `revised_by: [D110]` | **Partial.** Part of the old decision moved; the rest still governs. |
| `extends: [D044]` | `extended_by: [D141]` | The old decision still stands and reaches further. |

- **Only `supersedes` changes the target's status.** A `supersedes` link flips the target to `superseded`; a
  `revises` or `extends` link leaves it `adopted`, because it still governs everything the new entry did not take.
- **A status must never contradict what a later entry says about it.** The failure this prevents is real: a
  single-file constraint sat `adopted` for months after the decision that replaced it, and the index rendered a
  dead constraint as live policy.
- **The back-link is what makes a partial revision findable.** Without `revised_by`, a reader who opens the old
  entry alone is never told part of it moved — they would have to grep the whole log for its number.
- **The date of a supersession is the superseding entry's `decided:` date.** Never restated anywhere, so it cannot
  disagree with itself.
- **One ADR, one settled question.** If a draft would need `revises` against half of itself, it is two ADRs. Split
  at drafting time, where it costs nothing.
- **Never split or rewrite an existing entry to separate its revised and unrevised parts.** That fabricates
  decisions nobody made, at dates nobody decided them, and breaks every citation of the original. The relation
  graph carries the narrowing; the entry keeps the value it was decided with.

A test asserts that every declared relation has its mirror, and that every `superseded_by` target reads
`superseded`.

### Rules that hold the log together

- **A superseded decision is never deleted or rewritten.** It keeps the value it was decided with and points
  forward. That is the entire reason the log is worth keeping. Any doc-constant consistency test exempts the
  decisions tree, **by directory anchored at the repo root**, not by a hand-listed set of filenames.
- **Cite by number and slug — `D169-lazy-display-fields`, never a bare `D169`** — in code comments, commit
  messages, other docs, and chat. The number is the address, the slug a mnemonic; `decisions/D169-*.md` resolves
  whichever few words an older citation picked. The filename *is* the slug declaration, so no entry carries a
  "cite as" line. New references use this form; retrofit an old bare citation only when already editing the line.
- **A citation of another repo's ADR carries that repo.** Write `../snowdrift/decisions/D202-…`, not
  `decisions/D202-…`. The moment a second repo grows its own `decisions/`, every bare citation silently
  re-resolves against the local log — where it finds the wrong entry or none, and a reader concludes the decision
  does not exist. The same applies to a ported decision: say what was ported, from where, and **which half was
  deliberately not ported**.
- **Filenames avoid `token`, `secret` and `password`.** An agent sandbox refuses to read a path carrying one of
  those stems, and the log exists to be read by the sessions it would lock out. Word the slug around them; the
  body keeps the words. A citation must move with the file, or a session builds the denied path and reads the
  refusal as "no such ADR".
- **The body carries the argument, not a template.** State what was decided, what it replaced, what was rejected
  and why, how it was verified, and what a plausible-looking regression would look like. Prose over headings.
- **Amendments live in the entry they amend**, as a dated section at the end of that file.
- **Record provenance in the argument, not just the field.** Where a decision came from a live run, a measurement,
  or a review finding, say so — "has this ever leaked, and how was it found?" is answerable only if it is written.
- **Name what verified it.** An entry claiming a behaviour names the test, spike or live run that measured it, and
  what the negative control was. A claim with no named evidence is a belief.
- **Record what a decision costs, measured.** Removing a guard, widening an allowlist, or accepting a disclosure
  states the size of what it opens — the number, not the adjective.

### Adding one

Take the next number, write the file, regenerate the index, commit the entry and the regenerated index **in the
same commit** as the code change it settles.

## Evidence: measure, do not reason

Where the platform's failure mode is a plausible-looking success rather than an error — HTTP 200 with the wrong
body, a test that passes while running boilerplate, a write captured into the wrong set — a reasoned claim is
worth nothing and the docs must not carry one.

- **A claim that matters gets a measurement**, written as a one-question script under `cli/spikes/` (or the repo's
  equivalent) that runs against a real instance and prints what it found. Spikes are measurement records, not
  tests. `make spikes` lists each one and the question it answers, derived from their docstrings.
- **Prefer a negative control** — a check that fails if the mechanism were broken — over a check that merely
  passes. State the control alongside the claim. A guard written for one instance of a bug rather than its class
  is a guard that passes while the bug is present.
- **Mutation-check a guard**: break the thing it protects, confirm it fails, revert. Record how many mutations were
  checked.
- **A first measurement can be wrong.** Where a probe was too weak and the corrected measurement contradicted it,
  record both — the wrong answer, confidently held, is the reusable lesson.
- **A verification record carries the evidence in a column.** Each claim gets its verifying spike, test count and
  live instance beside it, so a reader audits the evidence without leaving the row.
- **Keep a "what the measurements changed" section** listing the cases where a measurement contradicted what had
  already been reasoned about. It is the argument for measuring at all, and it is the section a new session reads
  to calibrate how much to trust its own reasoning about the platform.

## Removals are recorded with their guard

A feature removed on purpose is a fact the docs must keep, or it grows back. Record it in the entry that removed it
and cite the standing test by name: **"`push_scopes` was removed on 2026-08-23. Do not reintroduce it;
`cli/tests/test_contract.py` fails if it comes back."**

- The removal states **why it cost more than it caught**, what it was honestly defending against, what still
  stands in its place, and **what replaced it — including "nothing, deliberately."**
- A negative-control test replaces the tests that policed the removed behaviour, and fails if any of it returns.
- Where the removal leaves inert state behind on a live system, say so and say how to clear it.
- The reasoning is kept because it is the *why*; the *what* is gone from the tree and does not need describing.

## The index is generated, never hand-listed

`decisions/README.md` and `documentation/CODEMAP.md` are emitted by scripts (`decision_index.py`, `codemap.py`) run
via `make decisions` / `make codemap`. Nothing is hand-listed: an entry appears the moment its file is written,
not the day someone remembers to add it. **A stale index is worse than no index — a reader stops at it and never
opens the file that contradicts it.** `codemap.py`'s hand-maintained module order silently omitted five modules for
months; that is the failure being designed out.

- A test holds the committed index to exactly what the generator writes.
- The hand-maintained part of a generated file is its preamble — conventions, not content.
- A generator emitting into a directory that is not its own has two different meanings for a relative path: the
  path in its source and the path in its output. Hand-check the embedded see-also block after moving anything.

### Generated regions inside a hand-written doc

A doc can be part generated without being generated. Mark the region and splice into it:

```markdown
<!-- generated: verbs — do not edit between these markers; run `make agent-docs` -->
| Verb | What it does |
...
<!-- /generated: verbs -->
```

- **Generate a section only where the source is strictly richer than the prose.** A verb table derived from the
  command registry is richer. An annotated path-grammar block is not — generating it would *remove* the per-line
  annotations to gain freshness, so it stays hand-written and gets a contract test instead. This is the dividing
  rule; apply it per section, not per file.
- Everything outside the markers is prose and stays hand-written: the rules, the measured constraints, the outputs
  that read as success. Generating those produces the bland reference the file exists not to be.
- `make check` fails with a diff when a region is stale, and the build depends on that check. Editing between the
  markers loses the change on the next run — say so in the file.
- The trigger for building one: a list that already exists three times (dispatch table, `--help` prose, markdown
  table) and gets hand-edited three times in one session, each time only after a test failed.

### Contract tests make "keep the docs in sync" enforceable

Where a doc states a fact the code owns, a test asserts they agree: the CLI grows a verb the reference does not
describe, a tree goes unmentioned, a documented guard rule disappears, a thin wrapper grows into a second copy of
the reference it points at. "Keep X in sync" without a test is aspiration — and the drift it is meant to prevent
has usually already happened once, silently.

## Backlog

**One file, `documentation/BACKLOG.md`.** Its information content is the relative order of its items, which
splitting destroys and which a `priority:` field nobody maintains does not restore.

- Opens with one line stating what it is and who it is for, then the `**See also:**` block.
- Sectioned by kind — *Known limitations* (correct-but-incomplete, with the operational caveat spelled out),
  *Deferred*, *Back-burner proposals*.
- Each entry: **a bold one-line statement of what is open**, then the rationale, the concrete failure it produces,
  the fix not yet taken and why it was not taken, and its provenance — **Raised by <name>, <date>** or
  **Originator: AI**.
- **Name the file and line where the defect lives**, and what a fix would have to touch. An entry a reader cannot
  act on without re-deriving the investigation has thrown away the expensive half.
- **Say what is unmeasured.** Where the fix depends on a fact nobody has established, name the fact and the spike
  that would settle it, rather than designing on reasoning alone.
- An entry that becomes settled moves to `decisions/` and leaves the backlog, and the backlog row is replaced by a
  one-line pointer to the ADR where the framing and the gathered facts are worth keeping. An entry proven wrong is
  deleted.
- Work deliberately set aside with a stated revisit condition is a `parked` ADR, not a backlog item. Work with no
  statable revisit condition is a backlog item, not an ADR.

## Every doc's header

The first three elements of any doc in the set, in order:

1. `# TITLE` matching the filename.
2. One or two lines stating what the file holds and who it is written for — an LLM agent picking up the work, an
   operator, a new contributor. No preamble beyond that.
3. A `**See also:**` line naming the sibling docs and what each answers, so a reader who opened the wrong file
   leaves it in one hop. Markdown links resolve from the file that carries them; prose citations in code and
   Makefiles are repo-relative.

A citation carries a path only when its target moved. A bare `AGENTS.md` is a root filename that resolves from
anywhere; a bare `MASKING.md` names no file once it lives under `documentation/`.

## What `AGENTS.md` carries

`AGENTS.md` is the conventions file an agent reads before touching anything, with `CLAUDE.md` symlinked to it.
Beyond the doc map and the code conventions, three parts earn their place:

**Ground rules first, as absolutes.** Where an action is prohibited outright — writes against a client instance,
running the loop as an admin account — state it at the top, in the imperative, with no override, no flag and no
"but". Name where it is enforced in code and the test that fails if the enforcement is removed. A rule that only
lives in prose is advice; a rule with an allowlist in code and a test behind it is a rule. Where the guard is
deliberately asymmetric, say so and say why: *reads go wide, writes stay narrow, and that asymmetry is the
product — do not collapse them.*

**A naming table.** Term → what it means, for every word the project uses in a specific sense, and especially for
pairs that are routinely confused (an *alias* names a connection; a *connection* is the sealed whole it names —
they are not synonyms). **A deliberate divergence gets written down rather than silently fixed**: where a directory,
a package and the deployed thing carry three different names because renaming would mean a new record plus a
redeploy and a re-grant, record that. An undocumented mismatch is how two service accounts drift apart.

**Dated standing instructions.** A rule the author set carries who set it and when — *(standing instruction, Andy,
2026-08-04)*. A rule that was removed carries its date and its guard — *removed 2026-09-09; do not reintroduce,
`test_config.py` fails if it comes back.* Without the date, a later reader cannot tell a current instruction from
one that a since-changed fact made obsolete.

## Shipped docs and internal docs are different trees

Where a project ships documentation to a consumer — an agent reference, a skill, a pasteable `CLAUDE.md` block —
that material lives in its own directory (`agent-docs/`), separate from the internal docs that never leave the
repo (`docs/` or `documentation/`).

- **The split is a disclosure boundary.** An internal instance name, a credential, an engagement path or an
  internal route belongs in one tree and never in the other. Applying the rule per file is how it stays true.
- **One source, thin wrappers.** The vendor-neutral Markdown reference is the single source; harness-specific
  wrappers (a Claude skill, a Cursor rule) point at it and carry triggers, not content. Two copies of an
  operational reference drift, and the stale copy is the one that gets read.
- **Shipped docs ride inside the build artefact** so a consumer needs the binary and no checkout. Edit the source
  tree; the staged copy is regenerated every build and never committed.
- **Keep it in step with the tool in the same commit.** A feature that ships in the code and an ADR but not the
  shipped docs leaves a session teaching stale syntax. Stale shipped docs make agents act wrongly with confidence,
  which is worse than absent ones.
- Installation into a consumer repo previews every destination and applies **all or nothing**, stamping each file
  it wrote so a refresh replaces only what it created and left untouched, skips what was edited, and never adopts
  a file it did not create.

## Cited code you do not own

`reference/` holds code cited but not owned — vendor source a port is diffed against, extracts from another
project — kept **verbatim**. Never imported, never built, never shipped; the build does not touch it.

**Do not edit these files.** A cited file that has been improved can no longer settle an argument about what the
original does. Deltas go in the port or in a header comment. `reference/README.md` indexes what is there and why.

This is distinct from `resources/` (cached source documents — see the Reference Caching mechanism in
`~/.claude/CLAUDE.md`). Sibling checkouts are cited the same way: **cite, don't copy**, naming the path and what
it is the source of.

## Retired docs stay, bannered

A doc describing a retired approach keeps its place in the tree with a **HISTORICAL** or **SUPERSEDED** banner as
its first line, naming what replaced it and when. It records why the approach was retired, which is the part a
later session needs before proposing it again.

Banner only what is actually dead. A doc that reads like a historical assessment but is the live justification for
a current choice is **not** historical, and mislabelling it invites the very re-litigation the log exists to stop —
say explicitly in the surrounding index which of a group is which.

A design doc whose feature has shipped is not historical either: mark it **BUILT**, state that where it and the
code disagree the code is right, and keep it as the design record.

## Writing rules for all of them

- Declarative and terse. State what the thing does, not what it might or should do. No hedging.
- Plain technical English. Use the correct term where it is the accurate one, glossed in plain English on first
  use in a passage. No jargon overlay, no academic framing, no stacked metaphors.
- **Docs describe the system as delivered, not its history.** No "was X", "renamed from Y", "previously did Z".
  Rationale and superseded choices live in `decisions/`; that is what the log is for.
- Bold key terms on first use in a paragraph; backticks for identifiers. Tables for comparisons, bullets for
  sequences, prose for rationale and trade-offs.
- Line length 120, in docs and code alike. Do not reflex-wrap at 80.
- No filler openers, no summary or conclusion paragraph that recaps what precedes it.
- A rename is not a licence to reflow a file. Rewrap only the lines the change itself rewrote — and a line the
  rewrap produces inherits eligibility, or the fix stops one line short of where the problem moved. Verify a
  rewrap by comparing whitespace-normalised word sequences before and after, per file.

## Applying this to a repo

**New repo** — seed in this order: `README.md`, `AGENTS.md` (+ `CLAUDE.md` symlink), `decisions/` with the
`decisions/README.md` preamble copied from snowdrift and the domain list adapted, the index generator and its
`make` target, then `documentation/` files as the content earns them. Do not create empty placeholder docs.

**Existing repo** — audit, then adopt incrementally:

1. Map what exists against the artefact table. Report the gaps before writing anything.
2. Keep the repo's existing directory names and filenames. Adopt formats, not paths.
3. Backfill decisions only where the rationale is still known — from commit messages, session history, or the
   author. Do not invent an ADR's argument; an entry that records only the *what* is a worse artefact than no entry.
4. Convert a monolithic decision file to per-file ADRs mechanically, and verify by reversing the transformation:
   re-promote each file's headings and match every entry against the committed original. No entry missing, added,
   or altered.
5. Add the index generator and its test in the same commit as the split.
6. Where a doc has drifted from the code, fix the doc in the commit that noticed — a doc nobody trusts is
   overhead, not an artefact.
