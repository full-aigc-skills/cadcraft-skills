# CADCraft Skills workflow

[简体中文](Workflow.zh-CN.md) · Applies to the three skills in this package at `0.1.0-dev.0`.

## Choose and run

| Need | Skill | Runtime path |
| --- | --- | --- |
| Unspecified 2D drawing task | `cadcraft-use` | Define units, source, geometry, format, and acceptance; route onward |
| One-off file inspection, drawing, export, or conversion | `cadcraft-cli` | `cadcraft-cli info`, `run`, `convert`, `commands` |
| Stateful precision drawing | `cadcraft-mcp` | `cadcraft-cli mcp` in a fresh headless session |
| Visible desktop state or UI actions | `cadcraft-mcp` | CADCraft `--control PORT` plus `cadcraft-cli mcp --connect 127.0.0.1:PORT` |

Use `cadcraft-cli commands` or MCP `list_commands` as the authority for the installed version's command IDs and parameter descriptions. Do not assume that a skill example lists every supported command. A new headless MCP process starts its own drawing state; save to a file to hand work to another process. A `render` image depicts drawing content; `screenshot` requires the desktop bridge.

## Acceptance sequence

1. Record source file, units, expected entity types/counts, coordinates, layers, output format, and destination. Work on a copy for an existing drawing unless the user explicitly requests replacement.
2. Run the chosen command. For MCP, inspect both JSON-RPC transport and tool result: `isError: true` means failure; a `command_line` result can also carry an `error` field while the tool call itself succeeds.
3. Inspect the drawing using `inspect_drawing` and `query_entities`; inspect constraints when relevant. Render or preview the whole result, including dimensions and labels.
4. Save to the agreed path, reopen the delivered file in a fresh process, and check the key entities again. `cadcraft-cli info` proves only that CADCraft can read it. External DXF/DWG compatibility needs a separate test in the intended CAD application.

## Recover without hiding uncertainty

| Symptom | First check | Next step |
| --- | --- | --- |
| `cadcraft-cli` is missing | `cadcraft-cli --version` in the host environment | Install/build from upstream or fix host PATH; retry discovery |
| Unknown command or parameter | `cadcraft-cli commands` or MCP `list_commands` | Use the installed CLI's contract; correct the call |
| `execute` or `command_line` reports failure | `isError`, `error`, `running`, and `prompt` | Inspect state before continuing; cancel or undo only after checking partial work |
| Desktop bridge times out or disconnects | Inspect current drawing or reopen the last saved file | Treat side effects as **unknown**; do not blindly repeat create/delete commands |
| Save or conversion fails | Exit code/tool result and destination file | Do not present an older file as new output; preserve the source and report the failure |
| Export opens in CADCraft but not elsewhere | Reproduce in the target application | Record the format/version and unsupported feature; internal round-trip is not proof |

CADCraft's remote backend reconnects and retries a control request after a transport error. This is a runtime behavior in the upstream source, not an exactly-once guarantee; a request may have executed before the reply was lost. The skill must verify the resulting state before any repeat action. There is no plugin-side durable operation ledger or automatic rollback.

## Evidence and ownership

The skill package validates metadata with `python3 scripts/validate_skills.py`. Geometry, file content, desktop state, host loading, and external interoperability require the corresponding runtime evidence. The skill source is maintained here; [`cadcraft-plugin`](https://github.com/full-aigc-plugins/cadcraft-plugin) distributes pinned copies. Change the source skill first, then explicitly sync and validate the plugin snapshot.
