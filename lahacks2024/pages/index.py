"""The home page of the app."""

import subprocess
import os
import shutil
from lahacks2024 import styles
from lahacks2024.templates import template
from lahacks2024 import *

import reflex as rx

import response_gen

class State(rx.State):
    """The app state."""

    # The images to show.
    img: list[str]

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        
        # Clear the uploaded_files folder
        uploaded_files_dir = rx.get_upload_dir()
        shutil.rmtree(uploaded_files_dir, ignore_errors=True)
        os.makedirs(uploaded_files_dir, exist_ok=True)
        
        frames_files_dir = rx.get_asset_path(".\\content\\frames")
        shutil.rmtree(frames_files_dir, ignore_errors=True)
        
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename
            assetPath = rx.get_asset_path() / file.filename

            # Save the file in uploaded_files.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)
            
            # Save the file in assets
            with assetPath.open("wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.img.append(file.filename)
            
        subprocess.run(["python", "response_gen.py"])

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