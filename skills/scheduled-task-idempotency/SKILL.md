---
name: scheduled-task-idempotency
description: Avoid duplicate work, duplicate PRs/issues/comments, and clobbered state when an agent runs the same task repeatedly on a schedule (cron, daily automation, recurring triggers) without a human watching each run. Use at the start of any recurring/scheduled job, before creating a branch, PR, issue, comment, file, or external-side-effect that a prior run of the same job may have already created.
---

# Scheduled Task Idempotency

A scheduled agent run has no memory of its own history beyond what it can observe in the environment. If it doesn't check for prior runs' output before acting, retries, overlapping schedules, or a rerun after a partial failure will silently produce duplicate branches, duplicate PRs, duplicate comments, or state that conflicts with a previous run's unmerged work. The fix is to always re-derive "what already exists" from the live system before creating anything, rather than assuming today's invocation starts from a clean slate.

## Procedure

1. **Enumerate existing artifacts from the same job before creating new ones.** For a PR-producing job: list open PRs/branches with the job's naming pattern (`gh pr list`, `git branch -a | grep automation/`) before opening a new one. For an issue- or comment-producing job: search for existing open issues/comments matching the job's signature before posting another.
2. **Decide update-vs-create explicitly.** If a prior run's artifact (branch, PR, issue) covering the same underlying work is still open/unmerged, update or extend it instead of creating a parallel duplicate — unless the task is genuinely a new, distinct unit of work from a prior one (e.g., yesterday's "add skill X" PR vs. today's unrelated "add skill Y" PR are legitimately separate).
3. **Re-sync with the latest remote state first.** Fetch and fast-forward from the authoritative branch (`git fetch && git pull`) before branching, so the new work is based on the latest merged state and conflicts with a just-merged prior run are visible immediately rather than discovered at push time.
4. **Make side effects safe to repeat.** Prefer operations that are naturally idempotent (overwrite-by-key, upsert, "create or update") over blind-append operations (always-append a new line, always-post a new comment) when the same job might run twice for the same logical event.
5. **Name artifacts so collisions are detectable, not just avoided this run.** Deterministic naming (date-stamped branches, a fixed issue title prefix, a fixed comment marker like `<!-- job:daily-report -->`) lets this run and future runs both find and reconcile with past output, including runs by a different invocation of the same agent.
6. **If a prior run's artifact is stale or abandoned, say so rather than silently superseding it.** Closing or overwriting someone else's in-progress state without a note (e.g., a PR a human already pushed commits to) destroys information; flag the conflict in the report instead of unilaterally resolving it.
7. **Treat "nothing to do" as a valid, reportable outcome.** A scheduled job that finds no new work and does nothing is not a failure; forcing an artifact to exist on every run to appear productive creates exactly the filler and duplication this skill exists to prevent.

## Guardrails and pitfalls

- Do not rely on local git branch state alone to detect prior runs — a previous run's branch may exist only on the remote, or the local clone may be from a different, stale checkout.
- Do not assume the most recent branch/PR from this job's naming pattern is still relevant; check its open/closed/merged status before deciding to update it.
- Do not create a new branch/PR when an equivalent one is already open just because today's date differs — same underlying change, different day, is still a duplicate.
- Do not silently overwrite another open PR's branch with a force-push unless it was created by this same automation and the task explicitly calls for updating it.
- Do not skip the existing-artifact check "just this once" because the task feels fast or low-risk — the scenarios that create duplicates (retries, overlapping triggers, manual re-runs) are exactly the ones that don't announce themselves in advance.

## Verification checklist

- [ ] Existing open artifacts (branches, PRs, issues, comments) matching this job's pattern were listed and reviewed before creating anything new.
- [ ] The run either updated a genuinely equivalent existing artifact or confirmed the new work is distinct, not both.
- [ ] The local working copy was synced with the authoritative remote branch before branching or editing.
- [ ] Any decision to leave a prior run's artifact untouched, supersede it, or merge into it was stated explicitly in the final report.
- [ ] A "no action taken" outcome was reported as such when no genuinely new or updatable work existed, rather than manufacturing a change.
