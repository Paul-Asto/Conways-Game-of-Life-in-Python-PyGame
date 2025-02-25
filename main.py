from core.game import ConwayGame
from ui.app import ConwayApp


game  = ConwayGame()
app = ConwayApp(game)

if __name__ == "__main__":
    app.run()
    




