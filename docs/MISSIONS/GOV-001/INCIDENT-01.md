# INCIDENT-01: loss of Gate 2 cycle 1 input

**Severity:** LOW (process, G2-10). **Status:** OPEN, owner acceptance pending.

## What happened and impact

According to copilot-sdk-main in 03-IMPLEMENTATION.md:103-104, the Orchestrator/Developer deleted GATE2-INPUT.sha256 while regenerating the Gate 2 input during cycle 2 on 2026-11-05. The precise time is not documented. GATE2-REVIEW-02.md documents discovery and impact. The original reviewed input is lost and cannot itself be inspected; the remaining trace depends on previously recorded hash and reviewer records. No business data, user or service impact is asserted.

## Containment and recovery

GATE2-INPUT-01.RECONSTRUCTED.sha256 is a declared reconstruction, not the original. Its raw SHA-256 is f0f7392a971467ad7816da81ae7bef57323249e36f0ac10c0838dbc1768c4a9b, recorded in GATE2-REVIEW-01.md and GATE3-EVIDENCE-01.md before the reconstruction script. The author and Quality cycle 1 reported producing 38 entries with this hash, without accredited independence. Provenance of 12 partial hashes is author-declared and not accredited. The earlier search for copies is declared, not established, in R-PLAN/GOV-001-R-PLAN-v8.md.

Reproduce in a clean clone with core.autocrlf true and again false: python -B docs/MISSIONS/GOV-001/GOV-R01-reconstruct.py --repo . --commit 6e5e929. The script reads Git blobs and reports MATCH or NO MATCH; .gitattributes protects the reconstructed file's bytes only.

## Explicit corrections without altering the originals

03-IMPLEMENTATION.md:104 states that byte-for-byte reconstruction is impossible; GATE2-REVIEW-02.md:44,64 expresses the resulting limitation. A reconstruction now has the pre-recorded hash. This does not recover the original or establish independent provenance of the partial inputs. Original records remain intact.

## Cause and prevention

The deletion during regeneration is declared; no further root cause is accredited. Gate inputs and evidence are append-only and numbered by cycle. Lost records require an incident and a declared reconstruction checked against a hash recorded before loss. This is a documentary rule, not enforced by the CLI.

## Evidence and follow-up

See R-PLAN for plans and reviews, and the reconstruction script. Independent technical review and post-commit comparison are pending. The Owner decides incident acceptance.
