# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 按实测毫米尺寸建立墙体层 | `layer.new` | `{"name":"WALL","current":true}` |
| 2. 沿测量坐标闭合外轮廓 | `pline` | `{"vertices":[[0,0],[5000,0],[5000,4000],[0,4000]],"closed":true}` |
| 3. 门窗与内墙逐段画线，示例为一条隔墙 | `line` | `{"points":[[2500,0],[2500,1800]]}` |
| 4. 放置不遮挡墙体的净尺寸 | `dimlinear` | `{"p1":[0,0],"p2":[5000,0],"at":[0,-400]}` |
| 5. 检查实体及单位 | `drawing.inspect` | `{"entities":true}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

本插件MCP包装：`execute`，参数 `{"command": "layer.new", "params": {"name": "WALL", "current": true}}`。后续行保持同一会话和对象选择，逐条检查实际结果。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

cadcraft-cli run input.dxf --cmd 'line {"points":[[0,0],[10,10]]}' --save output.dxf。多个 --cmd 同批次。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

核对房间净尺寸、门窗留口、墙体厚度与标注，不把示例矩形当真实房屋图。

边界：输入必须有可信单位与实测边长；多段线返回句柄后才可按需要 offset。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。
