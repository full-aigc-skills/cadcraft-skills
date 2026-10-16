---
name: cadcraft-scenario-playbooks
description: 使用 CADCraft 绘制安装板、法兰孔系、门洞平面、设备网格、折线路由、等距孔列、缺口零件和带标题栏图框时使用，提供真实 CLI/MCP 方法、毫米坐标与保存重开检查。
license: Apache-2.0
---

# CADCraft 绘图场景

从[8条场景流程](references/workflows.md)选当前任务；[recipes.json](references/recipes.json)提供有序方法与参数，[命令证据](references/command-evidence.json)保存原生命令描述，[来源](references/sources.json)固定 GitHub 文档提交。

先运行`cadcraft-cli --version`和`cadcraft-cli commands`确认CLI就绪；技能不附带CLI。缺失时按[官方发行说明](https://github.com/storytold/cadcraft/releases)选择系统版本，安装须遵守宿主授权。先确认单位、实际尺寸和输出用途。每条默认独立图纸；组合多个场景时先安排位置和偏移，避免都从原点叠放。所有示例为毫米模型空间，图框不等于打印设置。孔参数radius为半径；尺寸由几何计算，不把期望数值写入text冒充量测。房间示例仅在新图设置DIMSCALE=100，使文字和箭头适配5000毫米空间；既有图纸先检查现有标注样式，不全局覆盖。白底审阅图使用深色尺寸与标签，避免屏幕图层色造成低对比度。图层分开轮廓、孔、中心线和尺寸。

## MCP 与 CLI

内嵌编辑器已有任务时，使用同一 MCP 会话。先读取当前工具schema与命令目录，再按步骤调用；原生CAD工具用`execute {"command":"circle","params":{"center":[10,10],"radius":3}}`；插件将增强运行时工具转交给宿主，以当前tools/list返回的名称和schema为准，不凭其他Craft工具名推测。返回handle用于后续实际对象选择，不能猜测。

独立CLI：`cadcraft-cli run --metric --cmd 'circle {"center":[10,10],"radius":3}' --save part.dxf`。每个`方法ID 空格 JSON`是单个argv；同一图纸的步骤放一次run中。Windows优先用进程参数数组，避免shell解释JSON。已有图纸用`run input.dxf`，跳过全部`newDocumentOnly`步骤，包括INSUNITS设置。先用`getvar {"name":"INSUNITS"}`读取既有单位，只有已确认毫米图纸可直接采用这些示例；英寸或米图纸须先在副本中明确转换实际坐标和尺寸，不能仅改单位变量。不要把本例的new用于已有会话而清空图纸。

保存为新名称后，`cadcraft-cli run part.dxf --cmd 'drawing.inspect {"entities":true}'`查询真实实体；用`texts`查询可读文字，以`convert part.dxf part.svg`输出审阅图。标注、孔心、轮廓闭合、单位都要检查，不能只看文件存在。原生CLI编辑另一文件不能证明内嵌编辑器同步变化；同画面工作必须执行当前桥会话支持的方法。

## 交付

保留可编辑DXF和审阅图。例子不代替工程设计、公差或制造要求；未指定的孔距、材料与公差不能自行宣称满足。assertions仅适用于随附示例的技术回归，真实图样应按实际数据检查并查看成图。
