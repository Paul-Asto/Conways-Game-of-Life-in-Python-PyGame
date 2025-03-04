from src.core.game import ConwayGame
from src.core.infinite_board import InfiniteBoard

from src.cardinal import gen_coord_off_matriz

from src.ui.widgets import ReactCell
from src.ui.app import ConwayApp


board = InfiniteBoard(ReactCell)
game  = ConwayGame(board)
app = ConwayApp(game)

if __name__ == "__main__":
    app.run()
