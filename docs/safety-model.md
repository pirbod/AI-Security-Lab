# Safety Model

The lab is designed for local defensive learning.

## Allowed by default

- `127.0.0.1`
- `localhost`
- `::1`

## Blocked by default

- Public IP addresses
- Domains other than `localhost`
- Private lab networks unless explicitly enabled
- CIDR ranges larger than four addresses
- Any workflow that requires prompts, model downloads, deletion, credential collection, or destructive actions

## Private lab networks

Private ranges can be enabled with:

```bash
export AI_LAB_ALLOW_PRIVATE_NETWORKS=1
```

Use this only for a dedicated, authorized private lab. The clickable service discovery page still
defaults to loopback targets.

## Timeouts

Scanners use short socket and HTTP timeouts so local checks fail safely and do not hang the UI.
