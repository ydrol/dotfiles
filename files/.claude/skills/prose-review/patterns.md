# Patterns

Each entry pairs a failure with its repair. Add new entries as they are spotted.

## Sentences

| Failure | Repair |
|---|---|
| the source Fred supplies | the source that Fred supplies; the source supplied by Fred |
| records the job skipped | records that the job skipped |
| a field the form hides | a field that the form hides |
| x extends no y | x does not extend any y |
| the rule matches no records | the rule does not match any records |
| today, the integration polls hourly | currently, the integration polls hourly |
| each response, both from order placement and from every poll | each response, whether to the original order or to a later poll |
| Staging tables hold each response … Staging lets the control compare it | Staging tables hold each response … Keeping the response there lets the control compare it |
| a robust, seamless integration | an integration that retries failed requests three times with exponential back-off |
| the job leverages the API | the job uses the API |
| the build adds the following tables | the application contains the following tables |
| this section describes the retry policy | (state the retry policy) |
| (table cell) Custom table, covered the same way | (table cell) Custom table; covered by the bundled custom table allowance |
| (table cell) As above | (table cell) the full content of the cell above, repeated |

Object negation stays where it is idiomatic, with "have" and "be": "the table has no index" is
correct. "Today" stays where it means the calendar day. A noun that has named a thing must not
then name an activity: once "staging" means the tables, "staging lets…" makes the reader switch.

## Paragraphs

### Severed sentences, repeated openings, buried point

Before:

> Staging tables hold each supplier response, both from order placement and from every poll. The
> integration then applies each staged response to the supplier order and the request. Staging
> lets the single-fire control compare a response with the response last seen, and it lets the
> exchange be audited (§ 9.3). The staging tables are separate from the supplier order. They hold
> what the supplier returned, briefly, while the supplier order holds the lasting record.

After:

> Every supplier response, whether to the original order or to a later poll, lands first in a
> staging table, and the integration then applies it to the supplier order and the request. The
> staging tables keep each response only briefly; they are deliberately separate from the supplier
> order, which holds the lasting record. Keeping each raw response lets the single-fire control
> compare it with the previous one, and it gives auditors a record of the whole exchange with the
> supplier (§ 9.3).

Six short sentences carried three ideas with no grammar linking them; "hold" appeared three times;
"staging" switched from table to activity; "lets the exchange be audited" hid the actor.
