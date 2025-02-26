from core.chunk import Chunk
from src.cardinal import Coord

class InfiniteBoard:

    def __init__(self, chunk_size_y: int, chunk_size_x: int):
        self.chunk_size_y: int = chunk_size_y
        self.chunk_size_x: int = chunk_size_x

        self.content: dict[Coord, Chunk] = {}


    def get_chunk(self, coord: Coord) -> Chunk | None: ...


    def create_chunk(self, coord: Coord): ...


    def gen_and_get_chunck(self, coord: Coord): ...
