from typing import List, Dict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver
import uuid
from app.core.config import settings, ModelType
from app.services.graph.graph_state import GraphState
from app.services.graph.graph_nodes import (
    # decide_selected,
    txt2mongo_node,
    data_retrieval_node,
    reasoner_node,
    ambiguit_resolver_node,
    txt2pinecone_node,
)

class ChatService:
    def __init__(self):
        self.data_retrieval_graph = self._build_data_retrieval_graph()
        self.model = ChatOpenAI(
            model=ModelType.gpt4o,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.config = {"configurable": {"thread_id": uuid.uuid4(), 'checkpoint_ns': 'chat', 'checkpoint_id': uuid.uuid4()}}
    def _build_data_retrieval_graph(self):
        workflow = StateGraph(state_schema=GraphState)
        
        # Add nodes
        workflow.add_node("reasoner", reasoner_node)
        workflow.add_node("ambiguit_resolver", ambiguit_resolver_node)
        workflow.add_node("txt2mongo", txt2mongo_node)
        workflow.add_node("txt2pinecone", txt2pinecone_node)
        workflow.add_node("data_retrieval", data_retrieval_node)
        # Add edges
        workflow.add_edge(START, "reasoner")
        workflow.add_edge("ambiguit_resolver", "reasoner")
        workflow.add_edge("txt2mongo", "reasoner")
        workflow.add_edge("txt2pinecone", "reasoner")
        workflow.add_edge("data_retrieval", END)
        workflow.add_conditional_edges(
            "reasoner",
            lambda state: state.selected,
            {
                "txt2mongo": "txt2mongo",
                "txt2pinecone": "txt2pinecone",
                "data_retrieval": "data_retrieval",
                "ambiguit_resolver": "ambiguit_resolver",
            }
        )
        
        checkpointer = MemorySaver()

        app = workflow.compile(checkpointer=checkpointer)
        mermaid_code = app.get_graph().draw_mermaid()
        print(mermaid_code)
        
        return app

    def process_message(self, query: str, conversation_history: List[Dict[str, str]]) -> str:
        
        messages = conversation_history + [{"role": "user", "content": query}]
        initial_state = GraphState(messages=messages, query=query)
        
        flag= ""

        if(flag!=""):
            final_state = self.data_retrieval_graph.invoke(Command(resume={"edited_query": query}), config=self.config)
            flag= final_state.get("__interrupt__", "")
            return {"response": final_state["messages"][-1]["content"], "reason": final_state["history"]}
        else:
            final_state = self.data_retrieval_graph.invoke(initial_state, config=self.config)
            flag= final_state.get("__interrupt__", "")
            if(flag!=""):
                return {"response": flag[0].value["question"], "reason": final_state["history"]}
            else:
                return {"response": final_state["messages"][-1]["content"], "reason": final_state["history"]}
        # return {"response": final_state["messages"][-1]["content"], "context": final_state['raw_data']}
        

chat_service = ChatService()
