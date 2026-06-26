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
- H2N4 导出能力是否仍被标记为 pending local verification，除非用户已验证？
- 是否避免了 H2N4 UI 自动化和 direct H2N4 DB adapter？
- RAW / H2N_EXPORT / MANUAL_INPUT / BASE / DERIVED / METRIC 这些事实层是否仍然确定性？
- 输出事实是否保留 source label？
- 如果 h2n bridge、export contract、output layer、schema、tag、stat、detector 变化了，文档是否同步更新？
- ingest、parser、tag、stat、detector 或 report 行为是否有测试？
- issue card / candidate match 是否把 final result、showdown cards 或 hand_net_bb 当成错误证明？
- 面向用户的文案是否避免了实时建议？
- 验证结果是否如实说明？

输出时先列问题：
- 严重程度
- 文件或路径
- 问题说明
- 建议修复或验证方式

除非用户明确要求，否则不要直接改代码。
```
