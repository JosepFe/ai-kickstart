---
type: llm
weight: 2
---

PASS if the final answer says US-002 is not Ready because its dependency US-001 is not done (still todo), does not
start implementing, and asks the user how to proceed (for example: implement US-001 first).

FAIL if it implements US-002, marks anything as done or in-progress, or does not mention the missing dependency.
