import streamlit as st
from PIL import Image
from utils.storage import save_conversation, export_conversation_pdf, export_conversation_markdown
from datetime import datetime

def render_chat_interface():
    """Render the main chat interface"""
    
    # Initialize messages in session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Load conversation if selected from sidebar
    if 'loaded_conversation' in st.session_state:
        st.session_state.messages = st.session_state.loaded_conversation['messages']
        st.success(f"Loaded: {st.session_state.loaded_conversation['title']}")
        del st.session_state.loaded_conversation
    
    # Apply template if selected
    if 'current_template' in st.session_state:
        template_text = st.session_state.current_template
        del st.session_state.current_template
    else:
        template_text = ""
    
    # Chat interface
    col1, col2 = st.columns([3, 1])
    
    with col2:
        # Export options
        if st.session_state.messages:
            st.markdown("### Export Chat")
            
            if st.button("📄 Export PDF"):
                conv_data = {
                    "title": f"Chat - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                    "messages": st.session_state.messages,
                    "created_at": datetime.now().isoformat()
                }
                pdf_bytes = export_conversation_pdf(conv_data)
                st.download_button(
                    "Download PDF",
                    pdf_bytes,
                    "conversation.pdf",
                    "application/pdf"
                )
            
            if st.button("📝 Export Markdown"):
                conv_data = {
                    "title": f"Chat - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                    "messages": st.session_state.messages,
                    "created_at": datetime.now().isoformat()
                }
                md_content = export_conversation_markdown(conv_data)
                st.download_button(
                    "Download Markdown",
                    md_content,
                    "conversation.md",
                    "text/markdown"
                )
            
            # Save conversation
            if st.button("💾 Save Conversation"):
                title = st.text_input("Conversation title:", value=f"Chat - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                if title:
                    conv_type = st.session_state.get('conversation_type', 'general')
                    conv_id = save_conversation(title, st.session_state.messages, conv_type)
                    st.success(f"Saved as conversation #{conv_id}")
    
    with col1:
        # Display chat messages
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f'<div class="user-message">🧑‍💻 <strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bot-message">🤖 <strong>AI:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        
        # Input area
        st.markdown("### 💬 Your Message")
        
        # Multi-modal input
        input_type = st.radio("Input Type:", ["Text", "Text + Image"], horizontal=True)
        
        uploaded_image = None
        if input_type == "Text + Image":
            uploaded_image = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])
            if uploaded_image:
                st.image(uploaded_image, caption="Uploaded Image", width=300)
        
        # Text input with template
        user_input = st.text_area(
            "Type your message:",
            value=template_text,
            height=100,
            key="user_input"
        )
        
        # Send button and follow-up suggestions
        col_send, col_clear = st.columns([1, 1])
        
        with col_send:
            send_button = st.button("🚀 Send Message", type="primary", use_container_width=True)
        
        with col_clear:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        
        # Process message
        if send_button and user_input.strip():
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get AI response
            gemini_client = st.session_state.gemini_client
            conversation_type = st.session_state.get('conversation_type', 'general')
            temperature = st.session_state.get('temperature', 0.7)
            
            with st.spinner("🤔 AI is thinking..."):
                if uploaded_image:
                    # Handle image + text
                    image = Image.open(uploaded_image)
                    response = gemini_client.analyze_image(image, user_input)
                else:
                    # Handle text only
                    context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-5:]])
                    response = gemini_client.get_smart_response(user_input, context, conversation_type)
            
            # Add AI response
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.rerun()
        
        # Follow-up suggestions
        if st.session_state.messages and len(st.session_state.messages) >= 2:
            st.markdown("### 💡 Suggested Follow-ups")
            
            # Get conversation context for suggestions
            conversation_history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-4:]])
            
            try:
                suggestions = st.session_state.gemini_client.suggest_followup(conversation_history)
                
                cols = st.columns(len(suggestions))
                for i, suggestion in enumerate(suggestions):
                    with cols[i]:
                        if st.button(f"💭 {suggestion[:50]}...", key=f"suggestion_{i}"):
                            st.session_state.messages.append({"role": "user", "content": suggestion})
                            
                            # Get AI response for suggestion
                            with st.spinner("🤔 AI is thinking..."):
                                context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-5:]])
                                response = st.session_state.gemini_client.get_smart_response(
                                    suggestion, context, st.session_state.get('conversation_type', 'general')
                                )
                            
                            st.session_state.messages.append({"role": "assistant", "content": response})
                            st.rerun()
            except:
                pass  # Skip suggestions if there's an error