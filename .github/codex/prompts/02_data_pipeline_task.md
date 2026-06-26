# 数据管道任务模板

当任务涉及 session manifest、H2N4 export contract、CSV/YAML ingest、manual fallback、parser fallback 时，用这个模板。

```text
请先读取：
- AGENTS.md
- docs/agents/02_data_pipeline.md
- docs/h2n_export_contract.md
- docs/output_layer.md
- docs/07_test_plan.md

角色：
Data Pipeline Agent

任务：
<这里写具体任务>

规则：
- H2N4 导出解析和 manual fallback 解析必须是确定性的。
- 不允许加入漏洞解释、训练建议、AI 教练话术。
- 必须保留调试需要的来源文件、原始行或错误信息。
- 所有输出事实必须带来源标记：h2n4_csv / h2n4_manual / pts_generated / human_review。
- 只要 ingest 或 parser fallback 行为变化，就必须补 fixture 或测试。

允许修改的文件：
- src/poker_training_os/parser/**
- src/poker_training_os/models/**
- src/poker_training_os/db/**
- tests/parser/**
- tests/fixtures/**
- data/expected/**
- 如果 H2N4 导出或输出契约变化，可以改 docs/h2n_export_contract.md、docs/output_layer.md
- 如果 native parser fallback 数据契约变化，可以改 docs/03_data_schema.md

验收标准：
- 原始输入或 H2N4 导出能追溯到解析结果。
- 解析失败时有明确错误。
- 新增或修改的行为有测试覆盖。

验证方式：
python -m pytest tests/parser
```
