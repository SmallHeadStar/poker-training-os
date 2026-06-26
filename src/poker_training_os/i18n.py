"""Chinese display labels for user-facing artifacts.

Machine ids stay in English so H2N4 baseline comparison and tests remain stable.
"""

from __future__ import annotations

from typing import Any


SECTION_ZH = {
    "session": "本次牌局",
    "position_results": "位置结果",
    "preflop": "翻前指标",
    "showdown": "摊牌指标",
}

METRIC_ZH = {
    "hands": "手数",
    "total_profit_bb": "总盈亏 BB",
    "bb_per_100": "BB/100",
    "net_result": "净结果",
    "vpip": "VPIP 主动入池率",
    "pfr": "PFR 翻前加注率",
    "rfi": "RFI 首入池加注率",
    "three_bet": "3Bet 频率",
    "call_3bet": "面对 3Bet 跟注率",
    "fold_to_3bet": "面对 3Bet 弃牌率",
    "four_bet": "4Bet 频率",
    "wtsd": "WTSD 看到摊牌率",
    "w_sd": "W$SD 摊牌胜率",
    "wwsf": "WWSF 看翻牌后胜率",
}

SOURCE_ZH = {
    "top_loss_positions": "按位置亏损",
    "top_loss_pot_types": "按底池类型亏损",
    "top_loss_preflop_lines": "按翻前线路亏损",
    "top_loss_action_lines": "按行动线亏损",
    "top_loss_board_families": "按公共牌面亏损",
    "top_loss_combined_spots": "组合场景亏损",
}

SPOT_FIELD_ZH = {
    "hero_position": "Hero 位置",
    "pot_type": "底池类型",
    "preflop_line": "翻前线路",
    "action_line_before": "此前行动线",
    "board_family": "公共牌面类型",
    "hero_decision": "Hero 决策",
}

VALUE_ZH = {
    "BTN": "按钮位",
    "CO": "关煞位",
    "HJ": "劫位",
    "LJ": "低劫位",
    "UTG": "枪口位",
    "UTG+1": "枪口后一位",
    "SB": "小盲",
    "BB": "大盲",
    "BTN/SB": "单挑按钮/小盲",
    "UNKNOWN": "未知",
    "single_raised_pot": "单加注底池",
    "three_bet_pot": "3Bet 底池",
    "four_bet_plus_pot": "4Bet 及以上底池",
    "limped_pot": "跛入底池",
    "unopened_preflop": "翻前未开池",
    "hero_open": "Hero 首入池加注",
    "hero_open_faced_3bet": "Hero 开池后面对 3Bet",
    "hero_flat_vs_open": "Hero 跟注对手开池",
    "hero_3bet": "Hero 3Bet",
    "hero_vpip_other": "Hero 其他主动入池",
    "no_hero_vpip": "Hero 未主动入池",
    "no_hero_decision": "无 Hero 决策",
    "call": "跟注",
    "raise": "加注",
    "bet": "下注",
    "check": "过牌",
    "fold": "弃牌",
    "none": "无",
    "preflop": "翻前",
}

RELIABILITY_ZH = {
    "high": "高",
    "medium": "中",
    "low": "低",
}

WARNING_ZH = {
    "sample_too_small": "样本过小",
    "sample_moderate": "样本中等，仍需谨慎",
    "loss_concentrated_in_top_5": "亏损集中在前 5 手",
    "loss_somewhat_concentrated": "亏损有一定集中度",
}

STATUS_ZH = {
    "implemented_provisional": "已实现，等待 H2N4 同样本验证",
    "h2n4_validated": "已通过 H2N4 同样本验证",
    "needs_human_review": "需要人工复盘",
    "no_issues_generated": "本次未生成问题卡",
    "pending": "待处理",
    "unknown": "未标注",
    "reduce_or_explain_observed_loss": "减少或解释该场景的观察亏损",
}

OPPORTUNITY_REASON_ZH = {
    "hero_hand": "Hero 参与的手牌",
    "no_prior_voluntary_before_hero_first_decision": "Hero 首次决策前无人主动入池",
    "not_first_in_opportunity": "不是首入池机会",
    "facing_exactly_one_prior_raise_at_first_decision": "Hero 首次决策面对且仅面对一次加注",
    "not_three_bet_opportunity": "不是 3Bet 机会",
    "hero_opened_unopened_pot_and_faced_3bet": "Hero 未开池前开池加注，随后面对对手 3Bet",
    "not_facing_3bet_after_open": "Hero 未处于开池后面对 3Bet 的机会",
    "hero_saw_flop": "Hero 看到了翻牌",
    "hero_did_not_see_flop": "Hero 未看翻牌",
    "hero_went_to_showdown": "Hero 进入摊牌",
    "hero_did_not_go_to_showdown": "Hero 未进入摊牌",
}


def label_zh(value: Any) -> str:
    """Return a Chinese label for a known machine id."""

    if value is None:
        return ""
    text = str(value)
    return (
        SECTION_ZH.get(text)
        or METRIC_ZH.get(text)
        or SOURCE_ZH.get(text)
        or VALUE_ZH.get(text)
        or RELIABILITY_ZH.get(text)
        or WARNING_ZH.get(text)
        or STATUS_ZH.get(text)
        or OPPORTUNITY_REASON_ZH.get(text)
        or text
    )


def warning_zh(warning: str | None) -> str:
    if not warning:
        return ""
    return "；".join(label_zh(part.strip()) for part in warning.split(";") if part.strip())


def spot_key_zh(spot_key: dict[str, Any]) -> str:
    parts = []
    for field, value in spot_key.items():
        if value in (None, ""):
            continue
        field_label = SPOT_FIELD_ZH.get(field, field)
        value_label = label_zh(value)
        parts.append(f"{field_label}={value_label}")
    return "，".join(parts) if parts else "整体场景"
