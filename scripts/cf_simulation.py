import math

# ============================================================
# 物件基本情報
# ============================================================
PROPERTY_PRICE = 124_200_000
ANNUAL_INCOME  = 7_452_000
INTEREST_RATE  = 0.021
LOAN_YEARS     = 35
LOAN_MONTHS    = LOAN_YEARS * 12

MGMT_FEE_RATE      = 0.05
REPAIR_RESERVE_RATE = 0.05
PROPERTY_TAX_RATE   = 0.01
INSURANCE           = 100_000
MISC                = 100_000
VACANCY_RATE        = 0.05

# ============================================================
def monthly_payment(principal, annual_rate, months):
    r = annual_rate / 12
    if r == 0:
        return principal / months
    return principal * r * (1 + r)**months / ((1 + r)**months - 1)

def loan_balance(principal, annual_rate, months, after_months):
    r = annual_rate / 12
    if r == 0:
        return principal - principal / months * after_months
    pmt = monthly_payment(principal, annual_rate, months)
    return principal * (1 + r)**after_months - pmt * ((1 + r)**after_months - 1) / r

def calc_irr(cashflows, max_iter=2000):
    """IRR をビセクション法 + Newton法のハイブリッドで求める"""
    def npv(rate, cfs):
        return sum(cf / (1 + rate)**t for t, cf in enumerate(cfs))

    # まずビセクション法で探索
    lo, hi = -0.5, 5.0
    npv_lo = npv(lo, cashflows)
    npv_hi = npv(hi, cashflows)

    if npv_lo * npv_hi > 0:
        # 符号が変わらない → IRRが存在しないか範囲外
        # 全CFが負なら IRR は算出不能
        if all(cf <= 0 for cf in cashflows[1:]) or sum(cashflows) < 0:
            return None
        return None

    for _ in range(max_iter):
        mid = (lo + hi) / 2
        npv_mid = npv(mid, cashflows)
        if abs(npv_mid) < 1.0:  # 1円以下で収束
            return mid
        if npv_lo * npv_mid < 0:
            hi = mid
            npv_hi = npv_mid
        else:
            lo = mid
            npv_lo = npv_mid
    return (lo + hi) / 2

def calc_expenses(annual_income, property_price):
    mgmt    = annual_income * MGMT_FEE_RATE
    repair  = annual_income * REPAIR_RESERVE_RATE
    tax     = property_price * PROPERTY_TAX_RATE
    items = {
        "管理費 (5%)":       mgmt,
        "修繕積立金 (5%)":   repair,
        "固定資産税等 (1%)": tax,
        "保険料":            INSURANCE,
        "その他雑費":        MISC,
    }
    total = sum(items.values())
    return items, total

# ============================================================
eff_income = ANNUAL_INCOME * (1 - VACANCY_RATE)
expense_items, total_expense = calc_expenses(ANNUAL_INCOME, PROPERTY_PRICE)
noi = eff_income - total_expense

patterns = {
    "A (フルローン)":  {"down": 0,          "loan": 124_200_000},
    "B (頭金10%)":     {"down": 12_420_000, "loan": 111_780_000},
    "C (頭金20%)":     {"down": 24_840_000, "loan":  99_360_000},
}

print("=" * 72)
print("  不動産投資キャッシュフローシミュレーション")
print("  物件名: メゾンジュネス（東京都立川市曙町1丁目23-13）")
print("=" * 72)

print("\n■ 収入・経費の前提")
print(f"  想定年間収入（満室）:   {ANNUAL_INCOME:>14,} 円")
print(f"  空室率:                 {VACANCY_RATE*100:>13.1f} %")
print(f"  実効年間収入:           {eff_income:>14,.0f} 円")
print()
for k, v in expense_items.items():
    print(f"  {k:<20s}  {v:>14,.0f} 円")
print(f"  {'─'*20}  {'─'*14}")
print(f"  {'経費合計':<20s}  {total_expense:>14,.0f} 円")
print(f"\n  ★ NOI (実効収入 - 経費): {noi:>14,.0f} 円")

