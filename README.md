# AI Kickstart

**From idea to deployed app with Claude Code, without losing control of what gets built.**

AI Kickstart is a methodology for defining and building software with [Claude Code](https://claude.com/claude-code), packaged as a plugin. You describe what you want; Claude asks the right questions, draws an HTML prototype you approve, writes user stories bound to that prototype, and implements them one by one (or in parallel waves) with honest quality gates, a test for every acceptance criterion, and security checks before pushing and before deploying.

Built for one person or a small team. All project documentation lives **in the repo** (`internal_docs/`), so anyone who clones it and has the plugin can pick up the work.

Companion to [ai-knowledge](https://github.com/JosepFe/ai-knowledge) (notes and research).

---

## Getting started (10 minutes)

### 1. Prerequisites

| Tool | Needed for | Check | Install |
|---|---|---|---|
| [Claude Code](https://claude.com/claude-code) | everything | `claude --version` | see the Claude Code docs |
| git | everything | `git --version` | your OS package manager |
| [gitleaks](https://github.com/gitleaks/gitleaks) 8.19+ | the pre-commit hook and `check-sensitive` | `gitleaks version` | macOS `brew install gitleaks` · Linux and Windows: binary from the [releases](https://github.com/gitleaks/gitleaks/releases) (on Linux into `~/.local/bin`; distro packages are often too old) |
| Node 18+ | the default frontend stack and `security-audit` | `node --version` | [nodejs.org](https://nodejs.org) or your package manager |
| Docker | running the app and integration tests | `docker --version` | [docs.docker.com](https://docs.docker.com/get-docker/) |
| .NET SDK, Playwright | the default stack (Claude installs Playwright browsers per project) | `dotnet --version` | [dot.net](https://dot.net) |
| Cloudflare [security-audit skill](https://github.com/cloudflare/security-audit-skill) | the pre-deploy audit | `/security-audit` shows up in Claude Code | `npx skills add https://github.com/cloudflare/security-audit-skill --skill security-audit --global` |

Only Claude Code and git are needed to start defining a project. `new-project` checks the rest and tells you what is missing.

### 2. Install

Inside Claude Code:

```
/plugin marketplace add JosepFe/ai-kickstart
/plugin install ai-kickstart@ai-kickstart
```

No configuration needed: everything project-specific is asked per project.

### 3. Your first project

Start a new session and say:

```
new project
```

1. **Language**: English or Spanish for the project documentation (code and `CLAUDE.md` are always in English).
2. **Questionnaire**: vision, users, what it will and won't do, data, platform, deployment, stack, style. Only what you didn't already say, with options, in 2-3 rounds.
3. **Architecture and epic map**: you review two short docs and the list of epics and features.
4. **Prototype**: an HTML file you open in the browser. Nothing else moves until you approve it.
5. **Epics, features and stories**: written once, looking at the approved prototype.
6. **Scaffold**: repo structure, `CLAUDE.md`, Docker, the gitleaks hook, and a ready-to-paste prompt to start building.

Then:

```
implement epic E01            (or: implement epic E02 in parallel)
```

### Already have an app?

```
review the app <repo>
```

You get a diagnosis with `file:line` findings, screenshots against a mocked backend, a design review, a proposed prototype, epics and stories, and a `CLAUDE.md`, all on a `chore/ai-kickstart` branch for you to review.

---

## How it works

```
Define (new-project)
 0 language ─▶ 1 questionnaire ─▶ 2 architecture ─▶ 3 epic map ─▶ 4 PROTOTYPE ─▶ 5 epics, features ─▶ 6 QA, scaffold
                                                     + screen        (hard gate)    and stories           and index
                                                     inventory                      (single pass)
Build (run-epic / run-story)
 story by story, or parallel waves (git worktrees, max 3 agents)
   └▶ story gates ─▶ qa-reviewer ─▶ local commit (gitleaks hook)
 after each wave: merge ─▶ full gates ─▶ qa-reviewer over the whole
Close the epic
 epic Definition of Done ─▶ check-sensitive ─▶ push ─▶ security-audit ─▶ deploy
```

- **Prototype as contract**: one section per screen, states addressable by URL (`?state=empty`), `data-testid`s. Parity tests check the app has the same structure and copy (no pixel diffs).
- **One story per file**, Given/When/Then, bound to its screens. Every epic records decisions `D#`, assumptions `A#`, risks `R#` and open questions `Q#`.
- **Honest gates**: anything that could not run is reported as `NOT RUN`, never as green.
- **You stay in charge**: Claude never cuts scope, never records a decision as approved by you, never pushes or deploys without being told.
- **Default stack**: Angular + .NET with Vertical Slice Architecture + Postgres, on Docker. Change any piece in the questionnaire.

## What it creates in your repo

```
<repo>/
  CLAUDE.md                     how Claude works in this repo: gates, story loop, rules
  .githooks/pre-commit          gitleaks on every commit
  internal_docs/
    README.md                   project index: epics, roadmap, open questions
    Architecture/               00-vision.md, 01-architecture.md
    Design/                     prototype.html, README.md (tokens, parity matrix)
    Epics/                      00-epic-map.md, 00-screen-inventory.md, E01-…/EPIC.md, F01-…/FEATURE.md, US-001.md…
    QA/                         00-qa.md
```

Personal or sensitive notes (servers, accounts, people) and the `security-audit` summaries stay **outside** the repo, in your own notes.

## What's included

| Type | Name | What it does | Say |
|---|---|---|---|
| Skill | `new-project` | The 6 definition phases | "new project" |
| Skill | `review-app` | Apply the method to an existing app | "review the app <repo>" |
| Skill | `run-story` | Implement one story end to end | "implement E02/US-003" |
| Skill | `run-epic` | Implement an epic in series or parallel waves, then its Definition of Done | "implement epic E02 (in parallel)" |
| Skill | `check-sensitive` | Secrets and sensitive data in what is about to be pushed | "check sensitive", "can I push this?" |
| Agent | `qa-reviewer` | Independent, read-only review of a story or wave | used by `run-story` / `run-epic` |
| Template | `templates/githooks/pre-commit` | Blocks commits containing secrets | copied by `new-project` |
| Docs | [`methodology/`](methodology/README.md) | The full method: phases, templates, execution rules, prompts, questionnaire and stack | — |

The skills also understand requests in Spanish.

## Security, in four layers

| When | What |
|---|---|
| Every commit | gitleaks hook blocks secrets |
| Before every push | `check-sensitive`: real personal data, private domains, internal IPs, personal paths, private notes |
| Closing an epic | dependency audit (`npm audit`, `dotnet list package --vulnerable`) |
| Before deploying | `security-audit` (`quick` or `standard` profile); the summary goes to your personal notes, not the repo (it lists open weaknesses); fixes become stories and accepted risks a `D#` |

## Updating and uninstalling

```
/plugin marketplace update ai-kickstart
/plugin uninstall ai-kickstart@ai-kickstart
```

Your projects keep their `internal_docs/` and `CLAUDE.md`; they don't depend on the plugin being installed to be read.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `pre-commit: gitleaks not installed` | Install gitleaks 8.19+ (table above), or remove `core.hooksPath` if you really don't want the hook |
| gitleaks flags a false positive | Add its fingerprint to `.gitleaksignore` with a comment saying why |
| The hook doesn't run | Enable it once per clone: `git config core.hooksPath .githooks` |
| Parallel waves conflict on migrations | Expected: only one story per wave should create a migration; regenerate after merging |
| Claude starts coding before the prototype is approved | Say "prototype first": the prototype is a hard gate in the method |

## License

[MIT](LICENSE)
