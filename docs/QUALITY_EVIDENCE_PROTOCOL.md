# Quality evidence protocol

## v5 local fictional experimental profile

For v5 `LOCAL_FICTIONAL_EXPERIMENTAL`, `scope` contains exactly `profile`, `project_id`, and `owner_decision_ref`. The reference identifies an existing Owner decision; it is a declaration and need not be a new document. Each review block adds `scope_digest` and `reviewer_session` (a declared session identifier when available, otherwise null). Compute the digest as SHA-256 of UTF-8 `json.dumps(scope, sort_keys=True, ensure_ascii=True, separators=(',', ':'), allow_nan=False)` with no newline. The reviewer must differ from declared authors, state authorship independence, declare a real I0–I3 isolation token and identify the reviewed artifact. I0/G0 do not prove identity or isolation. Evidence voluntarily supplied still requires valid paths and hashes. For MEDIUM/HIGH, Gate 2 retains its existing pinned input requirements; Gate 3 retains actual test execution, commands and results in the report.

Changing any scope value invalidates reviews retaining the old digest; scope changes require new mission history and Owner decision as applicable. A restored value can reproduce the old digest; it does not prove absence of intermediate changes or revocation. The CLI does not authenticate the Owner, reviewer or reference, and cannot verify the real profile. Orchestrator and Quality consult accessible source decisions under normal responsibilities; unresolved contradictions and changed real scope are handled under AGENTS.md. No v1–v4 review block gains v5 fields or changes meaning.

## Every Gate

Identify the mission and exact reviewed version, authors, reviewer, sources, findings, result, execution evidence and limitations. The CLI checks document consistency and hashes, not the truth of content, real identities or isolation. The narrative is not parsed by the CLI. Reviews contain exactly one structured protheusai-review JSON block.

Authorship, operational isolation and traceability are distinct. PASS and PASS_WITH_RESERVATIONS retain a distinct declared reviewer and authorship declaration where the available records establish them. I0 is admissible at any risk; higher isolation may be declared when evidenced, but is not mandatory. Neither a declared identifier nor the CLI certifies identity or isolation.

The current matrix for v3/v4 permits I0/G0 and retains execution evidence and pinned inputs according to risk. The v5 profile retains its own scope and evidence rules; v1/v2 retain historical treatment. Evidence voluntarily supplied must use canonical relative mission paths and match its hash. The report, mission.json, six mission template files and reviewed artifact are excluded as evidence. A lack of identity or isolation certification alone does not block a decision.

The SHA-256 of bytes after CRLF-to-LF replacement is sha256_lf. The CLI recalculates report, evidence and path-backed sha256_lf artifact hashes; other hash and git references are declared identifiers, not checked by Git. A review block ties mission, gate, risk and decision to the manifest, and identifies reviewer, nonempty pertinent effective authors, artifact, declared isolation, evidence and date. FAIL remains traceable; PWR is not PASS. `can-implement` reports review status via its exit code; it does not grant or deny the Owner's authorization or the runner's permissions.

## Gate 1

Review contracts, negative cases, dependencies, identity changes, migration, rollback and test plan. A technical review does not itself certify implementation or enable a transition.

For the optional v4 owner waiver, Gate 1 remains PENDING with no gate review; `gate1_waiver.technical_review` identifies a separate technical PASS with the usual structured block. Only the I0 prohibition and I1/G1 identity minima are excepted in this specific HIGH local-fictional path. A reviewer distinct from all declared author roles, authorship declaration, report and artifact integrity, and `execution` evidence remain mandatory. Recorded prior FAIL reports retain their exact byte hashes. This records the history presented; completeness, owner identity, actual agent separation and authorization remain human checks. Expiry or any recorded revocation prevents new action but does not rewrite prior history. `validate` reports structural consistency without certifying historical authorization; `can-implement` and `can-close` return nonzero and request manual Owner verification rather than granting authority.

For accepted v4 records, structural validation uses a synthetic baseline waiver rule, not proof of the policy or pinned-artifact rule actually in force at acceptance. Current matrix differences generate warnings; transition checks reapply current requirements. The Owner must inspect historical policy and evidence independently; the CLI cannot reconstruct them.

## Gate 2

For MEDIUM and above the orchestrator records git status --porcelain --untracked-files=all and sha256_lf for each changed or new file in append-only, cycle-numbered GATE2-INPUT-<nn>.sha256. Before commissioning review, transmit that input hash in the instruction, or a git reference if the artifact is already committed. The reviewer cites the same reference.

After commit compare every committed change, including new or deleted paths, to the input and record the result in POST-GATE-VALIDATION-<suffix>.md. Compare the report reference to the instruction when its content is available; document an unreadable historical instruction as a limitation. Material differences in the reviewed artifact require a new review.

Before Owner acceptance compare the reviewed artifact and committed bytes where applicable. If a historical instruction is not readable, record that limitation without reconstructing its content; its absence alone does not block progress when current technical evidence is sufficient. The CLI cannot authenticate messages, Git references, or the provenance of the comparison.

## Deterministic anchor checks

The CLI offers two read-only checks for the mechanical comparisons that reviewers used to perform manually. `manifest <path>` recalculates the sha256_lf of every declared entry against the current tree and returns 0 when all match, 1 for mismatches, missing files, non-canonical paths, duplicates, ambiguous entries or a readable manifest without entries, and 2 when the manifest cannot be read or decoded. Prose and `#` comments are ignored, including comments containing a hash; any `git status --porcelain` token is accepted. Because it verifies the current tree, a historical manifest may legitimately no longer match after later changes.

`audit --mission <ID>` reuses the record checks and cross-checks registered review and evidence hashes with the anchors of the mission's manifests. A registered hash that matches no anchor is a discrepancy; a hash that matches an older cycle is reported as stale; drift between the effective anchor and the current file is advisory. Manifest anchors are repository-relative while record paths are mission-relative, so the cross-check maps the latter to `docs/MISSIONS/<ID>/<path>`. A manifest that cannot be read takes precedence (2). Product/governance classification is informative and never changes Gate membership. Neither command issues a Quality verdict, authenticates identities or isolation, or enables a transition.

## Gate 3

Record actual commands, exact artifact, environment, runtime, date, exit code and results, including negative cases. E2E NO EJECUTADO when applicable evidence is absent.

## Record handling

Gate inputs and evidence are append-only. A lost record requires an incident and may only be replaced with a declared reconstruction checked against a hash recorded before the loss. The CLI does not enforce this rule. It never issues a Quality PASS or certifies identity.

Historical v1 and decided v2 manifests are structural records only and cannot enable transitions. Pending v2 manifests can be migrated without inheriting approvals; see docs/MISSIONS/README.md.
