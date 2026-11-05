# Quality evidence protocol

## Every Gate

Identify the mission and exact reviewed version, authors, reviewer, sources, findings, result, execution evidence and limitations. The CLI checks document consistency and hashes, not the truth of content, real identities or isolation. The narrative is not parsed by the CLI. Reviews contain exactly one structured protheusai-review JSON block.

Authorship (A), operational isolation (B) and evidence traceability (C) are separate. PASS and PASS_WITH_RESERVATIONS always require a reviewer outside all author roles and an explicit true authorship declaration. I0 never suffices. The reviewer declares isolation: I0 shared context; I1 separate context without author history or memory, possibly sharing runtime, system user, workspace and credentials; I2 I1 plus imposed read-only permissions; I3 separate machine, organization or custody. I1 assignments carry objective, references and hashes; summaries must be source-checkable or declared otherwise. The CLI never certifies isolation.

The applicable matrix is quality/controls.json independence_minimums. G0 requires no evidence. G1 requires recorded files for each evidence type specified by the applicable rule, with recalculated sha256_lf. G2 additionally requires third-party records verifying the reviewer and pertinent authors; those third parties cannot be the reviewer or any author. These are recorded verifications, not identity certification or verification of isolation. Evidence kinds are identity, isolation and execution. The report, mission.json, six mission template files and the reviewed artifact are excluded as evidence. Evidence files must have canonical relative mission paths and match their hashes.

The SHA-256 of bytes after CRLF-to-LF replacement is sha256_lf. The CLI recalculates report, evidence and path-backed sha256_lf artifact hashes; other hash and git references are declared identifiers, not checked by Git. A review block ties mission, gate, risk and decision to the manifest, and identifies reviewer, nonempty pertinent effective authors, artifact, declared isolation, evidence and date. FAIL remains traceable but does not require A/B/C minima. PWR never enables transition.

## Gate 1

Review contracts, negative cases, dependencies, identity changes, migration, rollback and test plan. A technical review does not itself certify implementation or enable a transition.

## Gate 2

For MEDIUM and above the orchestrator records git status --porcelain --untracked-files=all and sha256_lf for each changed or new file in append-only, cycle-numbered GATE2-INPUT-<nn>.sha256. Before commissioning review, transmit that input hash in the instruction, or a git reference if the artifact is already committed. The reviewer cites the same reference.

After commit compare every committed change, including new or deleted paths, to the input and compare the report reference against the instruction; append results in POST-GATE-VALIDATION-<suffix>.md. Allowed additions are review reports, identity/isolation/execution evidence for ongoing Gates, gate decision and review entries, owner acceptance and 06-DECISION.md, post-Gate validations and hash citations. Any other difference reopens Gate 2.

Before Owner acceptance the Owner or a Quality reviewer who does not issue an I1 Gate decision in that mission reads the anchor directly from the runtime message record. The Gate 3 reviewer can inspect the orchestrator comparison as a declaration. Shared user permissions can permit alteration of the workspace, input and runtime message record. The comparison is necessary but not sufficient and the CLI does not perform it; if the comparison or independent anchor reading is omitted the discrepancy is not detected.

## Gate 3

Record actual commands, exact artifact, environment, runtime, date, exit code and results, including negative cases. E2E NO EJECUTADO when applicable evidence is absent.

## Record handling

Gate inputs and evidence are append-only. A lost record requires an incident and may only be replaced with a declared reconstruction checked against a hash recorded before the loss. The CLI does not enforce this rule. It never issues a Quality PASS or certifies identity.

Historical v1 and decided v2 manifests are structural records only and cannot enable transitions. Pending v2 manifests can be migrated without inheriting approvals; see docs/MISSIONS/README.md.
