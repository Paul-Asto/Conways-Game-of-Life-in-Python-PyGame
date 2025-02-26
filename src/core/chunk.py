from src.cardinal import Coord



class Cell:
    def __init__(self):
        self.state: bool = False





class Chunk:
    
    def __init__(self, size_y: int , size_x: int , coord: Coord):
        self.size_y: int = size_y
        self.size_x: int = size_x

        self.coord: Coord = coord
        self.content: dict[Coord, Cell] = {}