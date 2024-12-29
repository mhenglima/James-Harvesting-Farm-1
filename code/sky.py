import pygame
from settings import *
from support import *
from sprites import * 
from random import * 

class Drop(Generic):
    def __init__ (self, surf, pos, moving, groups, z):

        # general Setup
        super().__init__(pos, surf, groups, z)
        self.lifetime = randint(400, 500)
        self.start_time = pygame.time.get_ticks()  # Change pygame.timer to pygame.time

        # moving
        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2, 4)
            self.speed = randint(200, 250)
    
    def update(self, dt):
        # movement
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))  # Avoid truncating or it will look weird...

        # timer - Destroy timer if lived longer than allowed
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:  # Change pygame.timer to pygame.time
            self.kill()


class Rain:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.rain_drops = import_folder('graphics/rain/drops/')
        self.rain_floor = import_folder('graphics/rain/floor/')
        
        # Initialize the floor as a pygame.Rect object with the dimensions of the ground image
        self.floor = pygame.Rect(0, 0, *pygame.image.load('graphics/world/ground.png').get_size())
        self.floor_w, self.floor_h = self.floor.w, self.floor.h  # Extract width and height

    def create_floor(self):
        Drop(
            surf=choice(self.rain_floor),
            pos=(randint(0, self.floor_w), randint(0, self.floor_h)),
            moving=False,
            groups=self.all_sprites,
            z=LAYERS['rain floor'])

    def create_drops(self):
        Drop(
            surf=choice(self.rain_drops),
            pos=(randint(0, self.floor_w), randint(0, self.floor_h)),
            moving=True,
            groups=self.all_sprites,
            z=LAYERS['rain drops'])

    def update(self):
        self.create_drops()
        self.create_floor()