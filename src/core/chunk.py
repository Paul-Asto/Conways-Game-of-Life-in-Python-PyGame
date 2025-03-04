from src.cardinal import  gen_coord_off_matriz
from typing import Generic, TypeVar


class Cell:
    def __init__(self):
        self.private_state: bool = False

        
    @property
    def state(self) -> bool:
        return self.private_state
    
    @state.setter
    def state(self, value: bool):
        self.private_state = value


T = TypeVar("T", bound= Cell)
