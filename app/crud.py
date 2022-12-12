import copy
import uuid


from app.models import Product, ProductScrapeEvent


def create_entry(data: dict):
    return Product.create(**data)


def create_scrape_entry(data: dict):
    data["uuid"] = uuid.uuid1()  # uuid1 includes a timestamp
    return ProductScrapeEvent.create(**data)


def add_scrape_event(data: dict, fresh: bool = False):
    if fresh:
        data = copy.deepcopy(data)
    product = create_entry(data)
    scrape_object = create_scrape_entry(data)
    return product, scrape_object
