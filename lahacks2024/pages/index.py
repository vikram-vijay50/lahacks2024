"""The home page of the app."""
from lahacks2024 import styles
from lahacks2024.templates import template
from lahacks2024 import *

import reflex as rx

from response_gen import gen_response

import os
import shutil

class State(rx.State):
    """The app state."""
    # The img to show.
    img: list[str]
    
    # uploaded_file name
    filename: str

    async def handle_upload(self, files: list[rx.UploadFile]):
        directory_path = rx.get_upload_dir()
        shutil.rmtree(directory_path)
        
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename
            
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)
        
            self.img.append(file.filename)
            
        gen_response()
        

color = "rgb(107,99,246)"

@template(route="/", title="Home")
def index() -> rx.Component:
    """The main view."""
    return rx.vstack(
        rx.vstack(
            rx.heading(
                "Upload your footage here!",
                size="8"
            ),
        ),
        rx.upload(
            rx.vstack(
                rx.button("Select File", color=color, bg="white", border=f"1px solid {color}"),
                rx.text("Drag and drop files here or click to select files"),
            ),
            id="upload1",
            border=f"1px dotted {color}",
            padding="5em",
        ),
        rx.hstack(rx.foreach(rx.selected_files("upload1"), rx.text)),
        rx.button(
            "Upload",
            on_click=State.handle_upload(rx.upload_files(upload_id="upload1")),
        ),
        rx.button(
            "Clear",
            on_click=rx.clear_selected_files("upload1"),
        ),
        rx.foreach(State.img, lambda img: rx.image(src=rx.get_upload_url(img))),
        padding="5em",
    )