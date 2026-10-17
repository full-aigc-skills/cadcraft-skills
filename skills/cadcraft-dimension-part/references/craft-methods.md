# 真实零件的原生标注

本例先创建实际轮廓与两个圆孔，再由相同坐标生成尺寸；不是在空图上写80、40、R5。既有图纸先inspect/query_entities读取单位、轮廓端点、孔心与半径，按当前几何重算参数。仅新建时执行newDocumentOnly步骤，不向既有图纸叠画示例。

| 次序与目的 | 方法 | 参数示例 |
| --- | --- | --- |
| 1. 仅新图创建毫米文档 | `new` | `{"metric":true,"template":"."}` |
| 2. 仅新图显式毫米单位 | `setvar` | `{"name":"INSUNITS","value":4}` |
| 3. 仅新图使用零件尺寸标注比例 | `setvar` | `{"name":"DIMSCALE","value":1}` |
| 4. 轮廓与尺寸分层 | `layer.new` | `{"name":"OUTLINE","color":7,"current":true}` |
| 5. 按确认尺寸创建80×40外轮廓 | `pline` | `{"vertices":[[0,0],[80,0],[80,40],[0,40]],"closed":true}` |
| 6. 创建实际孔，后续尺寸必须对应孔心和孔径 | `circle` | `{"center":[20,20],"radius":5}` |
| 7. 创建实际孔，后续尺寸必须对应孔心和孔径 | `circle` | `{"center":[60,20],"radius":5}` |
| 8. 进入尺寸图层 | `layer.new` | `{"name":"DIMENSIONS","color":7,"current":true}` |
| 9. 量取外轮廓实际宽度 | `dimlinear` | `{"p1":[0,0],"p2":[80,0],"at":[40,-10]}` |
| 10. 量取外轮廓实际高度 | `dimlinear` | `{"p1":[80,0],"p2":[80,40],"at":[90,20]}` |
| 11. 标注两个真实孔心间距 | `dimlinear` | `{"p1":[20,20],"p2":[60,20],"at":[40,55]}` |
| 12. 用真实孔心与圆周点生成R5半径，不写文字冒充数值 | `dimradius` | `{"center":[20,20],"point":[25,20]}` |
| 13. 核对尺寸与实际几何 | `drawing.inspect` | `{"entities":true,"limit":200}` |

## 实际调用与核对

同一编辑器MCP使用`execute {"command":"dimlinear","params":{"p1":[20,20],"p2":[60,20],"at":[40,55]}}`；先等editor_status就绪并读取实时schema。不要为已有对象另开无关CLI进程后宣称画面同步。

独立文件任务把各行组合为同一次`cadcraft-cli run --metric --cmd <方法加JSON> ... --save part-dimensions.dxf`，每条为单个argv，Windows不拼接shell字符串。原文件任务使用副本、跳过初始化和示例几何，保留原始对象。

新进程`cadcraft-cli info part-dimensions.dxf`和`cadcraft-cli run part-dimensions.dxf --cmd 'drawing.inspect {"entities":true,"limit":200}'`核对闭合轮廓、两孔和四个原生尺寸。量测宽80、高40、孔距40、半径5；禁止尺寸文字覆盖为期望数字。导出SVG审阅尺寸重叠和小字。材料、公差与制造可用性需由用户另行确认，本流程不自动承诺。

步骤在[craft-steps.json](craft-steps.json)，参数目录在[craft-command-evidence.json](craft-command-evidence.json)，参考事实与许可在[workflow-sources.json](workflow-sources.json)。
