# Quality evidence protocol

## v5 local fictional experimental profile

For v5 `LOCAL_FICTIONAL_EXPERIMENTAL`, `scope` contains exactly `profile`, `project_id`, and `owner_decision_ref`. The reference identifies an existing Owner decision; it is a declaration and need not be a new document. Each review block adds `scope_digest` and `reviewer_session` (a declared session identifier when available, otherwise null). Compute the digest as SHA-256 of UTF-8 `json.dumps(scope, sort_keys=True, ensure_ascii=True, separators=(',', ':'), allow_nan=False)` with no newline. The reviewer must differ from declared authors, state authorship independence, declare a real I0–I3 isolation token and identify the reviewed artifact. I0/G0 are allowed only for this profile; they prove neither identity nor isolation. Evidence voluntarily supplied still requires valid paths and hashes. For MEDIUM/HIGH, Gate 2 retains its existing pinned input requirements; Gate 3 retains actual test execution, commands and results in the report.

Changing any scope value invalidates reviews retaining the old digest; scope changes require new mission history and Owner decision as applicable. A restored value can reproduce the old digest; it does not prove absence of intermediate changes or revocation. The CLI does not authenticate the Owner, reviewer or reference, and cannot verify the real profile. Orchestrator and Quality consult accessible source decisions under normal responsibilities; unresolved contradictions and changed real scope are handled under AGENTS.md. No v1–v4 review block gains v5 fields or changes meaning.

## Every Gate

Identify the mission and exact reviewed version, authors, reviewer, sources, findings, result, execution evidence and limitations. The CLI checks document consistency and hashes, not the truth of content, real identities or isolation. The narrative is not parsed by the CLI. Reviews contain exactly one structured protheusai-review JSON block.

Authorship (A), operational isolation (B) and evidence traceability (C) are separate. PASS and PASS_WITH_RESERVATIONS always require a reviewer outside all author roles and an explicit true authorship declaration. I0 never suffices under the ordinary v1–v4 rules; the separately authorized v4 waiver retains its existing limited exception. I0 is admissible under the ordinary v5 local fictional experimental profile described above. The reviewer declares isolation: I0 shared context; I1 separate context without author history or memory, possibly sharing runtime, system user, workspace and credentials; I2 I1 plus imposed read-only permissions; I3 separate machine, organization or custody. I1 assignments carry objective, references and hashes; summaries must be source-checkable or declared otherwise. The CLI never certifies isolation.

The applicable matrix for v3/v4 is quality/controls.json independence_minimums, subject to the existing narrowly scoped v4 waiver. The separate v5 local fictional experimental profile uses the I0/G0 rule above rather than that matrix; v1/v2 historical records retain their existing treatment. G0 requires no identity evidence. G1 requires recorded files for each evidence type specified by the applicable rule, with recalculated sha256_lf. G2 additionally requires third-party records verifying the reviewer and pertinent authors; those third parties cannot be the reviewer or any author. These are recorded verifications, not identity certification or verification of isolation. Evidence kinds are identity, isolation and execution. The report, mission.json, six mission template files and the reviewed artifact are excluded as evidence. Evidence files must have canonical relative mission paths and match their hashes.

The SHA-256 of bytes after CRLF-to-LF replacement is sha256_lf. The CLI recalculates report, evidence and path-backed sha256_lf artifact hashes; other hash and git references are declared identifiers, not checked by Git. A review block ties mission, gate, risk and decision to the manifest, and identifies reviewer, nonempty pertinent effective authors, artifact, declared isolation, evidence and date. FAIL remains traceable but does not require A/B/C minima. PWR never enables transition.

## Gate 1

Review contracts, negative cases, dependencies, identity changes, migration, rollback and test plan. A technical review does not itself certify implementation or enable a transition.

For the optional v4 owner waiver, Gate 1 remains PENDING with no gate review; `gate1_waiver.technical_review` identifies a separate technical PASS with the usual structured block. Only the I0 prohibition and I1/G1 identity minima are excepted in this specific HIGH local-fictional path. A reviewer distinct from all declared author roles, authorship declaration, report and artifact integrity, and `execution` evidence remain mandatory. Recorded prior FAIL reports retain their exact byte hashes. This records the history presented; completeness, owner identity, actual agent separation and authorization remain human checks. Expiry or any recorded revocation prevents new action but does not rewrite prior history. `validate` reports structural consistency without certifying historical authorization; `can-implement` and `can-close` return nonzero and request manual Owner verification rather than granting authority.

For accepted v4 records, structural validation uses a synthetic baseline waiver rule, not proof of the policy or pinned-artifact rule actually in force at acceptance. Current matrix differences generate warnings; transition checks reapply current requirements. The Owner must inspect historical policy and evidence independently; the CLI cannot reconstruct them.

## Gate 2

For MEDIUM and above the orchestrator records git status --porcelain --untracked-files=all and sha256_lf for each changed or new file in append-only, cycle-numbered GATE2-INPUT-<nn>.sha256. Before commissioning review, transmit that input hash in the instruction, or a git reference if the artifact is already committed. The reviewer cites the same reference.

After commit compare every committed change, including new or deleted paths, to the input and compare the report reference against the instruction; append results in POST-GATE-VALIDATION-<suffix>.md. Allowed additions are review reports, identity/isolation/execution evidence for ongoing Gates, gate decision and review entries, owner acceptance and 06-DECISION.md, post-Gate validations and hash citations. Any other difference reopens Gate 2.

Before Owner acceptance the Owner or a Quality reviewer who does not issue an I1 Gate decision in that mission reads the anchor directly from the runtime message record. The Gate 3 reviewer can inspect the orchestrator comparison as a declaration. Shared user permissions can permit alteration of the workspace, input and runtime message record. The comparison is necessary but not sufficient and the CLI does not perform it; if the comparison or independent anchor reading is omitted the discrepancy is not detected.

## Gate 3

Record actual commands, exact artifact, environment, runtime, date, exit code and results, including negative cases. E2E NO EJECUTADO when applicable evidence is absent.

## Record handling

Gate inputs and evidence are append-only. A lost record requires an incident and may only be replaced with a declared reconstruction checked against a hash recorded before the loss. The CLI does not enforce this rule. It never issues a Quality PASS or certifies identity.

Historical v1 and decided v2 manifests are structural records only and cannot enable transitions. Pending v2 manifests can be migrated without inheriting approvals; see docs/MISSIONS/README.md.
