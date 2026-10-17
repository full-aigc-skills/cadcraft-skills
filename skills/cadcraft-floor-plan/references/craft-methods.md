# 房间平面图：方法、参数与完成标准

输入示例：5000×4000毫米，底边2000至3000为1000毫米门洞。门开向内。用户尺寸不完整时先确认，不从照片猜测。先读实际CLI commands或同会话MCP工具schema。

仅新建绘图时执行标记`newDocumentOnly`的new、INSUNITS与DIMSCALE步骤。既有工程先读取单位、当前图层和目标实体；下列坐标只供独立新图示例，不能直接叠加到既有房间。

| 步骤 | 方法 | 参数示例 |
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

## 同一会话执行

MCP使用当前编辑器会话的`execute {"command":"line","params":{"points":[[0,0],[2000,0]]}}`，逐步检查返回。独立CLI把各行作为同一次`cadcraft-cli run --metric --cmd <方法加JSON> ... --save room-review.dxf`的argv；Windows使用参数数组，不拼接shell字符串。首次用实例必须在副本/新图，保存为新名称。

本例底墙由两段分开画，不能再用闭合四边形补齐，否则会封住门洞。单线墙不等于真实墙厚；需要双线墙、窗洞与净空时按用户确认后的实体另建。

## 保存与核对

新进程`cadcraft-cli info room-review.dxf`与`cadcraft-cli run room-review.dxf --cmd 'drawing.inspect {"entities":true,"limit":200}'`读取实体；核对五段墙、门扇及四分之一圆弧，底墙不能跨越[2000,3000]。原生DIMENSION须量得5000和4000，检查无自定义数值覆盖。检查INSUNITS=4、DIMSCALE=100以及ROOM A标签。

`cadcraft-cli convert room-review.dxf room-review.svg`导出审阅图；查看门开启方向、标注重叠和白底文字对比。尺寸与图层检查通过不等于施工图或宿主画面同步验收。

结构化步骤见[craft-steps.json](craft-steps.json)，命令目录见[craft-command-evidence.json](craft-command-evidence.json)，来源及许可见[workflow-sources.json](workflow-sources.json)。正文与参数为原创适配，来源不作运行依赖。
