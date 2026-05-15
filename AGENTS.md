# Contributor Guidance

This repository is a local defensive security lab. Keep every change aligned with safe,
authorized learning on a personal device.

## Rules

- Keep scanners local-first and safe by default.
- Reject public IP ranges and domains unless a future feature has an explicit documented safety model.
- Do not add weaponized proof-of-concept code.
- Do not add credential collection, destructive actions, or internet-wide scanning.
- Every check must return `OK`, `WARN`, `CRIT`, or `INFO`.
- Keep documentation practical and tied to local lab workflows.
- Python files use 2-space indentation in this repository.

## Quality Expectations

- Add or update tests for safety-sensitive behavior.
- Prefer readable Python over clever abstractions.
- Keep report output useful for remediation and responsible disclosure practice.
- Make warnings visible in the UI and documentation.
