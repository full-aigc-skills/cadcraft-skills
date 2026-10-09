---
name: cadcraft-mcp
description: 当 Agent 通过 CADCraft MCP 进行交互绘图、JSON 命令、图纸查询或渲染时使用；覆盖 Headless 与桌面连接模式及失败后的状态核实。
---

# CADCraft MCP

插件提供 `cadcraft` stdio 服务，默认运行 `cadcraft-cli mcp` 的 Headless 会话。若任务要求操作正在运行的桌面应用，可连接其 `127.0.0.1:PORT` 控制服务；在宿主 MCP 配置中将启动参数改为 `launch.py --connect 127.0.0.1:PORT`。一个 Headless MCP 进程只维护自己的图纸状态；不同进程间用保存文件交接。

## 操作

1. `list_commands` 发现当前命令 ID、参数文本和启用状态。
2. `command_line {"text":"rectang 0,0 100,60"}` 模拟逐步提示；`execute {"command":"circle","params":{"center":[10,10],"radius":4}}` 直接执行 JSON，通常更适合精确自动化。程序化调用不会弹出交互对话框。
3. `inspect_drawing` 与 `query_entities` 检查实体、图层和坐标；`render` 返回图纸 PNG。连接桌面后额外可用 `screenshot`、`ui_inspect` 和 `ui_click`。
4. `save {"path":"/absolute/output.dxf"}` 后重新打开并复核关键内容；保存或打开是文件写入/读取操作，先确定路径及覆盖授权。

`execute` 的 `isError` 应被视为失败。`command_line` 可能在正常 MCP 结果的 `error` 字段中报告命令错误，也要检查该字段和当前 `running` / `prompt`。若约束求解报告失败，检查约束状态与几何，不以命令返回成功替代验收。

桌面桥在传输失败后可能重发相同请求；发生超时或断线时，将创建/删除等副作用视为**结果未知**，先查询当前图纸或重新打开保存文件，确认是否已生效后再决定后续动作。取消交互命令可能保留已绘制的部分；需要恢复原状态时检查并明确执行撤销。脚本或多命令任务要在每个重要步骤后保存 Handle 和预期实体快照。
