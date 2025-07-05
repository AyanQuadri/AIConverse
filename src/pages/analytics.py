import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from utils.storage import get_conversation_stats, get_conversations

def render_analytics():
    """Render the analytics dashboard"""
    
    st.markdown('<h1 class="main-header">📊 Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Get analytics data
    stats = get_conversation_stats()
    conversations = get_conversations()
    
    if not conversations:
        st.info("No conversations yet. Start chatting to see analytics!")
        return
    
    # Overview metrics
    st.markdown("### 📈 Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Conversations", stats["total_conversations"])
    
    with col2:
        st.metric("Total Messages", stats["total_messages"])
    
    with col3:
        st.metric("Avg Messages/Chat", stats["avg_messages_per_conversation"])
    
    with col4:
        st.metric("Recent Activity (7 days)", stats["recent_activity"])
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Conversation types distribution
        st.markdown("### 🏷️ Conversation Types")
        
        if stats["type_distribution"]:
            type_df = pd.DataFrame(
                list(stats["type_distribution"].items()),
                columns=["Type", "Count"]
            )
            
            fig_pie = px.pie(
                type_df, 
                values="Count", 
                names="Type",
                title="Distribution by Conversation Type",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Messages per conversation
        st.markdown("### 💬 Messages per Conversation")
        
        message_counts = [conv["message_count"] for conv in conversations]
        
        fig_hist = px.histogram(
            x=message_counts,
            nbins=10,
            title="Distribution of Messages per Conversation",
            labels={"x": "Messages", "y": "Conversations"},
            color_discrete_sequence=["#667eea"]
        )
        fig_hist.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    # Activity timeline
    st.markdown("### 📅 Activity Timeline")
    
    # Prepare data for timeline
    timeline_data = []
    for conv in conversations:
        date = datetime.fromisoformat(conv["created_at"]).date()
        timeline_data.append({
            "date": date,
            "conversations": 1,
            "messages": conv["message_count"]
        })
    
    if timeline_data:
        timeline_df = pd.DataFrame(timeline_data)
        timeline_df = timeline_df.groupby("date").agg({
            "conversations": "sum",
            "messages": "sum"
        }).reset_index()
        
        # Create dual-axis chart
        fig_timeline = go.Figure()
        
        # Add conversations line
        fig_timeline.add_trace(
            go.Scatter(
                x=timeline_df["date"],
                y=timeline_df["conversations"],
                mode='lines+markers',
                name='Conversations',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            )
        )
        
        # Add messages bar (secondary y-axis)
        fig_timeline.add_trace(
            go.Bar(
                x=timeline_df["date"],
                y=timeline_df["messages"],
                name='Messages',
                yaxis='y2',
                opacity=0.7,
                marker_color='#764ba2'
            )
        )
        
        # Update layout for dual axis
        fig_timeline.update_layout(
            title="Daily Activity Timeline",
            xaxis_title="Date",
            yaxis=dict(title="Conversations", side="left"),
            yaxis2=dict(title="Messages", side="right", overlaying="y"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(x=0, y=1)
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    st.divider()
    
    # Detailed conversation list
    st.markdown("### 📋 Recent Conversations")
    
    # Sort conversations by date
    recent_conversations = sorted(conversations, key=lambda x: x["created_at"], reverse=True)[:10]
    
    # Create detailed table
    table_data = []
    for conv in recent_conversations:
        created_date = datetime.fromisoformat(conv["created_at"])
        table_data.append({
            "Title": conv["title"][:40] + "..." if len(conv["title"]) > 40 else conv["title"],
            "Type": conv.get("type", "general").title(),
            "Messages": conv["message_count"],
            "Created": created_date.strftime("%Y-%m-%d %H:%M"),
            "Days Ago": (datetime.now() - created_date).days
        })
    
    if table_data:
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Usage insights
    st.markdown("### 💡 Usage Insights")
    
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        st.markdown("#### 🎯 Top Insights")
        
        # Calculate insights
        total_days = (datetime.now() - datetime.fromisoformat(conversations[0]["created_at"])).days + 1 if conversations else 1
        avg_conversations_per_day = round(len(conversations) / total_days, 2)
        
        most_active_type = max(stats["type_distribution"], key=stats["type_distribution"].get) if stats["type_distribution"] else "general"
        
        longest_conversation = max(conversations, key=lambda x: x["message_count"]) if conversations else None
        
        st.write(f"📊 **Average conversations per day:** {avg_conversations_per_day}")
        st.write(f"🏆 **Most used conversation type:** {most_active_type.title()}")
        if longest_conversation:
            st.write(f"💬 **Longest conversation:** {longest_conversation['message_count']} messages")
        st.write(f"🔥 **Recent activity:** {stats['recent_activity']} conversations this week")
    
    with insights_col2:
        st.markdown("#### 📈 Trends")
        
        if len(conversations) >= 2:
            # Calculate growth
            recent_week = [c for c in conversations if (datetime.now() - datetime.fromisoformat(c["created_at"])).days <= 7]
            previous_week = [c for c in conversations if 7 < (datetime.now() - datetime.fromisoformat(c["created_at"])).days <= 14]
            
            growth = len(recent_week) - len(previous_week)
            growth_text = "📈 Increasing" if growth > 0 else "📉 Decreasing" if growth < 0 else "➡️ Stable"
            
            st.write(f"**Weekly trend:** {growth_text}")
            st.write(f"**Change:** {'+' if growth > 0 else ''}{growth} conversations")
            
            # Message complexity trend
            recent_avg_messages = sum(c["message_count"] for c in recent_week) / max(len(recent_week), 1)
            overall_avg = stats["avg_messages_per_conversation"]
            
            complexity_trend = "🔥 More engaging" if recent_avg_messages > overall_avg else "⚡ More concise"
            st.write(f"**Conversation style:** {complexity_trend}")
            st.write(f"**Recent avg messages:** {round(recent_avg_messages, 1)}")
        else:
            st.write("Need more conversations to show trends!")
    
    # Export analytics
    st.divider()
    st.markdown("### 📊 Export Analytics")
    
    if st.button("📄 Generate Analytics Report"):
        # Create comprehensive report
        report_data = {
            "generated_at": datetime.now().isoformat(),
            "summary": stats,
            "conversations": conversations,
            "insights": {
                "avg_conversations_per_day": avg_conversations_per_day,
                "most_active_type": most_active_type,
                "total_days_active": total_days
            }
        }
        
        import json
        report_json = json.dumps(report_data, indent=2, default=str)
        
        st.download_button(
            "📊 Download Analytics Report (JSON)",
            report_json,
            f"aiconverse_analytics_{datetime.now().strftime('%Y%m%d')}.json",
            "application/json"
        )