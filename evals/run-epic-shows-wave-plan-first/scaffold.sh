#!/usr/bin/env bash
# Three stories: US-001 and US-002 (M, independent), US-003 (S) depends on both.
set -euo pipefail
d=internal_docs/Epics/E01-lists/F01-lists
mkdir -p "$d"
printf '# Demo\nMethodology: AI Kickstart plugin.\n' > CLAUDE.md
cat > internal_docs/Epics/E01-lists/EPIC.md <<'MD'
---
type: epic
title: "E01 — Lists"
status: ready
---
# E01 — Lists
## Stories
| US | Title | Feature | Size | Depends on | Status |
|---|---|---|---|---|---|
| US-001 | Create a list (API) | F01 | M | none | todo |
| US-002 | Lists screen (UI with mocked API) | F01 | M | none | todo |
| US-003 | Connect the screen to the API | F01 | S | US-001, US-002 | todo |
## Dependencies
US-001 ──▶ US-003 ◀── US-002
MD
for x in "001:M:none" "002:M:none" "003:S:US-001, US-002"; do
  IFS=: read n size dep <<<"$x"
  cat > "$d/US-$n.md" <<MD
---
type: user-story
title: "E01/US-$n"
status: todo
---
# US-$n
Size: $size    Priority: High    Depends on: $dep
## Acceptance criteria
- **Given** a user **when** they act **then** it works.
## Technical notes
Shared files it touches: none.
MD
done
