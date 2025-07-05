import streamlit as st
import os
from dotenv import load_dotenv
from components.sidebar import render_sidebar
from components.chat import render_chat_interface
from pages.analytics import render_analytics
from utils.storage import init_storage, get_conversations
from utils.gemini_client import GeminiClient

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AIConverse",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-container {
        font-family: 'Inter', sans-serif;
        border-radius: 10px;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
    }
    
    .bot-message {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 20px;
        color: white;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize storage
    init_storage()
    
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Chat'
    if 'gemini_client' not in st.session_state:
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key and api_key != 'your_gemini_api_key_here':
            st.session_state.gemini_client = GeminiClient(api_key)
        else:
            st.session_state.gemini_client = None
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    if st.session_state.gemini_client is None:
        st.error("🔑 Please configure your Google API key in the .env file")
        st.code("GOOGLE_API_KEY=your_api_key_here")
        return
    
    # Page routing
    if st.session_state.current_page == 'Chat':
        st.markdown('<h1 class="main-header">AIConverse</h1>', unsafe_allow_html=True)
        render_chat_interface()
    elif st.session_state.current_page == 'Analytics':
        render_analytics()

if __name__ == "__main__":
    main()