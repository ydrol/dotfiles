# Writing style

These rules govern narrative and argument wherever they appear: chat, the prose sections of documents, commit
messages, client deliverables. Structured reference material is exempt and should stay structured. A High-Level
Design also follows the register in `hld.md`, beside this file.

- **BLUF is structural, not syntactic.** BLUF (bottom line up front) governs the order of information: lead with the
  conclusion. It does not mean compressed sentence construction. Write in connected, flowing paragraphs, not clipped,
  minute-taking style.
- **Concision is a property of the response, not the sentence.** Cut whole paragraphs that do not earn their place; do
  not buy brevity by stripping the words that hold a sentence together. Flowing prose is not a licence to pad.
- **Protect connective tissue.** Do not strip function words ("that", "which", "who is") for density. Name the actor:
  prefer the active voice, and where a passive or reduced clause is used, say who performs the action.
- **Vary the mechanics.** Vary sentence length deliberately. Avoid consecutive sentences opening with the same
  subject-verb pattern unless the repetition is deliberate.
- **Cohesion through grammar, not adverbs.** Connect related statements with subordinate clauses and conjunctions
  rather than stacking short sentences glued together with "However" or "Notably". Do not use a definite noun phrase
  ("the codes", "the room") for something not yet introduced.
- **Bullet discipline.** Bullets are for parallel items a reader will scan or look up: options, checks, inventories,
  cases. They are not for reasoning. Where the connection between two statements is the point, whether cause,
  exception, dependency or sequence, grammar has to carry it, and a bullet severs it. The rule applies by passage, not
  by document. A reference table belongs in a client report, and an argument broken into six bullets is wrong in a
  design doc.
- **Register.** Maintain a formal professional tone. Flowing prose does not mean conversational prose.
- **Endings still land.** Stopping once the information is delivered means adding no summary and no wrap-up, not
  ending mid-cadence.
- **No bare demonstratives in documents.** In a generated document, "this", "that", "these" and "those" never stand
  alone as a pronoun ("This means…", "That is set by…"). Follow each with a noun that names its referent ("this
  field", "that rule"), as long as the noun is brief. Where the referent's full name is long and recurs, introduce a
  short form with its first full use, such as "the order automation rule (the rule)", and use the short form from
  then on. A reader or an AI that meets the passage out of context, from a search hit, a diagram or a retrieved chunk,
  can still resolve the reference.
- **No undefined abbreviations.** Use an acronym or abbreviation only if it is well known outside the project (REST,
  JSON, API, URL, CMDB, ETL) or the project's glossary defines it. Otherwise write the term out every time, or write it
  out on first use and then use the glossary spelling. Vendor jargon from a stack the reader does not work in is
  mental load on top of the work, and each undefined acronym costs a lookup. If a term keeps recurring, propose a
  glossary entry rather than abbreviating it.
- **"Currently", not "today".** Where a sentence describes the present state of a system, product or process, write
  "currently" or "at present" rather than "today". Keep "today" where it means the calendar day.
- **Negate the verb, not the object.** Write "x does not extend any y", not "x extends no y"; "the table has no index"
  reads naturally, but "the rule matches no records" should be "the rule does not match any records". The
  object-negated form is terse and formal, and the reader has to reach the end of the clause before learning that it
  is a negative.
- **Plain words, after Gowers.** Choose the short, familiar word that says exactly what is meant, and the verb over the
  noun made from it. Write "decide", not "make a decision"; "check", not "carry out a check"; "to", not "in order to";
  "before" and "after", not "prior to" and "subsequent to"; "use", "help" and "start", not "utilise", "facilitate" and
  "commence"; "if", not "in the event that"; "about" or "for", not "with regard to" or "in respect of"; "some", not "a
  number of". Cut "the fact that" by recasting the sentence. Say a thing once, in the concrete term, rather than
  qualifying it into vagueness. A standard term of the domain, such as a platform's own name for a record or a
  feature, is the plain word for its reader and is never paraphrased away.
- **One term per thing.** Define each component or concept once and use exactly the same term for it every time
  afterwards. Vary the sentence, never the noun: a reader assumes that a different word names a different thing.
- **No promotional language.** Do not use untestable words such as "robust", "seamless", "best-in-class" or
  "cutting-edge". Replace each with the specific property it implies, such as a retry policy, a polling interval or a
  measured limit, and delete it if there is no such property. Write "use", not "leverage".
- **British spelling.** Use British spelling, with -ise endings, unless a house style says otherwise, and keep
  spelling consistent throughout a document.
