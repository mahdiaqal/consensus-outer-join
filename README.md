# ConsensusOuterJoin

Experimental one-to-one semantic full outer joins over independently fetched, commit-pinned public record tables.

## Problem and consensus boundary

Exact SQL/string joins miss synonyms; fuzzy scores can silently assign duplicate aliases to the wrong row. The contract materializes joined, left-only, right-only and unresolved records without forcing a match.

The contract fetches **both entire JSON tables inside the nondeterministic flow**. Every validator independently fetches them again, recomputes byte hashes, checks HTTP/UTF-8/schema constraints and derives every pair's semantic decision from the actual label and context. Exact report equality is required; there are no caller-provided confidence scores or threshold tolerances.

GenLayer is consequential: SAME/DIFFERENT/UNKNOWN judgments determine which full records can be paired. Hashes only bind acquired bytes; they never establish semantic identity.

```
Pinned public tables -> independent complete-body acquisition
                              |
                 independently reasoned pair matrix
                              |
                     exact report agreement
                              |
                deterministic one-to-one outer join
                 /          |          |          \
              JOINED     LEFT_ONLY  RIGHT_ONLY  UNRESOLVED
```

## Join semantics

For each left/right pair, SAME means equal concept and scope, DIFFERENT means clearly distinct, and UNKNOWN means insufficient information. Potential matches form temporary connected components for the query, not a persisted mutable graph.

Only an isolated one-left/one-right SAME component is joined. A component containing UNKNOWN is unresolved in its entirety. Any larger SAME component is AMBIGUOUS; no first-match, scoring, tie-break or maximum matching silently decides an identity. Isolated rows are preserved as left-only/right-only. Every acquired row appears exactly once in the output partition.

## Evidence schema and limits

```
{"schema":"join-table-v1","rows":[{"id":"A1","label":"physician","context":"A licensed medical practitioner who diagnoses and treats human illness."}]}
```

Each table has 1–5 rows, unique IDs, bounded strings and a maximum full response size of 5120 bytes. Row order is normalized by ID. Source URLs are constructed only for `raw.githubusercontent.com` using an explicit owner/repository/40-hex commit/path/64-hex SHA-256. Traversal, arbitrary hosts, branch names, truncation and duplicate JSON keys are rejected.

This joins **published descriptions**, not verified real-world persons, assets or facts. Commit pins provide historical reproducibility, not current freshness. Publishing both fixtures under one account is not independent authority corroboration. The demo is a controlled relational-data test, not third-party operational adoption.

## State and API

`materialize(nonce, owner, repo, commit, left_path, left_hash, right_path, right_hash)` creates an immutable result; `get_materialization(id)` returns acquisition, matrix and partition. `get_joined(id, root)` requires MATERIALIZED and the exact output root.

An evidence failure records BLOCKED with no joined output. Semantic uncertainty is preserved as unresolved components, without blocking unrelated certain matches. No graph proposals, owner-controlled version head, escrow, certificate or one-time consumption lifecycle. Domain-separated creator nonces prevent overwrite/replay; each creator has a 32-query bound.

## Tests

```
python -m pip install -r requirements.txt
genvm-lint check contracts/ConsensusOuterJoin.py
python -m pytest tests -q
npm ci
npm run test:sdk
```

28 local tests include all 19,683 three-by-three decision matrices and 81 transpose cases. Direct tests mock AI/web and run only the leader. A separate test executes the actual validator callback to reject decision, evidence and binding substitution; this is not a distributed disagreement test.

## Deploy

```
npm install -g genlayer@0.39.2
genlayer network set studionet
genlayer account use YOUR_ENCRYPTED_TEST_ACCOUNT
genlayer deploy --contract contracts/ConsensusOuterJoin.py
```

Never export keys. Confirm FINALIZED **and execution SUCCESS**, compare source, then read materialized rows. Optional scripts use an existing unlocked OS-vault account via `JOIN_TEST_ACCOUNT`; `JOIN_CLI_PATH` selects an installed CLI entrypoint. The CLI wrapper suppresses raw validator configuration and performs one-shot broadcasts. Check each receipt before the next transaction and never blindly repeat an uncertain broadcast.

See [architecture](docs/architecture.md), [threat model](SECURITY.md), [proof matrix](docs/proof-matrix.md), and [live proof ledger](LIVE_PROOFS.md). Experimental, unaudited; semantic consensus may share model errors. No production-safety or reviewer-acceptance guarantee.
