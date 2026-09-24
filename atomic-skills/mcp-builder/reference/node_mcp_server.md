# TypeScript MCP Server Implementation Guide

Use the official MCP TypeScript SDK documentation for the selected major version as the API source of truth. The v1 and v2 package layout and server APIs differ; never combine imports or registration syntax across major versions.

## Baseline workflow

1. Record Node.js, TypeScript, Zod/Standard Schema, SDK, protocol-era, transport, and target-host versions.
2. Use ESM, strict TypeScript, a lockfile, and the official SDK packages appropriate to the pinned major version.
3. Keep tool registration thin. Separate schemas, domain services, upstream clients, auth policy, output shaping, and error mapping.
4. Prefer stdio for local subprocesses and Streamable HTTP for remote servers. Treat standalone SSE as legacy compatibility.
5. Return structured output with an output schema when supported and retain concise text content for compatibility.
6. Test handlers in process, then test the actual transport and official Inspector.

## Current v2-style tool contract

The current v2 documentation uses split packages and Standard Schema. Confirm package names against the pinned release before installing.

```typescript
import { McpServer } from "@modelcontextprotocol/server";
import * as z from "zod/v4";

const server = new McpServer({ name: "catalog", version: "1.0.0" });

const inputSchema = z.object({
  query: z.string().min(2).max(200).describe("Keywords to match"),
  limit: z.number().int().min(1).max(50).default(10),
  cursor: z.string().optional(),
}).strict();

const outputSchema = z.object({
  items: z.array(z.object({ id: z.string(), title: z.string() })),
  nextCursor: z.string().nullable(),
});

server.registerTool(
  "search_items",
  {
    title: "Search catalog items",
    description: "Search catalog items by keyword and return a bounded cursor page.",
    inputSchema,
    outputSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true,
    },
  },
  async ({ query, limit, cursor }, extra) => {
    const data = outputSchema.parse(
      await catalog.search({ query, limit, cursor, signal: extra.signal }),
    );
    return {
      content: [{ type: "text", text: JSON.stringify(data) }],
      structuredContent: data,
    };
  },
);
```

For v1 projects, use the pinned v1 imports and registration API rather than mechanically translating this sample. Keep a migration test that snapshots `tools/list` and representative `tools/call` responses.

## Stdio runner

Current v2-style documentation uses a server factory so each connection receives an isolated server instance:

```typescript
import { McpServer } from "@modelcontextprotocol/server";
import { serveStdio } from "@modelcontextprotocol/server/stdio";

await serveStdio(() => {
  const server = new McpServer({ name: "catalog", version: "1.0.0" });
  registerTools(server);
  return server;
});
```

Never write to stdout. Use stderr or a structured log sink. Close resources and abort background work on connection shutdown.

## Streamable HTTP runner

Prefer stateless request handling unless the use case and selected protocol era require state. Current v2-style Node integration provides host/origin validation helpers:

```typescript
import { createServer } from "node:http";
import {
  localhostHostValidation,
  localhostOriginValidation,
  NodeStreamableHTTPServerTransport,
} from "@modelcontextprotocol/node";
import { McpServer } from "@modelcontextprotocol/server";

const validateHost = localhostHostValidation();
const validateOrigin = localhostOriginValidation();

createServer(async (req, res) => {
  if (!validateHost(req, res) || !validateOrigin(req, res)) return;

  const mcp = new McpServer({ name: "catalog", version: "1.0.0" });
  registerTools(mcp);
  const transport = new NodeStreamableHTTPServerTransport({
    sessionIdGenerator: undefined,
  });
  res.on("close", () => void transport.close());
  await mcp.connect(transport);
  await transport.handleRequest(req, res);
}).listen(3000, "127.0.0.1");
```

For public deployment, replace localhost validators with an explicit trusted-origin/host policy, terminate HTTPS correctly, authenticate requests, respect trusted proxy boundaries, and add request, connection, timeout, concurrency, and body-size controls. Reuse expensive application services through an application container while keeping protocol connection state isolated.

## Safe errors

Return expected domain/upstream failures as MCP tool errors:

```typescript
return {
  isError: true,
  content: [{
    type: "text",
    text: `Item not found. Search for a valid ID. Reference: ${correlationId}`,
  }],
};
```

Do not echo arbitrary `error.message`. It may contain secrets, URLs, headers, internal paths, or upstream response bodies. Classify errors and log redacted details server-side.

## Cancellation, deadlines, and progress

- Pass the SDK-provided `AbortSignal` into `fetch`, database calls, and long loops.
- Combine client cancellation with server deadlines.
- Retry only transient idempotent operations, with bounded exponential backoff and jitter.
- Send progress only if the request supplies the expected token/capability for the pinned protocol.
- Clean up transport and application resources on abort and disconnect.

## Strict typing

- Enable `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, and `useUnknownInCatchVariables` where compatible.
- Avoid `any`; validate upstream JSON with Zod/Standard Schema.
- Define explicit output contracts and validate them before return.
- Distinguish omitted, nullable, and defaulted fields deliberately.
- Use URL/path parsers and policy functions instead of string concatenation.

## Testing

Use an in-process handler/client where supported. Current v2 documentation supports injecting the handler's `fetch` into a Streamable HTTP client transport, enabling deterministic transport tests without opening a port.

Test:

- `tools/list` snapshots and pagination.
- Valid/invalid tool calls and unknown fields.
- `outputSchema`/`structuredContent` agreement.
- Tool error versus protocol error behavior.
- Abort/deadline propagation and cleanup.
- Concurrent requests and isolation.
- Origin/Host rejection, auth audience/scope/tenant checks, SSRF/path/command defenses, and log redaction.
- Actual stdio startup with zero stdout noise beyond protocol frames.

Run project equivalents of:

```bash
npm ci
npm run typecheck
npm run lint
npm test
npm run build
npx @modelcontextprotocol/inspector node ./dist/server.js
```

For Streamable HTTP, use Inspector's HTTP transport and scripted CLI calls documented for the installed Inspector version.
