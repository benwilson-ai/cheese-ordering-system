from pydantic import BaseModel
from datetime import date
from typing import Optional

class CheeseData(BaseModel):
    id: Optional[int] = None
    type: Optional[str] = None
    form: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
    price_per_lb: Optional[str] = None
    case_count: Optional[int] = None
    case_volume: Optional[str] = None
    case_weight: Optional[str] = None
    each_count: Optional[int] = None
    each_volume: Optional[str] = None
    each_weight: Optional[str] = None
    sku: Optional[int] = None               
    upc: Optional[int] = None
    image_url: Optional[str] = None
    product_url: Optional[str] = None
    wholesale: Optional[str] = None
    out_of_stock: Optional[str] = None
    class Config:
        from_attributes = True