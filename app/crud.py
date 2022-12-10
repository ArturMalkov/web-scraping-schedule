from cassandra.cqlengine.management import sync_table

from app.db import get_session
from app.models import Product


session = get_session()
sync_table(Product)  # to avoid running migrations


def create_entry(data: dict):
    return Product.create(**data)
