"""
楽待（rakumachi.jp）スクレイパー
首都圏の新着投資用物件を取得する
"""

import logging
import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

BASE_URL = "https://www.rakumachi.jp"
SEARCH_URL = f"{BASE_URL}/syuuekibukken/area/prefecture/dimAll/"


@dataclass
class Property:
    """物件データ"""
    title: str = ""
    url: str = ""
    price: str = ""
    gross_yield: str = ""
    net_yield: str = ""
    location: str = ""
    station: str = ""
    walk_minutes: str = ""
    building_age: str = ""
    building_age_years: Optional[int] = None
    structure: str = ""
    layout: str = ""
    area_sqm: str = ""
    floors: str = ""
    property_type: str = ""
    source: str = "楽待"
    fetched_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))


def fetch_page(area_code: int, config: dict) -> Optional[str]:
    """楽待の物件一覧ページを取得"""
    params = {
        "area": area_code,
    }
    # newly_listed が true の場合のみ新着フィルタを適用
    if config.get("filters", {}).get("newly_listed", False):
        params["newly"] = 1

    scraping_cfg = config.get("scraping", {})
    headers = {"User-Agent": scraping_cfg.get("user_agent", "")}
    timeout = scraping_cfg.get("timeout_seconds", 30)
    max_retries = scraping_cfg.get("max_retries", 3)

    for attempt in range(max_retries):
        try:
            resp = requests.get(SEARCH_URL, params=params, headers=headers, timeout=timeout)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as e:
            logger.warning(f"楽待 area={area_code} 取得失敗 (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(scraping_cfg.get("request_delay_seconds", 2))
    return None


def parse_building_age_years(age_str: str) -> Optional[int]:
    """築年数文字列から年数を抽出"""
    match = re.search(r"築(\d+)年", age_str)
    if match:
        return int(match.group(1))
    if "新築" in age_str:
        return 0
    return None


def parse_properties(html: str, area_name: str) -> list[Property]:
    """HTMLから物件情報をパース"""
    soup = BeautifulSoup(html, "lxml")
    properties = []

    # 楽待の物件カード要素を探索
    # 実際のHTML構造に応じて調整が必要
    property_cards = soup.select(".propertyBlock, .property-card, .search-result-item, article.property")

    if not property_cards:
        # フォールバック: テーブル形式の一覧
        property_cards = soup.select("table.property-table tr, .bukken-list > div, .list-item")

    for card in property_cards:
        try:
            prop = _parse_card(card, area_name)
            if prop and prop.title:
                properties.append(prop)
        except Exception as e:
            logger.debug(f"カードのパース失敗: {e}")
            continue

    # 構造化データが取得できない場合、簡易パースを試行
    if not properties:
        properties = _fallback_parse(soup, area_name)

    return properties


def _parse_card(card, area_name: str) -> Optional[Property]:
    """物件カード要素から情報を抽出"""
    prop = Property()

    # タイトル・リンク
    title_el = card.select_one("a.property-title, h2 a, h3 a, .title a, a[href*='syuuekibukken']")
    if title_el:
        prop.title = title_el.get_text(strip=True)
        href = title_el.get("href", "")
        prop.url = href if href.startswith("http") else f"{BASE_URL}{href}"

    # 価格
    price_el = card.select_one(".price, .property-price, [class*='price']")
    if price_el:
        prop.price = price_el.get_text(strip=True)

    # 利回り
    yield_el = card.select_one(".yield, .property-yield, [class*='yield'], [class*='rimawari']")
    if yield_el:
        prop.gross_yield = yield_el.get_text(strip=True)

    # 所在地
    location_el = card.select_one(".location, .address, [class*='address'], [class*='location']")
    if location_el:
        prop.location = location_el.get_text(strip=True)

    # 駅
    station_el = card.select_one(".station, .access, [class*='station'], [class*='access']")
    if station_el:
        text = station_el.get_text(strip=True)
        prop.station = text
        walk_match = re.search(r"徒歩(\d+)分", text)
        if walk_match:
            prop.walk_minutes = walk_match.group(1)

    # 築年数
    age_el = card.select_one("[class*='age'], [class*='year'], [class*='chiku']")
    if age_el:
        prop.building_age = age_el.get_text(strip=True)
        prop.building_age_years = parse_building_age_years(prop.building_age)

    # 構造
    structure_el = card.select_one("[class*='structure'], [class*='kouzou']")
    if structure_el:
        prop.structure = structure_el.get_text(strip=True)

    # テキスト全体からの補完パース
    card_text = card.get_text()
    if not prop.building_age:
        age_match = re.search(r"築(\d+)年", card_text)
        if age_match:
            prop.building_age = f"築{age_match.group(1)}年"
            prop.building_age_years = int(age_match.group(1))

    if not prop.structure:
        for s in ["RC造", "SRC造", "鉄筋コンクリート造", "鉄骨鉄筋コンクリート造"]:
            if s in card_text:
                prop.structure = s
                break

    return prop


def _fallback_parse(soup: BeautifulSoup, area_name: str) -> list[Property]:
    """構造化要素が見つからない場合の簡易パース"""
    properties = []
    # リンクベースの簡易抽出
    for link in soup.select("a[href*='syuuekibukken/cl_mansion'], a[href*='syuuekibukken/cl_apart']"):
        prop = Property()
        prop.title = link.get_text(strip=True)
        href = link.get("href", "")
        prop.url = href if href.startswith("http") else f"{BASE_URL}{href}"
        prop.location = area_name
        prop.source = "楽待"
        if prop.title:
            properties.append(prop)
    return properties


def search_properties(config: dict) -> list[Property]:
    """設定に基づいて楽待から物件を検索"""
    all_properties = []
    areas = config.get("areas", {}).get("rakumachi", [])
    scraping_cfg = config.get("scraping", {})
    delay = scraping_cfg.get("request_delay_seconds", 2)
    filters = config.get("filters", {})

    for area in areas:
        area_code = area["code"]
        area_name = area["name"]
        logger.info(f"楽待: {area_name} (code={area_code}) を検索中...")

        html = fetch_page(area_code, config)
        if not html:
            logger.warning(f"楽待: {area_name} のページ取得に失敗")
            continue

        properties = parse_properties(html, area_name)
        logger.info(f"楽待: {area_name} から {len(properties)} 件取得")
        all_properties.extend(properties)

        time.sleep(delay)

    # フィルタリング
    filtered = apply_filters(all_properties, filters)
    logger.info(f"楽待: フィルタ後 {len(filtered)}/{len(all_properties)} 件")
    return filtered


def parse_price_man(price_str: str) -> Optional[float]:
    """日本語の価格文字列を万円単位の数値に変換

    例: "1億4000万円" → 14000, "9000万円" → 9000, "2億3800万円" → 23800
    """
    if not price_str:
        return None
    oku = 0.0
    man = 0.0
    oku_match = re.search(r"(\d+(?:\.\d+)?)億", price_str)
    if oku_match:
        oku = float(oku_match.group(1)) * 10000
    man_match = re.search(r"(\d+(?:\.\d+)?)万", price_str)
    if man_match:
        man = float(man_match.group(1))
    total = oku + man
    return total if total > 0 else None


def parse_yield_percent(yield_str: str) -> Optional[float]:
    """利回り文字列をパーセント数値に変換

    例: "5.82%" → 5.82
    """
    if not yield_str:
        return None
    match = re.search(r"(\d+(?:\.\d+)?)\s*%", yield_str)
    if match:
        return float(match.group(1))
    return None


def parse_walk_minutes(walk_str: str) -> Optional[int]:
    """徒歩分数の文字列を整数に変換"""
    if not walk_str:
        return None
    try:
        return int(walk_str)
    except (ValueError, TypeError):
        return None


def apply_filters(properties: list[Property], filters: dict) -> list[Property]:
    """フィルタ条件を適用

    重要: データが取得できない（None・空文字・パース不能）場合は除外しない。
    データがあり、条件を満たさないことが確認できた場合のみ除外する。
    """
    max_age = filters.get("max_building_age_years")
    min_age = filters.get("min_building_age_years")
    structure_keywords = filters.get("structure", [])
    min_price = filters.get("min_price_man")
    max_price = filters.get("max_price_man")
    min_yield = filters.get("min_yield_percent")
    # NOTE: min_units フィルタは Property に戸数フィールドがないため現時点では適用不可。
    # 戸数データが取得可能になった際に追加すること。
    max_walk = filters.get("max_walk_minutes")
    property_types = filters.get("property_types", [])

    result = []
    for prop in properties:
        # --- 築年数フィルタ（上限） ---
        if max_age is not None and prop.building_age_years is not None:
            if prop.building_age_years > max_age:
                continue

        # --- 築年数フィルタ（下限） ---
        if min_age is not None and prop.building_age_years is not None:
            if prop.building_age_years < min_age:
                continue

        # --- 構造フィルタ ---
        if prop.structure and structure_keywords:
            if not any(kw in prop.structure for kw in structure_keywords):
                continue

        # --- 価格フィルタ ---
        price_man = parse_price_man(prop.price)
        if price_man is not None:
            if min_price is not None and price_man < min_price:
                continue
            if max_price is not None and price_man > max_price:
                continue

        # --- 利回りフィルタ ---
        gross = parse_yield_percent(prop.gross_yield)
        if min_yield is not None and gross is not None:
            if gross < min_yield:
                continue

        # --- 徒歩分数フィルタ ---
        walk = parse_walk_minutes(prop.walk_minutes)
        if max_walk is not None and walk is not None:
            if walk > max_walk:
                continue

        # --- 物件種別フィルタ ---
        if prop.property_type and property_types:
            if prop.property_type not in property_types:
                continue

        result.append(prop)
    return result
