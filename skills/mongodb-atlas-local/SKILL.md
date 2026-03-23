---
name: mongodb-atlas-local
description: This skill should be used when setting up, debugging, or operating MongoDB Atlas Local environments for development, especially host-networked Docker setups, auth-enabled local instances, vector-search bootstrap, keyfiles, and developer troubleshooting around `docker-compose-dev.yml` and local Mongo connectivity.
---

# MongoDB Atlas Local

## Overview

Run and troubleshoot Atlas Local development environments safely and repeatably. Focus on auth setup, keyfiles, host networking, user creation, vector search support, and common local-driver failure modes.

## When to use

- Bring up local Mongo for development or tests.
- Debug `mongo_health`, `127.0.0.1`, host-networking, or auth issues.
- Fix Atlas Local vector-search bootstrap problems.
- Review local setup instructions for developers joining the project.
- Diagnose why the app falls back to in-memory checkpointers locally.

## Core workflow

### 1. Prepare the environment

- Create the Mongo keyfile when required.
- Confirm Docker image, local storage path, and port bindings.
- Decide whether the app will connect from host Python or from another container.

### 2. Align networking with the runtime

- If the bot runs on the host, prefer `127.0.0.1` instead of Docker-internal service names.
- Confirm whether `network_mode: host` is assumed.
- Keep connection strings explicit.

### 3. Enable auth explicitly

- Create the application user deliberately.
- Document credentials and `authSource` expectations for local development.
- Verify that developers know the difference between unauthenticated and auth-enabled local runs.

### 4. Verify vector-search capability

- Confirm index creation behavior for memory/vector collections.
- Troubleshoot Atlas Local search-index errors separately from general Mongo connectivity.

### 5. Diagnose fallback behavior

- If the bot silently falls back to in-memory state, inspect URI validity, auth, DNS, port reachability, and driver handshake behavior.

## Repository guidance

Prioritize these files:

- `docker-compose-dev.yml`
- `config/config.env`
- `docs/Development.md`
- `docs/Troubleshooting.md`
- `bot/graph/workflow.py`
- `bot/database.py`

## Non-negotiables

- Match hostname choice to where the app actually runs.
- Keep auth options explicit in local connection strings.
- Document keyfile creation steps for fresh setups.
- Verify vector-search bootstrap separately from ordinary CRUD connectivity.
- Treat silent fallback to in-memory persistence as a real diagnostic signal.

## Deliverables

When using this skill, produce:

1. Local setup checklist.
2. Connection-string guidance.
3. Auth and keyfile notes.
4. Vector-search troubleshooting notes.
5. Validation commands or smoke checks.
