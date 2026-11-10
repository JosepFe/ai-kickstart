# AI Kickstart

A methodology for **defining and building projects with [Claude Code](https://claude.com/claude-code)**, packaged as a plugin: from idea to deployed app, with an HTML prototype as the visual contract, user stories bound to that prototype, story-by-story (or parallel-wave) implementation with honest quality gates, and security checks before pushing and before deploying.

Built for one person or a small team. Project documentation lives **in the repo** (`internal_docs/`), so anyone who clones the repo and has the plugin can keep working.

## How it works

```
Define (new-project)                                           Build (run-epic / run-story)
1 Questionnaire ─▶ 2 Architecture ─▶ 3 Epic map ─▶ 4 PROTOTYPE ─▶ 5 Epics, features, stories ─▶ 6 QA & scaffold
                                     + screen       (hard gate)    (single pass)
                                     inventory                                                │
           ┌──────────────────────────────────────────────────────────────────────────────────┘
           ▼
  story by story or parallel waves ─▶ gates ─▶ qa-reviewer ─▶ local commit (gitleaks)
           │
           ▼
  check-sensitive ─▶ push               epic DoD + security-audit ─▶ deploy
```

- **Prototype as contract**: `prototype.html` with one section per screen, states addressable by query string and `data-testid`s; the app is checked against it with parity tests (structure and copy, no pixel diffs).
- **One story per file**, Given/When/Then, bound to its screens; decisions `D#`, assumptions `A#`, risks `R#` and open questions `Q#` in every epic.
- **Honest gates**: anything that could not run is reported as `NOT RUN`, never as green.
- **Never cuts scope or approves decisions** on the user's behalf.
- **Default stack**: Angular + .NET with Vertical Slice Architecture + Postgres, on Docker (changeable in the questionnaire).

## What's included

| Type | Name | Purpose |
|---|---|---|
| Skill | `new-project` | Start a project: the 6 definition phases |
| Skill | `review-app` | Apply the methodology to an existing app (diagnosis, screenshots, design review, prototype, epics) |
| Skill | `run-story` | Implement one story end to end |
| Skill | `run-epic` | Implement an epic in series or in parallel waves (git worktrees) and close it with its Definition of Done |
| Skill | `check-sensitive` | Before a push: secrets and sensitive data in what is about to be uploaded |
| Agent | `qa-reviewer` | Independent, read-only review of a story or a wave |
| Template | `templates/githooks/pre-commit` | Hook that blocks commits containing secrets (gitleaks) |
| Docs | `methodology/` | Methodology, templates, prompts, questionnaire and default stack |

## Installation

In Claude Code:

```
/plugin marketplace add JosepFe/ai-kickstart
/plugin install ai-kickstart@ai-kickstart
```

To update: `/plugin marketplace update ai-kickstart`.

### Requirements

- [gitleaks](https://github.com/gitleaks/gitleaks) v8.19 or later on your `PATH` (used by the hook and by `check-sensitive`).
- Cloudflare's [security-audit skill](https://github.com/cloudflare/security-audit-skill) for the pre-deploy audit (needs Node):
  ```bash
  npx skills add https://github.com/cloudflare/security-audit-skill --skill security-audit --global
  ```
- For projects on the default stack: Docker, Node, the .NET SDK and Playwright.

## How to use it

The plugin itself (methodology, skills, agent) is in English; the skills also understand Spanish requests.

1. **Start a project**: say "new project" (`new-project`). The first thing Claude asks is **which language the project documentation should be in: English or Spanish**. Vision, architecture, epics, stories, QA and the project index are all written in that language; file names, endpoints, code and `CLAUDE.md` are always in English.
2. Answer the questionnaire (only what your first message didn't cover), approve the prototype, and review the epics and stories.
3. **Build**:
   ```
   implement epic E02 in parallel     → run-epic
   implement E02/US-003               → run-story
   ```
4. **Before pushing**: "check sensitive" (`check-sensitive`).
5. **Before deploying**: the epic Definition of Done and `security audit this repo, quick profile`.

For an existing app: "review the app <repo>" (`review-app`). It uses the language of the existing docs, or asks if there are none.

Optional: a personal list of terms that must never be pushed (company names, domains, people) in `~/.config/ai-kickstart/sensitive-terms.txt`, one per line. It lives outside the repo on purpose.

## License

[MIT](LICENSE)
