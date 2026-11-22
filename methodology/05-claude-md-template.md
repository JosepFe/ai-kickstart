---
type: reference
title: "AI Kickstart — CLAUDE.md, agent, skills and hook"
description: "Templates for the repo's CLAUDE.md, the qa-reviewer agent, the run-story and run-epic skills and the gitleaks pre-commit hook"
tags: [ai-kickstart, claude-code, template, claude-md, agents, skills, security]
timestamp: 2026-11-10T18:00:00Z
status: active
---

# CLAUDE.md, agent, skills and hook

Fill in the `{{}}`. The `qa-reviewer` agent and the `run-story` and `run-epic` skills ship with the `ai-kickstart` plugin (`agents/`, `skills/`): their templates are here in case you want to copy them into a repo and adapt them. The hook is ready in `templates/githooks/pre-commit` and the status script in `templates/scripts/epic-status.py`.

## CLAUDE.md

````markdown
# CLAUDE.md — {{Project}}

{{1-2 sentences: what it is and stack}}
Project docs language: {{English | Spanish}}.

## Where things are
| What | Where |
|---|---|
| Project index | `internal_docs/README.md` |
| Vision and architecture | `internal_docs/Architecture/` |
| Epic map, screen inventory, epics, features, stories | `internal_docs/Epics/` |
| Visual contract (prototype) and parity matrix | `internal_docs/Design/prototype.html`, `internal_docs/Design/README.md` |
| QA | `internal_docs/QA/` (security-audit summaries are kept outside the repo, in personal notes) |
| Methodology | AI Kickstart plugin (`ai-kickstart`, folder `methodology/`); `03-execution` is the playbook |

## Commands (gates, in order)
{{table: # · gate · command · level (story / wave-epic) · must pass}}
Secrets: `.githooks/pre-commit` runs gitleaks on every commit.
Dependencies: `npm audit --audit-level=high`, `dotnet list package --vulnerable --include-transitive`.

## Story loop — follow exactly
When asked to implement a story: READ (story, feature, epic D#/A#/Q#, prototype screen) →
IMPLEMENT only that story → TEST AUDIT (every changed file has a test) → GATES (story level) →
REPORT (into the story's `## Report`) → one local COMMIT, files staged by name, story
`status`/`finished` set and `python3 scripts/epic-status.py --write` run in the same commit.
The story `status` is the source of truth: never edit the Status column of EPIC/FEATURE by hand.

## Parallel waves
When asked to run an epic in parallel: plan waves from the epic dependencies (no shared
migration in the same wave), show the plan, run each story in its own worktree and branch
`story/E0N-US-NNN` (max 3), merge one by one, run wave-merge gates.

## Backend conventions (Vertical Slice)
One slice per use case in `Features/<Feature>/<UseCase>/` (endpoint, request/response,
handler, validation) with its tests. No shared "services" layer unless two slices need it.

## NEVER
- Skip the test audit, silence linters, skip tests or lower thresholds.
- Report a gate as passed without running it (use NOT RUN + reason).
- Change the UI without changing the prototype first (with approval).
- Ignore a data-testid or skip a screen in the parity specs.
- Reduce scope or record a decision as approved by the user without explicit approval.
- Push, deploy, edit git identity, `git add -A` / `git add .`, `--no-verify`.
- Put secrets, real personal data, private domains or internal IPs in the repo (code, fixtures or internal_docs).

## Conventions
{{frontend · backend · tests}}
````

## `.githooks/pre-commit`

````bash
#!/usr/bin/env bash
# Blocks the commit if gitleaks finds a secret in the staged changes.
# Needs gitleaks 8.19+ (the `git` subcommand).
set -euo pipefail
if ! command -v gitleaks >/dev/null; then
  echo "pre-commit: gitleaks not installed (https://github.com/gitleaks/gitleaks)" >&2
  exit 1
fi
gitleaks git --staged --redact --no-banner .
````

Enable once per clone: `git config core.hooksPath .githooks` (in the scaffold, with approval). False positives: `.gitleaksignore` with the fingerprint and the reason.

## `.claude/agents/qa-reviewer.md`

````markdown
---
name: qa-reviewer
description: Independent read-only review. Story mode (auth, personal data, crypto or external input only): acceptance criteria to test mapping, test audit, parity spec per screen, targeted checks. Epic mode at epic close. Never edits files.
tools: Read, Grep, Glob, Bash
---
You review work you did not write. Inputs: story paths, changed files, gates already run
with their log path. Budget about 5 minutes.
1. Map every acceptance criterion to a named test; list the ones without a test.
2. Every changed file has a test; UI stories have a parity spec per screen/state.
3. For a wave: check merged shared files (migrations, routes, DI registration) are consistent.
4. Re-run only targeted checks (one spec, grep). Gates you did not re-run are NOT VERIFIED.
5. Report: blockers, should-fix, nits. Never modify files.
Epic mode (epic close, one round): inputs are the output of `scripts/epic-status.py --summary E0N`, EPIC.md, each FEATURE.md, the stories' `## Report` and the EPIC's `## Waves`, not the diff. Don't redo what the summary counts; one section per feature: is each C# really proven by the named tests, did each non-functional check run, do D#/A#/Q# contradict a story.
````

## `.claude/skills/run-story/SKILL.md`

````markdown
---
name: run-story
description: Implement one story end to end with the story loop of CLAUDE.md and report.
---
Given a story id (E0N/US-NNN): check it is Ready (methodology 02-templates DoR), run the
story loop from CLAUDE.md, ask the qa-reviewer agent for an independent review only if the
story touches auth, personal data, crypto or external input (max 3 rounds), write the report into the story's `## Report` (03-execution §8), set the story status and `finished`, run `python3 scripts/epic-status.py --write`,
and make one local commit with files staged by name.
````

## `.claude/skills/run-epic/SKILL.md`

````markdown
---
name: run-epic
description: Implement a whole epic, in series or in parallel waves, and close it with the epic Definition of Done.
---
Given an epic id: read EPIC.md and its stories. If parallel was asked, build the wave plan
(03-execution §3: only independent M/L stories, max 3 per wave, one migration per wave),
show it and wait for approval. For each story, run-story (in parallel: one subagent per
story in its own worktree and branch). After each wave, merge one by one, run wave-merge
gates, `scripts/epic-status.py --write`, wave report into the EPIC's `## Waves`. At the end: epic gates,
`scripts/epic-status.py --summary E0N`, qa-reviewer in epic mode (one round, small model) only if the
summary says so, dependency audit, epic DoD
checklist (02-templates), security-audit if the app is ready to deploy, and the epic
report. Never push: tell the user to run check-sensitive first.
````
