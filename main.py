from src.core.game import ConwayGame
from src.core.infinite_board import ConwaysInfiniteBoard
from src.ui.app import ConwaysApp
from src.ui.widgets import ViewBoard
from src.data_cells import coords_random_cells
import asyncio


board = ConwaysInfiniteBoard()
game  = ConwayGame(board)
game.activate_cells(*coords_random_cells)


view_board = ViewBoard(
    topleft= (50, 20), 
    size= (1100, 700), 
    view_size= (1100, 700),
    size_cell=(5, 5),
    )

app = ConwaysApp(
    size_window= (1500, 800),
    game= game,
    view_board= view_board,
)

if __name__ == "__main__":
    asyncio.run(app.run())


