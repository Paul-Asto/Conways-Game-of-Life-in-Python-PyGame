from typing import Generator
from core.cardinal import Coord


def gen_coord_off_matriz(min_range_y: int, max_range_y: int, min_range_x: int, max_range_x: int) -> Generator[Coord]:
    for y in range(min_range_y, max_range_y):
        for x in range(min_range_x, max_range_x):
            yield Coord(y, x)


