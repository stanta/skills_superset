#!/usr/bin/env bash
# Railway GraphQL API helper
# Usage: railway-api.sh '<graphql-query>' ['<variables-json>']

set -e

SKILL_ID="use-railway"
SKILL_VERSION="${RAILWAY_SKILL_VERSION:-1.1.3}"

export RAILWAY_CALLER="${RAILWAY_CALLER:-skill:${SKILL_ID}@${SKILL_VERSION}}"
export RAILWAY_AGENT_SESSION="${RAILWAY_AGENT_SESSION:-railway-skill-$(date +%s)-$$}"

if ! command -v jq &>/dev/null; then
  echo '{"error": "jq not installed. Install with: brew install jq"}'
  exit 1
fi

# Never scrape credentials from Railway's on-disk CLI config. The caller/harness
# must explicitly scope a token into this process when direct API fallback is needed.
TOKEN="${RAILWAY_TOKEN:-}"
if [[ -z "$TOKEN" ]]; then
  echo '{"error": "RAILWAY_TOKEN is not set. Prefer Railway CLI; for direct API fallback, explicitly provide a task-scoped token."}'
  exit 1
fi

if [[ -z "$1" ]]; then
  echo '{"error": "No query provided"}'
  exit 1
fi

# Build payload with query and optional variables
if [[ -n "$2" ]]; then
  PAYLOAD=$(jq -n --arg q "$1" --argjson v "$2" '{query: $q, variables: $v}')
else
  PAYLOAD=$(jq -n --arg q "$1" '{query: $q}')
fi

HEADERS=(
  -H "Authorization: Bearer $TOKEN"
  -H "Content-Type: application/json"
  -H "X-Railway-Skill-Id: $SKILL_ID"
  -H "X-Railway-Skill-Version: $SKILL_VERSION"
  -H "X-Railway-Agent-Session: $RAILWAY_AGENT_SESSION"
)

curl -s https://backboard.railway.com/graphql/v2 "${HEADERS[@]}" -d "$PAYLOAD"
