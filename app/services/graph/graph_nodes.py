from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.types import interrupt
from app.core.config import settings, ModelType
from app.db.vectordb import vector_db
from app.db.mongodb import mongodb
from app.core.prompt_templates.generate_pinecone_query import generate_pinecone_query
from app.core.prompt_templates.reasoning import reasoning
from app.core.prompt_templates.generate_mongodb_query import generate_mongodb_query
from app.core.prompt_templates.generate_response import generate_response
from app.core.function_templates.determine_selected import determine_selected
from .graph_state import GraphState
from langsmith.wrappers import wrap_openai
from langsmith import traceable
import json

model = ChatOpenAI(
    model=ModelType.gpt4o,
    openai_api_key=settings.OPENAI_API_KEY, 
    temperature=0.3,
)

# def extract_function_params(prompt, function):
#     function_name = function["function"]["name"]
#     arg_name = list(function["function"]["parameters"]['properties'].keys())[0]
#     model_ = model.bind_tools(function, tool_choice=function_name)
#     messages = [SystemMessage(prompt)]
#     tool_call = model_.invoke(messages).tool_calls
#     prop = tool_call[0]['args'][arg_name]

#     return prop

    
def format_conversation_history(messages: List[Dict[str, str]]) -> str:
    return "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])


# def decide_selected(state: GraphState) -> str:
#     selected = extract_function_params(prompt=reasoning.format(
#         query=state.query,
#         conversation=format_conversation_history(state.messages)
#     ), function=determine_selected)
#     return selected
@traceable
def reasoner_node(state: GraphState) -> GraphState:
    
    if(len(state.history)==0):
        previous_action="previous action"
        observation="This is first step"
    else:
        if(state.history[-1]["observation"]):
            observation=state.history[-1]["observation"]
        else:
            observation=""
        previous_action=state.history[-1]["action"]
    
    print("Reasoning Step"+str(len(state.history)+1))
    result = model.invoke(state.messages + [SystemMessage(reasoning.format(
        query=state.query,
        conversation=format_conversation_history(state.messages),
        history=json.dumps(state.history), 
        previous_action=previous_action,
        observation=observation
    ))])
    json_result = json.loads(result.content.strip())
    state.selected = json_result["action"]
    print("Selected "+state.selected)
    print(json_result["thought"])
    state.history.append(json_result)
    state.input_query = json_result["plan"]
    return state
@traceable
def ambiguit_resolver_node(state: GraphState) -> GraphState:
    print("----------------------------------------------------")
    print("Ambiguit Resolver Plan: "+state.history[-1]["plan"])
    response = model.invoke(state.history[-1]["plan"])
    print("So I say like that: "+response.content)
    state.history[-1]["observation"] = "This question is not clear."
    print("----------------------------------------------------")
    result = interrupt({
        "question": response.content
    })
    state.query = result["edited_query"]
    return state
@traceable
def txt2mongo_node(state: GraphState) -> GraphState:
    response = model.invoke(state.messages + [SystemMessage(generate_mongodb_query.format(
        query=state.input_query,
        conversation=format_conversation_history(state.messages)
    ))])
    state.output_query = response.content.strip().replace('``mongo', '').replace('`', '')
    print(state.output_query)
    state.history[-1]["observation"] = "\nThis is result query: "+state.output_query
    results = []
    try:
        results = mongodb.query(state.output_query)
        # Remove _id field from results
        results = [{k: v for k, v in cheese.items() if k != '_id'} for cheese in results]
        state.raw_data = results
        context = "\n\n".join(
        "\n".join([
            f"{key.replace('_', ' ').title()}: {value}"
            for key, value in cheese.items()
            if value is not None
            ]) for cheese in results[0:min(3, len(results))]
        )
        state.history[-1]["observation"]+="\nFound "+str(len(results))+" results.\n This is result context: "+context
    except Exception as e:
        state.history[-1]["observation"]+="\nThis is error: "+str(e)
        state.raw_data = []
    
    return state
@traceable
def txt2pinecone_node(state: GraphState) -> GraphState:
    response = model.invoke(state.messages + [SystemMessage(generate_pinecone_query.format(
        query=state.input_query,
        conversation=format_conversation_history(state.messages)
    ))])
    state.output_query = response.content.strip().replace('``pinecone', '').replace('`', '')
    print(state.output_query)
    state.history[-1]["observation"] = "\nThis is result query: "+state.output_query
    results = []
    try:
        results = vector_db.query(state.query, top_k=3, filter=state.output_query)
        results = [result.model_dump() for result in results]
        # Remove _id field from results
        results = [{k: v for k, v in cheese.items() if k != '_id'} for cheese in results]
        state.raw_data = results
        context = "\n\n".join(
        "\n".join([
            f"{key.replace('_', ' ').title()}: {value}"
            for key, value in cheese.items()
            if value is not None
            ]) for cheese in results[0:min(3, len(results))]
        )
        state.history[-1]["observation"]+="\nFound "+str(len(results))+" results.\n This is result context: "+context
    except Exception as e:
        state.history[-1]["observation"]+="\nThis is error: "+str(e)
        state.raw_data = []
    
    return state
@traceable
def data_retrieval_node(state: GraphState) -> GraphState:
    try:
        results = state.raw_data
        # Convert ObjectId to string and handle other non-serializable types
        def convert_value(value):
            if hasattr(value, 'to_dict'):  # Handle ObjectId
                return str(value)
            elif isinstance(value, dict):
                return {k: convert_value(v) for k, v in value.items() if k != '_id'}
            elif isinstance(value, list):
                return [convert_value(item) for item in value]
            return value
                
        # Convert all results to serializable format and remove _id
        results = [convert_value(result) for result in results]
        
        # Dynamically build context string using only available fields
        context = "\n\n".join(
            "\n".join([
                f"{key.replace('_', ' ').title()}: {value}"
                for key, value in cheese.items()
                if value is not None and key != '_id'
            ]) for cheese in results
        )
        prompt = generate_response.format(
            context=context,
            size=str(len(results)), 
            query=state.query,
            conversation=format_conversation_history(state.messages)
        )
        state.history[-1]["observation"]="I think I have found the information you need. This is done."
        response = model.invoke(state.messages + [HumanMessage(prompt)])
        state.messages.append({"role": "assistant", "content": response.content})

    except Exception as e:
        print(f"Error in data retrieval: {str(e)}")
        state.messages.append({
            "role": "assistant",
            "content": "I apologize, but I encountered an error while retrieving the information. Could you please rephrase your question?"
        })

    return state