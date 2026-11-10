---
type: index
title: "AI Kickstart"
description: "Methodology to define and build projects with Claude Code: questionnaire and default stack, prototype as contract, stories bound to the prototype, docs in the repo (internal_docs), story-by-story or parallel-wave execution and security before deploying"
tags: [ai-kickstart, methodology, template, claude-code]
timestamp: 2026-11-10T18:00:00Z
status: active
---

# AI Kickstart — Methodology

| What it does | How it stays light |
|---|---|
| HTML prototype as the **visual contract** (before the stories) | Architecture: 2 docs |
| EPIC with decisions D#, assumptions A#, risks R#, questions Q# | QA: 1 doc |
| Epics, features and stories written **once**, after the prototype | Before the prototype, only a map (paragraph + feature sketch) and the screen inventory |
| One story per file, Given/When/Then, bound to its `#screen-` | Parity: E2E on **structure and copy** (no pixels) |
| Short DoR / DoD (story and epic), SPIDR for slicing | Consistency: a short checklist |
| 1 story = 1 iteration = 1 local commit, honest gates (`NOT RUN`) | Agents: `qa-reviewer` and, when it pays off, parallel implementers in waves |
| Project docs **in the repo** (`internal_docs/`) | Anything personal or sensitive stays outside the repo |
| Security: gitleaks on every commit, `check-sensitive` before pushing, `security-audit` before deploying | Default stack: Angular + .NET (Vertical Slice) + Postgres on Docker |
| Stop and ask before cutting scope | No separate ADRs: they live in the decisions table |

## Flow

1. **Define**: `new-project` skill (or the prompt in [04-prompts](04-prompts.md) §1). Claude runs the 6 phases of [01-methodology](01-methodology.md): discovery with questionnaire → architecture → epic map and screen inventory → **prototype** → epics, features and stories → QA, scaffold and index.
2. **Build**: `run-story` (one story) or `run-epic` (one epic, in series or in parallel waves), or the prompt in [04-prompts](04-prompts.md) §2. Rules in [03-execution](03-execution.md).
3. **Push**: `check-sensitive` before every push.
4. **Deploy**: epic DoD ([02-templates](02-templates.md)) and `security-audit`.

For an existing app: `review-app` skill.

## Notes

| Note | Content |
|---|---|
| [01-methodology](01-methodology.md) | The 6 phases, what each produces and its check |
| [02-templates](02-templates.md) | Repo / personal-notes structure, epic map, EPIC.md, FEATURE.md, US-NNN.md, inventory, story and epic DoR/DoD, SPIDR |
| [03-execution](03-execution.md) | Story loop, parallel waves, two-level gates, medium parity, security, when to stop, report, git |
| [04-prompts](04-prompts.md) | Kickoff prompt and epic launch prompt |
| [05-claude-md-template](05-claude-md-template.md) | Repo CLAUDE.md, `qa-reviewer` agent, `run-story` and `run-epic` skills, gitleaks hook |
| [06-questionnaire-and-stack](06-questionnaire-and-stack.md) | Phase 1 questions and default stack |
