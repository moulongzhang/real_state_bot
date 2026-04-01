#!/usr/bin/env python3
"""
楽待フルスキャン v2: サーバー側フィルタ + BeautifulSoup正確パース

■ アプローチ
  1. URLパラメータでサーバー側フィルタ（10,000件→900件、18ページ）
  2. BeautifulSoupで各propertyBlockを個別にパース（データずれなし）
  3. 条件合致候補をJSON出力

■ 条件
  - RC造一棟マンション
  - 価格: 5,000万〜1.8億円
  - 利回り: 5.5%以上
  - 築年: 2001〜2023年
  - 戸数: 6戸以上
  - 駅徒歩: 10分以内

■ 使い方
  pip install beautifulsoup4 lxml
  python3 scripts/rakumachi_scan.py
"""

import json
import re
import sys
import time
import urllib.request
from dataclasses import dataclass, field, asdict
from typing import Optional

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: pip install beautifulsoup4 lxml", file=sys.stderr)
    sys.exit(1)

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Server-side filter URL: RC一棟 + 条件フィルタ
SEARCH_URL = (
    "https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/"
    "?dim%5B%5D=1001"       # 一棟マンション
    "&kouzou%5B%5D=3"       # RC造
    "&area={area}"
    "&price_from=5000"      # 5,000万以上
    "&price_to=18000"       # 1.8億以下
    "&gross_from=5.5"       # 利回り5.5%以上
    "&year_from=2001"       # 築2001年以降
    "&year_to=2023"         # 築2023年以前
    "&min=10"               # 徒歩10分以内
    "&houses_ge=6"          # 6戸以上
    "&page={page}"
)

AREAS = [
    {"code": 13, "name": "東京都"},
    {"code": 14, "name": "神奈川県"},
    {"code": 11, "name": "埼玉県"},
    {"code": 12, "name": "千葉県"},
]


@dataclass
class Property:
    name: str = ""
    price_str: str = ""
    price_man: int = 0
    gross_pct: float = 0.0
    address: str = ""
    access: str = ""
    walk_min: int = 99
    age_str: str = ""
    age_year: int = 0
    structure: str = ""
    units: int = 0
    floors: str = ""
    area_sqm: str = ""
    land_sqm: str = ""
    url: str = ""
    area_name: str = ""
    source: str = "楽待"


def fetch_page(area_code: int, page: int) -> str:
    url = SEARCH_URL.format(area=area_code, page=page)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    resp = urllib.request.urlopen(req, timeout=20)
    return resp.read().decode("utf-8")


def get_total_count(html: str) -> int:
    m = re.search(r"<strong>([\d,]+)</strong>\s*件の物件", html)
    return int(m.group(1).replace(",", "")) if m else 0


def parse_price_man(text: str) -> int:
    """価格文字列を万円単位に変換"""
    total = 0
    oku = re.search(r"(\d+)億", text)
    man = re.search(r"([\d,]+)万", text)
    if oku:
        total += int(oku.group(1)) * 10000
    if man:
        total += int(man.group(1).replace(",", ""))
    return total


