# Python MCP Server Implementation Guide

Use the official MCP Python SDK documentation for the selected major version as the API source of truth. The SDK has materially different major-version APIs; do not copy imports or decorators between versions.

## Baseline workflow

1. Record the Python runtime, package name, exact SDK version, MCP protocol era, transport, and target clients.
2. Create an isolated project with `pyproject.toml` and a lockfile. Use the official `mcp` package unless a different framework is explicitly selected and justified.
3. Keep MCP registration thin. Place upstream clients, authorization, domain logic, formatting, and error mapping in independently testable modules.
4. Use Pydantic v2 or the SDK-supported schema mechanism for constrained inputs and typed outputs.
5. Reuse network/database clients through the SDK lifespan mechanism instead of constructing one client per tool call.
6. Use stdio for local subprocesses and Streamable HTTP for remote services. Treat standalone SSE as a compatibility path, not the default.
7. Test through the SDK client in-process, then through the actual transport and MCP Inspector.

## Tool contract pattern

Prefer direct typed parameters for simple tools. Introduce an input model when fields are reused, cross-field validation is required, or it improves the generated schema. Reject extras where supported.

```python
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field

mcp = FastMCP("catalog")


class SearchResult(BaseModel):
    id: str
    title: str


class SearchOutput(BaseModel):
    items: list[SearchResult]
    next_cursor: str | None = None


class SearchInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    query: Annotated[str, Field(min_length=2, max_length=200)]
    limit: Annotated[int, Field(ge=1, le=50)] = 10
    cursor: str | None = None


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def search_items(params: SearchInput) -> SearchOutput:
    """Search catalog items by keyword and return a bounded cursor page."""
    data = await search_service(params.query, params.limit, params.cursor)
    return SearchOutput.model_validate(data)
```

Verify the exact SDK behavior for structured tool results. Current SDK lines can derive output schemas from typed return values and expose structured content, but names and return wrappers vary by major version. Add a compatibility text representation when required by supported clients.

## Lifespan and shared dependencies

```python
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

import httpx
from mcp.server.fastmcp import FastMCP


@dataclass
class AppContext:
    http: httpx.AsyncClient


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(20.0, connect=5.0),
        follow_redirects=False,
    ) as http:
        yield AppContext(http=http)


mcp = FastMCP("catalog", lifespan=lifespan)
```

Access lifespan state through the exact `Context` API documented for the pinned SDK. Propagate asyncio cancellation and avoid catching `BaseException` or cancellation exceptions as generic tool failures.

## Safe errors

- Catch expected domain/upstream exceptions narrowly.
- Return the SDK's tool-error result for recoverable execution failures.
- Let protocol validation failures remain protocol validation failures.
- Never include raw exception text when it can contain URLs, headers, query strings, SQL, paths, or payloads.
- Log a redacted correlation ID to stderr/logging and include only that ID in the client-safe message.

## Streamable HTTP controls

- Use the SDK's Streamable HTTP application/runner for the pinned version.
- Validate Origin and trusted Host/proxy data before MCP handling.
- Bind developer servers to `127.0.0.1`; require HTTPS and real authentication remotely.
- Select stateless mode unless the workflow genuinely needs state and the selected protocol era supports it.
- Never use connection/session identifiers as identity. Bind explicit handles to actor, tenant, scope, TTL, and cleanup.
- Place health/readiness outside the MCP endpoint.

## Stdio controls

- Never print to stdout. Configure logging to stderr before importing modules that may emit output.
- Treat inherited environment variables as sensitive. Pass only required variables from client configuration.
- Handle EOF/signals and close clients, files, pools, and background tasks.

## Client capabilities

Use context APIs for progress, logging, roots, elicitation, or other client features only after checking support according to the pinned SDK/protocol. Provide a fallback. Never request credentials through ordinary elicitation.

## Python quality gates

Run the project's equivalents of:

```bash
python -m compileall src tests
ruff check .
ruff format --check .
mypy --strict src
pytest -q
```

Add in-process MCP client tests similar to:

```python
import pytest
from mcp import Client

from server import mcp


@pytest.fixture
async def client():
    async with Client(mcp, raise_exceptions=True) as value:
        yield value


@pytest.mark.anyio
async def test_search_items_contract(client: Client) -> None:
    result = await client.call_tool("search_items", {"params": {"query": "alpha"}})
    assert result.isError is not True
    assert result.structuredContent is not None
```

Adapt field names and argument shape to the pinned SDK. Also test invalid extras/bounds, output validation, tool errors, cancellation, timeout, concurrent calls, authorization, transport startup/shutdown, and absence of stdout noise.
