---
name: review-app
description: Analyse and improve an existing app with AI Kickstart - diagnosis with file:line, screenshots against a mocked backend, design review, proposed prototype, epic map, epics/stories, QA and CLAUDE.md on a branch. Use when the user says "review the app <x>", "analyse and improve <x>", "apply AI Kickstart to this repo", "revisa la app <x>" or similar.
---

# Review an existing app

The methodology lives in `../../methodology/` relative to this skill's folder. Deliver the whole package **without asking first**: new decisions are recorded as `proposed` and questions go at the end, in `internal_docs/README.md`. Everything goes on a `chore/ai-kickstart` branch of the repo, under `internal_docs/`. **Language**: that of the app's existing docs; if there are none, it is the only question asked up front (English or Spanish).

1. **Local repo** (to clone a private one, use `gh repo clone`). Branch `chore/ai-kickstart`.
2. **Old docs**: if the repo already has documentation, reorganise it with `git mv` (history keeps it); if it lives outside the repo, don't delete it.
3. **`Architecture/02-diagnosis.md`**: findings with `file:line`, an area / severity / epic table and baseline gates (anything not run: `NOT RUN`). For a large repo, read-only subagents.
4. **Real screenshots** with Playwright against a **mocked** backend (`page.route`, `routeWebSocket`) with made-up data, never against production. In `Design/screenshots/YYYY-MM-DD-current-*.png`.
5. **`Design/01-design-review.md`**: critical issues, improvements, craft details, what works and platform. If a design skill is installed (e.g. one based on Human Interface Guidelines), use it and cite it. Avoid the "made by AI" look: purple gradients, emojis as icons, generic cards.
6. **`Design/prototype.html`**: hard gate, `proposed` until the user approves it. `Design/README.md` with tokens, computed contrast and the parity matrix.
7. **Epic map (paragraph + feature sketch) and inventory** before the prototype; **epics, features, stories and QA** after it, in one pass. If the stack is being migrated, use the default stack in `06-questionnaire-and-stack.md`.
8. **`internal_docs/README.md`** with epics, open questions and the launch prompt.
9. **`CLAUDE.md`** (`05-claude-md-template.md`) and the `.githooks/pre-commit` hook (from `../../templates/githooks/`; enable it only with approval). **Local** commit; never push unless asked, and run `check-sensitive` before.
10. Short summary: serious findings, design proposal and what the user has to approve.
