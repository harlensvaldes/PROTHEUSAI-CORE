# GOV-R03: developer execution evidence, cycle 02

Author-produced evidence, not an independent Quality decision. Original cycle 01 evidence and FAIL/PENDING reports are preserved.

- G2 finding 1: synthetic accepted v3 missions with owner approved_by or date consisting only of spaces, or approver U+200B, previously passed; a focused test first failed for blank fields and then passed after checking canonical approver and stripped date. These cases must not enable can-close.
- Full suite: python -B -m unittest discover -s tests, custom unittest addSubTest counter, exit 0; 111 test methods run, 145 subtests, 0 failures/errors, 1 skipped. The skipped case is a real symlink requiring Windows privilege (WinError 1314); it is not counted as passed. A separate simulated symlink check and a real NTFS junction check ran.
- Mutation suite: 75 methods run, 74 passed, 1 skipped, exit 0. Each method identifies a mutant and test; several use combined mutants because of redundant defenses. The parser block-missing and invalid-JSON controls use a permissive parser simulation. See test_governance_mutations.py for exact cases; results must not be read as independent proof that every v15 negative has a separate mutation.
- The pre-migration manifest raw backup and original decision/plan history are retained. Formal Gates and owner acceptance remain PENDING. No R03 commit or independent Gate 2/3 PASS has occurred.
- E2E NO EJECUTADO.