def parse_property_block(block, area_name: str) -> Optional[Property]:
    """BeautifulSoupで1つのpropertyBlockを正確にパース"""
    prop = Property(area_name=area_name)

    # 物件名
    name_el = block.select_one(".propertyBlock__name")
    if name_el:
        prop.name = name_el.get_text(strip=True)

    # 価格
    price_el = block.select_one("b.price")
    if price_el:
        prop.price_str = price_el.get_text(strip=True)
        prop.price_man = parse_price_man(prop.price_str)

    # 利回り
    gross_el = block.select_one("b.gross")
    if gross_el:
        text = gross_el.get_text(strip=True)
        m = re.search(r"([\d.]+)%", text)
        if m:
            prop.gross_pct = float(m.group(1))

    # 所在地
    addr_el = block.select_one(".propertyBlock__address")
    if addr_el:
        prop.address = addr_el.get_text(strip=True)

    # 交通
    access_el = block.select_one(".propertyBlock__access")
    if access_el:
        prop.access = access_el.get_text(strip=True)
        walk_m = re.search(r"徒歩(\d+)分", prop.access)
        if walk_m:
            prop.walk_min = int(walk_m.group(1))

    # 物件詳細URL
    link_el = block.select_one("a.propertyBlock__content[href]")
    if link_el:
        href = link_el.get("href", "")
        prop.url = f"https://www.rakumachi.jp{href}" if href.startswith("/") else href

    # 詳細情報（築年月・構造・戸数等）は .propertyBlock__contents 内の span ペアから取得
    contents = block.select_one(".propertyBlock__contents")
    if contents:
        text = contents.get_text()
        # 築年月
        age_m = re.search(r"(\d{4})年(\d{1,2})月", text)
        if age_m:
            prop.age_str = f"{age_m.group(1)}年{age_m.group(2)}月"
            prop.age_year = int(age_m.group(1))
        # 構造
        for s in ["SRC造", "RC造", "鉄骨鉄筋コンクリート造", "鉄筋コンクリート造", "鉄骨造", "重量鉄骨造", "軽量鉄骨造", "木造"]:
            if s in text:
                prop.structure = s
                break
        # 戸数
        units_m = re.search(r"(\d+)戸", text)
        if units_m:
            prop.units = int(units_m.group(1))

    return prop if prop.name else None


def scan_area(area: dict) -> list[Property]:
    """1エリアの全ページをスキャン"""
    code = area["code"]
    name = area["name"]

    # 1ページ目を取得して総件数を確認
    html = fetch_page(code, 1)
    total = get_total_count(html)
    pages = (total + 49) // 50
    print(f"  {name}: {total}件 ({pages}ページ)", file=sys.stderr)

    all_props = []
    for page in range(1, pages + 1):
        if page > 1:
            time.sleep(0.5)
            html = fetch_page(code, page)

        soup = BeautifulSoup(html, "lxml")
        # PR広告を除外: class に "ad" を含む propertyBlock はスキップ
        blocks = soup.select("div.propertyBlock")
        for block in blocks:
            # PR広告ブロックを除外
            main = block.select_one(".propertyBlock__mainArea")
            if main and "ad-propertyListInfeedAd" in main.get("class", []):
                continue
            prop = parse_property_block(block, name)
            if prop:
                all_props.append(prop)

        if page % 5 == 0 or page == pages:
            print(f"    p{page}/{pages}: {len(all_props)}件", file=sys.stderr)

    return all_props


def main():
    print("楽待フルスキャン v2 (サーバーフィルタ + BeautifulSoup)", file=sys.stderr)
    print(f"条件: RC一棟 / 5000-18000万 / 5.5%+ / 築2001-2023 / 6戸+ / 徒歩10分", file=sys.stderr)
    print("", file=sys.stderr)

    all_props = []
    for area in AREAS:
        try:
            props = scan_area(area)
            all_props.extend(props)
        except Exception as e:
            print(f"  ERROR {area['name']}: {e}", file=sys.stderr)

    # ローカル側でRC/SRC確認（サーバーフィルタでRCを指定してもSRC等が混じる場合がある）
    rc_props = [p for p in all_props if "RC" in p.structure or "鉄筋コンクリート" in p.structure or not p.structure]

    print(f"\n=== 結果 ===", file=sys.stderr)
    print(f"全取得: {len(all_props)}件", file=sys.stderr)
    print(f"RC/不明: {len(rc_props)}件", file=sys.stderr)

    # JSON出力
    result = {
        "scan_date": time.strftime("%Y-%m-%d"),
        "total_fetched": len(all_props),
        "rc_candidates": len(rc_props),
        "properties": [asdict(p) for p in rc_props],
    }
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
