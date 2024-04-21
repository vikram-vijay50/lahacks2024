import asyncio
import reflex as rx
from lahacks2024 import styles
from lahacks2024.state import ChatState

def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.box(
            rx.text(question, style=styles.question_style),
            text_align="right",
        ),
        rx.box(
            rx.text(answer, style=styles.answer_style),
            text_align="left",
        ),
        margin_y="1em",
    )

def chat() -> rx.Component:
    return rx.box(
        rx.foreach(
            ChatState.chat_history,
            lambda messages: qa(messages[0], messages[1]),
        )
    )

def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(
            value=ChatState.question,
            placeholder="Ask a question",
            on_change=ChatState.set_question,
            style=styles.input_style),
        rx.button("Ask", 
                  on_click=ChatState.answer, 
                  style=styles.button_style),
    )


@rx.page(route="/chatapp", title="Chat App")
def chatapp() -> rx.Component:
    return rx.center(
        rx.vstack(
            chat(),
            action_bar(),
            align="center",
        )
    )