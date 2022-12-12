from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


# List View -> Detail View
class Product(Model):
    __keyspace__ = "scraper_app"

    asin = columns.Text(
        primary_key=True, required=True
    )  # 'asin' stands for 'Amazon shipping id number'
    title = columns.Text()
    price_str = columns.Text(default="-1")


# Detail View for asin
class ProductScrapeEvent(Model):
    __keyspace__ = "scraper_app"

    uuid = columns.UUID(primary_key=True)
    asin = columns.Text(index=True)
    title = columns.Text()
    price_str = columns.Text(default="-1")
