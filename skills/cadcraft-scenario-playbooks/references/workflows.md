# CADCraft 绘图场景

工作流借鉴 LibreCAD 的单位、分层、真实尺寸和标注次序，示例几何为原创。只读取本次需要的场景。

## mounting-plate-four-holes：四孔安装板及尺寸

输入：100×60毫米板、四角距边10毫米、孔直径6毫米；按实际零件重算。

| 步骤与目的 | 方法 | 参数 |
| --- | --- | --- |
| 1. 仅新建任务时初始化毫米图纸 | `new` | `{"metric":true,"template":"."}` |
| 2. 显式设置单位为毫米 | `setvar` | `{"name":"INSUNITS","value":4}` |
| 3. 分离OUTLINE图层 | `layer.new` | `{"name":"OUTLINE","color":7,"current":true}` |
| 4. 创建真实闭合轮廓 | `pline` | `{"vertices":[[0,0],[100,0],[100,60],[0,60]],"closed":true}` |
| 5. 分离HOLES图层 | `layer.new` | `{"name":"HOLES","color":1,"current":true}` |
| 6. 绘制圆孔或外圆 | `circle` | `{"center":[10,10],"radius":3}` |
| 7. 绘制圆孔或外圆 | `circle` | `{"center":[90,10],"radius":3}` |
| 8. 绘制圆孔或外圆 | `circle` | `{"center":[90,50],"radius":3}` |
| 9. 绘制圆孔或外圆 | `circle` | `{"center":[10,50],"radius":3}` |
| 10. 分离DIMENSIONS图层 | `layer.new` | `{"name":"DIMENSIONS","color":7,"current":true}` |
| 11. 以实际端点生成尺寸，不覆盖数值 | `dimlinear` | `{"p1":[0,0],"p2":[100,0],"at":[50,-12]}` |
| 12. 以实际端点生成尺寸，不覆盖数值 | `dimlinear` | `{"p1":[100,0],"p2":[100,60],"at":[115,30]}` |
| 13. 标注孔的真实直径 | `dimdiameter` | `{"center":[10,10],"point":[13,10]}` |

检查：闭合板轮廓面积6000平方毫米；四孔圆心和半径正确；三个原生尺寸实体保存重开后存在。

边界：本例不包含公差、材料或加工认证；实际生产按已批准图样补齐。

## flange-bolt-circle：带中心孔的法兰定位图

输入：外径60、内径24、孔径6、螺栓孔节圆直径40毫米。

| 步骤与目的 | 方法 | 参数 |
| --- | --- | --- |
| 1. 仅新建任务时初始化毫米图纸 | `new` | `{"metric":true,"template":"."}` |
| 2. 显式设置单位为毫米 | `setvar` | `{"name":"INSUNITS","value":4}` |
| 3. 分离RINGS图层 | `layer.new` | `{"name":"RINGS","color":7,"current":true}` |
| 4. 绘制圆孔或外圆 | `circle` | `{"center":[0,0],"radius":30}` |
| 5. 绘制圆孔或外圆 | `circle` | `{"center":[0,0],"radius":12}` |
| 6. 分离HOLES图层 | `layer.new` | `{"name":"HOLES","color":1,"current":true}` |
| 7. 绘制圆孔或外圆 | `circle` | `{"center":[20,0],"radius":3}` |
| 8. 绘制圆孔或外圆 | `circle` | `{"center":[0,20],"radius":3}` |
| 9. 绘制圆孔或外圆 | `circle` | `{"center":[-20,0],"radius":3}` |
| 10. 绘制圆孔或外圆 | `circle` | `{"center":[0,-20],"radius":3}` |
| 11. 分离CENTERLINES图层 | `layer.new` | `{"name":"CENTERLINES","color":8,"current":true}` |
| 12. 绘制定位线 | `line` | `{"points":[[-35,0],[35,0]]}` |
| 13. 绘制定位线 | `line` | `{"points":[[0,-35],[0,35]]}` |
| 14. 分离DIMENSIONS图层 | `layer.new` | `{"name":"DIMENSIONS","color":7,"current":true}` |
| 15. 标注外径 | `dimdiameter` | `{"center":[0,0],"point":[30,0]}` |
| 16. 标注内径 | `dimdiameter` | `{"center":[0,0],"point":[12,0]}` |

