from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Product(Model):
    __keyspace__ = "scraper_app"

    asin = columns.Text(primary_key=True, required=True)  # 'asin' stands for 'Amazon shipping id number'
    title = columns.Text()
    price_str = columns.Text(default="-1")
