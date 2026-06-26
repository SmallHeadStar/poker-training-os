# 分析引擎任务模板

当任务涉及节点标注、指标公式、bb/100、VPIP、3bet、候选匹配器、outcome evidence 时，用这个模板。

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
- candidate matcher 必须按决策时信息匹配，不能靠 AI 判断是否命中。
- candidate matching 禁止读取 final result、showdown cards、hand_net_bb。
- final result、showdown、hand_net_bb 只能作为匹配后的 outcome evidence。
- 如果 tag、指标、candidate matcher 的契约变化，必须更新对应文档。
- candidate matcher 变化时，至少要有命中、不命中、边界样例测试。

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
- 新增 tag、指标或 candidate matcher 已写入文档。
- 重要的命中和不命中场景都有测试。

验证方式：
python -m pytest tests/tagging tests/stats tests/detectors
```
