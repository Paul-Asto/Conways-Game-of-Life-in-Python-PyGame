from typing import TYPE_CHECKING
from textual import on
from textual.app import App
from textual.widgets import Button, Label
from textual.containers import Vertical
import asyncio



from src.ui.widgets import ConweyBoard, MacroBoard
from src.cardinal import (
    Coord,
    VECTOR_DOWN,
    VECTOR_LEFT,
    VECTOR_UP,
    VECTOR_RIGHT,
    )


if TYPE_CHECKING:
    from textual.events import Key
    from src.core.game import ConwayGame
    from src.core.chunk import  Cell


class ConwayApp(App):
    CSS_PATH = "style.tcss"

    def __init__(self, game: "ConwayGame"):
        super().__init__()

        self.game = game


    def compose(self):
        with Vertical(id= "main_content"):
            self.conwey_board = ConweyBoard(36, 45, Coord(-10, -15))
            yield self.conwey_board

            yield Label("CONWEYS GAME OF LIFE", id= "title_app")
            yield MacroBoard()

            with Vertical():
                yield Button("Iniciar", id= "btn_iniciar")
                yield Button("Pintar")
                yield Button("Borrar")
                yield Button("Salir")


    def on_mount(self):
        self.register_observeds_off_conwey_board()
        gen_nav_spacial = [    
            (6, 0),
            (7, 0),
            (6, 1),
            (7, 1),
            (6, 10),
            (7, 10),
            (8, 10),
            (5, 11),
            (9, 11),
            (4, 12),
            (10, 12),
            (7, 14),
            (4, 13),
            (10, 13),
            (5, 15),
            (9, 15),
            (6, 16),
            (8, 16),
            (7, 16),
            (7, 17),
            (4, 20),
            (5, 20),
            (6, 20),
            (4, 21),
            (5, 21),
            (6, 21),
            (3, 22),
            (7, 22),
            (2, 24),
            (3, 24),
            (7, 24),
            (8, 24),
            (4, 34),
            (5, 34),
            (4, 35),
            (5, 35),
        ]
        self.game.activate_cells(
            *gen_nav_spacial
        )


    @on(Button.Pressed, "#btn_iniciar")
    def init_game(self):
        asyncio.create_task(self.run_cicles())


    async def run_cicles(self):
        while True:
            await asyncio.sleep(0.15)
            self.game.next_turn()



    def register_observeds_off_conwey_board(self):
        for block in self.conwey_board.children:
            coord: tuple = block.coord.value
            cell: "Cell" = self.game.get_cell(coord)

            block.observed = cell
            block.react_changes()


    async def on_key(self, event: "Key") -> None:
        if event.key == "left":
            self.conwey_board.delet_observeds_off_childen()
            self.conwey_board.move_coords_off_children(VECTOR_LEFT)
            self.register_observeds_off_conwey_board()

        elif event.key == "right":
            self.conwey_board.delet_observeds_off_childen()
            self.conwey_board.move_coords_off_children(VECTOR_RIGHT)
            self.register_observeds_off_conwey_board()
            
        elif event.key == "up":
            self.conwey_board.delet_observeds_off_childen()
            self.conwey_board.move_coords_off_children(VECTOR_UP)
            self.register_observeds_off_conwey_board()
            
        elif event.key == "down":
            self.conwey_board.delet_observeds_off_childen()
            self.conwey_board.move_coords_off_children(VECTOR_DOWN)
            self.register_observeds_off_conwey_board()

