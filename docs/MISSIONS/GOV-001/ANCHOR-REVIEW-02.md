# GOV-001 - Anchor examination 02

Status: BLOCKED for direct verification of both original instruction anchors. This is an anchor-only examination, not a Gate decision or Owner acceptance. Date: 2026-11-05.

Reviewer declaration: Codex /root/anchor_verify_2026, a separate agent assigned this examination, not an author of the examined artifacts. This is not independent identity certification. The agent shares the runtime, system user and workspace; the user can alter both workspace and runtime records. No immutable custody or I2 isolation is claimed.

## Method and source access

Read AGENTS.md, agents/quality.md, docs/QUALITY_EVIDENCE_PROTOCOL.md, R-PLAN/GOV-001-R-PLAN-v15.md and ANCHOR-REVIEW-01.md. The evidence protocol, Gate 2 section, requires an eligible independent reader to read the anchor directly from the runtime message record before Owner acceptance. The comparison recorded by the Orchestrator is a declaration, not proof of the original instruction. This examination does not issue an I1 Gate decision.

Searched available tool descriptions for a runtime conversation, agent message or transcript reader. No tool was identified for the original collaboration instructions; the meeting transcript and document session tools describe different sources. Directly opened the local source record sessions/2026/11/05/rollout-2026-11-05T10-51-56-01a1ab1f-48f1-7ae3-8349-76fb791a245d.jsonl under the Codex user directory, using Python JSON parsing restricted to lines 305, 373 and 1458, and output only metadata. Lines 305 and 373 are followup_task calls targeting quality_r01; line 1458 targets quality_r03_g23. These locations alone do not establish that a particular call was the relevant commission. The message fields are opaque single strings without whitespace, and neither exact input hash occurs in their argument text. The instructions were not readable through this direct record access. No decoding, decryption, restriction bypass, or unrelated private content disclosure was attempted. The record is mutable by the shared user; locations are identifiers, not independent custody.

## Independently calculated sha256_lf and comparisons

All paths below are relative to docs/MISSIONS/GOV-001 unless otherwise stated. sha256_lf is SHA-256 of file bytes after replacing CRLF with LF. Values were calculated locally with Python -B. Readable reports and input hashes match each other; this does not establish what was transmitted in the original instruction.

- GATE2-INPUT-05.sha256: ccbcbc9a4cb28a06ed48569b5ce341efe7c3f4439986ad92eec62af6f4f92401. Same value appears in POST-GATE-VALIDATION-R01.md:7 and R01-GATE2-REVIEW-02.md:5 and R01-GATE3-REVIEW-02.md:5.
- GATE2-INPUT-10.sha256: bbe9300a58aa3fdf7e9bfa80372411d23a9b2ac4549773edf35cdbfaf0145a9f. Same value appears in POST-GATE-VALIDATION-R03.md:8 and R03-GATE2-REVIEW-04.md:22 and R03-GATE3-REVIEW-04.md:22.
- R01-GATE2-REVIEW-02.md: 678dbf7a4c7d19028766d71761475ee07de82ff006de7aa9b76bcadfb44b97d9; R01-GATE3-REVIEW-02.md: 020328f5c5520d8f1ddaf05976b7f3bf9c3795d519be30fc72039bb13b908b4b. Both match declarations in POST-GATE-VALIDATION-R01.md:8.
- R03-GATE2-REVIEW-04.md: 33bc758969bedecdc64eccae74ded71206ff95a92cf1f1ee56eeb051ec77d6a4; R03-GATE3-REVIEW-04.md: 0a32fa8b9224530828009f065097a04577715bbb06b7a9e36c4bcb7cdacd548c. Both match declarations in POST-GATE-VALIDATION-R03.md:9.
- R-PLAN/GOV-001-R-PLAN-v15.md: 1da8ab7b00ff988e525e850d401ff8ae82f4fd530111dabd75706dab2dc5f52a.
- ANCHOR-REVIEW-01.md: 122fc3ee1a549d713bc3d4b89a9910cc5a9fcf07010bcc29f097339c10c40aa6.
- POST-GATE-VALIDATION-R01.md: 632ac25e4a3bea2dfbbd7e57ef1c50bd4b7f4e56e6e9eb19c335099ac75f4c0b; POST-GATE-VALIDATION-R03.md: d3a24ab531e9d0f1c05a075edf9cf8ec7ddf5c9dd16503617f7edf4948193355.

## Execution and limits

Get-Content of mandated files, rg --files for the identified runtime session, Python -B metadata and hash comparisons, git status --porcelain --untracked-files=all, and git rev-parse HEAD each exited 0. HEAD observed: deee91c2bee87adce5d904b5529a4517a24a255c. Before creating this report, status included untracked ANCHOR-REVIEW-01.md, TEMP-CLEANUP-BLOCKED-01.md, TEMP-CLEANUP-OBSERVATION-02.md and five revalidation files. Concurrent changes may occur in this shared workspace.

No test, post-commit file comparison, manifest or code modification, Git write, or Gate adjudication was performed. The reports' statements about the original instruction do not replace its direct reading. Resolution requires an eligible reader to access the original instruction messages in readable form through an authorized mechanism, compare them with the relevant input hashes and report the custody limits.
