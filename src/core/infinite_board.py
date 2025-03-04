from src.core.chunk import Cell




class InfiniteBoard:

    def __init__(self, cell_class: type = Cell):
        self.cell_class: type = cell_class
        self.content: dict[tuple[int, int], Cell] = {}


    def get_cell(self, coord: tuple[int, int]) -> Cell | None: 
        return self.content.get(coord, None)


    def create_cell(self, coord: tuple[int, int]): 
        self.content[coord] = self.cell_class()


    def get_and_create_cell(self, coord: tuple[int, int]) -> Cell:
        cell = self.get_cell(coord)

        if cell == None:
            self.create_cell(coord)
            cell = self.get_cell(coord)

        return cell
