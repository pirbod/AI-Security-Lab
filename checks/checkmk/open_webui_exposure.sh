#!/usr/bin/env bash
# Safe Checkmk local check for local Open WebUI-style exposure signals.
# Output format examples:
# 0 "AI Open WebUI exposure" - OK: UI is not listening locally
# 1 "AI Open WebUI exposure" - WARN: UI listens on localhost only
# 2 "AI Open WebUI exposure" - CRIT: UI listens on all interfaces

set -u

service="AI Open WebUI exposure"
port="8080"

if ! command -v ss >/dev/null 2>&1; then
  echo "1 \"$service\" - WARN: ss command not available; cannot inspect local listeners"
  exit 0
fi

listeners="$(ss -ltn 2>/dev/null | grep ":$port " || true)"
if echo "$listeners" | grep -Eq '(^|[[:space:]])(0\.0\.0\.0|\[::\]|\*):8080'; then
  echo "2 \"$service\" - CRIT: local port 8080 appears bound to all interfaces"
elif echo "$listeners" | grep -Eq '127\.0\.0\.1:8080|\[::1\]:8080'; then
  echo "1 \"$service\" - WARN: UI listens on localhost; verify authentication and secure cookies"
else
  echo "0 \"$service\" - OK: UI is not listening locally on port 8080"
fi
