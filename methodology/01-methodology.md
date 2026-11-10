---
type: how-to
title: "AI Kickstart — Methodology in 6 phases"
description: "From idea to a defined project: discovery with a questionnaire, architecture, epic map with feature sketch and screen inventory, prototype as contract, epics/features/stories in a single pass, and closing (QA, scaffold, index)"
tags: [ai-kickstart, methodology, phases]
timestamp: 2026-11-10T18:00:00Z
status: active
---

# Methodology in 6 phases

After each phase, a short summary of what was created. No phase is ever replaced by a summary.

**Where things live:** all project documentation goes **in the repo**, under `internal_docs/` ([02-templates](02-templates.md) §Structure), versioned with the code. Each person's personal notes (outside the repo) keep only what must not go into the repo: personal notes, loose ideas, to-dos, sensitive data.

**Language:** the project documentation uses the language chosen in question 0 of the questionnaire (English or Spanish). File names, endpoints, code and `CLAUDE.md` are always in English.

## Phase 1 — Discovery

- Read whatever exists (code, APIs, notes, earlier prototypes).
- Run the **questionnaire** in [06-questionnaire-and-stack](06-questionnaire-and-stack.md): language first, then vision, users, functional description, scope and non-goals, data, platform, deployment, stack and style. Only ask what the opening prompt does not answer, with options, in 2-3 rounds at most.
- Unless told otherwise, use the **default stack** in [06-questionnaire-and-stack](06-questionnaire-and-stack.md) (Angular + .NET with Vertical Slice + Postgres, on Docker); the database choice is always justified.
- Answers are later recorded as decisions `D#` with *Approved by {{person}}, {{date}}*. Anything left unanswered that does not block becomes an assumption `A#`.

## Phase 2 — Architecture (2 docs)

| Doc | Content |
|---|---|
| `Architecture/00-vision.md` | Problem, vision, users and expected volume, functional description, scope in/out and non-goals, principles, justified stack (and why that database) |
| `Architecture/01-architecture.md` | ASCII diagram, flows, data model, endpoints (table), backend slices, integrations, deployment and environment variables, technical decisions (table) |

## Phase 3 — Epic map, feature sketch and screen inventory

Just enough to commission the prototype and keep it from growing unchecked. **`EPIC.md`, `FEATURE.md` and stories are not written yet**: they are written once, in phase 5, with the prototype approved.

- `Epics/00-epic-map.md` ([02-templates](02-templates.md) §Epic map): for each epic, **one paragraph** (problem, value, what is in) and a **sketch of its features** (name, one line and the screens it touches). Order, dependencies and ASCII roadmap.
- `Epics/00-screen-inventory.md`: `screen-id` → feature → states → data shown. **This is the prototype's brief.**
- Typical order: foundation → core → features → deployment and polish.

## Phase 4 — Prototype (hard gate)

`Design/prototype.html` is the **visual contract**: the app has the same structure, copy and states. A visual change goes to the prototype first (with approval) and then to the app. It stays `proposed` until the user approves it.

Requirements:
- One `<section id="screen-{id}">` per screen in the inventory; navigable via `#screen-{id}`.
- States addressable by query: `?state=empty|loading|error` (deterministic, no interaction).
- `?bare` hides the prototype's demo bar.
- `data-testid` on every meaningful element (titles, lists, rows, buttons, state messages), following `{screen}-{element}`.
- Realistic, fixed and **made-up** data (never real people's data): the same as the E2E fixtures.
- Tokens as CSS variables in `:root`; AA contrast.
- Build it in parts: skeleton with all screens → one screen per edit → navigation and state JS.

If a new screen or feature shows up while prototyping, update the inventory and the map (cheap: they only hold paragraphs and sketches).

Check (run and show):
```bash
ls -l internal_docs/Design/prototype.html
grep -o 'id="screen-[^"]*"' internal_docs/Design/prototype.html | sort -u    # = inventory
```

## Phase 5 — Epics, features and stories (single pass, looking at the prototype)

With the prototype approved, write everything at once from the map and the prototype ([02-templates](02-templates.md)):

- One `EPIC.md` per epic (decisions D#, assumptions A#, risks R#, questions Q#, story table and dependencies) and one `FEATURE.md` per feature.
- One story per file: its criteria quote the screen's copy, states and data.
- Every story with UI lists its `#screen-{id}` (which exist); stories without UI say `No UI`.
- Every prototype screen is referenced by at least one story.
- If a story needs something the prototype lacks: **prototype first**.
- Dependencies between stories are explicit: the parallel wave plan comes from them ([03-execution](03-execution.md) §3).

Check (run and show): prototype screens vs screens referenced by stories.
```bash
grep -o 'id="screen-[^"]*"' internal_docs/Design/prototype.html | sed 's/id="//;s/"//' | sort -u
grep -rhoE 'screen-[a-z0-9-]+' internal_docs/Epics/ | sort -u
```

## Phase 6 — Closing: QA, scaffold and index

1. `QA/00-qa.md`: test pyramid (what each layer tests and what it doesn't), gates with command and pass criterion, medium parity ([03-execution](03-execution.md) §5), test data, security ([03-execution](03-execution.md) §7).
2. Repo: `CLAUDE.md` ([05-claude-md-template](05-claude-md-template.md)), folder structure, `docker-compose.yml`, `.env.example`, configs, **pre-commit hook with gitleaks** and `.gitignore` with `.env`. **No stories implemented.**
3. `internal_docs/README.md`: project index (links, epic table with verified story counts, roadmap, open questions). In personal notes, only a short note linking to the repo.
4. Consistency check (short list):
   - [ ] Stories per epic = index table = epic map.
   - [ ] Prototype screens = screens referenced by stories.
   - [ ] Every internal link points to a file that exists (relative markdown links, no wikilinks).
   - [ ] Frontmatter (`type`, `title`, `description`, `tags`, `timestamp`, `status`) on every note.
   - [ ] Every decision has *Approved by* or is `proposed`.
   - [ ] Every story depending on an open `Q#` has an `A#`.
   - [ ] Nothing sensitive in `internal_docs/` (private domains, IPs, real emails or names, credentials): run `check-sensitive` before the first push.
5. Hand over the launch prompt ([04-prompts](04-prompts.md) §2) already filled in.
