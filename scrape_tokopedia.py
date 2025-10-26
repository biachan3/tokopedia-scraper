import argparse
import json
import time
import random
import re
from urllib.parse import quote_plus
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from utils import (
    logger,
    random_delay,
    retry,
    get_random_user_agent,
    extract_price,
    save_csv,
    save_json,
    build_playwright_context_options,
)

BASE_SEARCH_URL = "https://www.tokopedia.com/search?st=product&q={q}"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def parse_ld_json(soup):
    items = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "{}")
        except Exception:
            continue
        if isinstance(data, dict):
            if data.get("@type") in ("ItemList", "Product"):
                items.append(data)
        elif isinstance(data, list):
            items.extend([d for d in data if isinstance(d, dict)])
    return items


def fallback_parse_cards(soup):
    products = []
    cards = soup.select("div.css-5wh65g")

    for c in cards:
        a_tag = c.find("a", href=True)
        link = a_tag["href"] if a_tag else None

        # Nama produk
        name_tag = c.select_one(".SzILjt4fxHUFNVT48ZPhHA\\=\\= span")
        name = name_tag.get_text(strip=True) if name_tag else None

        # Harga
        price_tag = c.select_one(".urMOIDHH7I0Iy1Dv2oFaNw\\=\\=")
        price = price_tag.get_text(strip=True) if price_tag else None

        # Toko dan lokasi
        shop_block = c.select_one(".ljZNQLe6R-7wAWexijt7lA\\=\\=")
        shop, location = None, None
        if shop_block:
            spans = shop_block.find_all("span")
            if len(spans) >= 2:
                shop = spans[0].get_text(strip=True)
                location = spans[1].get_text(strip=True)

        # Rating (opsional)
        rating_tag = c.select_one(".c7W9YYbRQuC29\\+GfsfRTEA\\=\\= span")
        rating = rating_tag.get_text(strip=True) if rating_tag else None

        if name and price:
            products.append(
                {
                    "name": name,
                    "price": price,
                    "shop": shop,
                    "location": location,
                    "rating": rating,
                    "link": link,
                }
            )

    return products


@retry(tries=3, delay=2, backoff=1.8, logger=logger)
def scrape_query(query, pages=1, headless=True, delay_range=(1.0, 3.0)):
    query_enc = quote_plus(query)
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            **build_playwright_context_options(user_agent=get_random_user_agent())
        )
        page = context.new_page()
        for page_num in range(1, pages + 1):
            url = BASE_SEARCH_URL.format(q=query_enc)
            if page_num > 1:
                url += f"&page={page_num}"
            logger.info(f"[{page_num}/{pages}] Memuat: {url}")
            try:
                page.goto(url, timeout=30000)
                page.wait_for_load_state("networkidle", timeout=20000)
            except Exception as e:
                logger.warning(f"Gagal memuat halaman {page_num}: {e}")
                continue
            for _ in range(6):
                page.mouse.wheel(0, 3000)
                time.sleep(1.2)
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            ld_items = parse_ld_json(soup)
            if ld_items:
                for item in ld_items:
                    if item.get("@type") == "ItemList" and item.get("itemListElement"):
                        for li in item["itemListElement"]:
                            it = li.get("item") if isinstance(li, dict) else li
                            if isinstance(it, dict):
                                results.append(
                                    {
                                        "name": it.get("name"),
                                        "price": (it.get("offers") or {}).get("price"),
                                        "currency": (it.get("offers") or {}).get(
                                            "priceCurrency"
                                        ),
                                        "link": it.get("url"),
                                    }
                                )
                    elif item.get("@type") == "Product":
                        results.append(
                            {
                                "name": item.get("name"),
                                "price": (item.get("offers") or {}).get("price"),
                                "currency": (item.get("offers") or {}).get(
                                    "priceCurrency"
                                ),
                                "link": item.get("url"),
                            }
                        )
            else:
                cards = fallback_parse_cards(soup)
                results.extend(cards)
            random_delay(*delay_range)
        browser.close()
    results = [r for r in results if r.get("name") and r.get("price")]
    return results


def save_results(items, query):
    ts = int(time.time())
    csv_path = OUTPUT_DIR / f"tokopedia_{quote_plus(query)}_{ts}.csv"
    json_path = OUTPUT_DIR / f"tokopedia_{quote_plus(query)}_{ts}.json"
    save_csv(items, csv_path)
    save_json(items, json_path)
    logger.info(f"Hasil tersimpan di:\n - {csv_path}\n - {json_path}")
    return csv_path, json_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scraper Tokopedia berdasarkan kata kunci."
    )
    parser.add_argument(
        "--query",
        "-q",
        required=True,
        help="Kata kunci pencarian (misal: 'laptop gaming')",
    )
    parser.add_argument(
        "--pages", "-p", type=int, default=1, help="Jumlah halaman yang ingin diambil"
    )
    parser.add_argument(
        "--headless", action="store_true", help="Jalankan browser dalam mode headless"
    )
    args = parser.parse_args()
    logger.info("Memulai scraping Tokopedia...")
    data = scrape_query(args.query, pages=args.pages, headless=args.headless)
    logger.info(f"Jumlah item ditemukan: {len(data)}")
    save_results(data, args.query)
    logger.info("Selesai ✅")
