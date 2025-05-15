from app.services.chat_service import chat_service

    # Get the graph and ensure it's properly formatted
from IPython.display import Image, display
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles

app = chat_service._build_data_retrieval_graph()
display(Image(app.get_graph().draw_mermaid_png()))