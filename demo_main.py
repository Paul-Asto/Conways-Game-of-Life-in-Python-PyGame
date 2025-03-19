from src.core.game import ConwayGame
from src.core.infinite_board import ConwaysInfiniteBoard
from src.data_cells import coords_random_cells

from src.coordinate import gen_coord_off_matriz                


from src.coordinate import (
    Coord,
    VECTOR_DOWN,
    VECTOR_LEFT,
    VECTOR_RIGHT,
    VECTOR_UP,
    Vector
)

from time import sleep
import keyboard


board = ConwaysInfiniteBoard()
game  = ConwayGame(board)

class ViewBoard:

    def __init__(self, size_y: int, size_x: int):
        self.size_x = size_x
        self.size_y = size_y

        self.coords: list[Coord] = [Coord(*coord) for coord in gen_coord_off_matriz(0, self.size_y, 0, self.size_x)]

    def view(self) -> str:
        result = ""
        generator = iter(self.coords)

        for _ in range(0, self.size_y):
            for _ in range(0, self.size_x):
                coord = next(generator)
                state_cell = game.get_state_cell(coord.value)

                if state_cell:
                    result += "[]"
                
                else:
                    result += ".."

            result += "\n"
        
        return result


    def mov_coords(self, vector: Vector):
        for coord in self.coords:
            coord.move(vector)
        

view_board = ViewBoard(40, 50)



game.activate_cells(
    *coords_random_cells
)




import asyncio

async def main():

    
    task_1 = asyncio.create_task(read_events())
    task_2 = asyncio.create_task(update_screen())

    await task_1
    await task_2



async def read_events():
    while True:
        if len(game.board.content) == 0:
            break
        
        if keyboard.is_pressed("up"):
            view_board.mov_coords(VECTOR_UP)

        if keyboard.is_pressed("down"):
            view_board.mov_coords(VECTOR_DOWN)          

        if keyboard.is_pressed("left"):
            view_board.mov_coords(VECTOR_LEFT)

        if keyboard.is_pressed("right"):
            view_board.mov_coords(VECTOR_RIGHT)

        await asyncio.sleep(0.01)


async def update_screen():
    ciclos = 1
    while True:
        print("\033[H\033[J", end="")
        print(view_board.view())
        print()
        print(f"Coordenada: actual: ", view_board.coords[0].value)
        print(f"Total de celdas vivas: {len(game.board.content)}")

        if len(game.board.content) == 0:
            break

        ciclos += 1

        game.next_turn()
        await asyncio.sleep(0.1)

    print("Ciclos totales: ", ciclos)



asyncio.run(main())