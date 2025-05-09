import streamlit as st
import pandas as pd
from app.services.upload import upload_service
from app.services.chat import chat_service

# Set page config with theme support
st.set_page_config(
    page_title="Cheese Ordering Assistant",
    page_icon="🧀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add theme toggle in sidebar
with st.sidebar:
    st.header("Settings")
    st.header("Data Upload")
    uploaded_file = st.file_uploader("Upload data file", type=['csv', 'json'])
    if uploaded_file is not None:
        try:
            with st.spinner('Processing file...'):
                if uploaded_file.name.endswith('.csv'):
                    upload_service.process_csv(uploaded_file)
                elif uploaded_file.name.endswith('.json'):
                    upload_service.process_json(uploaded_file)
            st.success('File successfully processed and stored in databases!')
        except Exception as e:
            st.error(f'Error processing file: {str(e)}')

st.title("💬 Cheese Ordering Assistant")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

# Chat interface
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello, I am here to help you order any cheese, please tell me what you want to order this time!  "}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    
    # Show thinking indicator
    with st.spinner("Thinking..."):
        result = chat_service.process_message(prompt, st.session_state.messages)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": result["response"]})
    st.chat_message("assistant").write(result["response"])
