"""
健美家（kenbiya.com）スクレイパー
首都圏の新着投資用物件を取得する
"""

import logging
import re
import time
from typing import Optional

import requests
from bs4 import BeautifulSoup

from .rakumachi import Property, parse_building_age_years

logger = logging.getLogger(__name__)

BASE_URL = "https://www.kenbiya.com"


def fetch_page(area_path: str, config: dict) -> Optional[str]:
    """健美家の物件一覧ページを取得"""
    if config.get("filters", {}).get("newly_listed", False):
        url = f"{BASE_URL}/pp0/{area_path}/cd2=1/"  # 新着24時間以内
    else:
        url = f"{BASE_URL}/pp0/{area_path}/"  # 全物件
    scraping_cfg = config.get("scraping", {})
    headers = {"User-Agent": scraping_cfg.get("user_agent", "")}
    timeout = scraping_cfg.get("timeout_seconds", 30)
    max_retries = scraping_cfg.get("max_retries", 3)

    for attempt in range(max_retries):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as e:
            logger.warning(f"健美家 {area_path} 取得失敗 (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(scraping_cfg.get("request_delay_seconds", 2))
    return None


def parse_properties(html: str, area_name: str) -> list[Property]:
    """HTMLから物件情報をパース"""
    soup = BeautifulSoup(html, "lxml")
    properties = []

    # 健美家の物件リスト要素
    property_cards = soup.select(
        ".property-body, .search-result, .bukken-detail, "
        "table.bukken-table tr, .list-body > div, article"
    )

    for card in property_cards:
        try:
            prop = _parse_card(card, area_name)
            if prop and prop.title:
                properties.append(prop)
        except Exception as e:
            logger.debug(f"健美家カードのパース失敗: {e}")
            continue

    if not properties:
        properties = _fallback_parse(soup, area_name)

    return properties


def _parse_card(card, area_name: str) -> Optional[Property]:
    """物件カード要素から情報を抽出"""
    prop = Property(source="健美家")

    # タイトル・リンク
    title_el = card.select_one("a.bukken-title, h2 a, h3 a, .title a, a[href*='/pp/']")
    if title_el:
        prop.title = title_el.get_text(strip=True)
        href = title_el.get("href", "")
        prop.url = href if href.startswith("http") else f"{BASE_URL}{href}"

    # 価格
    price_el = card.select_one(".price, [class*='price'], [class*='kakaku']")
    if price_el:
        prop.price = price_el.get_text(strip=True)

    # 利回り
    yield_el = card.select_one("[class*='yield'], [class*='rimawari']")
    if yield_el:
        prop.gross_yield = yield_el.get_text(strip=True)

    # 所在地
    location_el = card.select_one(".address, [class*='address'], [class*='shozaichi']")
    if location_el:
        prop.location = location_el.get_text(strip=True)
    else:
        prop.location = area_name

    # 駅・交通
    station_el = card.select_one("[class*='station'], [class*='access'], [class*='traffic']")
    if station_el:
        text = station_el.get_text(strip=True)
        prop.station = text
        walk_match = re.search(r"徒歩(\d+)分", text)
        if walk_match:
            prop.walk_minutes = walk_match.group(1)

    # テキスト全体から情報補完
    card_text = card.get_text()

    # 築年数
    age_match = re.search(r"築(\d+)年", card_text)
    if age_match:
        prop.building_age = f"築{age_match.group(1)}年"
        prop.building_age_years = int(age_match.group(1))
    elif "新築" in card_text:
        prop.building_age = "新築"
        prop.building_age_years = 0

    # 構造
    for s in ["RC造", "SRC造", "鉄筋コンクリート造", "鉄骨鉄筋コンクリート造"]:
        if s in card_text:
            prop.structure = s
            break

    # 価格（テキストから補完）
    if not prop.price:
        price_match = re.search(r"(\d[\d,]+万円)", card_text)
        if price_match:
            prop.price = price_match.group(1)

    # 利回り（テキストから補完）
    if not prop.gross_yield:
        yield_match = re.search(r"(\d+\.?\d*%)", card_text)
        if yield_match:
            prop.gross_yield = yield_match.group(1)

    return prop


def _fallback_parse(soup: BeautifulSoup, area_name: str) -> list[Property]:
    """構造化要素が見つからない場合の簡易パース"""
    properties = []
    for link in soup.select("a[href*='/pp/']"):
        text = link.get_text(strip=True)
        if len(text) > 5:  # 短すぎるリンクは除外
            prop = Property(source="健美家")
            prop.title = text
            href = link.get("href", "")
            prop.url = href if href.startswith("http") else f"{BASE_URL}{href}"
            prop.location = area_name
            if prop.title:
                properties.append(prop)
    return properties


def search_properties(config: dict) -> list[Property]:
    """設定に基づいて健美家から物件を検索"""
    all_properties = []
    areas = config.get("areas", {}).get("kenbiya", [])
    scraping_cfg = config.get("scraping", {})
    delay = scraping_cfg.get("request_delay_seconds", 2)
    filters = config.get("filters", {})

    for area in areas:
        area_path = area["path"]
        area_name = area["name"]
        logger.info(f"健美家: {area_name} ({area_path}) を検索中...")

        html = fetch_page(area_path, config)
        if not html:
            logger.warning(f"健美家: {area_name} のページ取得に失敗")
            continue

        properties = parse_properties(html, area_name)
        logger.info(f"健美家: {area_name} から {len(properties)} 件取得")
        all_properties.extend(properties)

        time.sleep(delay)

    # フィルタリング
    from .rakumachi import apply_filters
    filtered = apply_filters(all_properties, filters)
    logger.info(f"健美家: フィルタ後 {len(filtered)}/{len(all_properties)} 件")
    return filtered
