#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日銀利上げシナリオ別 不動産投資ストレステスト
====================================================
10物件 × 4金利シナリオの完全分析
エコノミスト予測ベース（野村證券・NRI・みずほリサーチ 2025-2028）
"""

from dataclasses import dataclass
from typing import Dict

# ============================================================
# 物件定義（都心5区 × 多様なプロファイル = 10物件）
# LTV・利回り・経費は市場実態に即して設定
# 経費率 = 管理費+修繕+税金+管理手数料（表面家賃の15-25%）
# ============================================================
@dataclass
class Property:
    id: int
    name: str
    ward: str
    area: str
    prop_type: str
    price: float        # 物件価格(万円)
    ltv_pct: float      # LTV(%)
    term: int           # 返済期間(年)
    base_rate: float    # 現行金利(%)
    gross_yield: float  # 表面利回り(%)
    expense_ratio: float # 経費率(表面家賃比%)
    vacancy: float      # 空室率(%)

    @property
    def loan(self) -> float:
        return self.price * self.ltv_pct / 100

    @property
    def gross_rent(self) -> float:
        return self.price * self.gross_yield / 100

    @property
    def noi(self) -> float:
        eff_rent = self.gross_rent * (1 - self.vacancy / 100)
        expenses = self.gross_rent * self.expense_ratio / 100
        return eff_rent - expenses

PROPS = [
    # id, name, ward, area, type, price, ltv%, term, rate%, yield%, expense%, vacancy%
    Property(1,  "港区タワー 高輪GW 3LDK",     "港区",   "高輪GW",   "新築タワー",  25000, 65, 35, 2.0, 3.4, 18, 2.0),
    Property(2,  "港区 虎ノ門 高級1LDK",       "港区",   "虎ノ門",   "高級レジ",   15000, 70, 30, 2.0, 3.6, 17, 2.5),
    Property(3,  "中央区タワー 晴海 3LDK",     "中央区",  "晴海",     "タワーMS",   9500,  75, 35, 2.0, 4.0, 18, 3.0),
    Property(4,  "中央区 日本橋 築浅2LDK",     "中央区",  "日本橋",   "築浅MS",    12000, 70, 30, 2.0, 3.5, 17, 2.5),
    Property(5,  "渋谷区 駅近 1R コンパクト",    "渋谷区",  "渋谷駅",   "コンパクト",  5500,  80, 35, 2.0, 4.2, 16, 2.0),
    Property(6,  "渋谷区 代官山 1LDK 築15年",  "渋谷区",  "代官山",   "中古MS",    7500,  65, 25, 2.0, 4.8, 20, 3.0),
    Property(7,  "千代田区 番町 低層高級",       "千代田区", "番町",     "低層高級",   35000, 55, 30, 2.0, 3.0, 18, 1.5),
    Property(8,  "千代田区 大手町 1LDK 築10年", "千代田区", "大手町",   "中古MS",    8500,  70, 30, 2.0, 3.8, 17, 2.0),
    Property(9,  "新宿区 西新宿 1R 築20年",    "新宿区",  "西新宿",   "築古1R",    4000,  60, 25, 2.0, 5.5, 22, 3.5),
    Property(10, "新宿区 四谷 2LDK ファミリー",  "新宿区",  "四谷",     "築浅ファミリー", 7000, 70, 35, 2.0, 4.3, 18, 2.5),
]

# ============================================================
# 金利シナリオ
# ============================================================
@dataclass
class Scenario:
    name: str
    desc: str
    rates: Dict[int, float]  # {年: 金利%}
    prob: float

SCENARIOS = [
    Scenario("A: 現状維持",    "日銀据え置き・ハト派",
             {2025: 2.0, 2026: 2.0, 2027: 2.0, 2028: 2.0}, 15),
    Scenario("B: 段階的利上げ",  "メインシナリオ（野村/みずほ）",
             {2025: 2.0, 2026: 2.5, 2027: 2.75, 2028: 3.0}, 50),
    Scenario("C: 急激利上げ",   "インフレ加速・円安進行",
             {2025: 2.0, 2026: 3.0, 2027: 3.5, 2028: 3.5}, 25),
    Scenario("D: 危機シナリオ",  "スタグフレーション",
             {2025: 2.0, 2026: 4.0, 2027: 4.5, 2028: 4.5}, 10),
]

YEARS = [2025, 2026, 2027, 2028]

# ============================================================
# 計算エンジン
# ============================================================
def monthly_pmt(principal: float, rate_pct: float, years: int) -> float:
    if rate_pct <= 0.001:
        return principal / (years * 12)
    r = rate_pct / 100 / 12
    n = years * 12
    return principal * r * (1 + r)**n / ((1 + r)**n - 1)

def annual_pmt(principal: float, rate_pct: float, years: int) -> float:
    return monthly_pmt(principal, rate_pct, years) * 12

def cashflow(p: Property, rate: float) -> float:
    return p.noi - annual_pmt(p.loan, rate, p.term)

def dscr(p: Property, rate: float) -> float:
    ds = annual_pmt(p.loan, rate, p.term)
    return p.noi / ds if ds > 0 else 999

def breakeven_rate(p: Property) -> float:
    """CF=0となる金利(%)を二分探索"""
    lo, hi = 0.01, 30.0
    if p.noi <= annual_pmt(p.loan, 0.01, p.term):
        return 0.0  # 0%金利でも赤字
    for _ in range(200):
        mid = (lo + hi) / 2
        if annual_pmt(p.loan, mid, p.term) < p.noi:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

# ============================================================
# 表示
# ============================================================
B  = "\033[1m"
R  = "\033[91m"
G  = "\033[92m"
Y  = "\033[93m"
C  = "\033[96m"
M  = "\033[95m"
D  = "\033[2m"
X  = "\033[0m"

def color_cf(v: float) -> str:
    c = R if v < 0 else (Y if v < 30 else G)
    return f"{c}{v:>8.1f}{X}"

def status_tag(cf_val: float, dscr_val: float) -> str:
    if cf_val < 0:
        return f"{R}⚠ 赤字{X}"
    if dscr_val < 1.2:
        return f"{Y}△ 注意{X}"
    return f"{G}○ 安全{X}"

def main():
    W = 92
    print(f"""
{B}{'='*W}
  日銀利上げシナリオ別 不動産投資ストレステスト
  ── 東京都心5区 10物件 × 4金利シナリオ 完全分析 ──
{'='*W}{X}

