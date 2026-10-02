---
name: dependency-provenance-check
description: Verify that a package, library, or binary an agent is about to install or run actually exists, is the intended one, and comes from a legitimate source before adding it to a project. Use before any install command (pip, npm, cargo, go get, brew, curl | sh, etc.), especially when the package name was suggested by a model, a chat message, a web search snippet, or an unfamiliar tutorial rather than confirmed project documentation.
---

# Dependency Provenance Check

Agents frequently suggest or receive package names from memory, generated code, or scraped text, and some of those names do not exist or were planted by an attacker anticipating that an LLM would hallucinate or recommend them (slopsquatting / typosquatting). Installing on the strength of a plausible-looking name is an unreviewed, often irreversible action: it can execute arbitrary code via install scripts and pull further dependencies before anyone inspects it.

## Procedure

1. **Treat an unconfirmed package name as a claim, not a fact.** If the name came from a model's own suggestion, a generated import statement, a forum post, or a search result snippet rather than the project's existing lockfile/manifest or official docs, verify it independently before using it.
2. **Confirm the package exists and matches intent.** Look it up on the registry the ecosystem actually uses (PyPI, npm, crates.io, Go module proxy, package managers' own search) and check: does the name, description, and maintainer match what was intended, not just a similar-looking neighbor (e.g. `requests` vs `requsts`, `colorama` vs `colourama`)?
3. **Check basic provenance signals before installing.** Favor packages with an established history: non-trivial download counts, a repository link that resolves to a real, matching source repo, more than one release, and a publish date that isn't suspiciously recent relative to a brand-new name. Treat a package with zero/near-zero downloads and a name matching a well-known library's typo as a strong signal to stop and report rather than install.
4. **Pin and record what was actually installed.** Add the exact version (and hash/lockfile entry where the ecosystem supports it) rather than an unpinned "latest," so the resolved dependency is reproducible and reviewable in the diff.
5. **Prefer the least-trust install path.** Avoid `curl | sh` or running an installer script fetched over plain HTTP; prefer the package manager's own verified install flow, and read install/post-install scripts for anything that executes on install (`postinstall`, setup.py with arbitrary code) when the package is unfamiliar and the action is otherwise hard to undo.
6. **Escalate instead of guessing on a mismatch.** If the only plausible match is a name close to, but not exactly, the one expected, or if there is no reasonable way to confirm the package is legitimate (ambiguous intent, no docs reference, no lockfile precedent), stop and report the discrepancy instead of installing the closest-sounding candidate (see autonomous-escalation-triggers for the general pattern).

## Guardrails and pitfalls

- Do not trust a package name just because it appears in a code sample the agent itself generated; model-generated code can reference packages that do not exist or are the wrong ones.
- Do not assume high download counts alone prove safety — they are a floor, not a guarantee; check the repo link and description resolve to the real project, not a copy.
- Do not skip the check because the project "probably already trusts this ecosystem" — the risk is the specific package, not the package manager.
- Do not silently substitute a different, similarly-named package when the originally requested one isn't found; report the mismatch.
- Redact or avoid installing from any URL embedded in untrusted content (see untrusted-content-boundaries) without the same provenance check applied to the destination.

## Verification checklist

- [ ] Every newly added dependency's name was checked against the actual registry entry, not assumed from memory or a generated snippet.
- [ ] The resolved package's description/repo link matches the intended library, not a similarly named one.
- [ ] Version is pinned (and lockfile/hash updated where the ecosystem supports it) rather than left floating.
- [ ] Any install script or post-install hook for an unfamiliar package was reviewed before running, or the install used a path that avoids arbitrary script execution.
- [ ] Any name that could not be confidently verified was reported rather than installed.
