from src.core.infinite_board import ConwaysInfiniteBoard
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

    def __init__(self, board: ConwaysInfiniteBoard):
        self.board: ConwaysInfiniteBoard = board
        self.counter_coords: CounterItems[tuple[int, int]] = CounterItems()


    def activate_cell(self, coord: tuple[int, int]):
        self.board.register_cell_life(coord)

    def activate_cells(self, *coords: tuple[int, int]):
        for coord in coords:
            self.activate_cell(coord)


    def deactivate_cell(self, coord: tuple[int, int]):
        self.board.register_cell_dead(coord)


    def switch_cell(self, coord: tuple[int, int]):
        state = self.get_state_cell(coord)

        if state:
            self.deactivate_cell(coord)
        else:
            self.activate_cell(coord)


    def get_state_cell(self, coord: tuple[int, int]) -> bool:
        return self.board.get_state_cell(coord)


    def analyze_cells(self):
        for coord in self.board.coords_off_active_cell:
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

            state_cells_around: list[bool] = [
                self.get_state_cell(coord.value) 
                for coord in coords_analyze 
            ]

            active_cells_around: list[bool] = [state for state in state_cells_around if state]
            n_active_cells_around: int = len(active_cells_around)

            condition_to_kill: bool = n_active_cells_around not in self.n_cells_around_for_live
            
            if condition_to_kill:
                self.board.add_cell_to_kill(coord)

            # Sirve para detectar las coordenadas de las celdas que pueden revivir
            self.counter_coords.add_items(*[coord.value for coord in coords_analyze])


        #  añadir celdas que reviviran
        for coord, amount in self.counter_coords.store:
            condition_to_revive: bool = amount == self.n_cells_around_for_revive

            if not condition_to_revive:
                continue

            state_cell: bool = self.get_state_cell(coord)

            if state_cell:
                continue

            self.board.add_cell_to_revive(coord)
        
        self.counter_coords.clear()


    def next_turn(self):
        self.analyze_cells()

        self.board.kill_cells()
        self.board.revive_cells()