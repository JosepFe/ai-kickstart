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
| B2 | **Deployment** | **Docker only** (default: `docker compose` on any server or locally) · self-hosted server / homelab (its own flow is followed: proxy, domains, backups) · cloud (say which) |
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
