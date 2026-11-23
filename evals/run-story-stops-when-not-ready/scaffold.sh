#!/usr/bin/env bash
# An epic where US-002 depends on US-001, which is still todo: US-002 is not Ready.
set -euo pipefail
d=internal_docs/Epics/E01-auth/F01-login
mkdir -p "$d"
cat > CLAUDE.md <<'MD'
# Demo
Methodology: AI Kickstart plugin. Story loop: READ → IMPLEMENT → TEST AUDIT → GATES → REPORT → COMMIT.
MD
cat > internal_docs/Epics/E01-auth/EPIC.md <<'MD'
---
type: epic
title: "E01 — Auth"
status: ready
---
# E01 — Auth
## Stories
| US | Title | Feature | Size | Depends on | Status |
|---|---|---|---|---|---|
| US-001 | Sign in with email link | F01 | M | none | todo |
| US-002 | Sign out | F01 | S | US-001 | todo |
MD
cat > "$d/FEATURE.md" <<'MD'
---
type: feature
title: "E01/F01 — Login"
status: ready
---
## Acceptance criteria
| ID | Criterion | Covered by |
|---|---|---|
| C1 | The user signs in with a link sent by email | US-001 |
| C2 | The user signs out and the session is gone | US-002 |
## Stories
| US | Title | Covers | Size | Depends on | Status |
|---|---|---|---|---|---|
| US-001 | Sign in with email link | C1 | M | none | todo |
| US-002 | Sign out | C2 | S | US-001 | todo |
MD
for n in 001 002; do
  dep=none; [ "$n" = 002 ] && dep=US-001
  cat > "$d/US-$n.md" <<MD
---
type: user-story
title: "E01/US-$n"
status: todo
---
# US-$n
Size: S    Priority: High    Depends on: $dep
## Value
**As** a user **I want** this **so that** it works.
## Acceptance criteria
- **Given** a session **when** I act **then** it happens.
## Screens
No UI
## Out of scope
MD
done
