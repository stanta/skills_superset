---
name: ton-smart-contracts-specialist
description: Use when working on TON smart contracts, Tact/FunC code, opcode design, contract wrappers, or contract-to-app integration boundaries in this workspace.
source_repo: https://github.com/tact-lang/tact
source_validation: GitHub research confirmed 5+ stars/forks; observed public signals included ~687 stars and ~217 forks on 2026-03-13.
---

# ton-smart-contracts-specialist

## Purpose

This skill covers the TON contract layer present in [`architecton-voting-app/architecton-voting/contracts/multi_sig.tact`](../../../architecton-voting-app/architecton-voting/contracts/multi_sig.tact:1), [`architecton-voting-app/architecton-voting/contracts/op-codes.fc`](../../../architecton-voting-app/architecton-voting/contracts/op-codes.fc:1), and the surrounding project structure documented in [`architecton-voting-app/architecton-voting/README.md`](../../../architecton-voting-app/architecton-voting/README.md:1).

## Use this skill when

- Editing or reviewing `.tact` or `.fc` contracts.
- Designing message schemas, opcodes, state layout, or wrapper interfaces.
- Aligning frontend/backend TON calls with contract capabilities.
- Assessing contract security, gas implications, or deployment readiness.

## Do not use this skill when

- The task is limited to frontend UI state or generic TON SDK rendering concerns. Use [`frontend-react-dev`](../frontend-react-dev/SKILL.md) or [`react-expert`](../react-expert/SKILL.md).
- The task is generic API work unrelated to contract semantics. Use [`fastapi-expert`](../fastapi-expert/SKILL.md) or [`python-dev`](../python-dev/SKILL.md).

## Recommended workflow

1. **Identify the contract boundary**
   - Determine which contract owns the behavior, which messages it accepts, and which wrappers/scripts rely on that interface.
   - Review the repository layout in [`architecton-voting-app/architecton-voting/README.md`](../../../architecton-voting-app/architecton-voting/README.md:3).

2. **Prefer explicit interface design**
   - Keep opcode/message definitions centralized and documented.
   - Treat wrapper payload formats as compatibility contracts for app code.

3. **Separate storage, authorization, and transition logic**
   - Make state transitions explicit.
   - Review who is allowed to call each path and how replay or duplicate execution is prevented.

4. **Validate integration assumptions**
   - Check that frontend or backend callers use the same message schema and expected result model.
   - Keep app-side constants synchronized with contract opcodes and payload structure.

5. **Test before deployment changes**
   - Require contract-level tests for state transitions, negative paths, and unauthorized operations.
   - Add integration smoke checks for wrapper serialization and execution flow.

6. **Review security and cost**
   - Inspect authorization paths, upgradeability assumptions, bounce/error handling, and gas-sensitive loops.
   - Flag any contract behavior that could lock funds, break governance flow, or create stuck state.

## Project guidance

- Use this skill first for any work in [`architecton-voting-app/architecton-voting/contracts/multi_sig.tact`](../../../architecton-voting-app/architecton-voting/contracts/multi_sig.tact:1), [`architecton-voting-app/architecton-voting/contracts/passports/passport.fc`](../../../architecton-voting-app/architecton-voting/contracts/passports/passport.fc:1), or related wrapper/tests.
- Pair it with [`test-master`](../test-master/SKILL.md) for contract regression coverage and with [`security-reviewer`](../security-reviewer/SKILL.md) for high-risk changes.
- When a contract change impacts app behavior, follow with [`telegram-mini-apps-specialist`](../telegram-mini-apps-specialist/SKILL.md) or [`frontend-react-dev`](../frontend-react-dev/SKILL.md) to validate the UI integration boundary.

## Output expectations

When this skill is used, the output should include:

- contract/module scope,
- message/opcode compatibility notes,
- state/security review summary,
- test expectations,
- downstream integration impact on app or API layers.
