---
type: reference
title: "AI Kickstart — Questionnaire and default stack"
description: "Phase 1 questions (language, vision, users, functionality, scope, data, platform, deployment, stack, style) and the default stack: Angular + .NET with Vertical Slice + Postgres on Docker"
tags: [ai-kickstart, discovery, questionnaire, stack]
timestamp: 2026-11-10T18:00:00Z
status: active
---

# Questionnaire and default stack

## How to run it

- Only ask what the kickoff prompt and the existing material don't answer. If an answer is already there, don't ask again.
- Questions with options (plus "other"), in **2-3 rounds at most**: question 0 first, then A, then B and C together.
- Anything that doesn't block can stay unanswered: it becomes an `A#` assumption with the default value.
- Answers go into `Architecture/00-vision.md` and become `D#` decisions.

## 0 — Language (first, before anything else)

| # | Question | Options |
|---|---|---|
| 0 | **Project documentation language** | English · Spanish |

Vision, architecture, epics, stories, QA and the index are written in that language, and the rest of the questionnaire is asked in it. File names, endpoints, code and `CLAUDE.md` are always in English. Recorded as `D1`.

## A — Vision and product

| # | Question | Why |
|---|---|---|
| A1 | **Problem and vision**: what hurts today, and what does the project look like working a year from now? | Value proposition, principles |
| A2 | **Users**: who uses it and with which roles? How many are expected (1 · fewer than 10 · fewer than 100 · more)? Do they share data? | Auth, permissions, database, real time |
| A3 | **Functional description**: the 5-10 things a user will do with the app, in short sentences | Epic map and features |
| A4 | **v1 scope**: of the above, what is essential and what can wait? | Epic order |
| A5 | **Non-goals**: what is it not expected to do (even if it seems obvious)? | Out of scope, keeps it from growing |
| A6 | **Data**: what is stored, rough volume, sensitivity (personal, money, health), existing data or data to migrate, external integrations | Model, database, security, migration |

## B — Platform and operations

| # | Question | Options |
|---|---|---|
| B1 | **Platform** | Desktop web · mobile (PWA) · both (say which one leads) |
| B2 | **Deployment** | **Docker only** (default: `docker compose` on any server or locally) · self-hosted server / homelab (its own flow is followed: proxy, domains, backups; the app deploys by publishing a release, [03-execution](03-execution.md) §10) · cloud (say which) |
| B3 | **Access** | No login · own login · Google or other OAuth · company SSO. Exposed to the internet or internal network only? |
| B4 | **Special requirements** | Real time · offline · notifications · several languages · accessibility beyond AA · none |

## C — Stack, style and constraints

| # | Question | Options |
|---|---|---|
| C1 | **Stack** | Default (below) · change a piece (which and why) |
| C2 | **Style** | References or screenshots · existing design system · "let's agree on it with the prototype". Light, dark or both? |
| C3 | **Constraints** | Deadline, cost, licences, performance, regulation · none |

## Default stack

Used unless the user says otherwise. Versions: the latest stable (LTS for .NET) at kickoff time.

| Layer | Default | Notes |
|---|---|---|
| Frontend | **Angular** (standalone, signals) | Unit tests with the version's default runner; E2E and parity with Playwright |
| Backend | **.NET** with **Vertical Slice Architecture** | Minimal APIs; one slice per use case in `Features/<Feature>/<UseCase>/` (endpoint, request/response, handler, validation) with its tests next to it; EF Core with migrations; xUnit + Testcontainers for integration |
| Database | **Postgres** | Always justified in `00-vision.md`. **SQLite** if single-user or embedded, low volume and no concurrency; anything else (Redis, search…) only as a complement and with a reason |
| Runtime | **Docker**: one `Dockerfile` per service and `docker-compose.yml` | Configuration via environment variables, `.env.example` in the repo and `.env` in `.gitignore` |
| Quality | gitleaks (pre-commit), dependency audit (`npm audit`, `dotnet list package --vulnerable`), `security-audit` skill before deploying | [03-execution](03-execution.md) §7 |

## Repository layout (default)

A recommendation, not a rule: it is what the default stack ends up with, so agents find things without being told. Each repo writes its own in `CLAUDE.md` if it differs.

**One repo per app**: frontend, backend, docs and deployment together, with one version and one release. Several apps in one repo (a monorepo) only when they share code that changes with them (a common library); then each app has its own image workflow filtered by `paths`, and a release per app needs a prefixed tag (`news-v1.2.0`): the release template assumes one app per repo.

```
<repo>/
  CLAUDE.md  README.md  .env.example  docker-compose.yml
  .githooks/pre-commit
  .github/workflows/     CI (gates, then sha-<commit> images on the main branch) · release.yml
  scripts/               epic-status.py · gates.sh <level> (or the Makefile / npm scripts it calls)
  internal_docs/         02-templates
  backend/
    <App>.slnx  global.json  Directory.Build.props  Directory.Packages.props   (central package versions)
    Makefile               qa: format, build, unit, integration, coverage
    Dockerfile
    src/<App>.Api/         Features/<Feature>/<UseCase>/ (slices) · Data/ (DbContext, Migrations) · Common/
    tests/<App>.UnitTests/  tests/<App>.IntegrationTests/   (Testcontainers)
  frontend/
    angular.json  package.json  playwright.config.ts  Dockerfile  nginx.conf
    src/app/               core/ (auth, HTTP, shell) · features/<feature>/ · shared/
    e2e/                   <feature>/*.spec.ts · parity/<screen>.parity.spec.ts
```

- `features/` on both sides follow the epic map's features where they map cleanly; a use case lives in one slice, not spread over layers.
- Test fixtures and seeds use made-up data only (`ana@example.com`): `check-sensitive` reads them.
- Tests that pin the clock (prototype dates) must not mix it with the real clock: cookies, tokens and caches expire on the app's clock, so a test helper that keeps them (an HTTP cookie jar, a cache) uses the same fake clock, or the suite breaks on a date.
- Tests that check the app's version read it from where the release sets it (`<Version>` in the `.csproj`, `package.json`), never a literal: every release would break them.

## Optional skills (not installed by the scaffold)

Only when the project asks for them, installed with the user's approval (they write outside the workspace), and reviewed like `security-audit`: a pinned version where the tool allows it, telemetry off.

| Skill | When | Watch out |
|---|---|---|
| [modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance) (Google Chrome) | Frontend stories that need a modern platform feature (popover, dialog, view transitions, container queries, forms, accessibility, performance): the agent looks up the guide before writing a workaround | Installs and updates itself from `@latest` (no documented pin) and sends telemetry, search queries included, unless `DISABLE_TELEMETRY=1`. Framework-agnostic: the guide says what the platform does, the Angular way stays in the story |
| [Hallmark](https://github.com/Nutlope/hallmark) | Phase 4, only for a landing page or a marketing web, not the app's screens | It builds a self-contained HTML page with its own themes: the prototype stays the contract, so its output is a reference to copy from, never the prototype itself |
