# Human decision packet

## Header

- **Packet ID:** PACKET-NNN
- **Gate ID and type:** GATE-NNN / G0-G6
- **Gate status:** proposed | in_review | approved | approved_with_conditions | revised | rejected | deferred | expired | superseded
- **Decision owner:** named human
- **Decision-owner conflict declaration / alternate:** none or disclosed / named eligible alternate when required
- **Prepared by:** advisory agent runs and human contributors
- **Evidence snapshot:** immutable path and hash
- **Prepared at / expires at:** ISO timestamp or event

## One decision requested

State one decision as an action with a bounded object. Do not bundle later-gate authority.

## Options and consequences

| Option | Authority granted | What remains forbidden | Consequence |
|---|---|---|---|
| Approve |  |  |  |
| Approve with conditions |  |  |  |
| Revise | None until resubmitted |  |  |
| Reject | None |  |  |
| Defer | None until named trigger |  |  |

## Advisory recommendation

Label the recommendation `advisory`. State confidence, assumptions, strongest countercase, dissent, and evidence that would reverse it. An agent majority is not a quorum.

## Evidence ledger

| Claim or input | State | Exact provenance | Counterevidence | Freshness | Owner |
|---|---|---|---|---|---|
|  | observed / source_backed / reported / inferred / proposed / contradicted / unresolved |  |  |  |  |

## Acceptance and failure

- **Acceptance criteria:** observable conditions for this gate only.
- **Failure criteria:** observations that require revise, reject, quarantine, or stop.
- **Material unknowns:** use `unresolved`; do not infer favorable values.

## Authority delta

- **Newly authorized if approved:**
- **Still forbidden:**
- **Budget and source/data boundary:**
- **Expiry:**
- **First stop condition:**
- **Single-use consumption event:** completion, budget exhaustion, expiry, or another named stop trigger

## Roles and separation

| Function | Named human | Advisory agent | Conflict or recusal |
|---|---|---|---|
| Accountable decision |  | None |  |
| Evidence and method review |  | Evidence and Methods Challenger |  |
| Boundary review |  | Boundary Sentinel |  |
| Independent evaluation, if required |  | Blind Evaluation Assistant only as support |  |

Missing required humans are blockers. A different prompt, task, or model session does not by itself create independence.

## Human decision

- **Decision:** approve | approve_with_conditions | revise | reject | defer | expire
- **Conditions or requested revision:**
- **Rationale and dissent:**
- **Decision-maker identity:**
- **Conflict declaration / eligible alternate:**
- **Decided at:**
- **Approval decision hash:**
- **Trusted checkpoint / external signature evidence:**
- **Handoff ID / status:** unissued | issued | consumed | expired | revoked
- **Issued at / closed at / execution count:**
- **Reversal evidence:**

## Handoff

After an explicit human decision, record any required prior-terminal checkpoint attestation, then record exactly one next action with owner, allowed and forbidden work, inputs, budget, expiry, required output, validation, and stop rule. A second or later issuance requires a trusted checkpoint for the immediately preceding terminal event.
