# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 检查对象当前层与实体 | `drawing.inspect` | `{"entities":true}` |
| 2. 建立有用途的标注层 | `layer.new` | `{"name":"DIMENSIONS","color":2}` |
| 3. 把底图层锁定且不打印 | `layer.set` | `{"name":"REFERENCE","locked":true,"plot":false}` |
| 4. 统一墙体线宽 | `layer.set` | `{"name":"WALL","lineweight":0.35}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`execute`，参数 `{"command": "drawing.inspect", "params": {"entities": true}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

cadcraft-cli run input.dxf --cmd 'line {"points":[[0,0],[10,10]]}' --save output.dxf。多个 --cmd 同批次。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

整理前后实体数量变化有解释，锁定参考层仍存在，打印层配置正确。

边界：REFERENCE 与 WALL 是实际存在层名的示例；不存在时先查层，再创建或重映射。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。
