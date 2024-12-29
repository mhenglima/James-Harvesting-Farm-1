import pygame
from settings import *
from pytmx.util_pygame import load_pygame

class SoilTile(pygame.sprite.Sprite):
    def __init__ (self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil']

        self.add(groups)

class SoilLayer():
    def __init__(self, all_sprites):
        # sprite groups
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()

        # graphics
        self.soil_surf = pygame.image.load('graphics/soil/o.png')

        self.create_soil_grid()
        self.create_hit_rects()

    # One list for every type of tile - Add capital 'F' if farmable
    def create_soil_grid(self):
        ground = pygame.image.load('graphics/world/ground.png')  # how many in the plane (horizontal + vertical) <width/tile size>
        h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE

        self.grid = [ [[] for col in range(h_tiles)] for row in range(v_tiles)]
        for x, y, surf in load_pygame('data/map.tmx').get_layer_by_name('Farmable').tiles():
            self.grid[y][x].append('F')

    def create_hit_rects(self):
        self.hit_rects = []  # Corrected: initialize 'self.hit_rects' as an empty list
        # Go through all the lists 
        for index_row, row in enumerate(self.grid):
            # Go through the cells in the original list
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)  # create a rect object, 64 by 64
                    self.hit_rects.append(rect)  # Append to self.hit_rects instead of overwriting it

    def get_hit(self, point):
        # Convert rectangle position back to grid
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                x = rect.x // TILE_SIZE  # Floor divided by size of tile to get pixel position in the actual grid
                y = rect.y // TILE_SIZE

                if 'F' in self.grid[y][x]:  # Get the full list of actual cells
                    #print('Farmable')
                    self.grid[y][x].append('X')  # Add 'X' to the list to indicate that it has been hit 
                    self.create_soil_tiles()


    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:
                    SoilTile(
                        pos = (index_col * TILE_SIZE, index_row * TILE_SIZE), 
                        surf = self.soil_surf, 
                        groups = [self.all_sprites, self.soil_sprites])