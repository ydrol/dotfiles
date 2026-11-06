# Technical document register

These rules govern every technical document delivered on an engagement: a High-Level Design (HLD), a Low-Level Design
(LLD), a test plan, an interface specification, a runbook, a deployment guide and any document like them. Each one
describes a system, or how to build, test or operate it, for an engineer who will review, approve, build from or act
on it. The Microsoft Writing Style Guide and the rules in `style.md` apply in full; the rules below add to them for a
technical document.

- **A real actor is the subject.** In a design the actor is a component ("The MID Server forwards the payload"); in a
  test plan or runbook it is a component, a role or the person following the steps. Do not invent an actor to avoid
  the passive. A build, a release, the design, the solution or the document does not perform anything, so "The build
  adds the following tables" should be "The application contains the following tables". Where there is no real
  actor, describe the resulting state, or use the passive if the actor is unknown or irrelevant.
- **Must, should, may; never shall.** Use "must" for a mandatory requirement, "should" for recommended practice and
  "may" for a permitted option, and state that convention once near the start of the document. Do not use "shall".
- **Testable statements.** Write each requirement, acceptance criterion and expected result as an outcome that
  someone can observe and check: a value, a state, a count, a time limit or a message. "The request reaches the
  Closed Complete state within 15 minutes" is testable; "the request is processed correctly" is not.
- **State settled content plainly.** Do not hedge the main prose. Assumptions, open questions, risks and dependencies
  each go in a clearly labelled section of their own, which leaves the design, the procedure or the test free of
  qualification.
- **Structure follows the content.** Component descriptions, interfaces, non-functional requirements and test cases
  are reference material, so keep them concise and use tables and lists. Rationale, trade-off and approach sections
  are argument, so write them as connected prose.

## Example

Avoid:

> A robust, seamless integration will be leveraged to ensure data is synchronised.

Prefer:

> The integration retrieves changed records from the source API every 15 minutes and retries failed requests three
> times with exponential back-off.

The rewrite replaces "robust" and "seamless" with the properties they implied, a polling interval and a retry policy;
it makes the integration the subject of an active sentence, and it states the design in the present tense.
