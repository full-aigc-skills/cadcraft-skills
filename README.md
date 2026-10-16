# CADCraft Skills

[简体中文](README.zh-CN.md) · Version `0.1.0-dev.0` · Apache-2.0

Three independent Agent Skills for creating, inspecting, and delivering CADCraft 2D drawings. They guide an agent to choose an entry point and verify its output; the separate [CADCraft CLI](https://github.com/storytold/cadcraft) performs drawing work. Use this package for precise geometry, a headless file workflow, or an MCP drawing session.

```text
Drawing request → cadcraft-use → cadcraft-cli  → output file → reopen and inspect
                               ↘ cadcraft-mcp → session     → save, reopen and inspect
```

| Fact | Current state |
| --- | --- |
| Package | `full-aigc-skills/cadcraft-skills`, three skills, development version `0.1.0-dev.0` |
| Runtime | External `cadcraft-cli`; this package does not install or bundle it |
| Source baseline | CADCraft source `0.3.0`; inspect the installed CLI for its actual commands |
| Companion | [`full-aigc-plugins/cadcraft-plugin`](https://github.com/full-aigc-plugins/cadcraft-plugin), which pins copies of these skills |
| Evidence | Local structure checks and plugin native MCP tests; no current host-install or external CAD compatibility proof |

## Capabilities and boundaries

| Skill | Use when | Responsibility |
| --- | --- | --- |
| [`cadcraft-use`](skills/cadcraft-use/SKILL.md) | A drawing outcome is requested without a tool choice | Route the task; define and verify the deliverable |
| [`cadcraft-cli`](skills/cadcraft-cli/SKILL.md) | A repeatable headless file task is needed | CLI `info`, `run`, `convert`, and command discovery |
| [`cadcraft-mcp`](skills/cadcraft-mcp/SKILL.md) | The agent needs interactive or programmatic drawing | MCP commands, inspection, rendering, saving, and recovery guidance |

The skills do not implement CAD geometry, install CADCraft, or guarantee that another CAD application can open an export. A headless MCP session is separate from the desktop application. Desktop screenshots and UI actions require a running CADCraft control service and a bridged MCP connection.

## Install and verify

Install only the skills you need. Each is self-contained and refers to companions by name:

```sh
npx skills add full-aigc-skills/cadcraft-skills --skill cadcraft-use
npx skills add full-aigc-skills/cadcraft-skills --skill cadcraft-cli
npx skills add full-aigc-skills/cadcraft-skills --skill cadcraft-mcp
```

These coordinates are the intended published location; this local development checkout has no configured Git remote or verified public release. For local use, point your host's skill loader at the desired `skills/<name>/` directory. Install or build the external `cadcraft-cli` using the [upstream CADCraft instructions](https://github.com/storytold/cadcraft), then check it in the agent's environment:

```sh
cadcraft-cli --version
cadcraft-cli commands
python3 scripts/validate_skills.py
```

The last command validates this repository's manifest, frontmatter, and layout. It does not prove host loading or runtime behavior.

## Quick start

Ask an agent to use **`cadcraft-use`**: “Create a metric DXF with a circle centred at (10, 10), radius 4; save to a new file, reopen it, and report the circle count and a preview.” For a headless task, the equivalent CLI starting point is:

```sh
cadcraft-cli run --metric --cmd 'circle {"center":[10,10],"radius":4}' --save output.dxf --export preview.png
cadcraft-cli info output.dxf
```

Use a new output path unless overwriting is expressly intended. `info` shows that CADCraft can read the result; inspect entities and a render for geometry and layout. To prove interoperability with another CAD application, open the export there.

For MCP, load `cadcraft-mcp` or the companion plugin. Discover the live `list_commands` catalog, call `execute` or `command_line`, inspect with `inspect_drawing` / `query_entities`, render, save, and reopen. The [workflow guide](docs/Workflow.md) covers modes and failures.

## Package and development

`.claude-plugin/plugin.json` declares three distributable skill directories. Each `SKILL.md` is under 500 lines and contains a trigger description in YAML frontmatter. Granular installation requires no sibling directory. The plugin locks each `SKILL.md` by SHA-256 plus this package's source commit; edits to skills require an explicit plugin snapshot refresh.

Run `python3 scripts/validate_skills.py` after editing. CI runs the same structural gate on push and pull request; no host, desktop, or external-format job is configured. See [workflow and troubleshooting](docs/Workflow.md) for runtime checks. Licensed under [Apache-2.0](LICENSE).

## 场景技能开发候选

已增加 6 个领域场景技能及 1 个内嵌编辑器入口。详见 [场景目录](docs/scene-skills.md)。本地未发布候选，不代表全部场景的创作质量已验收。
