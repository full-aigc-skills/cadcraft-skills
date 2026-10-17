# 从技能商店适配的场景方法

以下内容是基于已阅读技能的原创 Craft 指导。沿用现有配方的实际命令；这里补充任务判断和结果检查，不将同一配方再计为新增场景。商店提供发现入口，原技能使用的软件、服务和依赖不会随本插件安装。

示例步骤是参数模板，不能直接作为通用执行脚本。先取当前会话的文档、图层、片段或故事ID，解析所有引用，再按实际工具schema执行；尺寸、坐标、路径和文本按本次任务调整。已打开编辑器时使用同一个MCP会话；独立CLI文件编辑不能证明界面同步。

## 由明确尺寸重建零件

参考：[pengxiaoan/autocad-dwg-redraw-skill/autocad-image-redraw](https://github.com/pengxiaoan/autocad-dwg-redraw-skill/blob/ed182ec5966caaaf1d82d6ad4015435a27a8a909/skills/autocad-image-redraw/SKILL.md)。

从原图或任务书提取单位、基准、孔径和孔距，区分已知尺寸、推算值与看不清的值；先主轮廓后孔和标注。没有标尺时不从像素直接猜毫米。

原配方：`mounting-plate-four-holes`。输入与边界：100×60毫米板、四角距边10毫米、孔直径6毫米；按实际零件重算。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `new` | `{"metric":true,"template":"."}` |
| 2 | `setvar` | `{"name":"INSUNITS","value":4}` |
| 3 | `layer.new` | `{"name":"OUTLINE","color":7,"current":true}` |
| 4 | `pline` | `{"vertices":[[0,0],[100,0],[100,60],[0,60]],"closed":true}` |
| 5 | `layer.new` | `{"name":"HOLES","color":1,"current":true}` |
| 6 | `circle` | `{"center":[10,10],"radius":3}` |
| 7 | `circle` | `{"center":[90,10],"radius":3}` |
| 8 | `circle` | `{"center":[90,50],"radius":3}` |
| 9 | `circle` | `{"center":[10,50],"radius":3}` |
| 10 | `layer.new` | `{"name":"DIMENSIONS","color":7,"current":true}` |
| 11 | `dimlinear` | `{"p1":[0,0],"p2":[100,0],"at":[50,-12]}` |
| 12 | `dimlinear` | `{"p1":[100,0],"p2":[100,60],"at":[115,30]}` |
| 13 | `dimdiameter` | `{"center":[10,10],"point":[13,10]}` |

检查：核对孔心、孔径、外形与尺寸实体；未知公差明确列出。

能力边界：示例100×60等尺寸必须替换；外观相似不构成制造精度证明。

原配方结果检查：["闭合板轮廓面积6000平方毫米", "四孔圆心和半径正确", "三个原生尺寸实体保存重开后存在"]

原配方限制：本例不包含公差、材料或加工认证；实际生产按已批准图样补齐。

## 平面图的几何关系

参考：[pengxiaoan/autocad-dwg-redraw-skill/autocad-image-redraw](https://github.com/pengxiaoan/autocad-dwg-redraw-skill/blob/ed182ec5966caaaf1d82d6ad4015435a27a8a909/skills/autocad-image-redraw/SKILL.md)；[js2005happy/autocad-dynamic-draw/autocad-dynamic-draw](https://github.com/js2005happy/autocad-dynamic-draw/blob/becde1bab887f04e5c370a9e318a126076e7cf1b/SKILL.md)。

逐视图确认比例，先墙段与门洞，再放门扇和开启弧；门洞宽度由标注决定，弧和门扇共用铰点。分步展示时使用当前编辑器会话。

原配方：`room-door-opening`。输入与边界：5000×4000毫米空间，底边2000至3000留1000毫米门洞。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `new` | `{"metric":true,"template":"."}` |
| 2 | `setvar` | `{"name":"INSUNITS","value":4}` |
| 3 | `setvar` | `{"name":"DIMSCALE","value":100}` |
| 4 | `layer.new` | `{"name":"WALLS","color":7,"current":true}` |
| 5 | `line` | `{"points":[[0,0],[2000,0]]}` |
| 6 | `line` | `{"points":[[3000,0],[5000,0],[5000,4000],[0,4000],[0,0]]}` |
| 7 | `layer.new` | `{"name":"DOOR","color":1,"current":true}` |
| 8 | `line` | `{"points":[[2000,0],[2000,1000]]}` |
| 9 | `arc` | `{"center":[2000,0],"radius":1000,"start":0,"end":90}` |
| 10 | `layer.new` | `{"name":"LABELS","color":7,"current":true}` |
| 11 | `text` | `{"at":[1800,2000],"text":"ROOM A","height":200}` |
| 12 | `layer.new` | `{"name":"DIMENSIONS","color":7,"current":true}` |
| 13 | `dimlinear` | `{"p1":[0,0],"p2":[5000,0],"at":[2500,-600]}` |
| 14 | `dimlinear` | `{"p1":[5000,0],"p2":[5000,4000],"at":[5600,2000]}` |

检查：墙线没有封住门洞，开启方向和尺寸符合任务。

能力边界：不调用AutoCAD COM/pywin32；独立CLI执行不能声称宿主画面实时变化。

原配方结果检查：["墙线未穿过门洞", "门扇与开启弧对应同一铰点", "总长总宽尺寸存在"]

原配方限制：墙体为单线示意，不是施工图；门弧只是开启示意，不自动检查碰撞或建筑规范。

## 可复核的图框交接

参考：[js2005happy/autocad-dynamic-draw/autocad-dynamic-draw](https://github.com/js2005happy/autocad-dynamic-draw/blob/becde1bab887f04e5c370a9e318a126076e7cf1b/SKILL.md)。

先定单位、基准和图元顺序，把图号、版本、单位做成可改文字；模型空间图框完成后再检查打印纸张、比例与边距。

原配方：`drawing-border-title`。输入与边界：毫米模型空间297×210边框，内框留10毫米；标题栏宽100高30。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `new` | `{"metric":true,"template":"."}` |
| 2 | `setvar` | `{"name":"INSUNITS","value":4}` |
| 3 | `layer.new` | `{"name":"BORDER","color":7,"current":true}` |
| 4 | `pline` | `{"vertices":[[0,0],[297,0],[297,210],[0,210]],"closed":true}` |
| 5 | `pline` | `{"vertices":[[10,10],[287,10],[287,200],[10,200]],"closed":true}` |
| 6 | `pline` | `{"vertices":[[187,10],[287,10],[287,40],[187,40]],"closed":true}` |
| 7 | `layer.new` | `{"name":"LABELS","color":7,"current":true}` |
| 8 | `text` | `{"at":[192,28],"text":"DRAWING A-001","height":3}` |
| 9 | `text` | `{"at":[192,19],"text":"UNITS mm","height":3}` |
| 10 | `text` | `{"at":[192,12],"text":"REV A","height":3}` |

检查：图号与版本可编辑，重开后尺寸实体保留，打印比例单独核对。

能力边界：模型297×210不自动代表A4打印1:1；没有移植DWG生成器或动态延时脚本。

原配方结果检查：["三个闭合框保留", "标题栏文字可编辑", "图框实体尺寸297×210毫米"]

原配方限制：模型图框不等于纸张配置；另行配置plot纸张、比例与边距，不能仅凭模型尺寸声称打印1:1。

## 版本与执行

执行包装沿用本技能主文件。先确定实际图纸单位和尺度；模型坐标、纸张和打印比例分别检查。无标尺的像素描图不能声称工程尺寸准确。 保存到未占用路径并重开，按实际产物检查；本轮文档适配未新增宿主或真实媒体验收。

本技能内的[商店来源与参数记录](market-adaptations.json)记录版本、内容哈希和观察方法；没有分发第三方脚本或正文。
