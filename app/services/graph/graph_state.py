from typing import List, Dict, Optional
from enum import Enum
from pydantic import BaseModel



class Message(BaseModel):
    role: str
    content: str

class GraphState(BaseModel):
    selected: Optional[str] = None
    messages: List[Dict[str, str]]
    query: Optional[str] = None
    input_query: Optional[str] = None
    output_query: Optional[str] = None
    raw_data: Optional[List[Dict]] = None
    history: List[Dict[str, str]] = []