检查：同心双圆和四个定位孔保留；中心线与实体分层；不把节圆半径误当直径。

边界：图示未做强度计算；交付前核对配合与公差，中心线层不代表已设置虚线。

## room-door-opening：带门洞和开启弧的房间平面

输入：5000×4000毫米空间，底边2000至3000留1000毫米门洞。

| 步骤与目的 | 方法 | 参数 |
| --- | --- | --- |
| 1. 仅新建任务时初始化毫米图纸 | `new` | `{"metric":true,"template":"."}` |
| 2. 显式设置单位为毫米 | `setvar` | `{"name":"INSUNITS","value":4}` |
| 3. 仅本新建房间图放大原生标注文字与箭头 | `setvar` | `{"name":"DIMSCALE","value":100}` |
| 4. 分离WALLS图层 | `layer.new` | `{"name":"WALLS","color":7,"current":true}` |
| 5. 绘制定位线 | `line` | `{"points":[[0,0],[2000,0]]}` |
| 6. 绘制定位线 | `line` | `{"points":[[3000,0],[5000,0],[5000,4000],[0,4000],[0,0]]}` |
| 7. 分离DOOR图层 | `layer.new` | `{"name":"DOOR","color":1,"current":true}` |
| 8. 绘制定位线 | `line` | `{"points":[[2000,0],[2000,1000]]}` |
| 9. 门开启示意弧 | `arc` | `{"center":[2000,0],"radius":1000,"start":0,"end":90}` |
| 10. 分离LABELS图层 | `layer.new` | `{"name":"LABELS","color":7,"current":true}` |
| 11. 加入房间标识 | `text` | `{"at":[1800,2000],"text":"ROOM A","height":200}` |
| 12. 分离DIMENSIONS图层 | `layer.new` | `{"name":"DIMENSIONS","color":7,"current":true}` |
| 13. 以实际端点生成尺寸，不覆盖数值 | `dimlinear` | `{"p1":[0,0],"p2":[5000,0],"at":[2500,-600]}` |
| 14. 以实际端点生成尺寸，不覆盖数值 | `dimlinear` | `{"p1":[5000,0],"p2":[5000,4000],"at":[5600,2000]}` |

检查：墙线未穿过门洞；门扇与开启弧对应同一铰点；总长总宽尺寸存在。

边界：墙体为单线示意，不是施工图；门弧只是开启示意，不自动检查碰撞或建筑规范。

## equipment-grid-layout：设备布置定位网格

输入：3000×3000毫米定位区，1000毫米间距；设备尺寸另行测量。

| 步骤与目的 | 方法 | 参数 |
| --- | --- | --- |
| 1. 仅新建任务时初始化毫米图纸 | `new` | `{"metric":true,"template":"."}` |
| 2. 显式设置单位为毫米 | `setvar` | `{"name":"INSUNITS","value":4}` |
| 3. 分离GRID图层 | `layer.new` | `{"name":"GRID","color":8,"current":true}` |
| 4. 创建真实闭合轮廓 | `pline` | `{"vertices":[[0,0],[3000,0],[3000,3000],[0,3000]],"closed":true}` |
| 5. 绘制定位线 | `line` | `{"points":[[1000,0],[1000,3000]]}` |
| 6. 绘制定位线 | `line` | `{"points":[[2000,0],[2000,3000]]}` |
| 7. 绘制定位线 | `line` | `{"points":[[0,1000],[3000,1000]]}` |
| 8. 绘制定位线 | `line` | `{"points":[[0,2000],[3000,2000]]}` |
| 9. 分离LABELS图层 | `layer.new` | `{"name":"LABELS","color":7,"current":true}` |
| 10. 网格单元标识 | `text` | `{"at":[300,450],"text":"A1","height":120}` |
| 11. 网格单元标识 | `text` | `{"at":[1300,450],"text":"B1","height":120}` |
| 12. 网格单元标识 | `text` | `{"at":[2300,450],"text":"C1","height":120}` |
| 13. 网格单元标识 | `text` | `{"at":[300,1450],"text":"A2","height":120}` |
| 14. 网格单元标识 | `text` | `{"at":[1300,1450],"text":"B2","height":120}` |
| 15. 网格单元标识 | `text` | `{"at":[2300,1450],"text":"C2","height":120}` |
| 16. 网格单元标识 | `text` | `{"at":[300,2450],"text":"A3","height":120}` |
| 17. 网格单元标识 | `text` | `{"at":[1300,2450],"text":"B3","height":120}` |
| 18. 网格单元标识 | `text` | `{"at":[2300,2450],"text":"C3","height":120}` |

