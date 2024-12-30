import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from support import *
from random import choice

class SoilTile(pygame.sprite.Sprite):
    def __init__ (self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil']

        self.add(groups)

class WaterTile(pygame.sprite.Sprite):
    def __init__ (self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil water']

class Plant(pygame.sprite.Sprite):
    def __init__ (self, plant_type, groups, soil):

        #Plant Setup and pictures
        super().__init__(groups)
        self.plant_type = plant_type
        self.frames = import_folder(f'graphics/fruit/{plant_type}')
        self.soil = soil
        #plant growing requirements
        self.age = 0 
        self.max_age = len(self.frames) - 1
        self.grow_speed = GROW_SPEED[plant_type]

        #sprites setup
        self.image = self.frames[self.age]
        self.y_offset = -16 if plant_type == 'corn' else -8
        self.rect = self.image.get_rect(midbottom = soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))
        self.z = LAYERS['ground plant']

class SoilLayer():
    def __init__(self, all_sprites):
        # sprite groups
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()

        # graphics
        self.soil_surf = pygame.image.load('graphics/soil/o.png')
        self.soil_surfs = import_folder_dict('graphics/soil/')  #cant use the import file, as this uses all of them without an order so we need to use an actual order
        #print(self.soil_surfs)
        self.water_surfs = import_folder('graphics/soil_water')

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
                    if self.raining:
                        self.water_all()

    #hit the soil with the water
    def water(self, target_pos): 
        for soil_sprites in self.soil_sprites:
            if soil_sprites.rect.collidepoint(target_pos):
                #print('Soil tile watered')
                #Add entry to the soil to convert to Watered soil
                x = soil_sprites.rect.x // TILE_SIZE
                y = soil_sprites.rect.y // TILE_SIZE
                self.grid[x][y].append('W') #add water to the soil

                #create a water sprite
                pos = soil_sprites.rect.topleft
                surf = choice(self.water_surfs)
                WaterTile(pos, surf,[self.all_sprites, self.water_sprites])

    def water_all(self):
        # Go through all the lists 
        for index_row, row in enumerate(self.grid):
            # Go through the cells in the original list
            for index_col, cell in enumerate(row):
                if 'X' in cell and 'W' not in cell: #check if soil tile and not already watered, and therefore go and water
                    cell.append('W')
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE

                    #water the tiles action
                    WaterTile((x,y), choice(self.water_surfs), [self.all_sprites, self.water_sprites])

    def remove_water(self):
        #destroy all water sprites
        for sprite in self.water_sprites.sprites():
            sprite.kill()
        
        #clean up the grid
        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')

    def plant_seed(self, target_pos, seed):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):

                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                if 'P' not in self.grid[y][x]:
                    self.grid[y][x].append('P') #if the condition is met then assign it as a "P" in the tile for plant
                    Plant(seed, [self.all_sprites, self.plant_sprites], soil_sprite)

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:

                    # Get the correct soil image based on the surrounding tiles
                    t = 'X' in self.grid[index_row - 1 ][index_col] #cell on top of the same cell
                    b = 'X' in self.grid[index_row + 1 ][index_col] #cell on top of the same cell
                    r = 'X' in row[index_col + 1] #row is accessible
                    l = 'X' in row[index_col - 1] #row is accessible

                    tile_type = 'o'

                    #all sides
                    if all((t, r, l, b)): tile_type = 'x'

                    #horizontal tiles only
                    if l and not any ((t,r,b)) : tile_type = 'r' #if tile to left and nothing else tile to right
                    if r and not any ((t,l,b)) : tile_type = 'l' #if tile to right and nothing else tile to left   
                    if r and l and not any ((t,b)) : tile_type = 'lr' #if tile to left + right and nothing else tile to left

                    #vertical tiles only
                    if t and not any ((l,r,b)) : tile_type = 'b' #if tile to top and nothing else tile to bottom
                    if b and not any ((l,r,t)) : tile_type = 't' #if tile to top and nothing else tile to bottom
                    if b and t and not any ((l,r)) : tile_type = 'tb' #if tile to top and nothing else tile to bottom
                    
                    #corners
                    if b and l and not any ((r,t)) : tile_type = 'tr' #if tile to top and nothing else tile to bottom
                    if b and r and not any ((l,t)) : tile_type = 'tl' #if tile to top and nothing else tile to bottom
                    if t and l and not any ((r,b)) : tile_type = 'br' #if tile to top and nothing else tile to bottom
                    if t and r and not any ((l,b)) : tile_type = 'bl' #if tile to top and nothing else tile to bottom

                    #t-shapes
                    if all((t,b,r)) and not l: tile_type = 'tbr'
                    if all((t,b,l)) and not r: tile_type = 'tbl'
                    if all((l,r,t)) and not b: tile_type = 'lrb'
                    if all((l,r,b)) and not t: tile_type = 'lrt'
                    
                    SoilTile(
                        pos = (index_col * TILE_SIZE, index_row * TILE_SIZE), 
                        surf = self.soil_surfs[tile_type], 
                        groups = [self.all_sprites, self.soil_sprites])

