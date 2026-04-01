#!/usr/bin/env python3
"""
健美家フルスキャン: サーバー側フィルタ + BeautifulSoupパース

■ アプローチ
  1. URLパスフィルタでサーバー側絞り込み（5,025件→18件）
  2. 個別物件ページをurllibで取得しBeautifulSoupでパース
  3. 条件合致候補をJSON出力

■ 使い方
  pip install beautifulsoup4 lxml
  python3 scripts/kenbiya_scan.py
"""

import json
import re
import sys
import time
import urllib.request
from dataclasses import dataclass, asdict
from typing import Optional

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: pip install beautifulsoup4 lxml", file=sys.stderr)
    sys.exit(1)

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Server-side filter: RC造/利回り5.5%+/築25年以内/6戸+/徒歩10分
# 価格フィルタは6個目になるため省略（クライアント側でチェック）
LIST_URL = "https://www.kenbiya.com/pp3/s/{pref}/koz=3/r1=5.5/rc2=25/s1=6/w2=10/"
LIST_URL_PAGE = "https://www.kenbiya.com/pp3/s/{pref}/koz=3/r1=5.5/rc2=25/s1=6/w2=10/n-{page}/"

AREAS = [
    {"pref": "tokyo", "name": "東京都"},
    {"pref": "kanagawa", "name": "神奈川県"},
    {"pref": "saitama", "name": "埼玉県"},
    {"pref": "chiba", "name": "千葉県"},
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
    url: str = ""
    area_name: str = ""
    source: str = "健美家"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    resp = urllib.request.urlopen(req, timeout=20)
    return resp.read().decode("utf-8")


def parse_price_man(text: str) -> int:
    total = 0
    oku = re.search(r"(\d+)億", text)
    man = re.search(r"([\d,]+)万", text)
    if oku:
        total += int(oku.group(1)) * 10000
    if man:
        total += int(man.group(1).replace(",", ""))
    return total


def get_property_urls(html: str) -> list[str]:
    """一覧ページから物件詳細URLを抽出"""
    urls = re.findall(r'href="(/pp3/s/[^"]*?re_[^"]*?)"', html)
    return list(dict.fromkeys(urls))


def get_pagination_urls(html: str, pref: str) -> list[str]:
    """一覧ページからページネーションリンクを抽出（存在する場合のみ）"""
    pattern = rf'href="(/pp3/s/{pref}/[^"]*n-(\d+)[^"]*)"'
    matches = re.findall(pattern, html)
    return list(dict.fromkeys(url for url, _ in matches))


def parse_detail_page(html: str, url: str, area_name: str) -> Optional[Property]:
    """個別物件ページをパース"""
    soup = BeautifulSoup(html, "lxml")
    prop = Property(area_name=area_name, url=f"https://www.kenbiya.com{url}")

    # 物件名
    title = soup.select_one("h1, .detail_title, .bukken_name")
    if title:
        prop.name = title.get_text(strip=True)[:60]

    text = soup.get_text()

    # 価格
    price_m = re.search(r"(?:価格|販売価格)[^\d]*([\d,]+万円|[\d.]+億[\d,]*万?円)", text)
    if price_m:
        prop.price_str = price_m.group(1)
        prop.price_man = parse_price_man(prop.price_str)

    # 利回り
    yield_m = re.search(r"(?:利回り|表面利回り)[^\d]*([\d.]+)\s*%", text)
    if yield_m:
        prop.gross_pct = float(yield_m.group(1))

    # 所在地
    addr_m = re.search(r"(?:所在地|住所)[^\n]*?([^\s]+[都道府県][^\n]{3,30})", text)
    if addr_m:
        prop.address = addr_m.group(1).strip()[:40]

    # 交通
    access_m = re.search(r"(?:交通|最寄り駅|アクセス)[^\n]*?([^\n]+駅[^\n]*)", text)
    if access_m:
        prop.access = access_m.group(1).strip()[:50]
        walk = re.search(r"徒歩(\d+)分", prop.access)
        if walk:
            prop.walk_min = int(walk.group(1))

    # 構造
    for s in ["SRC造", "RC造", "鉄筋コンクリート造", "鉄骨造", "木造"]:
        if s in text:
            prop.structure = s
            break

    # 築年
    age_m = re.search(r"(\d{4})年\d*月?\s*[（(]?築(\d+)年", text)
    if age_m:
        prop.age_year = int(age_m.group(1))
        prop.age_str = f"{age_m.group(1)}年（築{age_m.group(2)}年）"
    else:
        age_m2 = re.search(r"築\s*(\d+)\s*年", text)
        if age_m2:
            prop.age_str = f"築{age_m2.group(1)}年"
            prop.age_year = 2026 - int(age_m2.group(1))

    # 戸数
    units_m = re.search(r"(\d+)\s*戸", text)
    if units_m:
        prop.units = int(units_m.group(1))

    return prop if prop.name else None


def scan_area(area: dict) -> list[Property]:
    pref = area["pref"]
    name = area["name"]

    # 1ページ目を取得
    url = LIST_URL.format(pref=pref)
    try:
        html = fetch(url)
    except Exception as e:
        print(f"  {name}: ERROR fetching list - {e}", file=sys.stderr)
        return []

    # 物件URLを抽出
    all_urls = get_property_urls(html)

    # ページネーションリンクがあれば追加ページも取得
    page_urls = get_pagination_urls(html, pref)
    for page_url in page_urls:
        time.sleep(0.5)
        try:
            page_html = fetch(f"https://www.kenbiya.com{page_url}")
            all_urls.extend(get_property_urls(page_html))
        except Exception as e:
            print(f"    ページ取得ERROR: {e}", file=sys.stderr)

    all_urls = list(dict.fromkeys(all_urls))
    print(f"  {name}: {len(all_urls)}件", file=sys.stderr)

    # 個別ページを取得してパース
    props = []
    for i, prop_url in enumerate(all_urls):
        time.sleep(0.3)
        try:
            full_url = f"https://www.kenbiya.com{prop_url}"
            detail_html = fetch(full_url)
            prop = parse_detail_page(detail_html, prop_url, name)
            if prop:
                props.append(prop)
        except Exception as e:
            pass  # skip errors silently

        if (i + 1) % 10 == 0 or i + 1 == len(all_urls):
            print(f"    詳細取得: {i+1}/{len(all_urls)} ({len(props)}件パース成功)", file=sys.stderr)

    return props


def main():
    print("健美家フルスキャン (サーバーフィルタ + 個別ページ取得)", file=sys.stderr)
    print("条件: RC造 / 5.5%+ / 築25年以内 / 6戸+ / 徒歩10分", file=sys.stderr)
    print("", file=sys.stderr)

    all_props = []
    for area in AREAS:
        try:
            props = scan_area(area)
            all_props.extend(props)
        except Exception as e:
            print(f"  ERROR {area['name']}: {e}", file=sys.stderr)

    # ローカル側で価格フィルタ（サーバーフィルタでは省略したため）
    filtered = [p for p in all_props if 5000 <= p.price_man <= 18000]

    print(f"\n=== 結果 ===", file=sys.stderr)
    print(f"全取得: {len(all_props)}件", file=sys.stderr)
    print(f"価格フィルタ後: {len(filtered)}件", file=sys.stderr)

    result = {
        "scan_date": time.strftime("%Y-%m-%d"),
        "source": "健美家",
        "total_fetched": len(all_props),
        "price_filtered": len(filtered),
        "properties": [asdict(p) for p in filtered],
    }
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
