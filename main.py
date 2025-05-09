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
    theme = st.radio("Choose theme", ["Light", "Dark"], index=0)
    if theme == "Dark":
        st.markdown("""
            <style>
                .stApp {
                    background-color: #262730;
                    color: #FAFAFA;
                }
                .stChatMessage {
                    background-color: #2E2E3E;
                    color: #FAFAFA;
                }
                .stMarkdown {
                    background-color: #2E2E3E;
                    color: #FAFAFA;
                }
                .stSidebar {
                    background-color: #2E2E3E;
                    color: #FAFAFA;
                }
                .stSidebarContent {
                    background-color: #2E2E3E;
                    color: #FAFAFA;
                }
                .stAppHeader {
                    background-color: #2E2E3E;
                    color: #FAFAFA;
                }
                .stBottomBlockContainer {
                    background-color: #2E2E3E;
                    color: #FAFAFA;
                }
                /* Additional dark theme styles */
                .stTextInput input {
                    background-color: #2E2E3E;
                    color: #FAFAFA;
                    border: 1px solid #4A4A4A;
                }
                .stTextArea textarea {
                    background-color: #2E2E3E;
                    color: #FAFAFA;
                    border: 1px solid #4A4A4A;
                }
                .stButton button {
                    background-color: #2E2E3E;
                    color: #FAFAFA;
                    border: 1px solid #4A4A4A;
                }
                .stFileUploader {
                    background-color: #2E2E3E;
                    color: #FAFAFA;
                }
                .stRadio > div {
                    background-color: #2E2E3E;
                    color: #FAFAFA;
                }
                .stSelectbox > div {
                    background-color: #2E2E3E;
                    color: #FAFAFA;
                }
                .stMultiSelect > div {
                    background-color: #2E2E3E;
                    color: #FAFAFA;
                }
                .stCheckbox > div {
                    background-color: #2E2E3E;
                    color: #FAFAFA;
                }
                .stSlider > div {
                    background-color: #2E2E3E;
                    color: #FAFAFA;
                }
                .stProgress > div {
                    background-color: #2E2E3E;
                }
                .stProgress > div > div {
                    background-color: #4A4A4A;
                }
                .stProgress > div > div > div {
                    background-color: #6B6B6B;
                }
                /* Hover and focus states */
                .stButton button:hover {
                    background-color: #3E3E4E;
                    border-color: #6B6B6B;
                }
                .stTextInput input:hover,
                .stTextArea textarea:hover {
                    border-color: #6B6B6B;
                }
                .stTextInput input:focus,
                .stTextArea textarea:focus {
                    border-color: #6B6B6B;
                    box-shadow: 0 0 0 1px #6B6B6B;
                }
                /* Scrollbar styling */
                ::-webkit-scrollbar {
                    background-color: #2E2E3E;
                    width: 8px;
                }
                ::-webkit-scrollbar-thumb {
                    background-color: #4A4A4A;
                    border-radius: 4px;
                }
                ::-webkit-scrollbar-thumb:hover {
                    background-color: #6B6B6B;
                }
            </style>
        """, unsafe_allow_html=True)
    
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
    
    st.session_state.messages.append({"role": "assistant", "content": result["response"]})
    st.chat_message("assistant").write(result["response"])
