# GATE2 review

Narrative, findings, evidence, limitations and the reviewer declaration belong here.

```protheusai-review
{
  "mission": "GOV-002",
  "gate": "gate2",
  "risk": "HIGH",
  "decision": "PENDING",
  "reviewer": "",
  "artifact": {
    "name": "",
    "ref": "",
    "path": null
  },
  "effective_authors": [],
  "authorship_independent": false,
  "isolation": "I0_CONTEXTO_COMPARTIDO",
  "evidence": [],
  "date": ""
}
```

Before review, record git status --porcelain --untracked-files=all and sha256_lf of each changed or new file in append-only GATE2-INPUT-<nn>.sha256. Send its sha256_lf or committed git reference in the review instruction. After commit compare every committed change with the input and compare the review reference to the instruction; append the result in POST-GATE-VALIDATION-<suffix>.md. Before Owner acceptance the Owner or a Quality reviewer who does not issue a Gate decision for the mission reads the anchor from the runtime message record. The Gate 3 reviewer treats the comparison as a declaration. See QUALITY_EVIDENCE_PROTOCOL.md for allowed additions and residual risk.
