#!/usr/bin/env bash
# Safe Checkmk local check for local vLLM-style API exposure signals.
# Output format examples:
# 0 "AI vLLM exposure" - OK: vLLM API is not listening locally
# 1 "AI vLLM exposure" - WARN: vLLM API listens on localhost only
# 2 "AI vLLM exposure" - CRIT: vLLM API listens on all interfaces

set -u

service="AI vLLM exposure"
port="8000"

if ! command -v ss >/dev/null 2>&1; then
  echo "1 \"$service\" - WARN: ss command not available; cannot inspect local listeners"
  exit 0
fi

listeners="$(ss -ltn 2>/dev/null | grep ":$port " || true)"
if echo "$listeners" | grep -Eq '(^|[[:space:]])(0\.0\.0\.0|\[::\]|\*):8000'; then
  echo "2 \"$service\" - CRIT: local port 8000 appears bound to all interfaces"
elif echo "$listeners" | grep -Eq '127\.0\.0\.1:8000|\[::1\]:8000'; then
  echo "1 \"$service\" - WARN: vLLM-style API listens on localhost; require auth before remote use"
else
  echo "0 \"$service\" - OK: vLLM-style API is not listening locally on port 8000"
fi
