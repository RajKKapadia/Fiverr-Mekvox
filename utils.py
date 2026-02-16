import warnings
from typing import Any

try:
    from amazon_creatorsapi import AmazonApi
    from amazon_creatorsapi import get_asin
except ImportError:
    # Backward compatibility when only the old package is installed.
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message=r"The 'amazon_paapi' module is deprecated.*",
            category=DeprecationWarning,
        )
        from amazon_paapi import AmazonApi
        from amazon_paapi import get_asin

import config
from logger import amzn_bot_logger

amazon = AmazonApi(config.AWS_ACCESS_KEY_ID, config.AWS_SECRET_ACCESS_KEY,
                   config.AWS_ASSOCIATE_TAG, 'IT')


def _to_float(value) -> float | None:
    if value is None:
        return None
    if isinstance(value, (dict, list, tuple, set)):
        return None
    if isinstance(value, (int, float)):
        return float(value)

    raw = str(value).strip()
    if not raw:
        return None

    cleaned = []
    dot_seen = False
    for char in raw:
        if char.isdigit():
            cleaned.append(char)
        elif char in [".", ","]:
            if dot_seen:
                continue
            cleaned.append(".")
            dot_seen = True
        elif char == "-" and not cleaned:
            cleaned.append(char)

    if not cleaned or cleaned == ["-"]:
        return None

    try:
        return float("".join(cleaned))
    except ValueError:
        return None


def _first_numeric(*values) -> float | None:
    for value in values:
        number = _to_float(value)
        if number is not None:
            return number
    return None


def _get_field(data: Any, *path: str) -> Any:
    current = data
    for key in path:
        if current is None:
            return None
        if isinstance(current, dict):
            current = current.get(key)
        else:
            current = getattr(current, key, None)
    return current


def _pick_listing(listings: list[Any] | None) -> Any:
    if not listings:
        return None
    for listing in listings:
        if _get_field(listing, "is_buy_box_winner") is True:
            return listing
    return listings[0]


def _extract_from_offer_summaries(item) -> tuple[float | None, float | None, float | None]:
    offers = getattr(item, "offers", None)
    summaries = getattr(offers, "summaries", None) if offers is not None else None
    if not summaries:
        return None, None, None

    summary = summaries[0]
    summary_price = _first_numeric(
        getattr(summary, "lowest_price", None),
        getattr(getattr(summary, "lowest_price", None), "amount", None),
        getattr(getattr(summary, "lowest_price", None), "display_amount", None),
        getattr(summary, "price", None),
        getattr(getattr(summary, "price", None), "amount", None),
        getattr(getattr(summary, "price", None), "display_amount", None),
    )
    return summary_price, None, None


def get_product_info(url: str) -> tuple:
    """
    return : url, image_url, name, price, discount_price, percentage
    """
    amzn_bot_logger.info('Starting to fetch Amazon data.')
    asin = get_asin(url)
    amzn_bot_logger.info(f'Amazon URL -> {url}')
    amzn_bot_logger.info(f'ASIN -> {asin}')
    item = amazon.get_items(asin)[0]
    url = item.detail_page_url
    amzn_bot_logger.info(f'URL -> {url}')
    image_url = item.images.primary.large.url
    amzn_bot_logger.info(f'Image URL -> {image_url}')
    name = item.item_info.title.display_value
    amzn_bot_logger.info(f'Name -> {name}')
    offers = getattr(item, "offers", None)
    listings = getattr(offers, "listings", None) if offers is not None else None
    listing = _pick_listing(listings)
    if listing is None:
        offers_v2 = getattr(item, "offers_v2", None)
        listings_v2 = getattr(offers_v2, "listings", None) if offers_v2 is not None else None
        listing = _pick_listing(listings_v2)

    price = None
    discount_price = None
    discount_percentage = None

    if listing is not None:
        price_data = _get_field(listing, "price")
        price = _first_numeric(
            _get_field(price_data, "amount"),
            _get_field(price_data, "display_amount"),
            _get_field(price_data, "money", "amount"),
            _get_field(price_data, "money", "display_amount"),
        )

        savings = _get_field(price_data, "savings")
        discount_price = _first_numeric(
            _get_field(savings, "amount"),
            _get_field(savings, "display_amount"),
            _get_field(savings, "money", "amount"),
            _get_field(savings, "money", "display_amount"),
        )
        discount_percentage = _first_numeric(_get_field(savings, "percentage"))

        # Fallback when PA-API doesn't include "savings" but includes list/base price.
        saving_basis = _get_field(listing, "saving_basis")
        if saving_basis is None:
            saving_basis = _get_field(price_data, "saving_basis")
        base_price = _first_numeric(
            _get_field(saving_basis, "amount"),
            _get_field(saving_basis, "display_amount"),
            _get_field(saving_basis, "money", "amount"),
            _get_field(saving_basis, "money", "display_amount"),
        )
        if discount_price is None and price is not None and base_price is not None and base_price > price:
            discount_price = round(base_price - price, 2)
        if discount_percentage is None and discount_price is not None and base_price:
            discount_percentage = round((discount_price / base_price) * 100, 2)
    else:
        amzn_bot_logger.info("No offers.listings available for this ASIN; trying offers.summaries.")
        summary_price, summary_discount_price, summary_discount_percentage = _extract_from_offer_summaries(item)
        price = summary_price
        discount_price = summary_discount_price
        discount_percentage = summary_discount_percentage

    if price is None:
        amzn_bot_logger.info("Unable to get the price")
        price = 0.0
    if discount_price is None:
        discount_price = 0.0
    if discount_percentage is None:
        discount_percentage = 0.0

    return url, image_url, name, price, discount_price, discount_percentage
