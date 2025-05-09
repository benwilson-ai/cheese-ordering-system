import streamlit as st
import pandas as pd
import streamlit as st
import logging
from PIL import Image, ImageEnhance
import time
import json
import requests
import base64
from app.services.upload_service import upload_service
from app.services.chat_service import chat_service
# Set page config with theme support
st.set_page_config(
    page_title="Cheese Ordering Assistant",
    page_icon="🧀",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "Get help": "https://github.com/AdieLaine/Streamly",
        "Report a bug": "https://github.com/AdieLaine/Streamly",
        "About": """
            ## Streamly Streamlit Assistant
            ### Powered using GPT-4o-mini

            **GitHub**: https://github.com/AdieLaine/

            The AI Assistant named, Streamly, aims to provide the latest updates from Streamlit,
            generate code snippets for Streamlit widgets,
            and answer questions about Streamlit's latest features, issues, and more.
            Streamly has been trained on the latest Streamlit updates and documentation.
        """
    }
)
def img_to_base64(image_path):
    """Convert image to base64."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        logging.error(f"Error converting image to base64: {str(e)}")
        return None
    
@st.cache_data(show_spinner=False)
def long_running_task(duration):
    """
    Simulates a long-running operation.

    Parameters:
    - duration: int, duration of the task in seconds

    Returns:
    - str: Completion message
    """
    time.sleep(duration)
    return "Long-running operation completed."

@st.cache_data(show_spinner=False)
def load_and_enhance_image(image_path, enhance=False):
    """
    Load and optionally enhance an image.

    Parameters:
    - image_path: str, path of the image
    - enhance: bool, whether to enhance the image or not

    Returns:
    - img: PIL.Image.Image, (enhanced) image
    """
    img = Image.open(image_path)
    if enhance:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.8)
    return img

@st.cache_data(show_spinner=False)
def load_streamlit_updates():
    """Load the latest Streamlit updates from a local JSON file."""
    try:
        with open("data/streamlit_updates.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading JSON: {str(e)}")
        return {}

def get_streamlit_api_code_version():
    """
    Get the current Streamlit API code version from the Streamlit API documentation.

    Returns:
    - str: The current Streamlit API code version.
    """
    try:
        response = requests.get(API_DOCS_URL)
        if response.status_code == 200:
            return "1.36"
    except requests.exceptions.RequestException as e:
        logging.error(f"Error connecting to the Streamlit API documentation: {str(e)}")
    return None

def display_streamlit_updates():
    """Display the latest updates of the Streamlit."""
    with st.expander("Streamlit 1.36 Announcement", expanded=False):
        st.markdown("For more details on this version, check out the [Streamlit Forum post](https://docs.streamlit.io/library/changelog#version).")

def initialize_conversation():
    """
    Initialize the conversation history with system and assistant messages.

    Returns:
    - list: Initialized conversation history.
    """
    assistant_message = "Hello! I am Streamly. How can I assist you with Streamlit today?"

    conversation_history = [
        {"role": "system", "content": "You are Streamly, a specialized AI assistant trained in Streamlit."},
        {"role": "system", "content": "Streamly, is powered by the OpenAI GPT-4o-mini model, released on July 18, 2024."},
        {"role": "system", "content": "You are trained up to Streamlit Version 1.36.0, release on June 20, 2024."},
        {"role": "system", "content": "Refer to conversation history to provide context to your response."},
        {"role": "system", "content": "You were created by Madie Laine, an OpenAI Researcher."},
        {"role": "assistant", "content": assistant_message}
    ]
    return conversation_history

@st.cache_data(show_spinner=False)
def get_latest_update_from_json(keyword, latest_updates):
    """
    Fetch the latest Streamlit update based on a keyword.

    Parameters:
    - keyword (str): The keyword to search for in the Streamlit updates.
    - latest_updates (dict): The latest Streamlit updates data.

    Returns:
    - str: The latest update related to the keyword, or a message if no update is found.
    """
    for section in ["Highlights", "Notable Changes", "Other Changes"]:
        for sub_key, sub_value in latest_updates.get(section, {}).items():
            for key, value in sub_value.items():
                if keyword.lower() in key.lower() or keyword.lower() in value.lower():
                    return f"Section: {section}\nSub-Category: {sub_key}\n{key}: {value}"
    return "No updates found for the specified keyword."

def construct_formatted_message(latest_updates):
    """
    Construct formatted message for the latest updates.

    Parameters:
    - latest_updates (dict): The latest Streamlit updates data.

    Returns:
    - str: Formatted update messages.
    """
    formatted_message = []
    highlights = latest_updates.get("Highlights", {})
    version_info = highlights.get("Version 1.36", {})
    if version_info:
        description = version_info.get("Description", "No description available.")
        formatted_message.append(f"- **Version 1.36**: {description}")

    for category, updates in latest_updates.items():
        formatted_message.append(f"**{category}**:")
        for sub_key, sub_values in updates.items():
            if sub_key != "Version 1.36":  # Skip the version info as it's already included
                description = sub_values.get("Description", "No description available.")
                documentation = sub_values.get("Documentation", "No documentation available.")
                formatted_message.append(f"- **{sub_key}**: {description}")
                formatted_message.append(f"  - **Documentation**: {documentation}")
    return "\n".join(formatted_message)

@st.cache_data(show_spinner=False)
def on_chat_submit(chat_input, latest_updates):
    """
    Handle chat input submissions and interact with the OpenAI API.

    Parameters:
    - chat_input (str): The chat input from the user.
    - latest_updates (dict): The latest Streamlit updates fetched from a JSON file or API.

    Returns:
    - None: Updates the chat history in Streamlit's session state.
    """
    user_input = chat_input.strip().lower()

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = initialize_conversation()

    st.session_state.conversation_history.append({"role": "user", "content": user_input})

    try:
        model_engine = "gpt-4o-mini"
        assistant_reply = ""

        if "latest updates" in user_input:
            assistant_reply = "Here are the latest highlights from Streamlit:\n"
            highlights = latest_updates.get("Highlights", {})
            if highlights:
                for version, info in highlights.items():
                    description = info.get("Description", "No description available.")
                    assistant_reply += f"- **{version}**: {description}\n"
            else:
                assistant_reply = "No highlights found."
        else:
            response = client.chat.completions.create(
                model=model_engine,
                messages=st.session_state.conversation_history
            )
            assistant_reply = response.choices[0].message.content

        st.session_state.conversation_history.append({"role": "assistant", "content": assistant_reply})
        st.session_state.history.append({"role": "user", "content": user_input})
        st.session_state.history.append({"role": "assistant", "content": assistant_reply})

    except OpenAIError as e:
        logging.error(f"Error occurred: {e}")
        st.error(f"OpenAI Error: {str(e)}")

def initialize_session_state():
    """Initialize session state variables."""
    if "history" not in st.session_state:
        st.session_state.history = []
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

def main():
    """
    Display Streamlit updates and handle the chat interface.
    """
    initialize_session_state()

    if not st.session_state.history:
        initial_bot_message = "Hello! How can I assist you with Streamlit today?"
        st.session_state.history.append({"role": "assistant", "content": initial_bot_message})
        st.session_state.conversation_history = initialize_conversation()

    # Insert custom CSS for glowing effect
    st.markdown(
        """
        <style>
        .cover-glow {
            width: 100%;
            height: auto;
            padding: 3px;
            box-shadow: 
                0 0 5px #330000,
                0 0 10px #660000,
                0 0 15px #990000,
                0 0 20px #CC0000,
                0 0 25px #FF0000,
                0 0 30px #FF3333,
                0 0 35px #FF6666;
            position: relative;
            z-index: -1;
            border-radius: 45px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Load and display sidebar image
    img_path = "imgs/sidebar_streamly_avatar.png"
    img_base64 = img_to_base64(img_path)
    if img_base64:
        st.sidebar.markdown(
            f'<img src="data:image/png;base64,{img_base64}" class="cover-glow">',
            unsafe_allow_html=True,
        )

    st.sidebar.markdown("---")

    # Sidebar for Mode Selection
    mode = st.sidebar.radio("Select Mode:", options=["Latest Updates", "Chat with Streamly"], index=1)

    st.sidebar.markdown("---")

    # Display basic interactions
    show_basic_info = st.sidebar.checkbox("Show Basic Interactions", value=True)
    if show_basic_info:
        st.sidebar.markdown("""
        ### Basic Interactions
        - **Ask About Streamlit**: Type your questions about Streamlit's latest updates, features, or issues.
        - **Search for Code**: Use keywords like 'code example', 'syntax', or 'how-to' to get relevant code snippets.
        - **Navigate Updates**: Switch to 'Updates' mode to browse the latest Streamlit updates in detail.
        """)

    # Display advanced interactions
    show_advanced_info = st.sidebar.checkbox("Show Advanced Interactions", value=False)
    if show_advanced_info:
        st.sidebar.markdown("""
        ### Advanced Interactions
        - **Generate an App**: Use keywords like **generate app**, **create app** to get a basic Streamlit app code.
        - **Code Explanation**: Ask for **code explanation**, **walk me through the code** to understand the underlying logic of Streamlit code snippets.
        - **Project Analysis**: Use **analyze my project**, **technical feedback** to get insights and recommendations on your current Streamlit project.
        - **Debug Assistance**: Use **debug this**, **fix this error** to get help with troubleshooting issues in your Streamlit app.
        """)

    st.sidebar.markdown("---")

    # Load and display image with glowing effect
    img_path = "imgs/stsidebarimg.png"
    img_base64 = img_to_base64(img_path)
    if img_base64:
        st.sidebar.markdown(
            f'<img src="data:image/png;base64,{img_base64}" class="cover-glow">',
            unsafe_allow_html=True,
        )
    else:
        display_streamlit_updates()


# Add theme toggle in sidebar
with st.sidebar:
    st.header("Settings")
    st.header("DB Update")
    
    # Initialize button state in session state if not exists
    if 'is_auto_updating' not in st.session_state:
        st.session_state.is_auto_updating = False
        
    # Create custom CSS to center-align the buttons and add padding
    st.markdown("""
        <style>
        div[data-testid="stFileUploader"] {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
        }
        div[data-testid="stFileUploader"] > div {
            display: flex;
            justify-content: center;
        }
        button[data-testid="baseButton-secondary"] {
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Create a container for file uploader and button
    upload_container = st.container()
    with upload_container:
        uploaded_file = st.file_uploader("Update DB using file", type=['csv', 'json'])
        
        # Toggle button label based on state
        button_label = "Auto update DB" if st.session_state.is_auto_updating else "Auto update DB"
        auto_btn = st.button(button_label, key="auto_update_btn", use_container_width=True)
        
        if auto_btn:
            st.session_state.is_auto_updating = not st.session_state.is_auto_updating
            
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
            
    if st.session_state.is_auto_updating:
        try:
            with st.spinner('Scraping data...'):
                upload_service.process_auto_update()
            st.success('Scraping successfully processed and stored in databases!')
        except Exception as e:
            st.error(f'Error processing file: {str(e)}')
            st.session_state.is_auto_updating = False

st.title("🧀 Cheese Ordering Assistant")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

# Chat interface
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "user", "content": "Hi, my AI friend!💬"},
        {"role": "assistant", "content": "Hi, Cheese Lover, I am here to help you about our 🧀, please tell me what you want this time!💬"}
    ]

for msg in st.session_state.messages:
    
    if msg["role"] == "assistant": 
        avatar="imgs/avatar_streamly.png"     
    elif  msg["role"] == "user": 
        avatar="imgs/stuser.png"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(f'<div style="padding: 1em; border-radius: 1em; background: #23272f; color: #fff; margin-bottom: 0.5em;">{msg["content"]}</div>', unsafe_allow_html=True)

if prompt := st.chat_input():
    with st.chat_message("user", avatar="imgs/stuser.png"):
        st.markdown(f'<div style="padding: 1em; border-radius: 1em; background: #2d3748; color: #fff; margin-bottom: 0.5em;">{prompt}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Show thinking indicator
    with st.spinner("Thinking..."):
        result = chat_service.process_message(prompt, st.session_state.messages)
    
    st.session_state.messages.append({"role": "assistant", "content": result["response"]})
    with st.chat_message("assistant", avatar="imgs/avatar_streamly.png"):
        # st.markdown(f'<div style="padding: 1em; border-radius: 1em; background: #23272f; color: #fff; margin-bottom: 0.5em;">{result["context"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="padding: 1em; border-radius: 1em; background: #23272f; color: #fff; margin-bottom: 0.5em;">{result["response"]}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()    