# ============================================================
results = {}
for name, p in patterns.items():
    loan = p["loan"]; down = p["down"]
    mp = monthly_payment(loan, INTEREST_RATE, LOAN_MONTHS)
    ap = mp * 12
    annual_cf = noi - ap
    dscr = noi / ap
    total_repay = mp * LOAN_MONTHS
    ccr = annual_cf / down if down > 0 else None
    payback = down / annual_cf if annual_cf > 0 and down > 0 else None
    results[name] = {
        "月額返済額": mp, "年間返済額": ap,
        "年間CF": annual_cf, "月間CF": annual_cf/12,
        "DSCR": dscr, "総返済額": total_repay,
        "CCR": ccr, "回収期間": payback,
        "5年残高": loan_balance(loan, INTEREST_RATE, LOAN_MONTHS, 60),
        "10年残高": loan_balance(loan, INTEREST_RATE, LOAN_MONTHS, 120),
        "15年残高": loan_balance(loan, INTEREST_RATE, LOAN_MONTHS, 180),
        "5年累積CF": annual_cf*5, "10年累積CF": annual_cf*10,
        "15年累積CF": annual_cf*15,
        "頭金": down, "借入額": loan,
    }

# --- メイン比較表 ---
print("\n" + "=" * 72)
print("■ パターン別 キャッシュフロー比較表")
print("=" * 72)
pnames = list(patterns.keys())
hdr = f"{'項目':<24s}|{'A(フルローン)':>18s}|{'B(頭金10%)':>18s}|{'C(頭金20%)':>18s}"
print(hdr)
print("─" * len(hdr))

def row_yen(label, key, common=None):
    vals = []
    for n in pnames:
        v = common if common is not None else results[n][key]
        vals.append(f"{v:>15,.0f}円")
    print(f"  {label:<22s}|{vals[0]:>18s}|{vals[1]:>18s}|{vals[2]:>18s}")

row_yen("借入額", "借入額")
row_yen("頭金", "頭金")
row_yen("月額返済額", "月額返済額")
row_yen("年間返済額", "年間返済額")
row_yen("年間NOI", None, common=noi)
row_yen("年間CF（税引前）", "年間CF")
row_yen("月間CF", "月間CF")
row_yen("総返済額（35年）", "総返済額")

# DSCR
vals = [f"{results[n]['DSCR']:>16.2f}倍" for n in pnames]
print(f"  {'返済比率(DSCR)':<22s}|{vals[0]:>18s}|{vals[1]:>18s}|{vals[2]:>18s}")

# CCR
vals = []
for n in pnames:
    c = results[n]["CCR"]
    vals.append(f"{'―':>18s}" if c is None else f"{c*100:>16.2f}% ")
print(f"  {'CCR':<22s}|{vals[0]:>18s}|{vals[1]:>18s}|{vals[2]:>18s}")

# 回収期間
vals = []
for n in pnames:
    pb = results[n]["回収期間"]
    vals.append(f"{'―':>18s}" if pb is None else f"{pb:>16.1f}年")
print(f"  {'自己資金回収期間':<22s}|{vals[0]:>18s}|{vals[1]:>18s}|{vals[2]:>18s}")

print("─" * len(hdr))
print(f"  {'【ローン残高】':<22s}|")
for yr, key in [(5,"5年残高"),(10,"10年残高"),(15,"15年残高")]:
    row_yen(f"  {yr}年後", key)

print(f"  {'【累積CF】':<22s}|")
for yr, key in [(5,"5年累積CF"),(10,"10年累積CF"),(15,"15年累積CF")]:
    row_yen(f"  {yr}年後", key)

# ============================================================
# 13. 損益分岐入居率
# ============================================================
print("\n" + "=" * 72)
print("■ 損益分岐入居率（Break-Even Occupancy）")
print("=" * 72)
for name, p in patterns.items():
    ap = monthly_payment(p["loan"], INTEREST_RATE, LOAN_MONTHS) * 12
    fixed_costs = PROPERTY_PRICE * PROPERTY_TAX_RATE + INSURANCE + MISC
    # occ * income * (1 - mgmt_rate - repair_rate) - fixed_costs = ap
    variable_rate = 1 - MGMT_FEE_RATE - REPAIR_RESERVE_RATE  # 0.90
    be = (ap + fixed_costs) / (ANNUAL_INCOME * variable_rate)
    print(f"  {name:<18s}: {be*100:>6.2f}%  （12戸中 {math.ceil(be*12)}戸以上必要）")

