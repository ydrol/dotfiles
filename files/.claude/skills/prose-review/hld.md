# High-Level Design register

A High-Level Design (HLD) describes a system as designed, for an engineer who will review, approve or build from it.
Write it in the voice of one engineer explaining a design to a peer: formal, technical and plain. The rules in
`style.md` apply in full; the rules below add to them for an HLD and take precedence where they are more specific.

- **Present tense for the design.** Describe the design as it stands: "The integration polls the queue every five
  minutes", not "will poll". An HLD describes the system as designed, so the future tense belongs only to genuinely
  later phases and roadmap items.
- **The component is the subject.** Write active sentences with the component as their subject ("The MID Server
  forwards the payload"), so that the reviewer can see which component owns every action. Use the passive only where
  the actor is unknown or irrelevant.
- **Third person, except for decisions.** Describe the system in the third person. Use "we" only in a rationale
  section, where it explains a design decision, because decisions have authors and components do not.
- **Must, should, may; never shall.** Use "must" for a mandatory requirement, "should" for recommended practice and
  "may" for a permitted option, and state that convention once near the start of the document. Do not use "shall".
- **State settled design plainly.** Do not hedge the main prose. Assumptions, open questions, risks and dependencies
  each go in a clearly labelled section of their own, which leaves the design itself free of qualification.
- **Structure follows the content.** Component descriptions, interfaces and non-functional requirements are reference
  material, so keep them concise and use tables and lists. Rationale and trade-off sections are argument, so write
  them as connected prose; the bullet discipline in `style.md` applies there with full force.

## Example

Avoid:

> A robust, seamless integration will be leveraged to ensure data is synchronised.

Prefer:

> The integration retrieves changed records from the source API every 15 minutes and retries failed requests three
> times with exponential back-off.

The rewrite replaces "robust" and "seamless" with the properties they implied, a polling interval and a retry policy;
it makes the integration the subject of an active sentence, and it states the design in the present tense.
