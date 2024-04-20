"""The dashboard page."""
from lahacks2024.templates import template
import json

import reflex as rx

from typing import List, Dict

class GridForEachState(rx.State):
    card_info: Dict[str, List[Dict[str, str]]] = {}

    @classmethod
    def update_card_info(cls, data: Dict[str, List[Dict[str, str]]]):
        cls.card_info = {}
        
        for behavior_list in data.values():
            for behavior in behavior_list:
                # Extract timestamp, behavior, and description from each behavior
                timestamp = behavior['timestamp']
                behavior_name = behavior['behavior']
                description = behavior['description']

                # Concatenate behavior and description into a single string
                behavior_info = [f"{behavior_name}: {description}"]

                # Add behavior_info to card_info with timestamp as key
                cls.card_info[timestamp] = behavior_info

def display_grid(someVar: Dict[str, List[Dict[str, str]]]):
    return rx.box(
        rx.card(
            rx.button(someVar[0], weight="bold"),
            rx.text(someVar[1]),
        ),
        width="50vw"
    )

@template(route="/dashboard", title="Dashboard")
def dashboard() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """
    # Video path & component
    video_path = "/TouretteTics2.mp4"
    video_component = rx.vstack(
            rx.heading("Video", size="8"),
            rx.video(
              url=video_path,
              width="50vw",
              height="auto",
            ),
        )
    
    # Read JSON content from the file
    with open('./output_json/output_response.json', 'r') as json_file:
        data = json.load(json_file)

    # Update card_info in GridForEachState with the JSON data
    GridForEachState.update_card_info(data)

    return rx.vstack(
        video_component,
        rx.heading("Footage Breakdown", size="8"),
        rx.grid(
            rx.foreach(
                GridForEachState.card_info, display_grid
            ),
        ),
    )


