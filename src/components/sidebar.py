import streamlit as st
from utils.storage import get_conversations, search_conversations, delete_conversation

def render_sidebar():
    """Render the sidebar with navigation and conversation history"""
    
    with st.sidebar:
        st.markdown("## 🚀 AIConverse")
        
        # Navigation
        st.markdown("### Navigation")
        if st.button("💬 Chat", use_container_width=True):
            st.session_state.current_page = 'Chat'
            st.rerun()
        
        if st.button("📊 Analytics", use_container_width=True):
            st.session_state.current_page = 'Analytics'
            st.rerun()
        
        st.divider()
        
        # Conversation Type Selector
        st.markdown("### Conversation Style")
        conversation_types = {
            "general": "💬 General Chat",
            "creative": "🎨 Creative Writing",
            "technical": "🔧 Technical Help",
            "educational": "📚 Learning Mode",
            "casual": "😊 Casual Talk"
        }
        
        selected_type = st.selectbox(
            "Choose conversation style:",
            options=list(conversation_types.keys()),
            format_func=lambda x: conversation_types[x],
            key="conversation_type"
        )
        
        st.divider()
        
        # Quick Templates
        st.markdown("### Quick Templates")
        templates = {
            "Explain like I'm 5": "Explain this concept in simple terms that a 5-year-old would understand:",
            "Code Review": "Please review this code and suggest improvements:",
            "Creative Story": "Write a creative story about:",
            "Research Help": "Help me research information about:",
            "Problem Solving": "Help me solve this problem step by step:"
        }
        
        selected_template = st.selectbox(
            "Choose a template:",
            options=["None"] + list(templates.keys()),
            key="selected_template"
        )
        
        if selected_template != "None":
            if st.button("Apply Template", use_container_width=True):
                st.session_state.current_template = templates[selected_template]
                st.rerun()
        
        st.divider()
        
        # Conversation History
        st.markdown("### Conversation History")
        
        # Search conversations
        search_query = st.text_input("🔍 Search conversations", key="search_conversations")
        
        if search_query:
            conversations = search_conversations(search_query)
        else:
            conversations = get_conversations()
        
        # Display conversations
        if conversations:
            conversations = sorted(conversations, key=lambda x: x["created_at"], reverse=True)
            
            for conv in conversations[:10]:  # Show last 10 conversations
                with st.expander(f"💬 {conv['title'][:30]}...", expanded=False):
                    st.write(f"📅 {conv['created_at'][:10]}")
                    st.write(f"💬 {conv['message_count']} messages")
                    st.write(f"🏷️ {conv.get('type', 'general').title()}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Load", key=f"load_{conv['id']}"):
                            st.session_state.loaded_conversation = conv
                            st.rerun()
                    
                    with col2:
                        if st.button("Delete", key=f"delete_{conv['id']}"):
                            delete_conversation(conv['id'])
                            st.rerun()
        else:
            st.write("No conversations found")
        
        st.divider()
        
        # Settings
        st.markdown("### Settings")
        
        # Theme toggle
        if 'theme' not in st.session_state:
            st.session_state.theme = 'dark'
        
        theme = st.radio("Theme:", ["dark", "light"], key="theme_selector")
        
        # Temperature control
        temperature = st.slider("AI Creativity", 0.1, 1.0, 0.7, 0.1, key="temperature")
        # st.session_state.temperature = temperature
        
        # New conversation button
        if st.button("🆕 New Conversation", use_container_width=True, type="primary"):
            # Clear current conversation
            for key in ['messages', 'loaded_conversation', 'current_template']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()