# ============================================================
# 14. 金利感応度分析
# ============================================================
print("\n" + "=" * 72)
print("■ 金利感応度分析（パターンA: フルローン 借入1億2,420万円）")
print("=" * 72)
rates = [0.021, 0.025, 0.030, 0.035]
print(f"  {'金利':>6s}|{'月額返済':>12s}|{'年間返済':>14s}|{'年間CF':>14s}|{'月間CF':>12s}|{'DSCR':>7s}")
print("  " + "─" * 67)
for r in rates:
    mp_r = monthly_payment(124_200_000, r, LOAN_MONTHS)
    ap_r = mp_r * 12; cf_r = noi - ap_r
    tag = " ← 基準" if r == 0.021 else (" ⚠赤字拡大" if cf_r < -500_000 else "")
    print(f"  {r*100:>5.1f}%|{mp_r:>10,.0f}円|{ap_r:>12,.0f}円|{cf_r:>12,.0f}円|{cf_r/12:>10,.0f}円|{noi/ap_r:>6.2f}倍{tag}")

# ============================================================
# 15. 売却シミュレーション
# ============================================================
print("\n" + "=" * 72)
print("■ 売却シミュレーション（10年後）")
print("=" * 72)

# 複数キャップレートで売却価格を表示
print("\n  【参考: キャップレート別 売却想定価格】")
for cr in [0.05, 0.06, 0.065, 0.07, 0.08]:
    sp = noi / cr
    print(f"    Cap {cr*100:.1f}% → 売却価格 {sp:>14,.0f}円 (購入比 {sp/PROPERTY_PRICE*100:.1f}%)")

cap_rate = 0.07
sale_price = noi / cap_rate
selling_cost_rate = 0.035
selling_cost = sale_price * selling_cost_rate
closing_cost = PROPERTY_PRICE * 0.07

print(f"\n  ■ 基準ケース: キャップレート {cap_rate*100:.1f}%")
print(f"    売却価格: {sale_price:>14,.0f}円  売却経費(3.5%): {selling_cost:>10,.0f}円")
print()

for name, p in patterns.items():
    loan = p["loan"]; down = p["down"]
    mp_v = monthly_payment(loan, INTEREST_RATE, LOAN_MONTHS)
    ap_v = mp_v * 12; cf_v = noi - ap_v
    bal10 = loan_balance(loan, INTEREST_RATE, LOAN_MONTHS, 120)
    net_sale = sale_price - bal10 - selling_cost
    total_initial = down + closing_cost

    cfs = [-total_initial] + [cf_v]*9 + [cf_v + net_sale]
    irr_val = calc_irr(cfs)
    total_return = sum(cfs)

    print(f"  【{name}】")
    print(f"    初期投資（頭金+諸費用7%）: {total_initial:>14,.0f}円")
    print(f"    10年後ローン残高:          {bal10:>14,.0f}円")
    print(f"    売却手取り（残債差引後）:   {net_sale:>14,.0f}円")
    print(f"    10年間累積CF:              {cf_v*10:>14,.0f}円")
    print(f"    トータル損益:              {total_return:>14,.0f}円")
    if irr_val is not None:
        print(f"    ★ IRR:                     {irr_val*100:>13.2f}%")
    else:
        print(f"    ★ IRR:             算出不能（全期間赤字）")
    print()

# キャップレート5%（購入時水準）で売った場合も試算
print("  ■ 参考ケース: キャップレート 5.0%（購入時NOI利回り水準で売却）")
cap5 = 0.05
sale5 = noi / cap5
sell_cost5 = sale5 * selling_cost_rate
print(f"    売却価格: {sale5:>14,.0f}円  売却経費(3.5%): {sell_cost5:>10,.0f}円")
print()

for name, p in patterns.items():
    loan = p["loan"]; down = p["down"]
    mp_v = monthly_payment(loan, INTEREST_RATE, LOAN_MONTHS)
    ap_v = mp_v * 12; cf_v = noi - ap_v
    bal10 = loan_balance(loan, INTEREST_RATE, LOAN_MONTHS, 120)
    net_sale = sale5 - bal10 - sell_cost5
    total_initial = down + closing_cost

    cfs = [-total_initial] + [cf_v]*9 + [cf_v + net_sale]
    irr_val = calc_irr(cfs)
    total_return = sum(cfs)

    print(f"  【{name}】")
    print(f"    売却手取り（残債差引後）:   {net_sale:>14,.0f}円")
    print(f"    トータル損益:              {total_return:>14,.0f}円")
    if irr_val is not None:
        print(f"    ★ IRR:                     {irr_val*100:>13.2f}%")
    else:
        print(f"    ★ IRR:             算出不能（全期間赤字）")
    print()

