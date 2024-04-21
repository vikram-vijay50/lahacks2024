import reflex as rx

import os

import google.generativeai as genai
import response_gen

class ChatState(rx.State):
    question: str
    
    chat_history: list[tuple[str, str]]
    
    def answer(self):
        
        answer = "I don't know!"
        self.chat_history.append((self.question, answer))