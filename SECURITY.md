# Security

Experimental and unaudited. Model agreement is not formal semantic correctness. A malicious source can contain prompt injection or misleading descriptions; prompts delimit data but cannot guarantee immunity. The output reconciles published strings, not external facts or persons. Applications need independent trust rules before relying on it for identity, authorization or funds.

## Defenses

- HTTPS fixed-host/commit/path source construction; no arbitrary URL or path traversal.
- Entire bounded UTF-8 bodies, exact byte hashes and strict table schemas; no truncation or hashes standing in for meaning.
- Duplicate JSON keys/row IDs rejected; semantic duplicates deliberately remain distinct so cardinality ambiguity is visible.
- Validators acquire sources themselves and recompute every pair decision; complete report equality, no confidence tolerance.
- Deterministic evidence binding and identical-content consistency checks before materialization.
- UNKNOWN propagates through its whole potential-match component. Duplicate aliases cannot be greedily paired.
- Immutable contract/creator/nonce binding, output root and root-bound consumer reads. No reset or overwrite operation exists.
- Bounded tables (5×5), bodies, strings and creator query count. Sybil accounts can bypass per-creator limits; public network resource protections still apply.

Unavailable sources are BLOCKED. Divergent valid reports fail consensus and do not create a fake application CONFLICTED state. Historical evidence is reproducible, not necessarily fresh. Full source bodies are public in the resulting record; use public fixtures only.

No arbitrary interpreter, eval, asset movement, reentrancy-bearing external contract calls, upgrade proxy, key handling or issuer settlement authority. Report issues privately to the maintainer.
