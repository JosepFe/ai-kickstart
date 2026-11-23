---
type: llm
weight: 2
---

PASS if the final answer asks the user questions from the kickoff questionnaire before designing anything: it asks
which language the documents should be in (English or Spanish) or makes clear that language comes first, and offers
options for the questions it asks. Asking only part of the questionnaire in this first round is fine.

FAIL if it already proposes an architecture, a stack decision, an epic map, stories or a prototype as if decided, or
says it has created files or a repository.
