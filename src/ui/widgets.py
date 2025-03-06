import pygame as pg
from src.colors import COLOR_BLACK, COLOR_WHITE
from src.cardinal import (
    gen_coord_off_matriz,
    Coord,
    Vector,
    )




class ViewBoard:
    
    def __init__(self, topleft: tuple[int, int], size: tuple[int, int], size_cell: tuple[int, int]):    
        self.coord_cursor: Coord = Coord(0, 0)

        self.topleft: tuple[int, int] = topleft
        
        self.size_y: int = size[0]
        self.size_x: int = size[1]

        self.size_cell_y: int = size_cell[0]
        self.size_cell_x: int = size_cell[1]

        self.size_board_y: int = self.size_y * self.size_cell_y
        self.size_board_x: int = self.size_x * self.size_cell_x


        self.surface: pg.Surface = pg.Surface((self.size_board_x, self.size_board_y))
        self.content: dict[tuple[int, int], pg.Rect] = self.gen_init_content()

        self.init_draw()


    @property
    def rect(self):
        return self.surface.get_rect(center= (self.size_board_y // 2, self.size_board_x // 2))

    def gen_init_content(self):
        return {
            (coord_y, coord_x) : pg.Rect(
                coord_x * self.size_cell_x,
                coord_y * self.size_cell_y,
                self.size_cell_x,
                self.size_cell_y,
            ) 
            for coord_y, coord_x in 
            gen_coord_off_matriz(0, self.size_y, 0, self.size_x)
        }
    

    def init_draw(self): 
        for rect in self.content.values():
            pg.draw.rect(self.surface, COLOR_BLACK, rect)
            pg.draw.rect(self.surface, COLOR_BLACK, rect, 1)


    def load_view(self, screen: pg.Surface):
        screen.blit(self.surface, self.topleft)


    def get_coord_off_event_click(self, coord_click: tuple[int, int]) -> tuple[int, int]:
        click_x, click_y = coord_click
        left, top = self.topleft

        coord_base_y: int = click_y - top
        coord_base_x: int = click_x - left

        return (coord_base_y // self.size_cell_y, coord_base_x // self.size_cell_x)


    def get_coord_off_rect_view(self, coord_cell: tuple[int, int]) -> tuple[int, int]:
        new_y, new_x = coord_cell
        return (-self.coord_cursor.y + new_y, -self.coord_cursor.x + new_x)


    def get_coord_off_cell(self, coord_rect: tuple[int, int]) -> tuple[int, int]:
        new_y, new_x = coord_rect
        return (new_y + self.coord_cursor.y, new_x + self.coord_cursor.x)



    def get_rect(self, coord_cell: tuple[int, int]) -> pg.Rect | None:
        new_coord: tuple[int, int] = self.get_coord_off_rect_view(coord_cell)

        return self.content.get(new_coord, None)


    def load_view_rect(self, coord_cell: tuple[int, int] , color: tuple[int, int, int]):
        rect: pg.Rect = self.get_rect(coord_cell)

        if rect == None:
            return

        pg.draw.rect(self.surface, color, rect)
        pg.draw.rect(self.surface, COLOR_BLACK, rect, 1)


    def mov_coord_cursor(self, vector: Vector):
        self.coord_cursor.move(vector)


    def scalar(self, zoom_factor: int): ...

    
    def verify_click(self, event: pg.event.Event):
        rect = self.surface.get_rect(topleft = self.topleft)

        return rect.collidepoint(event.pos)