检查：四条内部网格线间距1000；九个格网标签保留；边界为闭合轮廓。

边界：仅定位网格，不代表设备已摆放或满足检修距离。

## pipe-route-length：折线路由分段长度图

输入：平面中心线路由三段80、60、80毫米；不含弯头附加长度。

| 步骤与目的 | 方法 | 参数 |
| --- | --- | --- |
| 1. 仅新建任务时初始化毫米图纸 | `new` | `{"metric":true,"template":"."}` |
| 2. 显式设置单位为毫米 | `setvar` | `{"name":"INSUNITS","value":4}` |
| 3. 分离ROUTE图层 | `layer.new` | `{"name":"ROUTE","color":1,"current":true}` |
| 4. 绘制有宽度的路由中心线 | `pline` | `{"vertices":[[0,0],[80,0],[80,60],[160,60]],"closed":false,"width":2}` |
| 5. 分离DIMENSIONS图层 | `layer.new` | `{"name":"DIMENSIONS","color":7,"current":true}` |
| 6. 以实际端点生成尺寸，不覆盖数值 | `dimlinear` | `{"p1":[0,0],"p2":[80,0],"at":[40,-12]}` |
| 7. 以实际端点生成尺寸，不覆盖数值 | `dimlinear` | `{"p1":[80,0],"p2":[80,60],"at":[95,30]}` |
| 8. 以实际端点生成尺寸，不覆盖数值 | `dimlinear` | `{"p1":[80,60],"p2":[160,60],"at":[120,75]}` |

检查：实际折线长度220毫米；不是首尾两点直线距离；三段尺寸均按几何生成。

边界：这只是平面路由；实际管材下料需计入弯曲半径、接头和三维高度。

## linear-hole-pattern：等距孔列定位图

输入：120×30毫米板，6个直径4孔；x=10开始，20毫米节距，y=15。

| 步骤与目的 | 方法 | 参数 |
| --- | --- | --- |
| 1. 仅新建任务时初始化毫米图纸 | `new` | `{"metric":true,"template":"."}` |
| 2. 显式设置单位为毫米 | `setvar` | `{"name":"INSUNITS","value":4}` |
| 3. 分离OUTLINE图层 | `layer.new` | `{"name":"OUTLINE","color":7,"current":true}` |
| 4. 创建真实闭合轮廓 | `pline` | `{"vertices":[[0,0],[120,0],[120,30],[0,30]],"closed":true}` |
| 5. 分离HOLES图层 | `layer.new` | `{"name":"HOLES","color":1,"current":true}` |
| 6. 绘制圆孔或外圆 | `circle` | `{"center":[10,15],"radius":2}` |
| 7. 绘制圆孔或外圆 | `circle` | `{"center":[30,15],"radius":2}` |
| 8. 绘制圆孔或外圆 | `circle` | `{"center":[50,15],"radius":2}` |
| 9. 绘制圆孔或外圆 | `circle` | `{"center":[70,15],"radius":2}` |
| 10. 绘制圆孔或外圆 | `circle` | `{"center":[90,15],"radius":2}` |
| 11. 绘制圆孔或外圆 | `circle` | `{"center":[110,15],"radius":2}` |
| 12. 分离DIMENSIONS图层 | `layer.new` | `{"name":"DIMENSIONS","color":7,"current":true}` |
| 13. 以实际端点生成尺寸，不覆盖数值 | `dimlinear` | `{"p1":[10,15],"p2":[30,15],"at":[20,42]}` |
| 14. 以实际端点生成尺寸，不覆盖数值 | `dimlinear` | `{"p1":[0,0],"p2":[120,0],"at":[60,-12]}` |

