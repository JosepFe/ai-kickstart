---
name: new-project
description: Start a new project with AI Kickstart - create the repo with internal_docs/, fill in the kickoff prompt and run the 6 phases (questionnaire, architecture, epic map, prototype, epics/features/stories, QA and scaffold). Use when the user says "new project", "start a project", "kickstart", "nuevo proyecto", "quiero empezar un proyecto" or similar.
---

# New project

The methodology lives in `../../methodology/` relative to this skill's folder. Read all of it (start with `README.md` and `01-methodology.md`) before phase 1.

1. **Language first**: ask whether the project documentation should be in **English or Spanish** (question 0 of `06-questionnaire-and-stack.md`) and continue the conversation and the documents in that language.
2. **Minimum to start**: name and repo path (default `~/Repos/<lowercase-name>`; if it exists, use it). Don't ask again for anything the user already said.
3. **Repo**: create the folder if missing and `git init` (never touch the git identity). Create the `internal_docs/` skeleton from `02-templates.md` §Structure.
4. **Personal notes** (optional): if the user has a notes system (Obsidian, etc.), ask where they want the project's index note linking to the repo. Nothing sensitive goes into the repo.
5. **Kickoff prompt**: fill in `04-prompts.md` §1 with what is known and show it. Ask whether to run it now in this session or in a new session inside the repo.
6. **Run** the 6 phases of `01-methodology.md`:
   - Phase 1: the rest of the questionnaire in `06-questionnaire-and-stack.md`, only what is missing, in 2-3 rounds with options. Default stack unless told otherwise.
   - Phase 3: epic map (paragraph + feature sketch) and screen inventory. No EPIC.md or stories yet.
   - Phase 4: prototype, hard gate, `proposed` until approved.
   - Phase 5: epics, features and stories in one pass, looking at the prototype.
   - Phase 6: QA, scaffold (with `CLAUDE.md` from `05-claude-md-template.md` and the hook from `../../templates/githooks/pre-commit` copied to `.githooks/`; enable it with `git config core.hooksPath .githooks` only with approval), `internal_docs/README.md` and the consistency check.
7. **Deliver** a summary after each phase and, at the end, the launch prompt (`04-prompts.md` §2) filled in. Local commit only if the user asks; never push.
