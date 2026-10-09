---
name: cadcraft-use
description: 当用户要用 CADCraft 创建或修改二维 CAD 图纸、图层、标注、块、布局或导出 DXF/DWG/PDF 时使用；负责选择 CLI 或 MCP 路径并验收真实图纸。
---

# CADCraft 绘图入口

CADCraft 的共同执行核心是 `Session` 命令注册表。先确定输入图纸、单位、目标几何、输出格式和交付路径；已有图纸时保留原件，在副本或明确授权的目标文件上操作。用 `list_commands` 查询当前安装版本的命令、参数说明和 enabled 状态，不把技能中的示例当成完整命令规格。

## 选择入口

- 在已安装 `cadcraft-plugin` 的宿主中，使用插件的 `cadcraft` MCP 服务。新图纸、交互式命令、程序化命令、查询和渲染参见 **`cadcraft-mcp`** 技能。独立安装：`npx skills add full-aigc-skills/cadcraft-skills --skill cadcraft-mcp`。
- 本机有 `cadcraft-cli` 且任务是单次文件处理或无窗口批处理时，使用 **`cadcraft-cli`** 技能。独立安装：`npx skills add full-aigc-skills/cadcraft-skills --skill cadcraft-cli`。
- 需要确认屏幕菜单、鼠标操作或当前桌面状态时，启动 CADCraft 桌面应用的 `--control` 回环端口，再用 `cadcraft-cli mcp --connect 127.0.0.1:PORT` 接入；Headless `render` 只渲染图纸内容，不是桌面截图。

## 完成标准

1. 创建或修改后用 `inspect_drawing`、`query_entities` 核对实体类型、数量、Handle、图层和关键坐标；带约束的图纸还要查询约束满足状态。
2. 使用 `render` 检查布局与标注；需要确认桌面 UI 时用连接桌面的 `screenshot` 或实际预览。
3. 保存后重新打开交付文件，确认文件可读并复核关键实体。DXF/DWG 的外部软件兼容性需要相应软件的实际打开证据；本项目内部往返不等于外部兼容。

不要把一次工具调用的传输成功等同于命令成功。远程连接超时后先查询图纸状态，避免盲目重发可能已执行的创建命令。Web 端当前不支持 DWG。
