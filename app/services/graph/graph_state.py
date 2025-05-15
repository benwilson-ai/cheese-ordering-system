from typing import List, Dict, Optional
from enum import Enum
from pydantic import BaseModel


class AvailableEnum(str, Enum):
    AVAILABLE = "available"
    NOT_AVAILABLE = "not available"
class DatabaseEnum(str, Enum):
    MONGO = "mongo"
    VECTORDB = "vectordb"

class Message(BaseModel):
    role: str
    content: str

class GraphState(BaseModel):
    messages: List[Dict[str, str]]
    database: Optional[DatabaseEnum] = DatabaseEnum.VECTORDB
    query: Optional[str] = None
    mongo_query: Optional[str] = None
    raw_data: Optional[List[Dict]] = None