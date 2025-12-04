from typing import Optional

from pydantic import BaseModel

class Stage1Analysis(BaseModel):
    is_product_page: bool
    content_language: Optional[str]
    title: Optional[str]
    available: Optional[bool]
    main_price_text: Optional[str]
    description_block: Optional[str]
    attributes_block: Optional[str]


class Product(BaseModel):
    title: str
    brand: Optional[str]
    price_value: Optional[float]
    price_currency: Optional[str]
    old_price_value: Optional[float]
    description: Optional[str]
    attributes: Optional[dict[str, str]]
