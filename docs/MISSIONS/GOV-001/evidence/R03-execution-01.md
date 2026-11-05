# GOV-R03: developer execution evidence

This is an author execution record, not a Quality decision. The changes are uncommitted.

- Before changes: 19 test methods, 68 executed subtests, 0 failures/errors.
- After changes: python -B -m unittest discover -s tests -q, exit 0; 30 test methods, 81 executed subtests, 0 failures/errors. Eleven new methods are in tests/test_governance_v3.py; 19 existing methods were adapted to the new contract. Subtest counts are from unittest.TestResult.addSubTest, not assertions.
- python -B scripts/quality_cli.py validate, exit 0; structural/metadata consistency only.
- can-implement --mission GOV-001 remains BLOCKED, exit 1; the manifest Gates and owner remain PENDING.
- Nine isolated mutations in a temporary copy were attempted: authorship, isolation, required evidence, report hash, evidence hash, third-party verification, pinned artifact, review equalities, and isolation-policy monotonicity. Eight were initially detected by the new test suite; the I0 mutation initially survived. Added test_i0_never_enables_even_if_policy_attempts_to_allow_it and reran that mutation: exit 1, detected. These are grouped mutations, not evidence that every negative scenario in v15 has an individual mutation control.
- mission.v2.json preserves the pre-migration working file bytes: SHA-256 2c84fa7ed86018c963c00f02fdf60449d7501fcd3e03300dcff490569a036feb. The prior Git blob has different line endings; sha256_lf matches. Byte preservation through the eventual commit requires a raw blob comparison.
- E2E NO EJECUTADO. Gate 2/3 technical review and independent tests remain pending.
