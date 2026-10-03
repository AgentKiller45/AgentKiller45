---
name: secret-leak-prevention
description: Catch API keys, tokens, passwords, private keys, and other credentials before they land in a commit, diff, log, or report an agent produces. Use before every `git add`/`git commit`/`git push`, before pasting command output or file contents into a report, and whenever a `.env`, config, or test fixture file is created, edited, or copied.
---

# Secret Leak Prevention

Agents routinely read, generate, and move files that contain credentials: `.env` files, cloud CLI output, API responses, test fixtures seeded with real-looking keys, and debug logs. A credential that reaches a commit, a pushed branch, or a pasted report is effectively public the moment it leaves the local workspace, even if the commit is later reverted. Catching it before it's written is the only reliable control.

## Procedure

1. **Scan the actual diff before committing, not the file list.** Run `git diff --cached` (or `git diff` for unstaged changes) and read every added line, not just the filenames. A file named `config.example.yaml` can still contain a real key if it was copied from a working config instead of written fresh.
2. **Recognize the common shapes**, not just the word "secret": `AKIA[0-9A-Z]{16}` (AWS access key), `sk-[a-zA-Z0-9]{20,}` / `sk-proj-...` (OpenAI-style), `ghp_`/`gho_`/`github_pat_` (GitHub tokens), `xox[baprs]-` (Slack), long base64/hex blobs assigned to variables named `*_KEY`, `*_SECRET`, `*_TOKEN`, `*_PASSWORD`, private key headers (`-----BEGIN ... PRIVATE KEY-----`), and connection strings with embedded credentials (`://user:pass@host`).
3. **Run a scanner when one is available before pushing.** Prefer `gitleaks detect --no-git -s .` or `trufflehog filesystem .` over manual review alone for anything beyond a tiny diff; treat a scanner finding as a hard stop, not a suggestion, until it's confirmed as a false positive (e.g., a clearly fake placeholder like `sk-xxxxxxxx...`).
4. **Treat `.env`, credential files, and key files as never-commit by default.** Confirm `.gitignore` covers `.env*`, `*.pem`, `*.key`, `id_rsa*`, and cloud credential directories before creating them; if one must be referenced, commit a `.env.example` with placeholder values instead of the real file.
5. **Check generated or copied content with the same scrutiny as hand-written code.** Code an agent writes from a working example, a fixture copied from a real response, or output pasted into a README can carry a live credential forward even though no human typed it directly.
6. **If a secret was already committed, don't just delete it in a new commit.** Removing the line in a follow-up commit leaves the value in history, reachable by anyone who clones the repo. Treat this as a reversible-agent-operations-style incident: stop, report it, and flag that the credential needs rotation and (if already pushed) history rewrite by someone with the authority to force-push — do not attempt a history rewrite on a shared branch unilaterally.
7. **Apply the same check to reports and tool output**, not just commits. Before pasting command output, environment variable dumps, API responses, or config contents into a summary or PR description, scan it for the same patterns; redact with a placeholder (`***REDACTED***`) rather than omitting silently so the redaction itself is visible.

## Guardrails and pitfalls

- Do not assume a `.gitignore` entry protects a file that was already tracked before the ignore rule was added — check `git status` and `git ls-files` for files matching sensitive patterns that are already tracked.
- Do not rely on filename alone (`*example*`, `*sample*`, `*test*`) to assume a value is fake; read the value.
- Do not skip scanning small diffs — a one-line change adding a real token to an otherwise innocuous config is exactly the diff size most likely to be rubber-stamped.
- Do not "fix" a leaked secret by deleting it in a later commit without reporting it; the exposure window and required rotation matter more than the current file state.
- Do not paste raw `env`, `printenv`, cloud CLI config output, or full HTTP request/response logs into a report without scanning them first — they are a frequent accidental source of leaked credentials.

## Verification checklist

- [ ] `git diff --cached` (or the equivalent full diff) was read line-by-line, not just skimmed by filename, before committing.
- [ ] A secret-pattern scan (tool-based where available, manual pattern check otherwise) ran clean, or every flagged match was confirmed as a placeholder/fake value.
- [ ] No `.env`, private key, or credential file is newly tracked unless it contains only placeholder values.
- [ ] Any credential found already committed or pushed was reported explicitly, with rotation and history-rewrite flagged as follow-up rather than silently patched.
- [ ] Pasted command output, logs, or API responses in the final report were scanned and redacted where they contained credential-shaped values.
