
import pygame as pg
from src.core.game import ConwayGame
from src.ui.widgets import ViewBoard
from time import sleep
from src.colors import COLOR_BLACK, COLOR_WHITE
import asyncio
from src.coordinate import (
    VECTOR_LEFT,
    VECTOR_DOWN,
    VECTOR_UP,
    VECTOR_RIGHT,
    )

class ConwaysApp:

    def __init__(self, size_window: tuple[int, int], game: ConwayGame, view_board: ViewBoard):
        self.screen: pg.Surface = pg.display.set_mode(size_window, pg.RESIZABLE | pg.DOUBLEBUF)
        self.game: ConwayGame = game
        self.view_board: ViewBoard = view_board
        self.running: bool = True
        self.running_game: bool = False

        self.mouse_in_pressed: bool = False
        self.ultimate_coord_mouse: tuple[int, int] = (0, 0)


    async def run(self):
        pg.init()

        task_draw_screen = asyncio.create_task(self.draw_screen())
        task_read_events = asyncio.create_task(self.read_events())
        task_iteration_game = asyncio.create_task(self.iteration_game())

        await task_draw_screen
        await task_read_events
        await task_iteration_game
    
        pg.quit()


    async def draw_screen(self):
        clock = pg.time.Clock()

        while self.running:
            self.screen.fill((255, 255, 0))

            if self.mouse_in_pressed:
                coord_mouse = pg.mouse.get_pos()
                coord_rect: tuple[int, int] = self.view_board.get_coord_off_event_click(coord_mouse)

                if self.ultimate_coord_mouse != coord_rect:
                        if self.view_board.verify_click(coord_mouse):
                            coord_cell: tuple[int, int] = self.view_board.get_coord_off_cell(coord_rect)

                            self.game.switch_cell(coord_cell)
                            self.ultimate_coord_mouse = coord_rect

            self.view_board.big_surface.fill((0, 0, 0))
            self.view_board.draw_cells(
                *self.game.board.coords_off_active_cell,
                color= COLOR_WHITE,
            )

            # Dibujar la sub-superficie dentro de la pantalla principal
            self.view_board.load_view(self.screen)

            pg.display.flip()
            clock.tick(60)

            await asyncio.sleep(0.1)


    
    async def read_events(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        self.running_game = False if self.running_game else True

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.mouse_in_pressed = True

                    elif event.button == 4:
                        self.view_board.maximize_scale()

                    elif event.button == 5:
                        self.view_board.minimize_scale()

                elif event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.mouse_in_pressed = False
                        

            keys = pg.key.get_pressed()

            if keys[pg.K_UP]:
                self.view_board.mov_coord_cursor(VECTOR_UP)

            elif keys[pg.K_DOWN]:
                self.view_board.mov_coord_cursor(VECTOR_DOWN)

            elif keys[pg.K_LEFT]:
                self.view_board.mov_coord_cursor(VECTOR_LEFT)

            elif keys[pg.K_RIGHT]:
                self.view_board.mov_coord_cursor(VECTOR_RIGHT)


            await asyncio.sleep(0.0001)
    
    
    async def iteration_game(self):
        while self.running:
            if self.running_game:
                self.game.next_turn()

            await asyncio.sleep(0.1)
