---
name: code-reuse-licensing
description: Check license compatibility and attribution requirements before incorporating code, text, or assets copied or adapted from another repository, Stack Overflow answer, blog post, or generated-from-a-specific-source snippet into a project. Use whenever an agent reuses more than a trivial fragment of someone else's published code or content rather than writing it from the task's own requirements.
---

# Code Reuse Licensing

An agent that answers "how do I do X" by pasting a snippet it found, adapting a GitHub file, or reproducing a Stack Overflow answer can silently import that source's license obligations (attribution, copyleft, non-commercial restrictions) or outright proprietary terms into the target project. The failure is invisible in a diff — the copied lines look like ordinary code — so it has to be caught at the point of reuse, not discovered later.

## Procedure

1. **Decide whether this is reuse or original authoring.** Writing an implementation from the task's requirements, well-known idioms, or your own reasoning is not reuse. Copying, closely paraphrasing, or algorithmically translating a specific external file/answer/snippet into the project is reuse — treat anything beyond a short, generic pattern (a standard loop, a common regex, a boilerplate config key) as reuse.
2. **Identify the source's license before including anything non-trivial.** For a GitHub/GitLab repo, check its `LICENSE`/`LICENSE.md` file and any per-file notices — don't assume MIT because the repo "feels open source." For Stack Overflow or similar Q&A content, treat answers as CC BY-SA (attribution required, and copyleft-like share-alike terms apply to the exact reused text). For a blog, docs site, or tutorial, check its stated terms or copyright notice; absence of an explicit license means default copyright applies and reuse is not implicitly permitted.
3. **Match the license's obligations to the target project before copying.** Permissive licenses (MIT, BSD, Apache-2.0) generally allow reuse with attribution retained; copyleft licenses (GPL, AGPL, LGPL) can obligate the receiving project to the same license terms; CC BY-SA requires attribution plus share-alike; "no license" or explicit proprietary/all-rights-reserved terms mean reuse is not authorized at all. If the target project's license is incompatible, or it's unclear, do not include the snippet — write an original implementation instead.
4. **Preserve required attribution and notices.** When a license permits reuse with attribution, keep the original copyright header/notice intact or add an equivalent comment citing the source, author, and license right next to the reused block — don't strip attribution to make the diff look cleaner.
5. **Keep direct reproduction to the minimum necessary.** Prefer reimplementing the underlying approach in the project's own style over copying verbatim, especially for anything beyond a short utility function; large verbatim blocks carry more license and provenance risk than an original solution inspired by the same idea.
6. **Treat "scrape this other repo for skills/content/structure" instructions the same way.** Mirroring another project's file layout or generic naming conventions is fine; copying its actual prose, code, or curated content wholesale is reuse and needs the same license check — do not bulk-copy another repository's files on the assumption that "it's public" means "it's free to reuse here."
7. **When the license or permission is genuinely unclear, don't guess permissive.** Escalate or omit the reused content (see autonomous-escalation-triggers) rather than assuming the most convenient license applies.

## Guardrails and pitfalls

- Do not assume a public GitHub repo is unlicensed-and-therefore-free-to-use; "public" and "permissively licensed" are different things, and a repo with no LICENSE file retains full copyright by default.
- Do not treat a generated snippet that was produced by closely paraphrasing one specific source as original just because no literal string matches — share-alike and copyleft obligations attach to derivative work, not only verbatim copies.
- Do not drop a source's copyright/attribution comment to make a file look self-authored.
- Do not mix incompatible licenses into one file or module (e.g., GPL-licensed code pasted into an MIT-licensed project) without flagging the conflict.
- Do not rely on the Stack Overflow snippet "looking too simple to be copyrightable" as a blanket excuse; apply judgment to genuinely trivial boilerplate only, not to the whole answer.

## Verification checklist

- [ ] Every non-trivial reused snippet's source and license were identified before inclusion, not assumed.
- [ ] The source license's terms are compatible with the target project's license, or the snippet was rewritten/omitted instead.
- [ ] Required attribution/copyright notices from the source are present in the final files.
- [ ] No large verbatim block was copied where an original, equivalent implementation would have avoided the licensing question entirely.
- [ ] Any case where the license or permission could not be confirmed was reported rather than resolved by assuming it was safe to use.
