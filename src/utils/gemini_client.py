import google.generativeai as genai
from PIL import Image
import streamlit as st
from datetime import datetime

class GeminiClient:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.vision_model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_text(self, prompt, temperature=0.7):
        """Generate text response from Gemini"""
        try:
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=1024,
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def analyze_image(self, image, prompt="Describe this image in detail"):
        """Analyze image with Gemini Vision"""
        try:
            response = self.vision_model.generate_content([prompt, image])
            return response.text
        except Exception as e:
            return f"Error analyzing image: {str(e)}"
    
    def get_smart_response(self, message, context="", conversation_type="general"):
        """Get contextually aware response"""
        templates = {
            "creative": "You are a creative writing assistant. Be imaginative and artistic in your responses.",
            "technical": "You are a technical expert. Provide detailed, accurate technical information.",
            "casual": "You are a friendly conversational partner. Keep responses natural and engaging.",
            "educational": "You are an educational tutor. Explain concepts clearly with examples.",
        }
        
        system_prompt = templates.get(conversation_type, "You are a helpful AI assistant.")
        
        full_prompt = f"{system_prompt}\n\nContext: {context}\n\nUser: {message}\n\nAssistant:"
        
        return self.generate_text(full_prompt)
    
    def suggest_followup(self, conversation_history):
        """Generate follow-up question suggestions"""
        try:
            prompt = f"""Based on this conversation, suggest 3 relevant follow-up questions:
            
{conversation_history[-200:]}

Provide exactly 3 short, engaging questions that would naturally continue this conversation."""
            
            response = self.generate_text(prompt, temperature=0.8)
            return [q.strip() for q in response.split('\n') if q.strip() and len(q.strip()) > 10][:3]
        except:
            return ["Tell me more about that", "Can you explain further?", "What's your opinion on this?"]