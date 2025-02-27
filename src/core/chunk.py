from src.cardinal import  gen_coord_off_matriz
from typing import Generic, TypeVar


class Cell:
    def __init__(self):
        self.__state: bool = False

        
    @property
    def state(self) -> bool:
        return self.__state
    
    @state.setter
    def state(self, value: bool):
        self.__state = value


T = TypeVar("T", bound= Cell)


class Chunk(Generic[T]):
    
    def __init__(self, size_y: int , size_x: int, cell_class: type[T] = Cell):
        self.size_y: int = size_y
        self.size_x: int = size_x

        self.cell_class: type[T] = cell_class
        
        self.content: dict[tuple[int, int], T] = {
            coord: self.cell_class() 
            for coord in
            gen_coord_off_matriz(0, self.size_y, 0, self.size_x)
        }


    def get_cell(self, coord: tuple[int, int]) -> Cell:
        cell = self.content.get(coord, None)

        if cell == None:
            raise Exception(f"En la coordenada {coord} no existe una celda, el tamaño del chunk es de {(self.size_y, self.size_x)}")
        
        return cell
