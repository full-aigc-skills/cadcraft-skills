# CADCraft Skills

独立的 CADCraft Agent Skills 源库，版本 `0.1.0-dev.0`。覆盖二维图纸创建与修改、无窗口 CLI 文件任务、MCP 绘图与验证。技能仅描述工作方法；实际绘图由 CADCraft `cadcraft-cli` / MCP 完成。

| Skill | 用途 |
| --- | --- |
| `cadcraft-use` | 选择入口并验收图纸 |
| `cadcraft-cli` | 无窗口生成、检查和转换 |
| `cadcraft-mcp` | Headless 或桌面桥 MCP 操作 |

安装单项：`npx skills add full-aigc-skills/cadcraft-skills --skill cadcraft-use`。三项可分别安装，不依赖兄弟技能目录。配套 Agent Plugin：`full-aigc-plugins/cadcraft-plugin`；插件中包含本库的哈希锁定快照。

当前源参考为 `storytold/cadcraft` `0.3.0`。运行前仍应检查本机 CLI 与命令目录。许可证 Apache-2.0。尚未进行宿主安装和真实 CAD 文件验收。

[简体中文](README.zh-CN.md)
