from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from celery import Celery
from celery.schedules import crontab
from celery.signals import beat_init, worker_process_init  # needed for scheduling tasks

from app import config, crud, db, models, schema, scraper as scraper_service


celery_app = Celery(__name__)
settings = config.get_settings()

REDIS_URL = settings.redis_url
celery_app.conf.broker_url = REDIS_URL
celery_app.conf.result_backend = REDIS_URL


def celery_on_startup(*args, **kwargs):
    if connection.cluster is not None:
        connection.cluster.shutdown()

    if connection.session is not None:
        connection.session.shutdown()

    cluster = db.get_cluster()
    session = cluster.connect()
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))
    sync_table(models.Product)
    sync_table(models.ProductScrapeEvent)


beat_init.connect(celery_on_startup)
worker_process_init.connect(celery_on_startup)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, *args, **kwargs):
    # sender.add_periodic_task(1, random_task.s("hello"), expires=10)  # to run a function every second for 10 seconds

    # sender.add_periodic_task(
    #     crontab(hour=8, minute=0, day_of_week=2),  # to run every Tuesday at 8AM
    #     random_task.s("hello")
    # )

    sender.add_periodic_task(  # to run scraping task every 5 minutes
        crontab(minute="*/5"), scrape_products.s()
    )


# celery --app app.worker.celery_app worker --beat -s celerybeat-schedule --loglevel INFO
@celery_app.task
def random_task(name):
    print(f"Hello, {name}")


@celery_app.task
def get_all_products():
    query = models.Product.objects().all().values_list("asin", flat=True)
    print(list(query))


@celery_app.task
def scrape_asin(asin):
    scraper = scraper_service.Scraper(asin=asin, endless_scroll=True)
    dataset = scraper.scrape()
    try:
        validated_data = schema.ProductListSchema(**dataset)
    except:
        validated_data = None

    if validated_data is not None:
        product, _ = crud.add_scrape_event(validated_data.dict())
        return product


@celery_app.task
def scrape_products():
    print("Doing scraping...")
    query = list(models.Product.objects().all().values_list("asin", flat=True))
    for asin in query:
        scrape_asin.delay(asin)
