import logging
import time
from typing import List

import requests
from django.core.management.base import BaseCommand
from products.models import Product

log = logging.getLogger(__name__)

API_TEMPLATE = (
    "https://search.wb.ru/exactmatch/ru/common/v5/search"
    "?query={query}&page={page}&resultset=catalog&sort=popular"
    "&spp=30&dest=-1257786,-11591238&reg=0&appType=1&curr=rub"
    "&pricemarginCoeff=1.0&suppressSpellcheck=false&locale=ru"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

SLEEP_BETWEEN_PAGES = 0.5


def fetch_page(query: str, page: int) -> List[dict]:
    url = API_TEMPLATE.format(query=query, page=page)
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    root = r.json()
    return root.get("data", {}).get("products") or []


def wb_to_product_kwargs(item: dict) -> dict:
    sizes = item.get("sizes") or []
    if sizes and sizes[0].get("price"):
        basic = sizes[0]["price"]["basic"]
        product = sizes[0]["price"]["product"]
    else:
        basic = item.get("priceU") or item.get("price") or 0
        product = (
            item.get("salePriceU")
            or item.get("salePrice")
            or basic
        )
    price = round(basic / 100, 2)
    sale_price = round(product / 100, 2)

    rating_raw = item.get("reviewRating", 0)
    rating = rating_raw if rating_raw <= 5 else round(rating_raw / 20, 2)

    return {
        "price": price,
        "sale_price": sale_price,
        "rating": rating,
        "reviews": item.get("feedbacks", 0),
    }


class Command(BaseCommand):
    help = "Парсит товары Wildberries по запросу и сохраняет их в БД."

    def add_arguments(self, parser):
        parser.add_argument("query", type=str)
        parser.add_argument("--pages", type=int, default=1)
        parser.add_argument("--per-page", type=int, default=100)

    def handle(self, *args, **opts):
        query = opts["query"]
        max_pages = opts["pages"]
        limit = opts["per_page"]
        created = updated = 0
        for page in range(1, max_pages + 1):
            try:
                items = fetch_page(query, page)[:limit]
            except Exception as exc:
                self.stderr.write(self.style.ERROR(f"Страница {page}: {exc}"))
                break
            if not items:
                self.stderr.write(self.style.WARNING("WB пустой ответ"))
                break
            for it in items:
                defaults = wb_to_product_kwargs(it)
                obj, is_new = Product.objects.update_or_create(
                    name=it["name"], defaults=defaults
                )
                created += is_new
                updated += 1 - is_new
            time.sleep(SLEEP_BETWEEN_PAGES)
        self.stdout.write(
            self.style.SUCCESS(f"Done! +{created} new, {updated} updated.")
        )
