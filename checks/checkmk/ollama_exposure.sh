#!/usr/bin/env bash
# Safe Checkmk local check for local Ollama exposure signals.
# Output format examples:
# 0 "AI Ollama exposure" - OK: Ollama is not listening locally
# 1 "AI Ollama exposure" - WARN: Ollama listens on localhost only
# 2 "AI Ollama exposure" - CRIT: Ollama listens on all interfaces

set -u

service="AI Ollama exposure"
port="11434"

if ! command -v ss >/dev/null 2>&1; then
  echo "1 \"$service\" - WARN: ss command not available; cannot inspect local listeners"
  exit 0
fi

listeners="$(ss -ltn 2>/dev/null | grep ":$port " || true)"
if echo "$listeners" | grep -Eq '(^|[[:space:]])(0\.0\.0\.0|\[::\]|\*):11434'; then
  echo "2 \"$service\" - CRIT: local port 11434 appears bound to all interfaces"
elif echo "$listeners" | grep -Eq '127\.0\.0\.1:11434|\[::1\]:11434'; then
  echo "1 \"$service\" - WARN: Ollama listens on localhost; keep auth and bind settings reviewed"
else
  echo "0 \"$service\" - OK: Ollama is not listening locally on port 11434"
fi
