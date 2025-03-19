import pygame as pg
from src.colors import COLOR_BLACK, COLOR_WHITE
from src.coordinate  import (
    gen_coord_off_matriz,
    Coord,
    Vector,
    )



class ViewBoard:
    
    def __init__(
            self,
            topleft: tuple[int, int],
            view_size: tuple[int, int], 
            size: tuple[int, int], 
            size_cell: tuple[int, int]

        ):   
        
        self.zoom_factor: float = 1
        self.change_zoom_factor: float = 0.1
        self.min_zoom: float = 0.75
        self.max_zoom: float = 4

        self.coord_cursor: Coord = Coord(0, 0)

        self.topleft_to_main: tuple[int, int] = topleft
        self.topleft_to_big: tuple[int, int] = (0, 0)
        
        self.lenght_y: int = size[0]
        self.lenght_x: int = size[1]

        self.init_size_cell_y: int = size_cell[0]
        self.init_size_cell_x: int = size_cell[1]

        self.size_big_y: int = self.lenght_y * self.init_size_cell_y
        self.size_big_x: int = self.lenght_x * self.init_size_cell_x

        self.size_view_y: int
        self.size_view_x: int


        self.view_surface: pg.Surface = pg.Surface(view_size)
        self.big_surface: pg.Surface = pg.Surface((self.size_big_x, self.size_big_y))

        # Creando y dibujando las celdas
        self.content: dict[tuple[int, int], pg.Rect] = {
            (coord_y, coord_x) : pg.Rect(
                coord_x * self.size_cell_x,
                coord_y * self.size_cell_y,
                self.size_cell_x,
                self.size_cell_y,
            ) 
            for coord_y, coord_x in 
            gen_coord_off_matriz(0, self.lenght_y, 0, self.lenght_x)
        }

        for rect in self.content.values():
            pg.draw.rect(self.big_surface, COLOR_BLACK, rect)
            pg.draw.rect(self.big_surface, COLOR_BLACK, rect, 1)


    @property
    def size_cell_y(self) -> int:
        return int(self.zoom_factor * self.init_size_cell_y)

    @property
    def size_cell_x(self) -> int:
        return int(self.zoom_factor * self.init_size_cell_x)
    
    def update_content(self):
        for coord, rect in self.content.items():
            y, x = coord
            rect.left = x * self.size_cell_x
            rect.top =  y * self.size_cell_y
            rect.width = self.size_cell_x
            rect.height = self.size_cell_y
        
        if self.zoom_factor > 3:
            for rect in self.content.values():
                pg.draw.rect(self.big_surface, COLOR_BLACK, rect)
                pg.draw.rect(self.big_surface, COLOR_WHITE, rect, 1)
        
        else:
            for rect in self.content.values():
                pg.draw.rect(self.big_surface, COLOR_BLACK, rect)
                pg.draw.rect(self.big_surface, COLOR_BLACK, rect, 1)


    def load_view(self, screen: pg.Surface):
        
        self.view_surface.blit(self.big_surface, self.topleft_to_big)
        screen.blit(self.view_surface, self.topleft_to_main)


    def get_coord_off_event_click(self, coord_click: tuple[int, int]) -> tuple[int, int]:
        click_x, click_y = coord_click
        left, top = self.topleft_to_main

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

        self.draw_cell(rect, color)
    
    def draw_cell(self, rect, color: tuple[int, int, int]):
        pg.draw.rect(self.big_surface, color, rect)

        if self.zoom_factor > 3:  
            pg.draw.rect(self.big_surface, COLOR_WHITE, rect, 1)
        else:      
            pg.draw.rect(self.big_surface, COLOR_BLACK, rect, 1)


    def mov_coord_cursor(self, vector: Vector):
        self.coord_cursor.move(vector)
    


    def maximize_scale(self):
        new_zoom = self.zoom_factor + (self.zoom_factor * self.change_zoom_factor)
        self.zoom_factor = min( new_zoom, self.max_zoom)
        self.update_content()


    def minimize_scale(self): 
        new_zoom = self.zoom_factor - (self.zoom_factor * self.change_zoom_factor)
        self.zoom_factor = max(new_zoom, self.min_zoom)
        self.update_content()


    
    def verify_click(self, coord: tuple[int, int]):
        rect = self.big_surface.get_rect(topleft = self.topleft_to_main)

        return rect.collidepoint(coord)

