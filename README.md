# 🤖 AIConverse

**AIConverse** is an intelligent AI conversation platform. Built with Streamlit and Google's Gemini AI, it offers multi-modal conversations, persistent memory, analytics, and export capabilities.

## ✨ Features

### 🚀 Core Features
- **Multi-Modal Conversations**: Chat with text and images
- **Smart Conversation Types**: Creative, Technical, Educational, and Casual modes
- **Persistent Memory**: Save and reload conversations
- **Export Capabilities**: PDF and Markdown export
- **Search Functionality**: Find conversations by content
- **Follow-up Suggestions**: AI-powered conversation continuations

### 📊 Analytics Dashboard
- Conversation statistics and insights
- Activity timeline visualization
- Usage patterns analysis
- Export analytics reports

### 🎨 User Experience
- Modern, responsive UI with custom styling
- Dark/Light theme support
- Quick templates for common use cases
- Conversation history management
- Real-time conversation search

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- Google Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone and navigate to project:**
```bash
git clone https://github.com/AyanQuadri/AIConverse.git
cd AIConverse
```

2. **Install dependencies using uv:**
```bash
uv sync
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and add your Google API key
```

4. **Run the application:**
```bash
uv run streamlit run src/main.py
```

## 🎯 Usage Guide

### Getting Started
1. Configure your Google Gemini API key in `.env`
2. Launch the application with `uv run streamlit run src/main.py`
3. Choose your conversation style from the sidebar
4. Start chatting!

### Key Features

#### Conversation Types
- **General**: Standard AI assistant
- **Creative**: Enhanced for creative writing and artistic tasks
- **Technical**: Optimized for technical questions and coding help
- **Educational**: Focused on learning and explanations
- **Casual**: Friendly, conversational tone

#### Templates
Use quick templates for common scenarios:
- "Explain like I'm 5" for simple explanations
- "Code Review" for technical feedback
- "Creative Story" for narrative generation
- "Research Help" for information gathering

#### Multi-Modal Chat
Upload images alongside text to get AI analysis and responses about visual content.

#### Analytics
Track your conversation patterns:
- Message counts and conversation lengths
- Most used conversation types
- Activity timeline
- Usage insights and trends

## 🔧 Configuration

### Environment Variables
```bash
# Required
GOOGLE_API_KEY=gemini_api_key

# Optional
APP_TITLE=AIConverse
DEFAULT_THEME=dark
ENABLE_ANALYTICS=true
```

## 📊 Analytics Features

The analytics dashboard provides insights into your AI conversations:

- **Overview Metrics**: Total conversations, messages, and averages
- **Type Distribution**: Pie chart of conversation types used
- **Activity Timeline**: Daily conversation and message counts
- **Usage Insights**: Trends and patterns analysis
- **Export Options**: Download analytics as JSON reports

## 🚀 Advanced Features

### Export Options
- **PDF Export**: Clean, formatted conversation documents
- **Markdown Export**: Text-based format for easy sharing
- **Analytics Reports**: JSON format with comprehensive data

### Search & History
- Full-text search across all conversations
- Quick load previous conversations
- Delete unwanted conversations
- Conversation categorization by type

### AI Enhancements
- Context-aware responses using conversation history
- Temperature control for AI creativity
- Smart follow-up question suggestions
- Multi-modal image analysis with Gemini Vision

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your Google Gemini API key is correctly set in `.env`
2. **Import Errors**: Run `uv add` commands to install missing dependencies
3. **Storage Issues**: Check that the `data/` directory is created and writable
4. **UI Issues**: Try refreshing the browser or restarting the Streamlit server


---