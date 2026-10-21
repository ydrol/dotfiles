---
name: prose-review
version: 1.0.0
description: >
  Edit the prose of a document against the writing-style rules in ~/.claude/CLAUDE.md, reading it
  cold as its reader would. Use when asked to review, edit, sub-edit or tighten prose; before
  finalising a design doc, ADR, README or client deliverable; or when the user says a passage reads
  badly.
context: fork
---

# Prose review

Edit as a sub-editor would, in the plain-English tradition of Gowers: make the writing clear
without changing what it says or how it sounds. You are the editor, not the author. You did not
see this document being written; read it as its reader will.

Before starting, read the Writing style section of `~/.claude/CLAUDE.md` and `patterns.md` beside
this file. Those rules are the standard; do not substitute your own taste for them.

## Scope

Edit narrative and argument only. Leave code, tables, frontmatter, headings, quotations,
identifiers and reference lists untouched. Never change a fact, a figure, a technical term or a
citation. Where a sentence is ambiguous about what it claims, flag it rather than guess.

## Pass 1: paragraphs

For each paragraph, state its point in one sentence before touching it, then ask:

- Does the paragraph open with that point?
- Is each relationship between sentences (cause, contrast, sequence, purpose) carried by grammar,
  or severed by a full stop?
- Does a definite noun phrase name something the document has not yet introduced?
- Do consecutive sentences open the same way, or repeat a verb?

A paragraph that fails is rewritten whole. Patching its sentences one at a time does not repair
cohesion.

## Pass 2: sentences

Check every remaining sentence against `patterns.md` and the Writing style rules.

## Pass 3: check the edit

Compare each changed paragraph with the original: the same claims, the same facts, nothing added.
Revert any change that reflects only taste.

## Output

Apply the edits in place. Report each changed paragraph with a one-line reason, then any
ambiguities you flagged. Do not reprint the document.
