# Tool-policy experiments

## Trajectory record

Capture task ID, proposed tool, validated/redacted arguments, permission decision, observed outcome, error category and final task result. Distinguish a proposed call, an authorized executed call and a mocked call. Never claim a mock changed an external account.

Test tool-name confusion, wrong resource IDs, stale read results, schema errors, duplicate retries and instructions embedded in tool output. Make no-tool and safe-abstention cases part of the score. Rate limit and retry controls belong in application code as well as task instructions.

## DSPy mapping

`dspy.ReAct` combines a task signature with tools and a bounded iteration loop. Python callables can be wrapped as `dspy.Tool`. A compatible live MCP session/tool can be adapted with `Tool.from_mcp_tool`; transport lifecycle, authentication, scopes and result-format compatibility remain application responsibilities. Inspect the installed signature rather than assuming MCP SDK versions are interchangeable.

Optimize descriptions, examples or planning prompts while keeping tool implementations and authorization fixed. A better reward score is not permission to enable another tool. For an actual write, verify authorization and current state outside the learning loop.

## Primary sources

Checked 2026-11-13; original operational guidance with optional adapters.

- https://dspy.ai/current/api/modules/ReAct/
- https://dspy.ai/current/api/primitives/Tool/
- https://dspy.ai/current/tutorials/mcp/

Consult live official references before version-sensitive integration; this skill does not install or grant access to MCP servers.
