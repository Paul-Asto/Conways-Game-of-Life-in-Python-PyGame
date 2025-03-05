
class ConwaysInfiniteBoard:

    def __init__(self):
        self.content: dict[tuple[int, int], bool] = {}

        self.coords_to_revive: list[tuple[int, int]] = []
        self.coords_to_kill: list[tuple[int, int]] = []

    @property
    def coords_off_active_cell(self) -> list[tuple[int, int]]:
        return list(self.content.keys())


    def get_state_cell(self, coord: tuple[int, int]) -> bool: 
        return self.content.get(coord, False)


    def register_cell_life(self, coord: tuple[int, int]): 
        self.content[coord] = True


    def register_cell_dead(self, coord: tuple[int, int]): 
        self.content.pop(coord)


    def add_cell_to_revive(self, coord: tuple[int, int]):
        self.coords_to_revive.append(coord)
    

    def add_cell_to_kill(self, coord: tuple[int, int]):
        self.coords_to_kill.append(coord)
    

    def revive_cells(self):
        for coord in self.coords_to_revive:
            self.register_cell_life(coord)
        
        self.coords_to_revive.clear()


    def kill_cells(self):
        for coord in self.coords_to_kill:
            self.register_cell_dead(coord)
        
        self.coords_to_kill.clear()
