---
name: cadcraft-bolt-circle
description: 当用户需要在CADCraft绘制等角螺栓孔、法兰孔位或按节圆直径重建均布孔图时使用；指导真实句柄绑定、极轴阵列、原生标注和保存重开几何核对。
license: Apache-2.0
---

# 等角孔分布图

先核对单位、圆心、外径、中心孔径、节圆直径、孔径、孔数和起始角。直径必须除以二再传入radius；count包括原始种子孔。下列尺寸只是可修改绘图示例，不是制造设计。

读取[方法与参数](references/craft-methods.md)、[原始步骤](references/craft-steps.json)、[命令证据](references/craft-command-evidence.json)和[GitHub来源](references/workflow-sources.json)。

1. 既有图先inspect和getvar读取单位、实体与目标区域，保留输入。独立脚本只创建新图，不能用于覆盖既有工程。
2. 按外轮廓/孔/节圆参考/尺寸分层；节圆不是加工孔。仅对当前任务创建的种子圆操作。
3. 用circle返回的真实handle调用arraypolar，不写死100，也不将图层全部圆选入阵列。angle固定360，count为完整圆周总孔数。
4. 读回每个孔圆心、半径及图层；按模360排序角度，检查首尾间隔，防止0/360重复孔。非关联阵列参数改变时从原输入重建，不能对全部旧孔再次阵列。
5. 根据同一孔心/圆周点生成原生半径尺寸，不用文字覆盖数值。保留DXF并导出PNG/SVG，重开量测、检查标注遮挡。

## CLI新图执行

`python3 <本技能目录>/scripts/draw_bolt_circle.py --cli <cadcraft-cli路径> --output <新输出.dxf> --count 6 --pitch-radius 40 --hole-radius 3 --outer-radius 55 --bore-radius 15`

可加`--start-angle 30 --center 100 50`。参数使用半径和毫米、角度使用度。执行器以argv调用真实CLI，无shell拼接；拒绝非有限数、布尔JSON值、重叠孔、边界相交和已有输出，ASCII转义JSON保留中文路径。几何检查仅说明二维相交关系，不代表边距或强度合格。

## 同画面MCP

交给 **cadcraft-editor** 技能，独立安装：`npx skills add full-aigc-skills/cadcraft-skills --skill cadcraft-editor`。等editor_status就绪后读取当前execute schema；在同一会话逐条execute，捕获种子handle并替换后续参数，保存和render仍在该会话。不能另起CLI进程修改文件后声称内嵌画面已经同步。

本技能的原生运行、Windows与宿主同步状态分开记录，未运行的目标平台不能视为通过。
