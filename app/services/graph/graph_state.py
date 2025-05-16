import operator
from typing import List, Dict   
from typing_extensions import TypedDict, Annotated
from enum import Enum
from pydantic import BaseModel



class Message(BaseModel):
    role: str
    content: str

class GraphState(TypedDict):
    selected: str
    messages: List[Dict[str, str]]
    query: str
    input_query: str
    output_query: str
    raw_data: Annotated[List[Dict], operator.add]
    history: List[Dict[str, str]] = []
    txt2mongo_result: str
    txt2pinecone_result: str
