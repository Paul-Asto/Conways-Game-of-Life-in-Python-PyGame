from src.core.chunk import Chunk, Cell

from enum import Enum, auto
from dataclasses import dataclass


class Quadrant(Enum):
    POS_Y_POS_X = auto()
    POS_Y_NEG_X = auto()
    NEG_Y_POS_X = auto()
    NEG_Y_NEG_X = auto()



@dataclass
class NavCardinal:
    quadrant: Quadrant
    coord_chunk: tuple[int]
    coord_cell: tuple[int]



class InfiniteBoard:

    def __init__(self, chunk_size_y: int, chunk_size_x: int):
        self.chunk_size_y: int = chunk_size_y
        self.chunk_size_x: int = chunk_size_x

        self.content: dict[Quadrant, dict[tuple[int, int], Chunk]] = {
            Quadrant.POS_Y_POS_X : {},
            Quadrant.POS_Y_NEG_X : {},
            Quadrant.NEG_Y_POS_X : {},
            Quadrant.NEG_Y_NEG_X : {},
        }


    def get_chunk(self, quadrant: Quadrant, coord: tuple[int, int]) -> Chunk | None: 
        return self.content[quadrant].get(coord, None)


    def create_chunk(self, quadrant: Quadrant, coord: tuple[int, int]): 
        self.content[quadrant][coord] = Chunk(self.chunk_size_y, self.chunk_size_x)


    def get_and_create_chunk(self, quadrant: Quadrant, coord: tuple[int, int]) -> Chunk:
        chunk = self.get_chunk(quadrant, coord)

        if chunk == None:
            self.create_chunk(quadrant, coord)
            chunk = self.get_chunk(quadrant, coord)

        return chunk


    def get_nav_cardinal_off_coord(self, coord: tuple[int, int]) -> NavCardinal:
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

        y_chunk, y_cell = divmod(y, self.chunk_size_y)
        x_chunk, x_cell = divmod(x, self.chunk_size_x)

        return NavCardinal(quadrant, (y_chunk, x_chunk), (y_cell, x_cell))