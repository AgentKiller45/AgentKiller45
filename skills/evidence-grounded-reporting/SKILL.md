---
name: evidence-grounded-reporting
description: Ground every claim of success, failure, or fact in output you actually observed from a real command, file read, or test run, and mark anything unverified as such. Use before reporting task completion, summarizing test results, describing file contents or API responses, or handing off work to a user or another agent.
---

# Evidence-Grounded Reporting

Separate what you verified from what you assumed, inferred, or expect to be true. A plausible-sounding claim is not a fact until something you actually ran or read confirms it.

## Procedure

1. **Tag each claim before writing it.** For every statement about state, results, or outcomes, identify its source: a command's actual output, a file you read, a test run, or an inference/assumption. Only the first three count as evidence.
2. **Re-run rather than recall.** If you are unsure whether a claim reflects the current state or a stale memory from earlier in the task, re-check it (re-read the file, re-run the command) instead of restating the earlier belief.
3. **Distinguish exit status from actual effect.** A zero exit code, an HTTP 200, or "no errors printed" means the command ran without crashing, not that it did what was intended. Confirm the resulting state (diff, file content, returned data, service behavior) separately.
4. **Never fabricate output.** If a tool call fails, times out, or is blocked (network, permissions, missing dependency), say so plainly and either try a real alternative or report the blocker. Do not synthesize command output, file contents, API responses, or metrics that resemble what a successful run would have produced.
5. **Carry uncertainty into the report.** When something could not be verified (flaky test, unreachable service, partial read, ambiguous log), state that explicitly next to the claim instead of rounding it up to a confirmed result.
6. **Cite the evidence inline.** Reference what was checked ("ran `pytest -q`, 42 passed", "read config.yaml lines 1-40", "diff shows only the intended file changed") so the reader can tell verified facts from narrative.

## Guardrails and pitfalls

- Do not let a confident tone substitute for an actual check; hedge honestly instead of hedging with authority.
- Do not reuse output from an earlier step to describe the current state after further changes were made.
- Do not describe a partially completed multi-step operation as done because most steps succeeded; report exactly which steps completed and which did not.
- Do not infer file or API contents from naming, conventions, or memory of similar systems and present that inference as a direct read.
- Do not suppress a failure or error to keep a report clean; a shorter accurate report beats a longer optimistic one.
- Watch for silent truncation or pagination in tool output; a claim about "all results" is only valid if nothing was cut off.

## Verification checklist

- [ ] Every completion or success claim maps to specific command output, a file read, or a test result you can point to.
- [ ] Exit codes and "no error" messages are backed by a check of the actual resulting state, not treated as sufficient alone.
- [ ] Any blocked, failed, or skipped step is reported as such rather than omitted or implied to have succeeded.
- [ ] Unverified or uncertain claims are explicitly labeled, not blended in with confirmed facts.
- [ ] Nothing in the report was generated to look like tool output without a real corresponding tool call.
