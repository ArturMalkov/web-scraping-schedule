import uvicorn
from cassandra.cqlengine.management import sync_table
from fastapi import FastAPI

from app import config, crud, db, models, schema


settings = config.get_settings()
app = FastAPI()

session = None


@app.on_event("startup")
def on_startup():
    global session
    session = db.get_session()
    sync_table(models.Product)  # to avoid running migrations
    sync_table(models.ProductScrapeEvent)


@app.get("/products", response_model=list[schema.ProductListSchema])
def get_all_products():
    return list(models.Product.objects.all())


@app.get("/products/{asin}")
def get_product_by_asin(asin: str):
    data = dict(models.Product.objects.get(asin=asin))
    events = list(
        schema.ProductScrapeEventDetailSchema(**scrape_event)
        for scrape_event in models.ProductScrapeEvent.objects()
        .filter(asin=asin)
        .limit(5)
    )
    data["events"] = events
    data["events_url"] = f"/products/{asin}/events"
    return data


@app.get(
    "/products/{asin}/events",
    response_model=list[schema.ProductScrapeEventDetailSchema],
)
def get_product_scrape_events(asin: str):
    events = list(models.ProductScrapeEvent.objects().filter(asin=asin).limit(5))
    return events


@app.post("/events/scrape")
def create_scrape_event(data: schema.ProductListSchema):
    product, _ = crud.add_scrape_event(data.dict())
    return product


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
