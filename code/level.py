import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree
from pytmx.util_pygame import load_pygame
from support import * 

class Level:
    def __init__(self):
        #level to display to the main screen  - get display surface
        self.display_surface = pygame.display.get_surface() 

        #sprite groups (allte players, trees etc)
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group() #keep a track which sprite is collidable
        self.tree_sprites = pygame.sprite.Group()

        self.setup()
        #create after the setup of the player
        self.overlay = Overlay(self.player)
    
    def setup(self):
        tmx_data = load_pygame('data/map.tmx')

        #house
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y* TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])
        
        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y* TILE_SIZE), surf, self.all_sprites, LAYERS['main'])

        #fence
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            Generic((x * TILE_SIZE, y* TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])

        #water
        water_frames = import_folder('graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites, LAYERS['water'])

        #trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.tree_sprites], obj.name, self.all_sprites,self.player_add)

        #wildflowers
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

        #collusions tiles
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)
        
        # Player 
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                # DEBUG: Print tree_sprites before passing to Player
                print("tree_sprites in Level setup:", self.tree_sprites)
                self.player = Player(
                    pos = (obj.x,obj.y), 
                    group = self.all_sprites, 
                    collision_sprites = self.collision_sprites,
                    tree_sprites = self.tree_sprites)

        Generic(pos = (0, 0), 
                surf = pygame.image.load('graphics/world/ground.png').convert_alpha(),
                groups = self.all_sprites,
                z = LAYERS['ground'])

    def player_add(self, item):
        self.player.item_inventory[item] += 1

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

        self.overlay.display()
        print(self.player.item_inventory)

class CameraGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # Calculate the offset based on the player's position
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        # Loop through all layers and draw sprites in those layers
        for layer_name, layer_value in sorted(LAYERS.items(), key=lambda x: x[1]):  # Sort layers by value
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.z):  # Sort sprites by their z value
                if sprite.z == layer_value:
                    # Apply the camera offset
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)