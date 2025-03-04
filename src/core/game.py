from typing import TYPE_CHECKING
from src.core.infinite_board import InfiniteBoard
from src.cardinal import (
    Coord,

    VECTOR_UP,
    VECTOR_DOWN,
    VECTOR_RIGHT,
    VECTOR_LEFT,
    VECTOR_UP_LEFT, 
    VECTOR_UP_RIGHT,
    VECTOR_DOWN_LEFT,
    VECTOR_DOWN_RIGHT
    )

if TYPE_CHECKING:
    from src.core.chunk import Cell


class AdminCell:

    def __init__(self):
        self._active_cells: dict[tuple[int, int], "Cell"] = {}

        self._cells_to_revive: list[tuple[tuple[int, int], "Cell"]] = []
        self._cells_to_kill: list["Cell"] = []

    @property
    def active_cells(self) -> list[tuple[tuple[int, int], "Cell"]]:
        return list(self._active_cells.items())

    @property
    def active_coords(self) -> list[tuple[int, int]]:
        return list(self._active_cells.keys())


    def add_cell_active(self, coord: tuple[int, int], cell: "Cell"):
        cell.state = True
        self._active_cells[coord] = cell

    
    def delete_cell_active(self, coord: tuple[int, int]):
        cell = self._active_cells.pop(coord)
        cell.state = False


    def add_cell_to_revive(self, coord: tuple[int, int], cell: "Cell"):
        self._cells_to_revive.append((coord, cell))
    

    def add_cell_to_kill(self, coord: tuple[int, int]):
        cell = self._active_cells.pop(coord, None)

        if cell == None:
            raise Exception(f"La celda de la coordenada {coord} no se encuentra activa, por lo tanto no se puede añadir a la lista de muerte")

        self._cells_to_kill.append(cell)
    

    def revive_cells(self):
        for coord, cell in self._cells_to_revive:
            self.add_cell_active(coord, cell)
        
        self._cells_to_revive.clear()


    def kill_cells(self):
        for cell in self._cells_to_kill:
            cell.state = False
        
        self._cells_to_kill.clear()



from typing import Generic, TypeVar

T = TypeVar("T")

class CounterItems(Generic[T]):
    
    def __init__(self):
        self._store: dict[T, int] = {}

    @property
    def store(self) -> list[tuple[T, int]]:
        return list(self._store.items())

    def add_item(self, item: T):
        amount = self._store.get(item, None)

        if amount != None:
            self._store[item] += 1
            return

        self._store[item] = 1

    
    def add_items(self, *items: T):
        for item in items:
            self.add_item(item)


    def clear(self):
        self._store.clear()



class ConwayGame:
    n_cells_around_for_live: tuple[int, int] = (2, 3)
    n_cells_around_for_revive: int = 3

    def __init__(self, board: InfiniteBoard):
        self.board: InfiniteBoard = board

        self.counter_coords: CounterItems[tuple[int, int]] = CounterItems()
        self.admin_cells: AdminCell = AdminCell()


    def activate_cell(self, coord: tuple[int, int]):
        cell = self.get_cell(coord)
        self.admin_cells.add_cell_active(coord, cell)

    def deactivate_cell(self, coord: tuple[int, int]):
        self.admin_cells.delete_cell_active(coord)



    def activate_cells(self, *coords: tuple[int, int]):
        for coord in coords:
            self.activate_cell(coord)


    def get_cell(self, coord: tuple[int, int]):
        quadrant, coord_cell = self.board.get_data_nav_board_off_coord(coord)
        return self.board.get_and_create_cell(quadrant, coord_cell)


    def analyze_cells(self):
        for coord in self.admin_cells.active_coords:
            coord_base = Coord(*coord) 
            
            coords_analyze: list[Coord] = [
                coord_base + VECTOR_UP,
                coord_base + VECTOR_DOWN,
                coord_base + VECTOR_LEFT,
                coord_base + VECTOR_RIGHT,
                coord_base + VECTOR_UP_LEFT,
                coord_base + VECTOR_UP_RIGHT,
                coord_base + VECTOR_DOWN_LEFT,
                coord_base + VECTOR_DOWN_RIGHT,
            ]

            cells_around: list["Cell"] = [
                self.get_cell(coord) 
                for coord in coords_analyze 
            ]

            active_cells_around: list["Cell"] = [cell for cell in cells_around if cell.state]
            
            n_active_cells_around: int = len(active_cells_around)

            condition_to_kill: bool = n_active_cells_around not in self.n_cells_around_for_live
            
            if condition_to_kill:
                self.admin_cells.add_cell_to_kill(coord)

            # Sirve para detectar las coordenadas de las celdas que pueden revivir
            self.counter_coords.add_items(*[coord.value for coord in coords_analyze])


        #  añadir celdas que reviviran
        for coord, amount in self.counter_coords.store:
            condition_to_revive: bool = amount == self.n_cells_around_for_revive

            if not condition_to_revive:
                continue

            cell = self.get_cell(coord)

            if cell.state:
                continue

            self.admin_cells.add_cell_to_revive(coord, cell)
        
        self.counter_coords.clear()


    def next_turn(self):
        self.analyze_cells()

        self.admin_cells.kill_cells()
        self.admin_cells.revive_cells()