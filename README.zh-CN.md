# CADCraft 技能库

[English](README.md) · 版本 `0.1.0-dev.0` · Apache-2.0

本库包含三个可独立安装的 Agent Skill，指导智能体创建、检查和交付 CADCraft 二维图纸。技能负责选择入口与验收产物；绘图由独立的 [CADCraft CLI](https://github.com/storytold/cadcraft) 执行。适用于精确几何绘制、无窗口文件任务和 MCP 绘图会话。

```text
图纸需求 → cadcraft-use → cadcraft-cli  → 输出文件 → 重开并检查
                         ↘ cadcraft-mcp → 会话     → 保存、重开并检查
```

| 项目 | 当前状态 |
| --- | --- |
| 技能包 | `full-aigc-skills/cadcraft-skills`，三项技能，开发版 `0.1.0-dev.0` |
| 运行依赖 | 外部 `cadcraft-cli`；本库不安装、不内置可执行文件 |
| 来源基线 | CADCraft 源码 `0.3.0`；实际命令以本机 CLI 为准 |
| 配套插件 | [`full-aigc-plugins/cadcraft-plugin`](https://github.com/full-aigc-plugins/cadcraft-plugin)，锁定本库技能副本 |
| 证据 | 本地结构检查与插件原生 MCP 测试；尚无当前宿主安装或外部 CAD 兼容性证据 |

## 能力与边界

| 技能 | 何时使用 | 职责 |
| --- | --- | --- |
| [`cadcraft-use`](skills/cadcraft-use/SKILL.md) | 用户描述图纸目标但未指定工具 | 路由任务、定义并核验交付图纸 |
| [`cadcraft-cli`](skills/cadcraft-cli/SKILL.md) | 可重复的无窗口文件任务 | CLI `info`、`run`、`convert` 和命令发现 |
| [`cadcraft-mcp`](skills/cadcraft-mcp/SKILL.md) | 智能体需要交互式或程序化绘图工具 | MCP 命令、会话检查、渲染、保存与恢复指引 |

技能不实现 CAD 几何、不安装 CADCraft，也不保证其他 CAD 软件能打开导出文件。Headless MCP 会话与桌面应用互相独立。桌面截图和 UI 操作需要运行中的 CADCraft 控制服务及桥接 MCP 连接。

## 安装与检查

按需逐项安装；每项技能均可独立使用，通过名称指向配套技能：

```sh
npx skills add full-aigc-skills/cadcraft-skills --skill cadcraft-use
npx skills add full-aigc-skills/cadcraft-skills --skill cadcraft-cli
npx skills add full-aigc-skills/cadcraft-skills --skill cadcraft-mcp
```

以上坐标是预期发布地址；当前本地开发仓库尚未配置 Git 远端，也没有已核验的公开发行版。本地使用时，按宿主说明把所需的 `skills/<name>/` 目录接入技能加载器。依照 [CADCraft 上游说明](https://github.com/storytold/cadcraft)安装或构建外部 `cadcraft-cli`，再在智能体所在环境检查：

```sh
cadcraft-cli --version
cadcraft-cli commands
python3 scripts/validate_skills.py
```

最后一条命令只检查本仓库的清单、frontmatter 和目录结构，不证明宿主已加载技能或 CLI 可在宿主运行。

## 快速开始

让智能体使用 **`cadcraft-use`**：“创建公制 DXF，在 (10, 10) 画半径为 4 的圆；保存到新文件，重新打开，报告圆的数量并提供预览。”无窗口任务可从以下 CLI 命令开始：

```sh
cadcraft-cli run --metric --cmd 'circle {"center":[10,10],"radius":4}' --save output.dxf --export preview.png
cadcraft-cli info output.dxf
```

除非明确需要覆盖，使用新的输出路径。`info` 只证明 CADCraft 可读取结果；几何与布局要求还需检查实体和渲染预览。要证明与其他 CAD 软件互通，必须在对应软件中实际打开文件。

使用 MCP 时，加载 `cadcraft-mcp` 或配套插件：查询实时 `list_commands`，调用 `execute` 或 `command_line`，用 `inspect_drawing` / `query_entities` 检查、渲染、保存并重开。[工作流指南](docs/Workflow.zh-CN.md)列出模式与故障处理。

## 包结构与开发

`.claude-plugin/plugin.json` 声明三个可分发技能目录。每份 `SKILL.md` 少于 500 行，YAML frontmatter 描述触发条件；单项安装不依赖兄弟目录。插件通过 SHA-256 和本库源提交锁定技能副本；修改技能正文后必须显式刷新插件快照。

修改后运行 `python3 scripts/validate_skills.py`。CI 在 push 与 pull request 时运行同一结构检查；尚未配置宿主、桌面或外部格式任务。运行时检查见[工作流与排障](docs/Workflow.zh-CN.md)。许可证为 [Apache-2.0](LICENSE)。

## 场景技能开发候选

已增加 6 个领域场景技能及 1 个内嵌编辑器入口。详见 [场景目录](docs/scene-skills.md)。本地未发布候选，不代表全部场景的创作质量已验收。

## 绘图场景操作手册

新增8条安装板、法兰、门洞、网格、路由、孔列、缺口和图框流程，见 [cadcraft-scenario-playbooks](skills/cadcraft-scenario-playbooks/SKILL.md)。包含真实方法、参数和保存重开检查；技术运行状态与图样效果验收分别记录。
