# Missions

Create a mission with python scripts/new_mission.py --id APP-001 --title "First mission" --risk MEDIUM --orchestrator orch-01 --architect arch-01. New schema v3 Gates start PENDING with review null; developer remains unassigned until actual work.

A review is a single protheusai-review JSON block in a report, with the manifest storing only decision and review {file, sha256_lf, reviewer_verification}. See QUALITY_EVIDENCE_PROTOCOL.md and quality/controls.json for the A/B/C dimensions, evidence, risk matrix and limitations. The CLI validates consistency, not reviewer identity, isolation, truth or Quality certification. PWR never enables transitions.

v1 and v2 manifests with any non-PENDING Gate are historical: validate checks structure only and emits a warning, without extending their approvals; can-implement and can-close never enable them. v2 with every Gate PENDING can migrate mechanically to v3. If preserving a v2 manifest, record its raw SHA-256 and rename the unchanged bytes to mission.v2.json; then create a v3 manifest with new PENDING Gates. Do not infer identities or transfer prior approvals.

Derived projects must upgrade quality/controls.json to schema_version 2 with complete independence_minimums. Without a valid monotonic matrix the v3 CLI fails closed.