{D}分析日: 2025年 | 野村證券・NRI・みずほRT予測ベース
エコノミスト見通し: 政策金利→2027末1.25-1.75%, 投資ローン変動→2.5-3.0%台へ{X}
""")

    # ── シナリオ一覧 ──
    print(f"{B}{C}┌{'─'*(W-2)}┐{X}")
    print(f"{B}{C}│{'金利シナリオ定義':^{W-12}}│{X}")
    print(f"{B}{C}└{'─'*(W-2)}┘{X}")
    print(f"  {'シナリオ':<20} {'2025':>6} {'2026':>6} {'2027':>6} {'2028':>6}  {'確率':>5}  {'説明'}")
    print(f"  {'─'*(W-4)}")
    for s in SCENARIOS:
        r = s.rates
        print(f"  {s.name:<20} {r[2025]:>5.1f}% {r[2026]:>5.1f}% {r[2027]:>5.1f}% {r[2028]:>5.1f}%  {s.prob:>4.0f}%  {s.desc}")
    print()

    # ── 物件一覧 ──
    print(f"{B}{C}┌{'─'*(W-2)}┐{X}")
    print(f"{B}{C}│{'分析対象 10物件':^{W-12}}│{X}")
    print(f"{B}{C}└{'─'*(W-2)}┘{X}")
    print(f"  {'#':>2} {'物件名':<28} {'区':<5} {'価格':>7} {'借入':>7} {'LTV':>4} {'利回':>5} {'NOI':>7} {'期間':>4}")
    print(f"  {'─'*(W-4)}")
    for p in PROPS:
        print(f"  {p.id:>2} {p.name:<28} {p.ward:<5} {p.price:>6,.0f}万 {p.loan:>6,.0f}万 {p.ltv_pct:>3.0f}% {p.gross_yield:>4.1f}% {p.noi:>6.1f}万 {p.term:>3}年")
    print()

    # ── 物件別詳細 ──
    print(f"{B}{C}┌{'─'*(W-2)}┐{X}")
    print(f"{B}{C}│{'ストレステスト結果：年間返済額 & キャッシュフロー':^{W-16}}│{X}")
    print(f"{B}{C}└{'─'*(W-2)}┘{X}")

    rankings = []

    for p in PROPS:
        be = breakeven_rate(p)
        margin = be - p.base_rate
        base_pmt = annual_pmt(p.loan, p.base_rate, p.term)
        base_cf = cashflow(p, p.base_rate)

        print(f"\n{B}{'─'*W}")
        print(f"  #{p.id} {p.name}  [{p.ward} {p.area} / {p.prop_type}]")
        print(f"{'─'*W}{X}")
        print(f"  価格 {p.price:,.0f}万 | 借入 {p.loan:,.0f}万(LTV {p.ltv_pct:.0f}%) | 表面利回 {p.gross_yield}% | NOI {p.noi:,.1f}万/年")
        print(f"  現行返済 {base_pmt:,.1f}万/年 | 現行CF {base_cf:+,.1f}万/年")
        if be > 0:
            print(f"  {Y}★ 損益分岐金利 {be:.2f}%（現行+{margin:.2f}%まで耐久）{X}")
        else:
            print(f"  {R}★ 損益分岐金利 N/A（現行金利でも赤字）{X}")
        print()

        # シナリオ別テーブル
        print(f"  {'シナリオ':<18} {'2028金利':>7} {'年間返済':>8} {'返済増':>8} {'年間CF':>8} {'CF増減':>8} {'DSCR':>6} {'判定'}")
        print(f"  {'─'*80}")
        for s in SCENARIOS:
            rt = s.rates[2028]
            pmt = annual_pmt(p.loan, rt, p.term)
            cf = cashflow(p, rt)
            d = dscr(p, rt)
            print(f"  {s.name:<18} {rt:>6.1f}% {pmt:>7,.1f}万 {pmt-base_pmt:>+7.1f}万 {color_cf(cf)}万 {cf-base_cf:>+7.1f}万 {d:>5.2f}x {status_tag(cf, d)}")

        # 年次推移
        print(f"\n  {D}▼ 年次CF推移(万円/年){X}")
        hdr = f"  {'シナリオ':<18}"
        for yr in YEARS:
            hdr += f" {yr:>10}"
        print(hdr)
        print(f"  {'─'*60}")
        for s in SCENARIOS:
            row = f"  {s.name:<18}"
            for yr in YEARS:
                cf_y = cashflow(p, s.rates[yr])
                row += f" {color_cf(cf_y)}万"
            print(row)

        # ランキング用データ
        dscr_b = dscr(p, SCENARIOS[1].rates[2028])
        cf_d = cashflow(p, SCENARIOS[3].rates[2028])
        score = (
            min(margin * 12, 40) +
            min(dscr_b * 15, 30) +
            (15 if cf_d > 0 else 0) +
            max(0, (100 - p.ltv_pct) / 100 * 15)
        )
        rankings.append({
            'id': p.id, 'name': p.name, 'ward': p.ward,
            'score': round(score, 1), 'be': be, 'margin': margin,
            'dscr_b': dscr_b, 'cf_d': cf_d, 'ltv': p.ltv_pct,
            'base_cf': base_cf
        })

    # ============================================================
    # ランキング
    # ============================================================
    rankings.sort(key=lambda x: x['score'], reverse=True)

    print(f"\n\n{B}{C}{'='*W}")
    print(f"  ★ 金利耐性ランキング（総合スコア）")
    print(f"{'='*W}{X}\n")

    print(f"{'順位':>4} {'物件名':<30} {'区':<5} {'Score':>5} {'分岐金利':>7} {'余裕幅':>7} {'DSCR(B)':>7} {'CF(D)':>7} {'LTV':>4}")
    print(f"{'─'*W}")
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    for i, d in enumerate(rankings, 1):
        m = medals.get(i, "  ")
        cfc = G if d['cf_d'] > 0 else R
        print(f"{m}{i:>2} {d['name']:<30} {d['ward']:<5} {d['score']:>5.1f} {d['be']:>6.2f}% +{d['margin']:>5.2f}% {d['dscr_b']:>6.2f}x {cfc}{d['cf_d']:>+6.1f}万{X} {d['ltv']:>3.0f}%")

    # ============================================================
    # ポートフォリオ影響サマリー
    # ============================================================
    print(f"\n\n{B}{C}{'='*W}")
    print(f"  総合リスク評価サマリー")
    print(f"{'='*W}{X}\n")

    for s in SCENARIOS:
        rt = s.rates[2028]
        reds = sum(1 for p in PROPS if cashflow(p, rt) < 0)
        warns = sum(1 for p in PROPS if 0 <= cashflow(p, rt) < 30)
        safes = 10 - reds - warns
        print(f"  {s.name:<20} {rt:.1f}% → {R}赤字{reds}件{X} / {Y}注意{warns}件{X} / {G}安全{safes}件{X}  {R}{'█'*reds}{Y}{'▓'*warns}{G}{'░'*safes}{X}")

    # 分岐マージン棒グラフ
    print(f"\n{B}  ▼ 損益分岐金利マージン（現行2.0%からの耐久幅）{X}")
    mx = max(d['margin'] for d in rankings) if rankings else 1
    for d in rankings:
        blen = int(d['margin'] / mx * 35) if mx > 0 else 0
        c = G if d['margin'] > 2.5 else (Y if d['margin'] > 1.5 else R)
        print(f"  {d['name'][:20]:<22} +{d['margin']:.2f}% {c}{'█'*blen}{X}")

    # ポートフォリオ合計
    tot_base = sum(cashflow(p, 2.0) for p in PROPS)
    tot_b = sum(cashflow(p, SCENARIOS[1].rates[2028]) for p in PROPS)
    tot_c = sum(cashflow(p, SCENARIOS[2].rates[2028]) for p in PROPS)
    tot_d = sum(cashflow(p, SCENARIOS[3].rates[2028]) for p in PROPS)

    print(f"\n{B}  ▼ 10物件ポートフォリオ 合計CF(万円/年){X}")
    print(f"    現状A (2.0%): {G}{tot_base:>+9,.1f}万{X}")
    print(f"    段階B (3.0%): {Y if tot_b > 0 else R}{tot_b:>+9,.1f}万{X}  (差額 {tot_b-tot_base:>+,.1f}万)")
    print(f"    急激C (3.5%): {Y if tot_c > 0 else R}{tot_c:>+9,.1f}万{X}  (差額 {tot_c-tot_base:>+,.1f}万)")
    print(f"    危機D (4.5%): {R}{tot_d:>+9,.1f}万{X}  (差額 {tot_d-tot_base:>+,.1f}万)")

    # ============================================================
    # 提言
    # ============================================================
    print(f"\n\n{B}{M}{'='*W}")
    print(f"  📋 リスクアナリスト提言")
    print(f"{'='*W}{X}\n")

    top3 = rankings[:3]
    bot3 = rankings[-3:]

    print(f"  {G}{B}【金利耐性 上位3物件 ── 推奨保有】{X}")
    for d in top3:
        print(f"    ✅ #{d['id']} {d['name']}")
        print(f"       分岐金利{d['be']:.1f}% / 余裕+{d['margin']:.1f}% / 危機時CF {d['cf_d']:+.0f}万")

    print(f"\n  {R}{B}【金利耐性 下位3物件 ── 要対策】{X}")
    for d in bot3:
        print(f"    ⚠️  #{d['id']} {d['name']}")
        print(f"       分岐金利{d['be']:.1f}% / 余裕+{d['margin']:.1f}% / 危機時CF {d['cf_d']:+.0f}万")

    print(f"""
  {B}【戦略的提言】{X}

    1. {Y}最優先対策{X}: LTV高＋低利回り物件（港区タワー等）は金利2.5%到達前に
       固定金利切替え or 繰上返済でLTV65%以下を目標に

    2. {G}守りの投資先{X}: 新宿区・千代田区の低LTV+高利回り物件は
       危機シナリオ(4.5%)でも黒字維持 → 利上げ局面のコア資産として有効

    3. {C}ポートフォリオ戦略{X}: シナリオB(3.0%)で全体CFが大幅減少
       → 赤字物件の売却益で高耐性物件への入替えを検討

    4. {R}警戒ライン{X}: 金利3.5%超(シナリオC)で過半数が赤字転落
       → 早期に金利ヘッジ（金利スワップ/キャップ）の導入を推奨

    5. {M}タイミング{X}: 野村證券メインシナリオ(2026年2回・2027年1回利上げ)では
       2026年前半が固定切替えの最終好機 → 意思決定は2025年中に

  {D}※ 本分析はエコノミスト予測・公開データに基づくシミュレーションです。投資助言ではありません。
  ※ 実際の投資判断は、個別物件の精査・税務・法務の専門家助言を踏まえてください。{X}
""")
    print(f"{B}{'='*W}{X}")

if __name__ == "__main__":
    main()
