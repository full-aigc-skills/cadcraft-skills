---
name: cadcraft-cli
description: 当需要用已安装的 cadcraft-cli 无窗口检查、生成、修改、转换或渲染 CADCraft 图纸时使用；适合单次可重复的文件任务。
---

# CADCraft CLI

先运行 `cadcraft-cli --version` 和 `cadcraft-cli commands` 确认实际可用命令。该 CLI 是 CADCraft 的独立可执行文件；技能包不安装或附带它。可从 CADCraft 官方发行版安装，或按源仓库构建。不要从未核实的来源下载二进制。

常用入口：

```sh
cadcraft-cli info drawing.dxf
cadcraft-cli run --metric --cmd 'circle {"center":[10,10],"radius":4}' --save output.dxf --export preview.png
cadcraft-cli run input.dxf --script 'LINE 0,0 10,0\n' --save output.dxf
cadcraft-cli convert input.dxf output.svg
```

`--cmd` 接受命令 ID 和 JSON 参数；`--script` 走交互式命令行语法。复杂命令的实际参数通过同版本 `cadcraft-cli commands` 或 MCP `list_commands` 获取。源图纸和输出文件应分开，除非用户明确要求覆盖。生成后用 `info` 检查文件，必要时用新的进程打开并导出预览。

`info` 只能说明 CADCraft 能读取文件；几何、图层、标注、布局、PDF 可视结果还要按任务逐项检查。DWG 走原生 `acadrust`↔DXF 桥；Web 构建不支持 DWG。对于输入损坏、命令错误或转换失败，记录退出码和错误，不把先前文件当成新结果。
