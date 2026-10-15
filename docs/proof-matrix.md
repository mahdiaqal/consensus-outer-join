# Proof matrix

| Case | Required output | Local evidence | Live evidence |
|---|---|---|---|
| Synonyms with unique partners | Two joined pairs; unmatched rows retained | direct mock | Pending |
| Duplicate aliases | Ambiguous component; unaffected pair retained | direct mock | Pending |
| UNKNOWN bridging two pairs | Whole connected component unresolved | direct/helper tests | Not claimed |
| Wrong byte commitment | BLOCKED; empty joined output | direct mock | Pending |
| HTTP/schema/encoding/size failure | BLOCKED | direct mock | Not claimed |
| Nonce replay | Error; immutable result unchanged | direct mock | Pending |
| Changed semantic label/evidence/binding | Actual validator callback rejects | callback unit test | Not claimed |
| Identical contents reported different | Rejected before materialization | helper test | Not claimed |
| Every 3×3 label matrix | Each row partitioned exactly once; no ambiguous joined pair | 19,683 exhaustive matrices | Not a live test |

28 tests pass. Unit mocks are not distributed consensus. Actual live receipts must be FINALIZED with successful execution, followed by source equality and row/root readback. Expected-error transactions are never counted as successful executions.
