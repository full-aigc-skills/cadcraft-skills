# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 与第二版图纸建立几何比较 | `compare` | `{"path":"input/revision-b.dxf"}` |
| 2. 逐区域查看差异 | `compare.next` | `{}` |
| 3. 结束比较后保留工作图 | `compareclose` | `{}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`execute`，参数 `{"command": "compare", "params": {"path": "input/revision-b.dxf"}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

cadcraft-cli run input.dxf --cmd 'line {"points":[[0,0],[10,10]]}' --save output.dxf。多个 --cmd 同批次。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

检查 added/removed/changed 与区域；排除单位和坐标原点差异。

边界：比较前先打开A版；不按内部句柄单独判定几何是否相同。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。

## 两个真实版本与无差异分支

先打开A、明确B路径，读取两者单位与坐标基准；比较不做自动缩放或对齐。调用compare后先读取counts和regions，再逐项复核实体类型、位置与变化含义。只有返回非空regions才执行compare.next；完全相同的图纸不应请求不存在的变化区域。

最后compareclose关闭叠加；需要另存审阅状态时使用新路径。A/B文件不能被覆盖，叠加框不是新增设计实体。保存重开后复核当前图纸实体和原始文件摘要。方法返回成功不等于版本差异已审阅，更不等于可自动采用B的变更。
