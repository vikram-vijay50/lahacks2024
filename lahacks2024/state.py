import reflex as rx

import os

import google.generativeai as genai
import response_gen

# Make GenerateContent request with the structure described above.
def make_request(prompt, files):
  request = [prompt]
  for file in files:
    request.append(file.timestamp)
    request.append(file.response)
  return request

class ChatState(rx.State):
    # Question for chat app
    question: str
    # Chat history for chat app
    chat_history: list[tuple[str, str]]
    
    # Boolean for chat app hide/show
    show: bool = False
    
    def changeShow(self):
        self.show = not (self.show)
    
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
        all_files = response_gen.all_files
        
        chat = model.start_chat(history=[])
        
        request = make_request(self.question, all_files)
        response = chat.send_message(request)
        self.chat_history.append((self.question, response.text))
        
        self.question = ""
        yield