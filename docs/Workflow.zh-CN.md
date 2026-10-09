# CADCraft 技能工作流

[English](Workflow.md) · 适用于本库 `0.1.0-dev.0` 的三项技能。

## 选择与执行

| 需求 | 技能 | 运行路径 |
| --- | --- | --- |
| 未指定工具的二维绘图需求 | `cadcraft-use` | 明确单位、来源、几何、格式和验收，再分流 |
| 单次文件检查、绘图、导出或转换 | `cadcraft-cli` | `cadcraft-cli info`、`run`、`convert`、`commands` |
| 有状态的精确绘图 | `cadcraft-mcp` | 新 Headless 会话中的 `cadcraft-cli mcp` |
| 可见桌面状态或 UI 操作 | `cadcraft-mcp` | CADCraft `--control PORT` 加 `cadcraft-cli mcp --connect 127.0.0.1:PORT` |

当前安装版本的命令 ID 与参数说明以 `cadcraft-cli commands` 或 MCP `list_commands` 为准，不把技能示例当成完整命令目录。新的 Headless MCP 进程有独立图纸状态；跨进程交接须保存文件。`render` 呈现图纸内容；`screenshot` 需要桌面桥。

## 验收顺序

1. 记录源文件、单位、期望的实体类型/数量、坐标、图层、输出格式和路径。已有图纸默认在副本上处理，除非用户明确要求替换。
2. 执行命令。MCP 同时检查 JSON-RPC 传输与工具结果：`isError: true` 是失败；`command_line` 即使工具调用成功，也可能在结果的 `error` 字段报告命令错误。
3. 用 `inspect_drawing` 和 `query_entities` 核对图纸；必要时检查约束。渲染或预览整体图纸，包括标注与文字。
4. 保存到约定路径，在新进程重开交付文件，再检查关键实体。`cadcraft-cli info` 只证明 CADCraft 能读取。外部 DXF/DWG 兼容性须在目标 CAD 软件中单独测试。

## 故障恢复与不确定结果

| 现象 | 先检查 | 下一步 |
| --- | --- | --- |
| 找不到 `cadcraft-cli` | 宿主环境中的 `cadcraft-cli --version` | 按上游说明安装/构建或修复 PATH，再重新发现 |
| 命令或参数未知 | `cadcraft-cli commands` 或 MCP `list_commands` | 使用本机 CLI 契约修正调用 |
| `execute` 或 `command_line` 失败 | `isError`、`error`、`running` 与 `prompt` | 先检查状态；确认部分结果后再取消或撤销 |
| 桌面桥超时或断线 | 检查当前图纸或重开最近保存文件 | 把副作用视为**结果未知**，不要盲目重复创建/删除 |
| 保存或转换失败 | 退出码/工具结果与目标文件 | 不把旧文件当作新产物；保留来源并报告失败 |
| 导出文件在 CADCraft 可打开、在其他软件失败 | 用目标软件复现 | 记录格式/版本和不支持的特性；内部往返不是外部兼容证据 |

CADCraft 上游远程后端在传输错误后会重连并重试控制请求。这是实际运行行为，不是恰好执行一次的保证；回复丢失前请求可能已经执行。技能须核对图纸状态后才能决定是否重复。插件侧目前没有持久操作账本或自动回滚。

## 证据与归属

技能库通过 `python3 scripts/validate_skills.py` 检查元数据。几何、文件内容、桌面状态、宿主加载和外部互通各需对应的运行证据。技能源在本库维护；[`cadcraft-plugin`](https://github.com/full-aigc-plugins/cadcraft-plugin) 分发锁定副本。先修改源技能，再显式同步并验证插件快照。
