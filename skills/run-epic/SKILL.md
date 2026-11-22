---
name: run-epic
description: Implement a whole AI Kickstart epic, in series or in parallel waves of stories (git worktrees), and close it with the epic Definition of Done. Use when the user says "implement epic E0N", "run-epic", "run the epic in parallel", "implementa la épica E0N" or similar in a repo with internal_docs/.
---

# Implement an epic

The methodology lives in `../../methodology/` relative to this skill's folder (the `ai-kickstart` plugin). Rules: `03-execution.md` (§3 waves, §4 gates, §7 security, §8 report); epic DoD in `02-templates.md`.

1. **Read** `CLAUDE.md`, `internal_docs/Epics/<E0N>/EPIC.md` (D#, A#, Q#) and its stories. Check which gates can run here (Docker, browser, network) and that the gitleaks hook is active.
2. **Series or parallel**: if not stated, ask. Recommend parallel only with at least 2 independent stories of size M or L.
3. **Wave plan** (if parallel): groups of stories with no dependencies between them, at most 3 per wave, at most one story with a migration per wave, the prototype never edited in parallel. Show it as a table (wave → stories → shared files) and **wait for approval**.
4. **For each story**: `run-story`. In parallel, one subagent per story in its own worktree and branch `story/E0N-US-NNN`, with a self-contained prompt (story, run-story rules, which shared files it may touch).
5. **After each wave**: merge branches one by one into the epic branch, resolve conflicts (migrations: regenerate if they clash), **wave-merge gates** (03 §4), `python3 scripts/epic-status.py --write` (EPIC and FEATURE tables are not resolved by hand in a conflict), wave report into the EPIC's `## Waves`, remove the worktrees. If a conflict changes another story's behaviour, stop and ask. When a feature's last story is done, its **feature gate** runs.
6. **Close**: epic gates, **QA pass** (`03-execution` §8): `python3 scripts/epic-status.py --summary E0N` first; `qa-reviewer` in epic mode only if the summary says so (more than one wave, or non-functional requirements), with a small model (e.g. Haiku), one round, read-only, inputs the summary, `EPIC.md`, each `FEATURE.md` and the reports, no diff, one section per feature; otherwise the summary is the QA, dependency audit, epic DoD checklist, `security-audit` at the pinned commit (required before deploying: if the pin check in `03-execution` §7 fails, stop the deploy step and show the install block; `quick` or `standard` profile), with its summary in the user's personal notes (never in the repo; in the repo only fix stories or a `D#`), and the final report, which proposes the version (major / minor / patch by the table in `03-execution` §10, a major or `1.0.0` only with the user's approval) and drafts the release notes.

Never push, tag or deploy: at the end, remind the user to run `check-sensitive` before pushing.
