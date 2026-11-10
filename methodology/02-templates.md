---
type: reference
title: "AI Kickstart — Templates"
description: "internal_docs structure in the repo and personal notes outside it, templates for the epic map, EPIC.md, FEATURE.md, US-NNN.md and screen inventory, story and epic Definition of Ready/Done, and slicing rules (SPIDR, INVEST)"
tags: [ai-kickstart, template, epic, user-story, dor, dod]
timestamp: 2026-11-10T18:00:00Z
status: active
---

# Templates

Headings below are in English; in a Spanish project, translate them (the structure stays the same).

## Structure

### In the repo (everything needed to work from any machine)

```
<repo>/
  CLAUDE.md
  .claude/                               (only repo-specific additions: the agent and skills come with the plugin)
  .githooks/pre-commit                   (gitleaks)
  internal_docs/
    README.md                            index: links, epic table, roadmap, open questions
    Architecture/  00-vision.md  01-architecture.md
    Design/        prototype.html  README.md (tokens, parity matrix)
    Epics/         00-epic-map.md  00-screen-inventory.md
                   E01-<name>/EPIC.md
                   E01-<name>/F01-<name>/FEATURE.md  US-001.md ...
    QA/            00-qa.md  security/YYYY-MM-DD-security-audit.md
```

- **Relative markdown links** (`[EPIC](../E01-x/EPIC.md)`), no wikilinks: they work on GitHub, in the editor and in Obsidian (opening `internal_docs/` as a vault).
- Git keeps the history: no `_archive-v1/` folders in the repo.
- Story numbering is **continuous per epic** (`E03/US-004`), not per feature.
- Documents in the language chosen at kickoff (English or Spanish, questionnaire question 0); file names, endpoints, code and `CLAUDE.md` in English.

### Personal notes (what does not go into the repo)

In your own notes system (Obsidian, Notion, a folder…), outside the repo:

```
<Project>/
  Index          what it is, link to the repo and to internal_docs/README.md, one-line status
  To-do          where the work was left
  Notes/         ideas, personal notes, private context (servers, accounts, people)
```

Rule: if something should not be visible on GitHub even in a private repo, it goes into personal notes; if it is needed to implement, it goes into the repo **without the sensitive value** (e.g. "the public domain, in the `PUBLIC_URL` variable").

## Epic map (phase 3)

```markdown
---
type: reference
title: "<Project> — Epic map"
description: "<n> epics, their order and dependencies"
tags: [<project>, epics, roadmap]
timestamp: <ISO>
status: draft
---
# Epic map

## E01 — <name>
<Paragraph: problem it solves, value and what is in. 3-5 sentences.>

| Feature | What it does (one line) | Screens |
|---|---|---|
| F01 — <name> | … | `screen-…`, `screen-…` · or No UI |

## E02 — …

## Order and dependencies
| Epic | Depends on | Phase |
(ASCII roadmap)
```

In phase 5 the map is completed with the number of stories per epic.

## EPIC.md (phase 5)

```markdown
---
type: epic
title: "E0N — <name>"
description: "<one line>"
tags: [<project>, epic, e0n]
timestamp: <ISO>
status: draft | ready | in-progress | done
---
# E0N — <name>

## Problem and value
## Epic acceptance criteria   (observable, 3-6)
## Decisions
| ID | Decision | Why | Deferred | Approved by |
## Assumptions      | ID | Assumption | If it does not hold |
## Risks            | ID | Risk | Mitigation |
## Open questions   | ID | Question | Owner | Assumption meanwhile |
## Stories          | US | Title | Feature | Size | Depends on | Status |
## Dependencies     (ASCII: US-001 ──▶ US-003 ──▶ US-005)
```

A decision the user has not stated stays **`proposed`**: never "approved by the user" on their behalf.

## FEATURE.md

Visible capability, non-functional requirements (performance, security, accessibility) and a table of its stories.

## US-NNN.md

```markdown
---
type: user-story
title: "E0N/US-NNN — <title>"
description: "<one line>"
tags: [<project>, user-story, e0n]
timestamp: <ISO>
status: todo | in-progress | done | deferred
---
# US-NNN — <title>

Size: S | M | L    Priority: High | Medium | Low    Depends on: US-xxx | none

## Value
**As** <persona> **I want** <action> **so that** <benefit>.

## Acceptance criteria
- **Given** … **when** … **then** …   (3-5, each with its test)

## Screens
`#screen-<id>` (+ states) — or `No UI`. Criteria quote the prototype's copy and data.

## Technical notes
Hints, not orders: slice/endpoints, tables, components, links to architecture.
Shared files it touches (migrations, routes, service registration): matters for parallel work.

## Tests
| Level | File | Criterion |

## Out of scope
```

Sizes: **S** 15-30 min · **M** 30-60 min · **L** 1-2 h. Bigger, or more than 5 criteria: slice it before planning.

## Screen inventory

| screen-id | Feature | States | Data shown | Stories |
|---|---|---|---|---|

## Slicing (SPIDR)

**S**pike (unknown → time-box) · **P**aths (paths with their own value) · **I**nterfaces (API and UI separately) · **D**ata (fewer fields first) · **R**ules (one rule at a time). Vertical first; foundations (workspace, E2E, parity, deployment) are stories of their own.

## Definition of Ready (story)

1. Value, 3-5 criteria, notes, tests and out of scope written.
2. Size S/M/L; dependencies done or mockable.
3. Open questions answered or covered by an `A#`.
4. With UI: screens exist in the prototype, with their row in the parity matrix and planned `data-testid`s.

## Definition of Done (story)

1. Every criterion proven by a named test.
2. Applicable gates green; those that could not run, `NOT RUN` with the reason.
3. With UI: its screen's parity test passes.
4. Touched docs (`internal_docs/`) updated **in the same commit**; story status and EPIC table updated.
5. Local commit with the gitleaks hook green.
6. Report delivered ([03-execution](03-execution.md) §8).

## Definition of Done (epic)

1. Every story `done`, or `deferred` with explicit approval.
2. **Full gates** green after integrating the last wave (unit, integration, build, E2E, parity of every screen in the epic, docker build); `NOT RUN` with reason.
3. **Dependencies** with no high or critical vulnerabilities (`npm audit`, `dotnet list package --vulnerable --include-transitive`), or accepted in writing as a `D#`.
4. **Migrations** reviewed: they apply from scratch and over the previous version; with real data, a rollback plan.
5. **`check-sensitive`** clean before the push.
6. If the epic leaves the app ready to deploy (or is the last one): **`security-audit`** done (`quick` or `standard` profile, [03-execution](03-execution.md) §7), summary in `internal_docs/QA/security/` and no open critical or high findings.
7. **Operations** (if deployed): environment variables in `.env.example` and in the architecture, healthcheck, database backups and, on a self-hosted server, its setup there (proxy, domains, backups, monitoring).
8. Docs up to date: `internal_docs/README.md`, epic map, EPIC and the epic's final report.
