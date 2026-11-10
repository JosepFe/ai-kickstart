---
name: run-story
description: Implement one AI Kickstart user story end to end (READ → IMPLEMENT → TEST AUDIT → GATES → REVIEW → REPORT → COMMIT) and report. Use when the user says "implement US-NNN", "run-story E0N/US-NNN", "next story", "implementa la US-NNN" or similar in a repo with internal_docs/.
---

# Implement one story

The methodology lives in `../../methodology/` relative to this skill's folder (the `ai-kickstart` plugin). Rules: `03-execution.md` (§2 loop, §4 gates, §5 parity, §6 when to stop, §8 report); DoR and DoD in `02-templates.md`.

Given a story (`E0N/US-NNN`):

1. **Ready**: check the DoR. If something is missing (dependency not done, open question without an `A#`, screen missing from the prototype), stop and ask.
2. **Read**: the story, its FEATURE, the EPIC (D#, A#, Q#) in `internal_docs/Epics/`, the architecture of what it touches and its screen in `internal_docs/Design/prototype.html`. The repo's `CLAUDE.md` rules on commands and conventions.
3. **Implement** only what the story asks (and everything its screen shows).
4. **Test audit**: every changed file has its test, before the gates.
5. **Story-level gates** from `CLAUDE.md`, in order. Anything that can't run: `NOT RUN` with the reason.
6. **Review**: `qa-reviewer` agent with a self-contained prompt (story, files, gates run and their log). Max 3 rounds.
7. **Report** (§8) and **one local commit** with files staged by name (never `git add -A`, never `--no-verify`), with the story `status` and the EPIC table updated in the same commit.

Never push or deploy. If cutting scope or deferring something seems necessary: ask.
