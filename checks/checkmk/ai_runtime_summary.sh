#!/usr/bin/env bash
# Safe Checkmk local summary for common AI runtime listener ports.
# Output format examples:
# 0 "AI runtime summary" ai_ports=0 OK: no common AI runtime ports are listening
# 1 "AI runtime summary" ai_ports=2 WARN: local AI runtime ports are listening
# 2 "AI runtime summary" ai_ports=1 CRIT: one or more AI runtime ports bind all interfaces

set -u

service="AI runtime summary"
ports="11434 8000 8080"

if ! command -v ss >/dev/null 2>&1; then
  echo "1 \"$service\" ai_ports=0 WARN: ss command not available; cannot inspect local listeners"
  exit 0
fi

listeners="$(ss -ltn 2>/dev/null)"
local_count=0
critical_count=0

for port in $ports; do
  if echo "$listeners" | grep -Eq "(0\.0\.0\.0|\[::\]|\*):$port"; then
    critical_count=$((critical_count + 1))
  elif echo "$listeners" | grep -Eq "(127\.0\.0\.1|\[::1\]):$port"; then
    local_count=$((local_count + 1))
  fi
done

if [ "$critical_count" -gt 0 ]; then
  echo "2 \"$service\" ai_ports=$((local_count + critical_count)) CRIT: $critical_count AI runtime port(s) appear bound to all interfaces"
elif [ "$local_count" -gt 0 ]; then
  echo "1 \"$service\" ai_ports=$local_count WARN: $local_count AI runtime port(s) listen on localhost"
else
  echo "0 \"$service\" ai_ports=0 OK: no common AI runtime ports are listening"
fi
