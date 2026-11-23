---
type: llm
weight: 2
---

PASS if the final answer shows a wave plan (a table or equivalent list) where US-001 and US-002 go together in the
first wave and US-003 goes in a later wave because it depends on both, and it asks the user to approve the plan before
implementing.

FAIL if it starts implementing or launching agents, puts US-003 in the first wave, or does not ask for approval.
