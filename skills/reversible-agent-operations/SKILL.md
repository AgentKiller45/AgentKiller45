---
name: reversible-agent-operations
description: Plan and execute agent changes that affect files, services, or external systems with explicit scope, dry runs, checkpoints, rollback steps, and post-change evidence. Use before migrations, bulk edits, configuration changes, destructive commands, or API operations where mistakes could be costly.
---

# Reversible Agent Operations

Turn a consequential action into a bounded, inspectable change. Preserve the user's control by making the intended effect, failure mode, and recovery path visible before execution.

## Procedure

1. **Define the operation.** State the target resources, intended end state, exclusions, success criteria, and whether the action is local, remote, or externally visible. Resolve ambiguous scope from available repository or system context; do not silently widen it.
2. **Record a baseline.** Capture the current state needed to compare and recover: version-control status and diff, configuration values, resource counts, health checks, or an export/backup. Keep secrets out of logs and artifacts.
3. **Choose the safest execution mode.** Prefer a dry run, preview, plan, transaction, staging environment, or one-item canary. Separate preparation from commit and use the smallest permission and blast radius that can complete the task.
4. **Write the rollback.** Before changing anything, specify the inverse operation and its prerequisites. For irreversible actions, stop and obtain explicit confirmation unless the user already authorized that exact destructive scope; if no true rollback exists, create a backup or narrow the operation further.
5. **Checkpoint and execute.** Save the baseline and plan in a recoverable location, then apply the change in bounded batches. Stop on the first unexpected result rather than continuing through a partially understood failure.
6. **Verify the outcome.** Re-read the affected state and compare it with the success criteria and baseline. Check adjacent invariants such as permissions, references, service health, generated artifacts, and user-visible behavior.
7. **Report plainly.** Summarize what changed, what was not touched, evidence from verification, any residual risk, and the exact rollback command or recovery location. Never imply reversibility or completion that was not tested.

## Guardrails and pitfalls

- Do not treat `--dry-run` as proof that the real command will succeed; validate permissions, inputs, and assumptions separately.
- Do not use a backup that is incomplete, stale, inaccessible, or stored in the same failure domain as the data it protects.
- Do not mix unrelated cleanup into a scoped operation, especially in a repository with existing user changes.
- Do not retry a failed external operation blindly: it may have partially succeeded. Inspect status and idempotency before retrying.
- Redact credentials, tokens, personal data, and sensitive payloads from plans, diffs, logs, and reports.
- A successful command is not a successful operation; verify the resulting state, not only the exit code.

## Verification checklist

- [ ] Scope and exclusions are recorded.
- [ ] A baseline or backup exists and can be read.
- [ ] A dry run, canary, or equivalent low-blast-radius check was used where available.
- [ ] Rollback steps are specific, available, and appropriate to the actual change.
- [ ] Post-change state satisfies the success criteria and key invariants.
- [ ] The report distinguishes verified facts from assumptions and unresolved risk.
