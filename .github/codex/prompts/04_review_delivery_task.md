# 复盘交付任务模板

当任务涉及中文 session review、GTO study cards、训练计划、复盘队列、UI 展示时，用这个模板。

```text
请先读取：
- AGENTS.md
- docs/agents/04_review_delivery.md
- docs/02_workflow.md
- docs/output_layer.md

角色：
Review Delivery Agent

任务：
<这里写具体任务>

规则：
- 所有结论必须基于已经计算出来的事实。
- 所有事实必须显示或保留来源：h2n4_csv / h2n4_manual / pts_generated / human_review。
- 必须区分“系统检测到的问题”和“用户确认的问题”。
- 不允许修改 parser、stat、detector 的核心逻辑。
- 所有文案必须保持赛后复盘语气，不能像实时建议。

允许修改的文件：
- src/poker_training_os/reports/**
- src/poker_training_os/training/**
- src/poker_training_os/ui/**
- tests/reports/**
- tests/ui/**
- 如果报告或 UI 行为变化，可以改相关 docs

验收标准：
- 用户能看到 session summary、Top 3 issue cards、代表手牌、下一步训练任务。
- 报告或 UI 不暗示实时打牌建议。

验证方式：
python -m pytest tests/reports tests/ui
```
