---
name: shell-argument-safety
description: Build shell commands so that interpolated paths, filenames, and variable values cannot be misparsed, split, glob-expanded, or interpreted as extra flags/commands. Use whenever a command string is assembled by concatenating or interpolating a variable (file path, branch name, user-supplied text, tool output) rather than typed as a literal, especially with filenames containing spaces, quotes, `$`, backticks, or a leading `-`.
---

# Shell Argument Safety

An agent that builds shell commands by string interpolation (`f"rm {path}"`, `` `git commit -m "$msg"` ``, `os.system(cmd)`) silently breaks or misbehaves the moment the interpolated value contains a space, quote, glob character, newline, or a leading `-`. The command still "runs" and often still exits 0, so the failure mode is usually a wrong result (wrong file touched, argument swallowed as a flag, word-split into multiple arguments) rather than a visible error — exactly the kind of mistake that passes a quick glance at the exit code.

## Procedure

1. **Identify every interpolated value in a command before running it.** Anything derived from a variable, a prior command's output, a filename discovered via listing/search, user text, or a loop is a candidate for breakage — not just values explicitly labeled "untrusted."
2. **Quote every interpolated value, even ones that "look safe."** Double-quote variables in shell (`"$path"`, `"$branch"`) so spaces and most special characters pass through as one argument. Never rely on bare `$var` or unquoted `{var}` in an f-string destined for a shell.
3. **Treat values starting with `-` or `--` as potential flag injection.** A filename like `-rf` or `--force` passed positionally can be read as an option by the receiving program. Use `--` to end option parsing before positional arguments when the command supports it (`git checkout -- "$file"`, `rm -- "$file"`), or pass an explicit `./` prefix for paths.
4. **Prefer argument arrays/lists over shell strings when the calling layer supports it.** `subprocess.run([cmd, arg1, arg2])` or an array-based exec avoids a shell parse step entirely; use this instead of building and executing one big string whenever the tool allows it.
5. **Never build a command by concatenating untrusted text into a string that is then passed to a shell interpreter (`sh -c`, `os.system`, `eval`).** If a value could contain `;`, `&&`, backticks, `$(...)`, or newlines, string concatenation into a shell context is command injection, not just a formatting bug — construct the invocation so that value is always a single argument, not interpreted shell syntax.
6. **Watch glob and brace expansion on unquoted variables.** An unquoted path containing `*`, `?`, `[`, or `{` can expand against the current directory's contents instead of being treated literally; quoting prevents this.
7. **After constructing the command, print or log the fully substituted form before executing destructive or irreversible operations**, so the actual argument boundaries are visible, not just the template.

## Guardrails and pitfalls

- Do not assume filenames are "normal" (no spaces/quotes) because the repository looks clean — generated files, downloaded assets, and user uploads routinely aren't.
- Do not pass a loop variable from `for f in $(find ...)` without quoting; unquoted command substitution word-splits on whitespace and expands globs.
- Do not use `eval` to assemble a command from parts; it reintroduces every injection and word-splitting risk the rest of this procedure avoids.
- Do not trust that a command "worked" because it exited 0 — a word-split or flag-swallowed argument frequently still produces a zero exit with the wrong effect (e.g., `rm` deletes the wrong file, `grep` searches the wrong path).
- Do not skip quoting for values your own code generated (timestamps, branch names, slugs) — a stray space or special character introduced upstream still breaks an unquoted interpolation downstream.

## Verification

- [ ] Every variable interpolated into a shell command or command string is quoted or passed as a separate array element, not concatenated unquoted.
- [ ] Values that could start with `-` are protected with `--` or an explicit path prefix before being passed positionally.
- [ ] No command is built via `eval`, `os.system`, or `sh -c` with untrusted or variable text concatenated into the string.
- [ ] For destructive or irreversible commands, the fully substituted command was printed/logged and inspected before execution.
- [ ] A quick test with a deliberately awkward value (a path containing a space) was considered for any new script that accepts file arguments.
