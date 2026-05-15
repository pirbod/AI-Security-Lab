# Checkmk Local Checks

The `checks/checkmk/` directory contains safe local checks for AI runtime listener signals.

## Install locally

On a Checkmk-monitored Linux host, copy a script into the local checks directory used by your agent.
Common paths include:

```bash
/usr/lib/check_mk_agent/local/
/usr/local/lib/check_mk_agent/local/
```

Make it executable:

```bash
chmod +x /path/to/local/check.sh
```

## Safety

The scripts only inspect local listening sockets with `ss`. They do not connect to remote targets
and do not send prompts or mutate services.

## Output states

- `0`: OK
- `1`: WARN
- `2`: CRIT

Each script includes examples in comments.
