from amazon_paapi import AmazonApi
from amazon_paapi import get_asin

import config

amazon = AmazonApi(config.AWS_ACCESS_KEY_ID, config.AWS_SECRET_ACCESS_KEY,
                   config.AWS_ASSOCIATE_TAG, 'IT')


def get_product_info(url: str) -> tuple:
    """
    return : url, image_url, name, price, discount_price, percentage
    """
    asin = get_asin(url)
    item = amazon.get_items(asin)[0]
    url = item.detail_page_url
    image_url = item.images.primary.large.url
    name = item.item_info.title.display_value
    price = item.offers.listings[0].price.amount
    try:
        discount_price = item.offers.listings[0].price.savings.amount
        discount_percentage = item.offers.listings[0].price.savings.percentage
    except:
        discount_price = 0.0
        discount_percentage = 0.0

    return url, image_url, name, price, discount_price, discount_percentage
