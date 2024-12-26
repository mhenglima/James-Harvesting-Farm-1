import pygame
import pygame.camera
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic

class Level:
    def __init__(self):
        #level to display to the main screen  - get display surface
        self.display_surface = pygame.display.get_surface() 

        #sprite groups (allte players, trees etc)
        self.all_sprites = CameraGroup()

        self.setup()
        #create after the setup of the player
        self.overlay = Overlay(self.player)
    
    def setup(self):
        Generic(pos = (0,0), 
                surf = pygame.image.load('graphics/world/ground.png').convert_alpha(),
                groups = self.all_sprites,
                z = LAYERS['ground'])

        self.player = Player((640,360), self.all_sprites)

    def run(self,dt):
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

        self.overlay.display()

class CameraGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # Calculate the offset based on the player's position
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        # Drawing sprites based on their layers
        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    # Create a new rect with the updated offset
                    offset_rect = sprite.rect.copy()  # Copy the sprite's rect
                    offset_rect.center -= self.offset  # Apply the offset to the rect center
                    self.display_surface.blit(sprite.image, offset_rect)  # Draw the sprite using the offset rect

    