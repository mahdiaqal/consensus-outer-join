# Builder → Intelligent Contracts

## Title

ConsensusOuterJoin — Cardinality-Safe Semantic Record Joins

## Notes / Description

ConsensusOuterJoin materializes one-to-one semantic full outer joins. Leader and validators independently fetch commit-pinned JSON tables, verify full-body hashes and schemas, and reason over every record pair from actual labels and context. Exact acquisition and SAME/DIFFERENT/UNKNOWN agreement is required; no confidence tolerance or caller-supplied result controls output.

Only isolated unambiguous pairs are joined. Duplicate aliases remain AMBIGUOUS, UNKNOWN propagates across the whole potential-match component, and unmatched rows retain lineage. Evidence failure yields BLOCKED with no joined output. Results are immutable and bound to creator/nonce, source commitments and output root.

StudioNet proofs show a clean join, duplicate handling, bad-hash blocking and replay rejection. Source matches deployment; 28 tests cover all 19,683 3×3 matrices. This reconciles published descriptions, not real-world identity. No graph-update or certificate lifecycle.

## Evidence URLs

- GitHub Repository: https://github.com/mahdiaqal/consensus-outer-join
- GitHub File: https://github.com/mahdiaqal/consensus-outer-join/blob/main/contracts/ConsensusOuterJoin.py
- GitHub File: https://github.com/mahdiaqal/consensus-outer-join/blob/main/LIVE_PROOFS.md
- GitHub File: https://github.com/mahdiaqal/consensus-outer-join/blob/main/docs/proof-matrix.md
- GenLayer Explorer Contract: https://explorer-studio.genlayer.com/address/0x814C939149bB6CD0F369241a3860D651027A1471
- Other — clean join: https://explorer-studio.genlayer.com/tx/0x66858f9b0228cd64c72b51462319991f303736567937c782e50df5d350e8c036
- Other — duplicate handling: https://explorer-studio.genlayer.com/tx/0xc5f299ca282b54be1085278c1b1a369cbc920aa8084182d3e2a00363fd8315ce
- Other — integrity-negative BLOCKED result: https://explorer-studio.genlayer.com/tx/0x66193829a40bb0a87f41eead0af98974da86d86435b3c1cd8879c34a8c6b5467

The proof ledger also links deployment and expected replay error. These are controlled public fixtures, not independent-authority corroboration or evidence of third-party adoption. No production-safety or acceptance guarantee is claimed.
