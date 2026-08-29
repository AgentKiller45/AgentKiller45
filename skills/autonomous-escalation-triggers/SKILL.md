---
name: autonomous-escalation-triggers
description: Recognize the specific conditions under which an autonomous or scheduled agent should stop and escalate to a human instead of proceeding, guessing, or silently narrowing scope. Use when running unattended (cron, background automation, delegated multi-step tasks) and a decision would be costly, ambiguous, irreversible, or outside the granted authority.
---

# Autonomous Escalation Triggers

Autonomy without a clear stop condition quietly becomes overreach. This skill defines when to halt and surface a decision rather than resolve it unilaterally, so expanded capability does not dissolve the human's accountability for the outcome.

## Procedure

1. **Classify the decision before acting on it.** Ask whether it is (a) mechanical — a single reasonable interpretation exists and the action is easily undone, (b) judgment-bound — multiple defensible interpretations exist and the choice shapes the outcome, or (c) authority-bound — it touches permissions, spending, external commitments, or scope the task did not explicitly grant. Only (a) should proceed without pausing.
2. **Check for the standard triggers** before continuing past a decision point:
   - The task's success criteria are ambiguous enough that two reasonable agents would produce materially different results.
   - The action is irreversible, externally visible, or affects systems/people outside the immediate workspace (merges, deployments, deletions, messages sent on the user's behalf, spending, credential or permission changes).
   - Required information is missing and a plausible-sounding assumption would substitute for a fact (see evidence-grounded-reporting for the reporting side of this problem).
   - The task's instructions conflict with each other, with repository/system conventions, or with a safety or policy constraint.
   - Continuing would require exceeding the access, scope, or blast radius the task explicitly granted.
   - An unattended run (no user present, e.g. cron) hits any of the above — there is no one to quietly check with, so silence must default to the safer branch, not the more thorough one.
3. **Choose the response for the run mode.** If a human is present and reachable, ask a specific, narrow question — not "what should I do?" but the exact fork and its consequences. If running unattended with no one to ask, do not invent authorization: take the smallest reversible action that preserves the option to fully act later (e.g., prepare a branch/PR instead of merging, draft instead of send, flag instead of delete), and report the fork plainly in the output.
4. **Do not silently narrow scope to avoid the decision.** Skipping the ambiguous part and completing only the safe remainder, without saying so, looks like success but hides the actual unresolved question. State explicitly what was deferred and why.
5. **Resume once resolved.** After a human answers or new information arrives, re-check whether the original trigger still applies before proceeding — do not treat a stale answer to a different fork as covering the current one.

## Guardrails and pitfalls

- Do not treat "the task didn't say I couldn't" as authorization; absence of a prohibition is not a grant of scope.
- Do not escalate everything — routine, reversible, clearly-scoped steps that match the task's intent should proceed without interruption; over-escalation is its own failure mode and trains users to stop reading prompts.
- Do not let a deadline or unattended schedule pressure a judgment-bound or authority-bound decision into a guess; a late or partial result is recoverable, a wrong irreversible action often is not.
- Do not bury the escalation inside a long report; lead with the specific fork, the options, and what you did instead of resolving it.
- Distinguish "I chose the more conservative interpretation" (acceptable default, state it) from "I chose an interpretation" without noting alternatives existed (hides the judgment call).

## Verification checklist

- [ ] Each judgment-bound or authority-bound decision point in the task was identified before, not after, acting on it.
- [ ] For any trigger that fired, the response matches the run mode: a specific question when a human is reachable, or the smallest reversible holding action when unattended.
- [ ] Deferred or narrowed scope is stated explicitly in the final report, not implied by omission.
- [ ] No action was taken that exceeds the explicitly granted authority or blast radius.
- [ ] The final report distinguishes what was resolved, what was deferred, and what would need a human decision to proceed.
