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
5. **After each wave**: merge branches one by one into the epic branch, resolve conflicts (migrations: regenerate if they clash), **wave-level gates**, `qa-reviewer` over the whole, wave report, remove the worktrees. If a conflict changes another story's behaviour, stop and ask.
6. **Close**: epic gates, dependency audit, epic DoD checklist, `security-audit` (`quick` or `standard` profile) if the app is ready to deploy, with its summary in the user's personal notes (never in the repo; in the repo only fix stories or a `D#`), and the final report.

Never push or deploy: at the end, remind the user to run `check-sensitive` before pushing.
