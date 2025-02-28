from typing import TYPE_CHECKING
from textual.widget import Widget
from textual.containers import Vertical
from src.cardinal import Coord, Vector, gen_coord_off_matriz
from src.observer_interface import Observer, Observed
from src.core.chunk import Cell

if TYPE_CHECKING:
    from src.ui.app import ConwayApp

class ReactCell(Cell, Observed):
    

    def __init__(self):
        super().__init__()
        Observed.__init__(self) 
        

    @property
    def state(self) -> bool:
        return self.private_state
    
    @state.setter
    def state(self, value: bool):
        self.private_state = value
        self.report_changes()



class ReactBlock(Widget, Observer[ReactCell]):
    app: "ConwayApp"
    
    def __init__(self, coord: Coord):
        super().__init__()

        self.coord: Coord = coord


    def react_changes(self):
        color: str = 'white' if self.observed.state else 'black'
        self.set_styles(f"background: {color};")

    def render(self):
        # Devuelve una cadena vacía para no mostrar el nombre del widget
        return ""
    
    def on_click(self):
        if self.observed.state:
            self.app.game.deactivate_cell(self.coord.value)

        else:
            self.app.game.activate_cell(self.coord.value)



class ConweyBoard(Vertical):
    children: tuple[ReactBlock]
    
    def __init__(self, size_y: int, size_x: int, coord_init: Coord, name = None, id = None, classes = None):
        super().__init__(name=name, id=id, classes=classes)

        self.size_y: int = size_y
        self.size_x: int = size_x
        self.coord_init: Coord = coord_init

        list_coord = [
            Coord(*coord) 
            for coord in 
            gen_coord_off_matriz(
                self.coord_init.y,
                self.size_y + self.coord_init.y, 
                self.coord_init.x, 
                self.size_x + self.coord_init.x)
        ]

        for coord in list_coord:
            self._add_child(ReactBlock(coord))
    

    def move_coords_off_children(self, vector: Vector):
        for child in self.children:
            child.coord.move(vector)


    def delet_observeds_off_childen(self):
        for child in self.children:
            child.delete_observed()



class MacroBoard(Vertical):
    pass
