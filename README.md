# AI Kickstart

**From idea to deployed app with Claude Code, without losing control of what gets built.**

A Claude Code plugin with a method for defining and building software. You describe what you want; Claude asks the right questions, draws an HTML prototype you approve, writes user stories bound to that prototype, and implements them one by one (or in parallel waves) with honest quality gates, a test for every acceptance criterion, and security checks before pushing and before deploying.

Built for one person or a small team. All project documentation lives **in the repo** (`internal_docs/`), so anyone who clones it and has the plugin can pick up the work.

Companion to [ai-knowledge](https://github.com/JosepFe/ai-knowledge), which is about notes and research.

## Install

Needs Claude Code and git. Inside Claude Code:

```
/plugin marketplace add JosepFe/ai-kickstart
/plugin install ai-kickstart@ai-kickstart
```

No configuration: everything project-specific is asked per project. `new-project` checks the other tools (gitleaks, Node, Docker, .NET) and tells you what is missing and how to install it. gitleaks 8.19+ is needed before the first commit.

The pre-deploy audit uses the Cloudflare `security-audit` skill, pinned to a reviewed commit. Its install block and the check are in [methodology/03-execution.md](methodology/03-execution.md) §7.

## Use

```
new project
review the app <repo>
implement epic E01            (or: implement epic E02 in parallel)
check sensitive
```

Skills also understand requests in Spanish.

## What it contains

| Name | Type | What it does |
|---|---|---|
| `new-project` | skill | The six definition phases: language, questionnaire, architecture, epic map, prototype, epics and scaffold |
| `review-app` | skill | Applies the method to an existing app on a `chore/ai-kickstart` branch |
| `run-story` | skill | Implements one story end to end: read, implement, test audit, gates, report, local commit |
| `run-epic` | skill | Implements an epic in series or parallel waves, then closes it with its Definition of Done |
| `check-sensitive` | skill | Secrets and sensitive data in what is about to be pushed |
| `qa-reviewer` | agent | Independent, read-only review. At epic close it checks the feature criteria against the stories |
| `pre-commit` | hook | gitleaks on every commit (`templates/githooks/`, copied by `new-project`) |
| `methodology/` | docs | The full method: phases, templates, execution rules, prompts, questionnaire and stack |

Each story is one Given/When/Then file bound to its prototype screens. Each epic records decisions `D#`, assumptions `A#`, risks `R#` and open questions `Q#`.

## Security

| When | What |
|---|---|
| Every commit | gitleaks hook blocks secrets |
| Before every push | `check-sensitive`: real personal data, private domains, internal IPs, personal paths, private notes |
| Closing an epic | dependency audit (`npm audit`, `dotnet list package --vulnerable`) |
| Before deploying | `security-audit` at its pinned commit (`quick` or `standard` profile); the summary goes to your personal notes, not the repo, and fixes become stories or accepted risks `D#` |

## Privacy

Everything stays in your repo and your machine:

- Project docs and `CLAUDE.md` live in the repo. Personal or sensitive notes (servers, accounts, people) and `security-audit` summaries stay outside it.
- Claude never pushes, tags or deploys unless you ask.
- Anything that could not run is reported as `NOT RUN`, never as passed.

## Updating and uninstalling

```
/plugin marketplace update ai-kickstart
/plugin uninstall ai-kickstart@ai-kickstart
```

Your projects keep their `internal_docs/` and `CLAUDE.md`; they don't depend on the plugin being installed to be read.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `pre-commit: gitleaks not installed` | Install gitleaks 8.19+, or remove `core.hooksPath` if you really don't want the hook |
| gitleaks flags a false positive | Add its fingerprint to `.gitleaksignore` with a comment saying why |
| The hook doesn't run | Enable it once per clone: `git config core.hooksPath .githooks` |
| Parallel waves conflict on migrations | Expected: only one story per wave should create a migration; regenerate after merging |
| Claude starts coding before the prototype is approved | Say "prototype first": the prototype is a hard gate in the method |

## License

[MIT](LICENSE)
