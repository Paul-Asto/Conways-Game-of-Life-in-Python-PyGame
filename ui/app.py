from typing import TYPE_CHECKING
from textual.app import App
from textual.widgets import Button, Label
from textual.containers import Horizontal, Vertical
from ui.widgets import ConweyBoard, MacroBoard


if TYPE_CHECKING:
    from core.game import ConwayGame


class ConwayApp(App):
    CSS_PATH = "style.tcss"

    def __init__(self, game: "ConwayGame"):
        super().__init__()


    def compose(self):
        with Vertical(id= "main_content"):
            yield ConweyBoard()
            yield Label("CONWEYS GAME OF LIFE", id= "title_app")
            yield MacroBoard()

            with Vertical():
                yield Button("Iniciar")
                yield Button("Pintar")
                yield Button("Borrar")
                yield Button("Salir")
