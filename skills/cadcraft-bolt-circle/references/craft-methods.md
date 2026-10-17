# 原生方法与绑定

`circle {"center":[40,0],"radius":3}` 返回`{"handle":"..."}`。保存真实handle，然后`arraypolar {"handles":[真实handle],"center":[0,0],"count":6,"angle":360,"rotate":true,"associative":false}`。此调用新增5孔，合计6孔，不再额外创建终点孔。

默认外半径55、中心孔15、节圆半径40、孔半径3。圆心为C，起始角a，孔心为`C+P*(cos(a+360*i/N),sin(a+360*i/N))`，i=0..N-1。需满足`P+r<R外`、`P-r>R内`和`2*P*sin(pi/N)>2*r`。相切也拒绝。全部参数为确认的绘图尺寸，不能据此承诺制造可用性。

同画面MCP对各步使用`execute {"command":命令,"params":参数}`；`$seed.handle`是手册绑定标记，原生API不会替换。CLI执行器先保存临时DXF以取得返回句柄，再对该临时图调用阵列，最终保存至新输出。临时图不属于用户工程。

非关联阵列明确为独立圆；本流程不宣称arrayedit可修改它。改孔数时从原始图重建，导出加工轮廓前排除PITCH_GUIDE与DIMENSIONS，并与用户确认真实交付规范。返回DXF、PNG、SVG及核对结果，不交付未经核查的文件。
