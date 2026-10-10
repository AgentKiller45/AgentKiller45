---
name: diff-scoped-commits
description: Review the actual staged/working diff against the intended change before committing or opening a PR, so accidental edits, stray debug output, unrelated files, and formatting-only noise do not ship alongside the real work. Use before every `git add`/`git commit` in an automated or unattended workflow, and always before `git push` or opening a pull request.
---

# Diff-Scoped Commits

An agent that edits files across multiple steps can accumulate changes it never intended to ship: a config value flipped for local testing and left that way, a debug `print`/`console.log` added while investigating, a file touched by a tool run (formatter, linter --fix, generated lockfile) that has nothing to do with the task, or a stale branch that silently picked up someone else's unrelated commit. None of these show up unless the diff is actually read before it becomes a commit — by then it is in history and, if pushed, visible to reviewers or merged without anyone ever having decided it should be there.

## Procedure

1. **Decide the task's intended file scope up front.** Before editing, know roughly which files/paths the change should touch. This is the yardstick the diff gets checked against, not something inferred after the fact.
2. **Diff before staging, then diff what's staged.** Run `git status` and `git diff` to see all working-tree changes, not just the files you remember editing. After `git add`, run `git diff --staged` (or `--cached`) and confirm it is byte-for-byte what you intend to commit — staging everything with `git add -A` without reading the result is how unrelated changes slip in.
3. **Read every changed file in the diff, not just a stat summary.** `git diff --stat` tells you *how many* lines changed per file, not *what* changed or *why* it's there. For each file in the diff, confirm the change belongs to the task: no leftover debug statements, no commented-out code, no temporary test values, no accidental whitespace-only reformatting of untouched code.
4. **Treat any file outside the intended scope as a signal to stop and investigate, not to shrug and include it.** If a file you didn't mean to touch appears in the diff, find out why (a formatter ran automatically, a prior branch state leaked in, a script wrote somewhere unexpected) before deciding whether to keep, revert, or `git restore` it.
5. **Separate mechanical changes from substantive ones when both occur.** If a formatter or linter reformatted a wider area than your actual edit, either keep the formatting change intentional and call it out, or revert the incidental reformatting so the diff reflects only the real change — don't let large-diff noise bury the three lines that matter.
6. **Re-check after any auto-fix, rebase, or merge.** Commands that can rewrite files you didn't directly edit (`--fix`, `go fmt`, auto-merge resolution, generated file regeneration) require re-running the diff review afterward; the state you reviewed before the command ran is no longer the state you're about to commit.
7. **Before pushing or opening a PR, diff the branch against its merge base, not just the latest commit.** `git diff main...HEAD` (or the equivalent against the PR's target branch) shows the full cumulative change the PR will introduce — review that, since intermediate commits can net out to something different from any single commit's diff.

## Guardrails and pitfalls

- Do not run `git add -A` or `git add .` as a reflex; stage deliberately (`git add <path>`) when the working tree may contain incidental changes, then verify with `--staged` diff.
- Do not equate "tests pass" or "the file compiles" with "the diff is clean" — a stray debug line or an accidentally-reverted unrelated fix can pass tests while still being wrong to ship.
- Do not assume a clean `git status` before you started means the tree stayed clean; background tools, prior branch switches, or earlier steps in the same session can leave residue.
- Do not skip diff review because the change "felt small" — small intended changes are exactly where an unrelated one-line accident is easiest to miss.
- Do not commit generated or dependency-lock files that changed as a side effect of an unrelated command unless that update is actually part of the task.

## Verification checklist

- [ ] The task's intended file scope was defined before editing and the final diff matches it.
- [ ] `git diff` (working tree) and `git diff --staged` were both read in full before committing, not just their stat summaries.
- [ ] Every file in the diff was confirmed to belong to the task; any unexpected file was investigated and explicitly kept or removed, not left in by default.
- [ ] No debug statements, commented-out code, or temporary test values remain in the committed diff.
- [ ] The branch's cumulative diff against its target branch was reviewed immediately before push/PR, not only the most recent individual commit.
