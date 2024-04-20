"""The dashboard page."""

from lahacks2024.templates import template

import reflex as rx


@template(route="/dashboard", title="Dashboard")
def dashboard() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """
    return rx.vstack(
        rx.heading("Upload a video", size="8"),
        rx.upload(
        rx.text(
            "Drag and drop files here or click to select files"
        ),
        id="my_upload",
        border="1px dotted rgb(107,99,246)",
        padding="5em",
    )
)
