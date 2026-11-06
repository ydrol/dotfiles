# Writing style

Follow the [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/) with British
spelling: -ise endings, "colour", "behaviour", "programme" for a plan of work, and spelling kept consistent throughout
a document. Where a project or client sets a house style of its own, that style takes precedence.

The rules below cover ground that the Microsoft guide does not. They apply to narrative and argument wherever they
appear: chat, the prose sections of documents, commit messages and client deliverables. Structured reference material
is exempt, except that the rule on table cells applies to it. A technical document, such as a design, test plan or
runbook, also follows `technical.md`, beside this file.

- **Protect connective tissue.** Do not strip function words ("that", "which", "who is") for density. Where a passive
  or reduced clause is used, say who performs the action. The actor must be real: do not make a build, a document or
  "the solution" the subject of an action it does not perform.
- **Vary the mechanics.** Vary sentence length deliberately. Avoid consecutive sentences opening with the same
  subject-verb pattern unless the repetition is deliberate.
- **Cohesion through grammar, not adverbs.** Connect related statements with subordinate clauses and conjunctions
  rather than stacking short sentences glued together with "However" or "Notably". Do not use a definite noun phrase
  ("the codes", "the room") for something not yet introduced.
- **Bullets are not for reasoning.** Where the connection between two statements is the point, whether cause,
  exception, dependency or sequence, grammar has to carry it, and a bullet severs it. The rule applies by passage, not
  by document: a reference table belongs in a client report, and an argument broken into six bullets is wrong in a
  design doc.
- **Endings still land.** Stopping once the information is delivered means adding no summary and no wrap-up, not
  ending mid-cadence.
- **No bare demonstratives in documents.** In a generated document, "this", "that", "these" and "those" never stand
  alone as a pronoun ("This means…", "That is set by…"). Follow each with a noun that names its referent ("this
  field", "that rule"), as long as the noun is brief. Where the referent's full name is long and recurs, introduce a
  short form with its first full use, such as "the order automation rule (the rule)", and use the short form from
  then on. A reader or an AI that meets the passage out of context, from a search hit, a diagram or a retrieved chunk,
  can still resolve the reference.
- **Glossary for recurring terms.** An abbreviation that is not well known outside the project is usable only if the
  project's glossary defines it. If a term keeps recurring, propose a glossary entry rather than abbreviating it.
- **"Currently", not "today".** Where a sentence describes the present state of a system, product or process, write
  "currently" or "at present" rather than "today". Keep "today" where it means the calendar day.
- **Negate the verb, not the object.** Write "x does not extend any y", not "x extends no y"; "the table has no index"
  reads naturally, but "the rule matches no records" should be "the rule does not match any records". The
  object-negated form is terse, and the reader has to reach the end of the clause before learning that it is a
  negative.
- **Replace promotional words with properties.** Replace an untestable word such as "robust", "seamless" or
  "best-in-class" with the specific property it implies, such as a retry policy, a polling interval or a measured
  limit, and delete it if there is no such property.
- **Table cells stand alone.** Every cell must make sense to a reader who sees only its row, so repeat the full content
  rather than writing "as above", "same as above", "covered the same way" or "ditto". Readers scan a table by row, sort
  and filter it, and an AI may retrieve a single row; a back-reference fails in each case. If the repetition makes a
  column heavy, move the shared part into the column heading or a note under the table, and keep each cell complete.
  Identical cells down a column are not a fault: they show that the rows are the same.
