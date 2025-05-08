from pydantic import BaseModel
from datetime import date
from typing import Optional

class RetailLease(BaseModel):
    id: Optional[int] = None
    start_date: Optional[date] = None
    expiry_date: Optional[date] = None
    current_rent_pa: Optional[float] = None
    current_rent_sqm: Optional[float] = None
    centre_name: Optional[str] = None
    tenant_category: Optional[str] = None
    tenant_subcategory: Optional[str] = None
    lessor: Optional[str] = None
    lessee: Optional[str] = None
    area: Optional[float] = None

    class Config:
        from_attributes = True