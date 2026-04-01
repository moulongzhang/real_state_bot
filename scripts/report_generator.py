"""
日次不動産レポート生成モジュール
物件データからMarkdownレポートを生成する
"""

import os
from datetime import datetime
from typing import Optional

from scripts.scrapers.rakumachi import Property


def generate_report(
    properties: list[Property],
    report_dir: str = "docs",
    date_str: Optional[str] = None,
) -> str:
    """日次レポートMarkdownを生成してファイルに保存"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y%m%d")

    display_date = datetime.now().strftime("%Y年%m月%d日")
    os.makedirs(report_dir, exist_ok=True)
    filepath = os.path.join(report_dir, f"{date_str}_daily_property_report.md")

    # ソース別に分類
    by_source: dict[str, list[Property]] = {}
    for p in properties:
        by_source.setdefault(p.source, []).append(p)

    md = _build_markdown(properties, by_source, display_date, date_str)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md)

    return filepath


def _build_markdown(
    properties: list[Property],
    by_source: dict[str, list[Property]],
    display_date: str,
    date_str: str,
) -> str:
    """Markdownコンテンツを組み立て"""
    lines: list[str] = []

    # ヘッダー
    lines.append(f"# 📋 日次不動産物件レポート — {display_date}")
    lines.append("")
    lines.append(f"**レポートID**: {date_str}-daily")
    lines.append(f"**対象エリア**: 首都圏（東京都・神奈川県・埼玉県・千葉県）")
    lines.append(f"**フィルタ条件**: 築3〜25年 / RC・SRC造 / 5,000万〜1.8億 / 利回り5.5%↑ / 6戸↑ / 駅徒歩10分以内")
    lines.append(f"**総取得件数**: {len(properties)} 件")
    lines.append("")
    lines.append("---")
    lines.append("")

    if not properties:
        lines.append("## 本日の新着物件はありませんでした")
        lines.append("")
        lines.append("条件に合致する新着物件が見つかりませんでした。")
        lines.append("明日の更新をお待ちください。")
        lines.append("")
        _append_footer(lines)
        return "\n".join(lines)

    # サマリーセクション
    lines.append("## 📊 サマリー")
    lines.append("")
    lines.append(f"| ソース | 件数 |")
    lines.append(f"|--------|------|")
    for source, props in by_source.items():
        lines.append(f"| {source} | {len(props)} 件 |")
    lines.append(f"| **合計** | **{len(properties)} 件** |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ソース別物件リスト
    for source, props in by_source.items():
        lines.append(f"## 🏠 {source} — 新着 {len(props)} 件")
        lines.append("")
        _append_property_table(lines, props)
        lines.append("")

        # 個別物件詳細
        for i, prop in enumerate(props, 1):
            _append_property_detail(lines, prop, i)

        lines.append("---")
        lines.append("")

    _append_footer(lines)
    return "\n".join(lines)


def _append_property_table(lines: list[str], properties: list[Property]):
    """物件一覧テーブル"""
    lines.append("| # | 物件名 | 価格 | 利回り | 築年数 | 構造 | 所在地 |")
    lines.append("|---|--------|------|--------|--------|------|--------|")
    for i, p in enumerate(properties, 1):
        title = f"[{_truncate(p.title, 30)}]({p.url})" if p.url else _truncate(p.title, 30)
        lines.append(
            f"| {i} | {title} | {p.price or '-'} | {p.gross_yield or '-'} "
            f"| {p.building_age or '-'} | {p.structure or '-'} | {_truncate(p.location, 20)} |"
        )


def _append_property_detail(lines: list[str], prop: Property, index: int):
    """物件詳細カード"""
    lines.append(f"### 物件{index}: {prop.title or '（名称不明）'}")
    lines.append("")
    lines.append("| 項目 | 内容 |")
    lines.append("|------|------|")

    details = [
        ("所在地", prop.location),
        ("最寄駅", prop.station),
        ("駅徒歩", f"{prop.walk_minutes}分" if prop.walk_minutes else ""),
        ("価格", prop.price),
        ("表面利回り", prop.gross_yield),
        ("築年数", prop.building_age),
        ("構造", prop.structure),
        ("間取り・面積", f"{prop.layout} {prop.area_sqm}" if prop.layout or prop.area_sqm else ""),
        ("物件タイプ", prop.property_type),
    ]

    for label, value in details:
        if value:
            lines.append(f"| {label} | {value} |")

    if prop.url:
        lines.append(f"\n🔗 **詳細**: {prop.url}")

    lines.append("")


def _append_footer(lines: list[str]):
    """フッター"""
    lines.append("---")
    lines.append("")
    lines.append("## 📎 参考リンク")
    lines.append("")
    lines.append("| サイト | URL |")
    lines.append("|--------|-----|")
    lines.append("| 楽待（新着） | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?newly=1 |")
    lines.append("| 健美家（新着24h） | https://www.kenbiya.com/pp0/cd2=1/ |")
    lines.append("| REINS成約価格 | http://www.contract.reins.or.jp/ |")
    lines.append("| ハザードマップ | https://disaportal.gsi.go.jp/ |")
    lines.append("")
    lines.append("> ⚠️ **免責**: 本レポートは自動生成された情報提供目的のものであり、投資助言ではありません。")
    lines.append("> 物件の詳細は各サイトで最新情報を確認してください。投資判断は自己責任で行ってください。")
    lines.append("")
    lines.append(f"*自動生成: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")


def _truncate(text: str, max_len: int) -> str:
    """文字列を指定長で切り詰め"""
    if not text:
        return "-"
    return text[:max_len] + "…" if len(text) > max_len else text


def generate_issue_body(properties: list[Property], report_path: str) -> str:
    """GitHub Issue本文を生成"""
    date_str = datetime.now().strftime("%Y年%m月%d日")
    lines: list[str] = []

    lines.append(f"## 🏠 {date_str} 首都圏 築浅RC 新着物件レポート")
    lines.append("")

    if not properties:
        lines.append("本日は条件に合致する新着物件がありませんでした。")
        lines.append("")
        lines.append(f"📄 詳細レポート: `{report_path}`")
        return "\n".join(lines)

    lines.append(f"**新着 {len(properties)} 件**を検出しました。")
    lines.append("")

    # TOP 10のみ表示（Issue本文は簡潔に）
    display_count = min(len(properties), 10)
    lines.append(f"### 📌 注目物件 TOP {display_count}")
    lines.append("")
    lines.append("| # | 物件名 | 価格 | 利回り | 築年数 | 構造 | ソース |")
    lines.append("|---|--------|------|--------|--------|------|--------|")

    for i, p in enumerate(properties[:display_count], 1):
        title = f"[{_truncate(p.title, 25)}]({p.url})" if p.url else _truncate(p.title, 25)
        lines.append(
            f"| {i} | {title} | {p.price or '-'} | {p.gross_yield or '-'} "
            f"| {p.building_age or '-'} | {p.structure or '-'} | {p.source} |"
        )

    if len(properties) > display_count:
        lines.append(f"\n*他 {len(properties) - display_count} 件は詳細レポートを参照*")

    lines.append("")
    lines.append(f"📄 **詳細レポート**: `{report_path}`")
    lines.append("")
    lines.append("---")
    lines.append("*このIssueは GitHub Actions により自動生成されました*")

    return "\n".join(lines)
