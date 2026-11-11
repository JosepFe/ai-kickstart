---
name: check-sensitive
description: Check what is about to be pushed to GitHub (unpushed commits) for secrets and sensitive data - gitleaks plus a review for personal data, private domains, internal IPs, personal paths and private notes in internal_docs. Use before every push, when closing a feature or epic, or when the user says "check sensitive", "can I push this?", "make sure nothing sensitive goes up", "revisa sensibles" or similar.
---

# Check for sensitive data before pushing

Read-only. **Never pushes, rewrites history or deletes anything**: it reports and proposes.

## 1. What is about to be pushed

```bash
git fetch --quiet 2>/dev/null || true
git rev-parse --abbrev-ref @{u} 2>/dev/null   # no upstream: review everything not in origin/<default branch>
git log --oneline @{u}..HEAD
git diff --stat @{u}...HEAD
```

No upstream (new branch): the range is `origin/HEAD..HEAD`; if the repo has no remote, the whole history. If there is nothing to push, say so and stop.

## 2. Secrets (deterministic)

```bash
gitleaks git --log-opts="<range>" --redact --no-banner .
```

If gitleaks is not installed, say so (`NOT RUN`) and do step 3 with extra care on keys and tokens.

## 3. Judgement review

Over `git diff <range>` (for long diffs, delegate to a cheap read-only subagent and ask only for findings with `file:line`). Look for:

| Category | Examples |
|---|---|
| Credentials gitleaks misses | passwords in docker-compose, connection strings with user and password, a committed `.env`, cookies or tokens pasted into tests |
| Real personal data | emails, full names, phone numbers, national IDs, IBANs, addresses in fixtures, seeds, prototype, screenshots or docs (test data must be made up: `ana@example.com`) |
| Private infrastructure | own or company domains, internal or Tailscale/VPN IPs, hostnames, internal service ports, server paths |
| Personal paths and environment | `/home/<user>`, `C:\Users\…`, synced-drive or notes-vault paths |
| Content that isn't the project's | personal notes, to-dos, third-party work data inside `internal_docs/` |
| Security-audit output | `security-audit` reports or summaries (`*security-audit*.md`, `findings.json`, `REPORT.md`) anywhere in the repo: they belong in personal notes |
| Files that shouldn't be there | database dumps, backups, `.pem`/`.key`, `.p12`, exports, screenshots with real data |

If `~/.config/ai-kickstart/sensitive-terms.txt` exists (outside the repo, one term per line: company names, domains, people), also search for those terms with `grep -niF -f`.

## 4. Report

- **Blockers** (don't push): with `file:line`, commit and what it is.
- **Review** (doubtful): with the reason.
- One line per check: gitleaks pass / fail / NOT RUN, review, own terms.
- Verdict: **OK to push** or **don't push until fixed**.

If something blocks and has not been pushed yet: propose fixing it in a new commit **and**, if it is a secret, that it must be rotated anyway and removed from history (`git rebase` or `git filter-repo`) before pushing. Rewrite history only with explicit approval.
