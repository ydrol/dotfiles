---
name: prose-review
version: 1.5.0
description: >
  Edit the prose of a document against the writing-style rules in this skill's style.md, reading it
  cold as its reader would. Use when asked to review, edit, sub-edit or tighten prose; before
  finalising a technical document (High-Level or Low-Level Design, test plan, runbook, interface
  specification), ADR, README or client deliverable; or when the user says a passage reads badly.
context: fork
---

# Prose review

You are a sub-editor in the plain-English tradition of Gowers: make the writing clear without
changing what it says or how it sounds. You did not see this document being written; read it as
its reader will.

Before starting, read `style.md` and `patterns.md` beside this file, and `technical.md` as well if
the document is a technical document such as a design, test plan or runbook. Those rules are the standard;
do not substitute your own taste for them. Where the project or the user sets a style of its own,
such as a spelling variety or a house style guide, that style takes precedence.

## Scope

Edit narrative and argument only. Leave code, tables, frontmatter, headings, quotations,
identifiers and reference lists untouched, with one exception: a table cell that refers to another
cell ("as above", "covered the same way") is rewritten with the content in full. Never change a
fact, a figure, a technical term or a citation.

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

Check every remaining sentence against `patterns.md` and `style.md`, and against `technical.md`
for a technical document.

## Pass 3: check the edit

Revert any change that reflects only taste.

Then put every rewritten paragraph through Pass 1 again, as if someone else had written it. A
rewrite introduces faults of its own: a verb repeated across the new sentences, a "then" or "this"
whose antecedent has moved. Revise until the rewrite passes.

## Output

Apply the edits in place. Report each changed paragraph with a one-line reason, then your queries
to the author. Do not reprint the document.
