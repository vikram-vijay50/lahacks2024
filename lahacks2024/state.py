import reflex as rx

import os

import google.generativeai as genai
import response_gen

class ChatState(rx.State):
    question: str
    
    chat_history: list[tuple[str, str]]
    
    async def answer(self):
        Safety_settings = [
            {
                "category": "HARM_CATEGORY_DANGEROUS",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]
    
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest", safety_settings=Safety_settings, generation_config=genai.GenerationConfig(
        temperature=0.9,))
        
        chat = model.start_chat(history=[])
        
        response = chat.send_message(self.question)
        self.chat_history.append((self.question, response.text))
        
        self.question = ""
        return response.text
        