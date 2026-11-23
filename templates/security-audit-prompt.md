# Full security audit — prompt to copy and paste

Copy this file to `<Project>/Security/security-audit-prompt.md` in your personal notes (never into the repo), fill in
the `{{}}` once, and paste the block into Claude Code, opened in the repo, whenever you decide to run the full audit.
It is expensive: every agent is a full model run. The light review at each epic close
([03-execution](../methodology/03-execution.md) §7) is the routine one; this is the deep pass.

When it pays off: before exposing the app outside your own network, before its first release to real users, after big
changes to auth, personal data or dependencies, or once in a while (every few months).

```text
Security audit this repo with the security-audit skill, full audit mode.

- Check first that the skill is at its pinned commit (AI Kickstart 03-execution §7). If not, stop and tell me.
- Profile: {{quick | standard}}. Scope: {{the whole repo | the diff since the last audit: <commit or tag> }}.
- Budget: at most {{12}} agent invocations in total, counting reconnaissance, hunters, critics and verifiers.
  Before launching anything, show me the plan (units, hunters, critics, verifiers) and its agent count, and wait for my
  OK. If the plan does not fit, cut scope and say what stays uncovered; never go over the budget.
- Prior runs: read ~/security-audit-skill/{{repo}}/ and build on them; do not repeat units already covered with no
  change since.
- Do not run the project's code outside an OS sandbox: anything you cannot verify stays needs_validation.
- When it ends: write the summary to {{<notes>/<Project>/Security/}}YYYY-MM-DD-security-audit.md (date, commit,
  profile, agents used, coverage, findings by severity with status, needs_validation). Nothing about the findings goes
  into the repo: there, only a fix story or a D# that does not describe the weakness.
```

Previous runs of this project (date · profile · agents · result):

| Date | Profile | Agents | Result |
|---|---|---|---|
| | | | |
