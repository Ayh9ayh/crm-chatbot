from pydantic import BaseModel, EmailStr
from typing import Optional

class Lead(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    phone: str
    city: Optional[str] = None  # Changed from "location" to "city"
    company: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    notes: Optional[str] = None
    created_date: Optional[str] = None  # Changed from "last_contacted"
    product: Optional[str] = None  # Changed from "interested_product"
    budget: Optional[int] = None
    priority: Optional[str] = None  # Added priority field

class LeadQuery(BaseModel):
    query: str
    
class LeadResponse(BaseModel):
    message: str
    leads: Optional[list] = None
    data: Optional[dict] = None