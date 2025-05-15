from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import pandas as pd

from app.core.config import settings, ModelType
from app.db.vectordb import vector_db
from app.db.mongodb import mongodb
from app.core.prompt_templates.query_transformation import query_transformation
from app.core.prompt_templates.mongo_vector import mongo_vector
from app.core.prompt_templates.generate_query import generate_query
from app.core.prompt_templates.generate_response import generate_response
from app.core.function_templates.mongo_vector import mongo_vector_tool
from .graph_state import GraphState, DatabaseEnum, AvailableEnum

model = ChatOpenAI(
    model=ModelType.gpt4o,
    openai_api_key=settings.OPENAI_API_KEY
)

def extract_function_params(prompt, function):
    function_name = function[1]["function"]["name"]
    arg_name = list(function[1]["function"]["parameters"]['properties'].keys())[0]
    model_ = model.bind_tools(function, tool_choice=function_name)
    messages = [SystemMessage(prompt)]
    tool_call = model_.invoke(messages).tool_calls
    prop = tool_call[0]['args'][arg_name]

    return prop
def extract_is_available(prompt, function):
    function_name = function[0]["function"]["name"]
    arg_name = list(function[0]["function"]["parameters"]['properties'].keys())[0]
    model_ = model.bind_tools(function, tool_choice=function_name)
    messages = [SystemMessage(prompt)]
    tool_call = model_.invoke(messages).tool_calls
    prop = tool_call[0]['args'][arg_name]
    return prop
    
def format_conversation_history(messages: List[Dict[str, str]]) -> str:
    return "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])

def determine_about_cheese(state: GraphState) -> GraphState:
    is_available = extract_is_available(prompt=mongo_vector.format(
        query=state.query,
        conversation=format_conversation_history(state.messages)
    ), function=mongo_vector_tool)
    if is_available == "yes":
        return AvailableEnum.AVAILABLE 
    else:
        return AvailableEnum.AVAILABLE

def query_transformation_node(state: GraphState) -> GraphState:
    return state

def determine_database(state: GraphState) -> DatabaseEnum:
    is_mongo = extract_function_params(prompt=mongo_vector.format(
        query=state.query,
        conversation=format_conversation_history(state.messages)
    ), function=mongo_vector_tool)
    if is_mongo == "yes":
        return DatabaseEnum.MONGO
    else:
        return DatabaseEnum.VECTORDB

def txt2mongo_node(state: GraphState) -> GraphState:
    state.database = DatabaseEnum.MONGO
    response = model.invoke(state.messages + [SystemMessage(generate_query.format(
        query=state.query,
        conversation=format_conversation_history(state.messages)
    ))])

    state.mongo_query = response.content.strip().replace('``mongo', '').replace('`', '')
    return state

def data_retrieval_node(state: GraphState) -> GraphState:
    try:
        if state.database == DatabaseEnum.MONGO:
            print("MONGO QUERY: ", state.mongo_query)
            results = mongodb.query(state.mongo_query)
        else:
            print("VECTOR QUERY: ", state.query)
            results = vector_db.query(state.query, top_k=3)
            results = [result.model_dump() for result in results]
        state.raw_data = results
        
        # Dynamically build context string using only available fields
        context = "\n\n".join(
            "\n".join([
                f"{key.replace('_', ' ').title()}: {value}"
                for key, value in cheese.items()
                if value is not None
            ]) for cheese in results
        )
        prompt = generate_response.format(
            context=context,
        )

        response = model.invoke(state.messages + [HumanMessage(prompt)])
        state.messages.append({"role": "assistant", "content": response.content})

    except Exception as e:
        print(f"Error in data retrieval: {str(e)}")
        state.messages.append({
            "role": "assistant",
            "content": "I apologize, but I encountered an error while retrieving the information. Could you please rephrase your question?"
        })

    return state