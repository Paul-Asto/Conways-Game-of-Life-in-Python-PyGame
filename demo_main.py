from src.core.game import ConwayGame
from src.core.infinite_board import InfiniteBoard

from src.cardinal import gen_coord_off_matriz                


from src.cardinal import (
    Coord,
    VECTOR_DOWN,
    VECTOR_LEFT,
    VECTOR_RIGHT,
    VECTOR_UP,
    Vector
)

from time import sleep
import keyboard


board = InfiniteBoard(10, 10)
game  = ConwayGame(board)

class ViewBoard:

    def __init__(self, size_y: int, size_x: int):
        self.size_x = size_x
        self.size_y = size_y

        self.coords: list[Coord] = [Coord(*coord) for coord in gen_coord_off_matriz(0, self.size_y, 0, self.size_x)]

    def view(self):
        result = ""
        generator = iter(self.coords)

        for _ in range(0, self.size_y):
            for _ in range(0, self.size_x):
                coord = next(generator)

                nav = game.board.get_nav_cardinal_off_coord(coord)
                chunk = game.board.get_chunk(nav.quadrant, nav.coord_chunk)

                if chunk == None:
                    result += ".."
                    continue

                if chunk.get_cell(nav.coord_cell).state:
                    result += "[]"
                
                else:
                    result += "OO"

            result += "\n"
        
        return result


    def mov_coords(self, vector: Vector):
        for coord in self.coords:
            coord.move(vector)
        

view_board = ViewBoard(40, 50)

coords_oscilador = [    
    (2, 4),
    (2, 5),
    (2, 6),
    (8, 4),
    (8, 5),
    (8, 6),
    (4, 2),
    (5, 2),
    (6, 2),
    (4, 8),
    (5, 8),
    (6, 8),
]

coords_gen_nav_spacial = [    
    (6, 0),
    (7, 0),
    (6, 1),
    (7, 1),
    (6, 10),
    (7, 10),
    (8, 10),
    (5, 11),
    (9, 11),
    (4, 12),
    (10, 12),
    (7, 14),
    (4, 13),
    (10, 13),
    (5, 15),
    (9, 15),
    (6, 16),
    (8, 16),
    (7, 16),
    (7, 17),
    (4, 20),
    (5, 20),
    (6, 20),
    (4, 21),
    (5, 21),
    (6, 21),
    (3, 22),
    (7, 22),
    (2, 24),
    (3, 24),
    (7, 24),
    (8, 24),
    (4, 34),
    (5, 34),
    (4, 35),
    (5, 35),
]


coords_matusalen = [
    (-7, 3),
    (-8, 9),
    (-7, 4),
    (-6, 4),
    (-6, 8),
    (-6, 9),
    (-6, 10),
]

from random import randint

coords_random_cells = [(randint(-100, 100), randint(-100, 100)) for _ in range(5000)]

game.activate_cells(
    *coords_random_cells
)

ciclos = 1
while True:
    print("\033[H\033[J", end="")
    print(view_board.view())
    print()
    print(f"coord: actual: ", view_board.coords[0].value)
    print(f"Total de celdas vivas: {len(game.admin_cells._active_cells)}")
    print(f"Total de chunks cargados: {sum([len(d) for d in game.board.content.values()])}")
    

    if len(game.admin_cells.active_cells) == 0:
        break

    
    if keyboard.is_pressed("up"):
        view_board.mov_coords(VECTOR_UP)

    if keyboard.is_pressed("down"):
        view_board.mov_coords(VECTOR_DOWN)          

    if keyboard.is_pressed("left"):
        view_board.mov_coords(VECTOR_LEFT)

    if keyboard.is_pressed("right"):
        view_board.mov_coords(VECTOR_RIGHT)

    ciclos += 1

    game.next_turn()
    sleep(0.1)

print("Ciclos totales: ", ciclos)
