# 分析引擎任务模板

当任务涉及节点标注、指标公式、bb/100、VPIP、3bet、漏洞检测器时，用这个模板。

```text
请先读取：
- AGENTS.md
- docs/agents/03_analysis_engine.md
- docs/04_tag_dictionary.md
- docs/05_stats_dictionary.md
- docs/06_leak_detectors.md

角色：
Analysis Engine Agent

任务：
<这里写具体任务>

规则：
- tag 必须是确定性的。
- 指标公式必须写清楚分母。
- detector 必须按规则匹配，不能靠 AI 判断是否命中。
- 如果 tag、指标、detector 的契约变化，必须更新对应文档。
- detector 变化时，至少要有命中、不命中、边界样例测试。

允许修改的文件：
- src/poker_training_os/tagging/**
- src/poker_training_os/stats/**
- src/poker_training_os/detectors/**
- tests/tagging/**
- tests/stats/**
- tests/detectors/**
- docs/04_tag_dictionary.md
- docs/05_stats_dictionary.md
- docs/06_leak_detectors.md

验收标准：
- 新增 tag、指标或 detector 已写入文档。
- 重要的命中和不命中场景都有测试。

验证方式：
python -m pytest tests/tagging tests/stats tests/detectors
```
