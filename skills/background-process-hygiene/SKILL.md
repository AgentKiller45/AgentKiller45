---
name: background-process-hygiene
description: Start, monitor, and clean up background processes (dev servers, watchers, long builds, containers) an agent launches during a task so none are left running, orphaned, or silently failed after the task ends. Use whenever a command is backgrounded or detached (server, build daemon, test watcher, container, tunnel) and before declaring the task complete.
---

# Background Process Hygiene

A backgrounded process keeps running after the command that launched it returns, so its outcome is invisible unless the agent deliberately checks on it. Agents routinely start a dev server to test a UI, a build in watch mode, or a container for integration tests, confirm the launch "succeeded" because the start command returned a PID, and then never verify the process stayed up, finished what it was for, or got stopped. The result is false-positive verification (the server never actually became ready), wasted resources (an orphaned process still holding a port or consuming CPU after the session ends), or port/name collisions on the next run.

## Procedure

1. **Track every process you background.** Note its purpose, the session/PID it was launched under, and the port or resource it occupies. If the tooling returns a session id (e.g. a job handle), record it instead of relying on memory — you may background several things in one task.
2. **Verify readiness, don't assume it from a launch command returning.** A process accepting the "start" command and returning a PID only means it began executing, not that a server is listening or a build finished its first pass. Poll logs or hit a health endpoint until the expected ready signal appears, with a bounded timeout — never loop on blind `sleep`.
3. **Check exit status and tail output before trusting a backgrounded task's result.** For one-shot background work (a long build, a test suite, a migration), poll until it exits, then read its actual exit code and the last portion of its output — a process that is merely "not running anymore" may have crashed rather than completed.
4. **Free the resource when you're done with it.** Stop servers, close watch-mode builds, and remove containers you started once they've served their purpose in the task, rather than leaving them for the port/name to collide with a later run or to keep consuming resources after the session ends.
5. **Clean up on failure paths too, not just the happy path.** If a later step in the task fails, still stop or note the background processes you started before ending the task — don't let an error partway through leave orphaned servers or containers as a side effect of the failure.
6. **Reconcile at the start of a new task/session rather than assuming a clean slate.** Before starting a server or binding a port, check whether something from an earlier run or session is already using it (list running sessions/processes, check the port) and decide whether to reuse, stop, or pick a different one.

## Guardrails and pitfalls

- Do not treat "the launch command returned without error" as proof the service is actually ready; check logs or a health signal.
- Do not poll a never-ending server in a tight loop waiting for it to "finish" — only one-shot/bounded background tasks have a terminal exit status to wait for.
- Do not leave a background process running "just in case it's needed later" without saying so in the final report — undocumented live processes are the main source of orphaned state across runs.
- Do not kill a process you did not start, or one that predates your task, without first confirming it is actually yours and safe to stop.
- Do not assume a fixed port is free; a prior crashed run or an unrelated process may already hold it.

## Verification checklist

- [ ] Every backgrounded process has a recorded purpose and session/PID, not just an assumed-successful launch.
- [ ] Readiness was confirmed via logs, a health check, or an explicit ready signal — not a blind sleep or the launch command's own exit code.
- [ ] One-shot background work was polled to actual completion and its exit code and output were read, not just its running/not-running state.
- [ ] Processes and resources started for the task were stopped/removed once no longer needed, including on a failure path.
- [ ] Any process intentionally left running past the end of the task is explicitly called out in the final report.
