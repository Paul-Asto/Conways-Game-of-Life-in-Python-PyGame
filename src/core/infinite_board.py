from src.core.chunk import Cell
from enum import Enum, auto



class Quadrant(Enum):
    POS_Y_POS_X = auto()
    POS_Y_NEG_X = auto()
    NEG_Y_POS_X = auto()
    NEG_Y_NEG_X = auto()



class InfiniteBoard:

    def __init__(self, cell_class: type = Cell):
        self.cell_class: type = cell_class
        self.content: dict[Quadrant, dict[tuple[int, int], Cell]] = {
            Quadrant.POS_Y_POS_X : {},
            Quadrant.POS_Y_NEG_X : {},
            Quadrant.NEG_Y_POS_X : {},
            Quadrant.NEG_Y_NEG_X : {},
        }


    def get_cell(self, quadrant: Quadrant, coord: tuple[int, int]) -> Cell | None: 
        return self.content[quadrant].get(coord, None)


    def create_cell(self, quadrant: Quadrant, coord: tuple[int, int]): 
        self.content[quadrant][coord] = self.cell_class()


    def get_and_create_cell(self, quadrant: Quadrant, coord: tuple[int, int]) -> Cell:
        cell = self.get_cell(quadrant, coord)

        if cell == None:
            self.create_cell(quadrant, coord)
            cell = self.get_cell(quadrant, coord)

        return cell
    


    def get_data_nav_board_off_coord(self, coord: tuple[int, int]) -> tuple[Quadrant, tuple[int, int]]:
        y, x = coord

        y_is_pos = y >= 0
        x_is_pos = x >= 0
        
        quadrant: Quadrant

        if y_is_pos and x_is_pos:
            quadrant = Quadrant.POS_Y_POS_X

        elif y_is_pos and not x_is_pos:
            quadrant = Quadrant.POS_Y_NEG_X
            x -= 1

        elif not y_is_pos and x_is_pos:
            quadrant = Quadrant.NEG_Y_POS_X
            y -= 1

        elif not y_is_pos and not x_is_pos:
            quadrant = Quadrant.NEG_Y_NEG_X
            x -= 1
            y -= 1
        
        y = abs(y)
        x = abs(x)

        return (quadrant, (y, x))