# ============================================================
# 投資判断サマリー
# ============================================================
cf_a = results["A (フルローン)"]["年間CF"]
cf_b = results["B (頭金10%)"]["年間CF"]
cf_c = results["C (頭金20%)"]["年間CF"]
dscr_a = results["A (フルローン)"]["DSCR"]

# 金利3.5%時のCF
cf_35 = noi - monthly_payment(124_200_000, 0.035, LOAN_MONTHS) * 12

print("=" * 72)
print("■ 投資判断サマリー")
print("=" * 72)
print(f"""
┌─────────────────────────────────────────────────────────┐
│ 物件: メゾンジュネス（立川市曙町）                       │
│ RC造3階建 1R×12戸 / 築22年 / 1億2,420万円               │
│ 表面利回り6.00% / NOI利回り{noi/PROPERTY_PRICE*100:.2f}%                        │
└─────────────────────────────────────────────────────────┘

【収益性評価】
  ・NOI利回り {noi/PROPERTY_PRICE*100:.2f}% は金利2.1%を上回るが、スプレッドは
    わずか約{(noi/PROPERTY_PRICE - INTEREST_RATE)*100:.2f}%pt。イールドギャップが極めて薄い。
  ・パターンA（フルローン）: 年間CF {cf_a:>+,.0f}円 → DSCR {dscr_a:.2f}倍で赤字。
    フルローンでの投資は成立しない。
  ・パターンB（頭金10%）: 年間CF {cf_b:>+,.0f}円（月{cf_b/12:>+,.0f}円）
    → 黒字だが極めて薄い。CCR 3.1%、回収32.7年。
  ・パターンC（頭金20%）: 年間CF {cf_c:>+,.0f}円（月{cf_c/12:>+,.0f}円）
    → CCR 3.5%、回収28.2年。投資効率は低い。

【リスク要因】 ⚠
  1. 金利上昇耐性が極めて低い
     → 金利3.0%で年間CF▲84万円、3.5%で▲{abs(cf_35):,.0f}円（パターンA）
  2. 損益分岐入居率がパターンAで96.3%（12戸中12戸必要）
     → 1戸でも空室が出れば赤字
  3. 築22年 → 大規模修繕（外壁・防水・給排水）が5年以内に発生見込み
     → 追加500〜1,000万円の支出リスク
  4. 接道3.0m → 建築基準法上のセットバック要否を要確認
  5. 土地102㎡ → 土地値での出口が限定的
  6. 10年後Cap7%売却 → 全パターンで大幅な売却損
     （残債>売却価格の「オーバーローン」状態）

【ポジティブ要因】 ✓
  1. 立川駅徒歩8分 → 単身者向け賃貸需要は底堅い
  2. RC造・法定耐用年数残25年 → 融資は付きやすい
  3. 近隣商業地域（容積率240%）→ 将来の建替余地あり
  4. 1R×12戸 → 収入分散効果あり

【総合判断】
  ┌──────────────────────────────────────────────────┐
  │  投資推奨度: ★★☆☆☆（慎重）                    │
  │                                                  │
  │  この物件は表面利回り6%に対し、NOI利回りが3.94% │
  │  と低く、金利2.1%でもフルローンでは赤字。        │
  │  頭金20%でも年間CF88万円・CCR3.5%と投資効率が  │
  │  低い。金利上昇・空室・修繕リスクに対する        │
  │  バッファが不足している。                        │
  │                                                  │
  │  購入を検討する場合の条件:                        │
  │   ① 価格交渉で1億円以下（利回り7.5%以上）       │
  │   ② レントロールで現況賃料の確認と増額余地       │
  │   ③ 修繕履歴の精査と今後10年の修繕計画策定      │
  │   ④ 金利1%台の融資先確保                        │
  └──────────────────────────────────────────────────┘
""")
