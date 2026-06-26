# 分析引擎任务模板

当任务涉及 H2N4 指标规范化、issue cards、review queue scoring、训练重点，或后续 native 节点标注/候选匹配器时，用这个模板。

```text
请先读取：
- AGENTS.md
- docs/agents/03_analysis_engine.md
- docs/output_layer.md
- docs/05_stats_dictionary.md
- docs/h2n_bridge.md
- docs/06_leak_detectors.md

角色：
Analysis Engine Agent

任务：
<这里写具体任务>

规则：
- H2N4 导出指标必须保留 source label，不要伪装成 PTS 重新计算的事实。
- PTS 自己生成的指标公式必须写清楚分母。
- issue card 必须基于来源明确的证据，不能靠 AI 判断是否命中。
- 不允许把最终亏损直接写成“已确认错误”；它只能作为复盘证据。
- 如果 output、指标、issue card、tag、candidate matcher 的契约变化，必须更新对应文档。
- 行为变化时，至少要有命中、不命中、缺失数据样例测试。

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
- docs/output_layer.md

验收标准：
- 新增指标、issue card、tag 或 candidate matcher 已写入文档。
- 重要的命中、不命中和缺失数据场景都有测试。

验证方式：
python -m pytest tests/tagging tests/stats tests/detectors
```
