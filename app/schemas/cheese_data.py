from pydantic import BaseModel
from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, ValidationError

class CheeseData(BaseModel):
    _id: Optional[str] = None
    image_url: Optional[str] = None
    name: Optional[str] = None
    brand: Optional[str] = None
    department: Optional[str] = None
    each_itemCount: Optional[int] = None
    case_itemCount: Optional[int] = None
    each_dimension: Optional[str] = None
    case_dimension: Optional[str] = None
    each_weight: Optional[float] = None
    case_weight: Optional[float] = None
    more_image_url: Optional[list[str]] = None
    relateds: Optional[list[str]] = None
    each_price: Optional[float] = None
    case_price: Optional[float] = None
    price_per: Optional[float] = None
    sku: Optional[str] = None               
    wholesale: Optional[int] = None
    out_of_stock: Optional[bool] = None
    product_url: Optional[str] = None
    priceOrder: Optional[int] = None
    popularityOrder: Optional[int] = None
    weight_unit: Optional[str] = None
    class Config:
        from_attributes = True