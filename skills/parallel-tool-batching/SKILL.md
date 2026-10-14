---
name: parallel-tool-batching
description: Identify when multiple tool calls in a task are independent of one another and issue them together in a single turn instead of one-by-one, to cut wall-clock time and avoid resending full context on every round-trip. Use whenever a step involves reading several files, running several read-only checks, or searching multiple unrelated things before any of them can affect the next action.
---

# Parallel Tool Batching

Agents default to calling tools serially: read file A, wait, read file B, wait, run check C, wait. When A, B, and C don't depend on each other's output, this is pure latency with no benefit — every extra round-trip resends the growing conversation and adds a full network/inference turn for information that was already knowable as "needed" before the first call returned. The fix is cheap: recognize independence before issuing the first call, then issue the independent calls together.

## Procedure

1. **Before writing the first tool call of a step, list every tool call the step will plausibly need**, not just the next one. Investigation phases (orient on a repo, gather status, check several configs) almost always need more than one lookup.
2. **Classify each candidate call as independent or dependent.** A call is independent of another if its arguments do not come from that other call's result and its purpose does not change based on that result (e.g., reading a README and listing recent git log entries are independent; reading a file and then patching based on its exact contents are dependent).
3. **Group all currently-known independent calls into one turn/response.** Issue reads, searches, status checks, and other side-effect-free lookups together rather than sequentially, even across different tools (e.g., a file read plus a terminal `git log` plus a search-files call in the same batch).
4. **Keep genuinely dependent calls serial.** Do not batch a write that depends on a read's exact content, a patch that depends on a search's match location, or any action that needs to branch on a prior result. Correctness comes before speed — only batch when the arguments and purpose truly don't depend on an unseen result.
5. **Re-batch at each new decision point.** After a batch returns, look again for the next set of independent calls (e.g., having read three config files, you may now know you need to check two more unrelated things) rather than reverting to one-at-a-time out of habit.
6. **For long or many-step investigations, batch in waves rather than one giant wave.** It's fine to do 3–6 independent lookups, evaluate, then batch the next wave — the goal is eliminating unnecessary serialization, not forcing every possible call into one mega-batch regardless of how later calls depend on earlier ones.

## Guardrails and pitfalls

- Do not batch a write/mutating action alongside a read whose result it should have waited for (e.g., don't patch a file in the same batch as reading it for the first time — you don't yet know what to change).
- Do not force interdependent steps into a batch just to "look efficient"; a batch that guesses at arguments because a true dependency was ignored produces wrong results, which costs far more time than the serial round-trip it saved.
- Do not assume two calls are independent just because they use different tools — a terminal command that depends on a file a previous read call needs to inspect first is still dependent.
- Watch for hidden dependencies: two file reads are independent, but a search's result determining *which* file to read next is not — only batch the search, then the resulting read in the next wave.
- Batching has diminishing returns past the point where one call in the batch is likely to fail or return something that changes whether the others are worth doing; don't batch a risky/exploratory call with several others that assume it will succeed.

## Verification

- [ ] Before issuing tool calls for a step, independent lookups were identified and grouped into one batch rather than issued one-by-one by default.
- [ ] No batched call's arguments depended on another call in the same batch — all true dependencies were kept serial.
- [ ] Each new wave of calls was re-evaluated for further batching opportunities rather than falling back to serial-by-default.
- [ ] A call likely to fail or redirect the task was not bundled with several calls that assumed its success.
