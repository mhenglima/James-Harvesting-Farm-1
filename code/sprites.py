import pygame
from settings import *
from random import randint, choice  # Added choice import
from timer1 import Timer

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate((-self.rect.width * 0.2, -self.rect.height * 0.75))  # Small width, vertical access needs overlap

class Water(Generic):
    def __init__(self, pos, frames, groups, z):
        # Animation setup
        self.frames = frames
        self.frame_index = 0

        # Sprite setup
        super().__init__(
            pos=pos, 
            surf=self.frames[self.frame_index], 
            groups=groups, 
            z=LAYERS['water'])

    def animate(self, dt):
        self.frame_index += 5 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)

class WildFlower(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate((-20, -self.rect.height * 0.9))

class Tree(Generic):
    def __init__(self, pos, surf, groups, name, all_sprites):
        super().__init__(pos, surf, groups)
        self.all_sprites = all_sprites
        # Tree attributes
        self.health = 5
        self.alive = True
        stump_path = f'graphics/stumps/{"small" if name == "Small" else "large"}.png'
        self.stump_surf = pygame.image.load(stump_path).convert_alpha()
        self.invul_timer = Timer(200)

        # Apples
        self.apple_surf = pygame.image.load('graphics/fruit/apple.png')
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

    def damage(self):
        # Damaging the tree
        self.health -= 1

        # Remove an apple
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())  # Fixed undefined choice error
            random_apple.kill()

    def check_death(self):
        if self.health <= 0:
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.alive = False

    def update(self, dt):
        if self.alive:
            self.check_death()

    def create_fruit(self):
        for pos in self.apple_pos:
            if randint(0, 10) < 4:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                print(f"Creating apple at position: {x}, {y}")  # Debug output
                print(f"Apple sprites: {len(self.apple_sprites.sprites())}")  # This should show how many apples are in the group.

                apple = Generic(
                    pos=(x, y),
                    surf=self.apple_surf,
                    groups=[self.apple_sprites, self.groups()[0]],  # Ensure apple is added to the correct groups
                    z=LAYERS['fruit'])  # Apples should be rendered in the 'fruit' layer
                
                # Add the apple to the all_sprites group
                self.all_sprites.add(apple)  # Add to the main all_sprites group

                print(f"Apple sprites after creation: {len(self.apple_sprites)}")  # Debug print to track apple count


