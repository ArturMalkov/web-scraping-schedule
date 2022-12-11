import uvicorn
from cassandra.cqlengine.management import sync_table
from fastapi import FastAPI

from app import config, db, models, schema


settings = config.get_settings()
app = FastAPI()

session = None


@app.on_event("startup")
def on_startup():
    global session
    session = db.get_session()
    sync_table(models.Product)
    sync_table(models.ProductScrapeEvent)


@app.get("/products", response_model=list[schema.ProductListSchema])
def list_all_products():
    return list(models.Product.objects.all())


@app.get("/products/{asin}")
def list_product(asin: str):
    data = dict(models.Product.objects.get(asin=asin))
    events = list(schema.ProductScrapeEventDetailSchema(**scrape_event)
                  for scrape_event in models.ProductScrapeEvent.objects().filter(asin=asin).all())
    data["events"] = events
    return data


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
