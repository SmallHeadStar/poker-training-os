# 验收检查模板

当一个任务做完后，用这个模板让 Codex 站在验收视角检查一遍。

```text
请先读取：
- AGENTS.md
- docs/agents/00_agent_map.md

检查对象：
<这里写要检查的文件、功能或 PR>

检查重点：
- 任务是否仍然保持本地、赛后、手动导入的边界？
- RAW / BASE / DERIVED / METRIC 这些事实层是否仍然确定性？
- 如果 schema、tag、stat、detector 变化了，文档是否同步更新？
- parser、tag、stat、detector 的行为是否有测试？
- 面向用户的文案是否避免了实时建议？
- 验证结果是否如实说明？

输出时先列问题：
- 严重程度
- 文件或路径
- 问题说明
- 建议修复或验证方式

除非用户明确要求，否则不要直接改代码。
```
