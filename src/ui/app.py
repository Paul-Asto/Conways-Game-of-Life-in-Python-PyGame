
import pygame as pg
from src.core.game import ConwayGame
from src.ui.widgets import ViewBoard
from time import sleep
from src.colors import COLOR_BLACK, COLOR_WHITE
import asyncio
from src.cardinal import (
    VECTOR_LEFT,
    VECTOR_DOWN,
    VECTOR_UP,
    VECTOR_RIGHT,
    )

class ConwaysApp:

    def __init__(self, size_window: tuple[int, int], game: ConwayGame, view_board: ViewBoard):
        self.screen: pg.Surface = pg.display.set_mode(size_window, pg.RESIZABLE | pg.DOUBLEBUF)
        self.game: ConwayGame = game
        self.running: bool = True
        self.view_board: ViewBoard = view_board


    async def run(self):
        pg.init()
        clock = pg.time.Clock()

        asyncio.create_task(self.read_events())
        asyncio.create_task(self.iteration_game())

        while self.running:
            self.screen.fill((255, 255, 0))

            for coord_cell in  self.game.board.coords_off_active_cell:
                self.view_board.load_view_rect(coord_cell, COLOR_WHITE)

            # Dibujar la sub-superficie dentro de la pantalla principal
            self.view_board.load_view(self.screen)

            pg.display.flip()
            clock.tick(60)

            for coord_cell in  self.game.board.coords_off_active_cell:
                self.view_board.load_view_rect(coord_cell, COLOR_BLACK)

            await asyncio.sleep(0.1) 

        pg.quit()

    
    async def read_events(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.view_board.verify_click(event):
                        coord_rect: tuple[int, int] = self.view_board.get_coord_off_event_click(event.pos)
                        coord_cell: tuple[int, int] = self.view_board.get_coord_off_cell(coord_rect)

                        self.game.switch_cell(coord_cell)

            keys = pg.key.get_pressed()

            if keys[pg.K_UP]:
                self.view_board.mov_coord_cursor(VECTOR_UP)

            elif keys[pg.K_DOWN]:
                self.view_board.mov_coord_cursor(VECTOR_DOWN)

            elif keys[pg.K_LEFT]:
                self.view_board.mov_coord_cursor(VECTOR_LEFT)

            elif keys[pg.K_RIGHT]:
                self.view_board.mov_coord_cursor(VECTOR_RIGHT)

            await asyncio.sleep(0.01)
    
    
    async def iteration_game(self):
        while self.running:
            self.game.next_turn()
            await asyncio.sleep(0.1)
