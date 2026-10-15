# Architecture

## Ownership

Applications own previews, pagination and source selection. The contract owns independent HTTP acquisition, full-response commitments, normalization, semantic pair decisions, one-to-one cardinality and immutable materialization. Public publishers own source contents; they are not automatically trusted authorities. The output does not verify factual truth or real-world identity.

## Material difference

The durable state is a table of immutable relational query results, keyed by authenticated creator/nonce. There are no participant task sessions, knowledge graph mutations, owner-controlled proposal/version transitions, certificates, consumable approvals, classifier programs or irreversible circuit breakers. Temporary component traversal implements a cardinality constraint; it is not a versioned graph protocol.

The nondeterministic result is the complete pair matrix derived from fetched record bodies. The deterministic layer cannot compute synonym/context identity from the original state alone. Changing a matrix decision changes the materialized dataset; validators independently derive each decision and re-fetch the exact inputs.

## Data path

`pinned source coordinates -> complete HTTP responses -> SHA-256/strict schema -> normalized actual rows -> independent semantic matrix -> exact consensus -> immutable relational output`

Acquisition failure yields BLOCKED. Successful acquisition yields MATERIALIZED, which may include unresolved rows; MATERIALIZED is not a certificate or a claim that all identities are resolved. Consumers use the exact output root and only receive unambiguous pairs from `get_joined`.

## Cardinality rule

Build temporary bipartite edges for SAME or UNKNOWN. An UNKNOWN anywhere quarantines the entire connected component. A larger all-SAME component is AMBIGUOUS. Only a component with exactly one row from each side and a SAME edge yields a joined pair. Isolated rows retain lineage and are not dropped.

This conservative rule intentionally sacrifices recall. No score tolerance, greedy assignment, provider confidence, or first-row preference can overrule ambiguity. Identical label/context content cannot be reported DIFFERENT/UNKNOWN; this deterministic consistency check rejects contradictory AI output rather than silently accepting it.

## Scope

No latest-data claim: a commit pin is a historical snapshot. No source independence claim: the sources may share an owner. Source strings never execute. Onchain full bodies are public; do not submit private datasets. No asset custody or external writes.
