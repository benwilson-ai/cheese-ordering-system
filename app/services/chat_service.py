from typing import List, Dict
from langgraph.graph import StateGraph, START
from langchain_openai import ChatOpenAI
from app.core.config import settings, ModelType
from app.services.graph.graph_state import GraphState, DatabaseEnum, AvailableEnum
from app.services.graph.graph_nodes import (
    determine_about_cheese,
    determine_database,
    query_transformation_node,
    txt2mongo_node,
    data_retrieval_node,
)

class ChatService:
    def __init__(self):
        self.data_retrieval_graph = self._build_data_retrieval_graph()
        self.model = ChatOpenAI(
            model=ModelType.gpt4o,
            openai_api_key=settings.OPENAI_API_KEY
        )

    def _build_data_retrieval_graph(self):
        workflow = StateGraph(state_schema=GraphState)
        
        # Add nodes
        workflow.add_node("txt2mongo", txt2mongo_node)
        workflow.add_node("data_retrieval", data_retrieval_node)
        workflow.add_node("query_transformation", query_transformation_node)
        # Add conditional edges
        workflow.add_conditional_edges(
            START,
            determine_about_cheese,
            {
                AvailableEnum.AVAILABLE: "query_transformation",
                AvailableEnum.NOT_AVAILABLE: "data_retrieval"
            }
        )
        workflow.add_conditional_edges(
            "query_transformation",
            determine_database,
            {
                DatabaseEnum.MONGO: "txt2mongo",
                DatabaseEnum.VECTORDB: "data_retrieval"
            }
        )

        # Add edges
        workflow.add_edge("txt2mongo", "data_retrieval")
        workflow.set_finish_point("data_retrieval")
        
        return workflow.compile()

    def process_message(self, query: str, conversation_history: List[Dict[str, str]]) -> str:
        messages = conversation_history + [{"role": "user", "content": query}]
        initial_state = GraphState(messages=messages, query=query)
        
        final_state = self.data_retrieval_graph.invoke(initial_state)
        print(final_state)
        # Check if visualization is needed
        # if "compare" in query.lower() or "chart" in query.lower():
        return {"response": final_state["messages"][-1]["content"], "context": final_state['raw_data']}
        # return {"response": final_state["messages"][-1]["content"]}

chat_service = ChatService()