检查：孔数6且节距20；两端余量10；孔半径2而非直径2。

边界：孔列位置由当前板件尺寸重算，不能直接复制示例到不同比例图纸。

## notched-part-area：缺口零件轮廓与面积

输入：100×80毫米外包矩形，右上30×30缺口。

| 步骤与目的 | 方法 | 参数 |
| --- | --- | --- |
| 1. 仅新建任务时初始化毫米图纸 | `new` | `{"metric":true,"template":"."}` |
| 2. 显式设置单位为毫米 | `setvar` | `{"name":"INSUNITS","value":4}` |
| 3. 分离OUTLINE图层 | `layer.new` | `{"name":"OUTLINE","color":7,"current":true}` |
| 4. 创建真实闭合轮廓 | `pline` | `{"vertices":[[0,0],[100,0],[100,50],[70,50],[70,80],[0,80]],"closed":true}` |
| 5. 查询当前示例轮廓面积 | `area` | `{"points":[[0,0],[100,0],[100,50],[70,50],[70,80],[0,80]]}` |
| 6. 分离DIMENSIONS图层 | `layer.new` | `{"name":"DIMENSIONS","color":7,"current":true}` |
| 7. 以实际端点生成尺寸，不覆盖数值 | `dimlinear` | `{"p1":[0,0],"p2":[100,0],"at":[50,-12]}` |
| 8. 以实际端点生成尺寸，不覆盖数值 | `dimlinear` | `{"p1":[70,50],"p2":[100,50],"at":[85,65]}` |

检查：DXF实际闭合顶点面积7100；缺口尺寸30×30；不是直接把外包矩形面积当净面积。

边界：area示例points必须与实际轮廓一致；已有图纸优先对实际handle查询而非重输假定点。

## drawing-border-title：带标题栏的模型空间图框

输入：毫米模型空间297×210边框，内框留10毫米；标题栏宽100高30。

| 步骤与目的 | 方法 | 参数 |
| --- | --- | --- |
| 1. 仅新建任务时初始化毫米图纸 | `new` | `{"metric":true,"template":"."}` |
| 2. 显式设置单位为毫米 | `setvar` | `{"name":"INSUNITS","value":4}` |
| 3. 分离BORDER图层 | `layer.new` | `{"name":"BORDER","color":7,"current":true}` |
| 4. 创建真实闭合轮廓 | `pline` | `{"vertices":[[0,0],[297,0],[297,210],[0,210]],"closed":true}` |
| 5. 创建真实闭合轮廓 | `pline` | `{"vertices":[[10,10],[287,10],[287,200],[10,200]],"closed":true}` |
| 6. 创建真实闭合轮廓 | `pline` | `{"vertices":[[187,10],[287,10],[287,40],[187,40]],"closed":true}` |
| 7. 分离LABELS图层 | `layer.new` | `{"name":"LABELS","color":7,"current":true}` |
| 8. 图号 | `text` | `{"at":[192,28],"text":"DRAWING A-001","height":3}` |
| 9. 单位 | `text` | `{"at":[192,19],"text":"UNITS mm","height":3}` |
| 10. 修订 | `text` | `{"at":[192,12],"text":"REV A","height":3}` |

检查：三个闭合框保留；标题栏文字可编辑；图框实体尺寸297×210毫米。

边界：模型图框不等于纸张配置；另行配置plot纸张、比例与边距，不能仅凭模型尺寸声称打印1:1。

