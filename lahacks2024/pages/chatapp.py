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
        rx.button("Ask", on_click=ChatState.answer, style=styles.button_style),
    )
    
async def answer(self):
    # Our chatbot is not very smart right now...
    answer = "I don't know!"
    self.chat_history.append((self.question, ""))

    # Clear the question input.
    self.question = ""
    # Yield here to clear the frontend input before continuing.
    yield

    for i in range(len(answer)):
        # Pause to show the streaming effect.
        await asyncio.sleep(0.1)
        # Add one letter at a time to the output.
        self.chat_history[-1] = (
            self.chat_history[-1][0],
            answer[: i + 1],
        )
        yield

@rx.page(route="/chatapp", title="Chat App")
def chatapp() -> rx.Component:
    return rx.center(
        rx.vstack(
            chat(),
            action_bar(),
            align="center",
        )
    )