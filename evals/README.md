# Evals

Behaviour checks for the skills, run with [`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals.md).

| Case | What must hold |
|---|---|
| `new-project-starts-with-questionnaire` | `new-project` opens with the questionnaire, language first, and designs nothing yet |
| `run-story-stops-when-not-ready` | `run-story` stops without editing when a dependency is not done |
| `run-epic-shows-wave-plan-first` | `run-epic` in parallel shows the wave plan and waits for approval, no agent launched |
| `check-sensitive-blocks-personal-data` | `check-sensitive` blocks a real email, an internal IP and a home path in the unpushed range |

Three cases build their starting repo with a `scaffold.sh` (bash written here, nothing downloaded), so they need
`--scaffold`. Grant the tools the cases must be free to use, or the "no edit" graders pass only because the tool was
missing: Edit and Write (`run-story`, `run-epic`) and Bash (`check-sensitive`: git, gitleaks).

```bash
claude plugin eval . --scaffold --allow-tools Bash Edit Write --max-cost-usd 5
claude plugin eval . --case 'run-story-*' --scaffold --allow-tools Edit Write --runs 1 --ablation none   # one case, cheap
```

Each case runs 3 times with the plugin and 3 without (the baseline); the LLM graders use Haiku. Results go to
`evals/results/` (git-ignored). Reference: one run of each case without baseline cost about $1.00 in total
(2026-11-23, all 4 at 1.00).
