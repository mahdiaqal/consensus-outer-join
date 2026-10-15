# Live proofs

## Deployment — 2026-10-14

- Network: gasless StudioNet, chain ID 61999.
- Contract: [0x814C939149bB6CD0F369241a3860D651027A1471](https://explorer-studio.genlayer.com/address/0x814C939149bB6CD0F369241a3860D651027A1471).
- Dedicated test signer: `0x7a413BB4AB62E31d62d4cD9efC8C8a8Dae37FB42`, encrypted native CLI/OS-vault signing, no key export.
- Pinned contract/fixture commit: `a9c5d823c8e336ca734fa3cbe9feb192f56b9ac8`.
- Explorer/RPC source matches the tested contract file after LF/trailing-newline normalization.
- Source SHA-256: `132d1281b6e5683501625da830559077ebc5c7f75c1b011bc344618f7645fd12`.

Deployment [c6d77347…](https://explorer-studio.genlayer.com/tx/0xc6d7734719a38ff9aad3f12f43fb46db02b8a1cce7eee78fdf8c707cbfc96049) finalized with leader execution SUCCESS and MAJORITY_AGREE.

## Verified clean join

Transaction [66858f9b…](https://explorer-studio.genlayer.com/tx/0x66858f9b0228cd64c72b51462319991f303736567937c782e50df5d350e8c036) finalized with SUCCESS and MAJORITY_AGREE.

Readback: L1 motorcar ↔ R1 automobile; L2 physician ↔ R3 doctor; L3 pear remains left-only; R4 granite remains right-only. Both fetched source bodies were HTTP 200 with exact committed byte hashes. The complete three-by-three semantic matrix is stored onchain.

- Materialization ID: `aea169e45456316eb661b1f3afe873f4e99b5330fbcab41c3b5a35bbf8f8c613`.
- Result root: `ed42c53c7bdecf887aa06245b42067aba7f5ea6a75b18261d54b8936da3a510d`.

## Verified duplicate-alias join

Transaction [c5f299ca…](https://explorer-studio.genlayer.com/tx/0xc5f299ca282b54be1085278c1b1a369cbc920aa8084182d3e2a00363fd8315ce) finalized with SUCCESS and MAJORITY_AGREE.

The independently derived matrix marks L1 motorcar equal to both R1 automobile and R2 car. The deterministic one-to-one operator does **not** choose either alias: it records `{left:[L1],right:[R1,R2],reason:AMBIGUOUS}`. The unrelated L2 physician/R3 doctor pair remains joined; pear and granite remain unmatched. No record is lost or assigned twice.

- Materialization ID: `b9e6ea24c3c26a381ead26ca7e3623651028b8c2178a52ba3260d3db5ccd88c4`.
- Result root: `0a50142e96717b0b041b37faede96a1b2a786a6503abd77fc41642bb9b49a4c5`.

## Verified integrity failure

Transaction [66193829…](https://explorer-studio.genlayer.com/tx/0x66193829a40bb0a87f41eead0af98974da86d86435b3c1cd8879c34a8c6b5467) finalized with SUCCESS and MAJORITY_AGREE. This is successful execution of the **negative evidence path**, not a successful join.

The real left body was acquired with HTTP 200, but its actual SHA-256 differed from the deliberately wrong expected commitment. The result is BLOCKED, with an empty matrix and empty joined/unmatched/unresolved output. The consumer method refuses this result even with its correct root.

- Materialization ID: `ae01a2328407bd4490a0a21c71ffa00a887ce2b179110fc4a165ef4613abbdb5`.
- Result root: `802fdd23f039781af06b1436ee2d89a863155dfa1f0e3375a075b8cb7f1c0224`.

## Expected replay error — not successful execution

Transaction [ece541da…](https://explorer-studio.genlayer.com/tx/0xece541da5e7d95e381cf5de9cff24e011b263529bd69a0601f0e77059a1242e0) finalized with execution ERROR and MAJORITY_AGREE. Its decoded stderr contains `Materialization nonce used`. The clean result was not overwritten.

There are **four successful finalized executions** (deployment, clean join, duplicate-aware join, integrity-negative BLOCKED result) and **one expected execution error**. Do not describe these as five successful joins.

## Evidence byte commitments

All source URLs use owner `mahdiaqal`, repository `consensus-outer-join`, and the full commit above. These exact public raw bytes were also downloaded outside the contract and compared with the local fixtures.

| Path | SHA-256 |
|---|---|
| `examples/left.json` | `06bfb86fb74da02eacf927ce672a7c188cc322e0a508032cfa2e4fc3fe134ac8` |
| `examples/right-clean.json` | `d933437826f60a9b7c2a948fd6346368eab5c10200d91ce87cb38cb489a9cef2` |
| `examples/right-duplicate.json` | `333341f0be9a374e4f9f364845127c9e5c79af81ea01378cb19e3658266628bf` |

## Reproduction and scope

Use `node scripts/check.mjs success TX`, `error TX EXPECTED_TEXT`, `source ADDRESS`, and `state ADDRESS SIGNER`. The state verifier recomputes output roots, acquired body hashes, source/identity binding and the full outer partition and checks root-bound consumer behavior. Transport failures are errors, not successful blocked reads. A transient RPC read failure occurred during verification; only reads were retried and no transaction was rebroadcast.

The demo runner accepts `clean`, `duplicate`, `badhash`, or `replay` followed by the contract and fixture commit. Do not replay it blindly: existing nonces will revert. Fresh nonces are necessary for a separate run.

Fixtures are controlled published test data, not independently authoritative facts or real adoption. They demonstrate actual contract-side acquisition and semantic relational transformation, not verification of real-world identities. Commit pins provide historical reproducibility, not current freshness.

28 local tests, all 19,683 three-by-three decision matrices, 81 transpose cases and three SDK calldata roundtrips pass. Direct mocks are not live consensus; the actual validator callback was unit-tested for disagreement/substitution, but real distributed disagreement or appeal was not induced. UNKNOWN propagation, invalid table/encoding/size and HTTP-error cases are locally tested, not claimed as live proofs. No audit, formal semantic correctness or production-safety guarantee.
