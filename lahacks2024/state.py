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
        
        chat_session = model.start_chat(history=[])
        
        answer = ""
        self.chat_history.append((self.question, answer))
        
        self.question = ""
        yield
        
        async for item in chat_session:
            if hasattr(item.choices[0].delta, "content"):
                if item.choices[0].delta.content is None:
                    break
                answer += item.choices[0].delta.content
                self.chat_history[-1] = (self.chat_history[-1][0], answer)
                yield