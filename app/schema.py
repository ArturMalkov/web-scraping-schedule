import uuid
from typing import Any, Optional

from pydantic import BaseModel, root_validator

from app import utils


class ProductSchema(BaseModel):
    asin: str
    title: Optional[str]


class ProductListSchema(BaseModel):
    asin: str
    title: Optional[str]
    price_str: Optional[str]


class ProductScrapeEventSchema(BaseModel):
    uuid: uuid.UUID
    asin: str
    title: Optional[str]
    price_str: Optional[str]


class ProductScrapeEventDetailSchema(BaseModel):
    asin: str
    title: Optional[str]
    price_str: Optional[str]
    created: Optional[Any] = None

    @root_validator(pre=True)
    def extra_create_time_from_uuid(cls, values):  # assume that datetime from uuid is 'created' time
        values["created"] = utils.uuid1_time_to_datetime(values["uuid"].time)
        return values
