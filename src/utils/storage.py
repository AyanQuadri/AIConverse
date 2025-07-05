import json
import os
from datetime import datetime
import streamlit as st
from fpdf import FPDF
# import markdown # type: ignore

DATA_DIR = "data"
CONVERSATIONS_FILE = os.path.join(DATA_DIR, "conversations.json")

def init_storage():
    """Initialize storage directory and files"""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CONVERSATIONS_FILE):
        with open(CONVERSATIONS_FILE, 'w') as f:
            json.dump([], f)

def save_conversation(title, messages, conversation_type="general"):
    """Save a conversation to storage"""
    conversations = get_conversations()
    
    new_conversation = {
        "id": len(conversations) + 1,
        "title": title,
        "messages": messages,
        "type": conversation_type,
        "created_at": datetime.now().isoformat(),
        "message_count": len(messages)
    }
    
    conversations.append(new_conversation)
    
    with open(CONVERSATIONS_FILE, 'w') as f:
        json.dump(conversations, f, indent=2)
    
    return new_conversation["id"]

def get_conversations():
    """Retrieve all conversations"""
    try:
        with open(CONVERSATIONS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def search_conversations(query):
    """Search conversations by content"""
    conversations = get_conversations()
    results = []
    
    for conv in conversations:
        # Search in title
        if query.lower() in conv["title"].lower():
            results.append(conv)
            continue
        
        # Search in messages
        for msg in conv["messages"]:
            if query.lower() in msg["content"].lower():
                results.append(conv)
                break
    
    return results

def delete_conversation(conv_id):
    """Delete a conversation"""
    conversations = get_conversations()
    conversations = [c for c in conversations if c["id"] != conv_id]
    
    with open(CONVERSATIONS_FILE, 'w') as f:
        json.dump(conversations, f, indent=2)

def export_conversation_pdf(conversation):
    """Export conversation as PDF"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt=conversation["title"], ln=True, align="C")
    pdf.ln(10)
    
    # Messages
    pdf.set_font("Arial", size=10)
    for msg in conversation["messages"]:
        role = "You" if msg["role"] == "user" else "AI"
        pdf.set_font("Arial", style="B", size=10)
        pdf.cell(200, 10, txt=f"{role}:", ln=True)
        pdf.set_font("Arial", size=10)
        
        # Split long text
        content = msg["content"]
        for i in range(0, len(content), 80):
            pdf.cell(200, 5, txt=content[i:i+80], ln=True)
        pdf.ln(5)
    
    # return pdf.output(dest='S').encode('latin-1')
    return bytes(pdf.output(dest='S'))  # ✅ convert to proper binary format

def export_conversation_markdown(conversation):
    """Export conversation as Markdown"""
    md_content = f"# {conversation['title']}\n\n"
    md_content += f"**Created:** {conversation['created_at']}\n\n"
    
    for msg in conversation["messages"]:
        role = "**You**" if msg["role"] == "user" else "**AI Assistant**"
        md_content += f"{role}: {msg['content']}\n\n"
    
    return md_content

def get_conversation_stats():
    """Get analytics data for conversations"""
    conversations = get_conversations()
    
    total_conversations = len(conversations)
    total_messages = sum(conv["message_count"] for conv in conversations)
    
    # Conversations by type
    type_counts = {}
    for conv in conversations:
        conv_type = conv.get("type", "general")
        type_counts[conv_type] = type_counts.get(conv_type, 0) + 1
    
    # Recent activity (last 7 days)
    recent_count = 0
    week_ago = datetime.now().timestamp() - (7 * 24 * 60 * 60)
    
    for conv in conversations:
        conv_time = datetime.fromisoformat(conv["created_at"]).timestamp()
        if conv_time > week_ago:
            recent_count += 1
    
    return {
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "type_distribution": type_counts,
        "recent_activity": recent_count,
        "avg_messages_per_conversation": round(total_messages / max(total_conversations, 1), 1)
    }