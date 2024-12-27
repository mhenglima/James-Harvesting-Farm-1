import pygame
from settings import *
from random import randint, choice
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

class Particle(Generic):
    def __init__(self, pos, surf, groups, z, duration = 200):
        super().__init__(pos, surf, groups, z)
        self.start_time = pygame.time.get_ticks()
        self.duration = duration
        self.image.set_alpha(255)  # Start with full opacity

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time
        # Fade the particle over time (from 255 to 0)
        alpha = max(255 - int((elapsed_time / self.duration) * 255), 0)
        self.image.set_alpha(alpha)
        
        # If the particle has finished its duration, remove it
        if elapsed_time > self.duration:
            self.kill()

class Tree(Generic):
    def __init__(self, pos, surf, groups, name, all_sprites, player_add):
        super().__init__(pos, surf, groups)
        self.all_sprites = all_sprites
        
        # Tree attributes
        self.health = 5
        self.alive = True
        stump_path = f'graphics/stumps/{"small" if name == "Small" else "large"}.png'
        self.stump_surf = pygame.image.load(stump_path).convert_alpha()
        self.invul_timer = Timer(200)

        # Apples and apple positions
        self.apple_surf = pygame.image.load('graphics/fruit/apple.png')
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

        self.player_add = player_add

    def damage(self):
        # Damaging the tree
        self.health -= 1

        # Handle apple removal when the tree is damaged
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())  # Randomly pick an apple
            self.create_particle_effect(random_apple)  # Create particle effect at the apple's position
            self.player_add('apple')  # Add an apple to the player's inventory
            #self.remove_apple(random_apple)  # Remove the apple from the game

    def create_particle_effect(self, apple):
        # Create a particle effect when an apple "dies"
        print(f"Creating particle effect at {apple.rect.topleft}")  # Debugging the particle creation
        particle = Particle(
            pos=apple.rect.topleft, 
            surf=apple.image, 
            groups=[self.all_sprites],  # Add to the main sprite group
            z=LAYERS['fruit']
        )
        print(f"Particle added to group, total sprites: {len(self.all_sprites.sprites())}")  # Debug output


    def remove_apple(self, apple):
        # Change the apple's image to indicate it is destroyed (or use a placeholder image)
        destroyed_image = pygame.Surface((apple.rect.width, apple.rect.height))
        #destroyed_image.fill((255, 255, 255))  # White color for destroyed apple (or use a specific "destroyed" image)
        #apple.image = destroyed_image  # Replace the apple's image

        # Optionally, remove the apple sprite after some time or instantly
        #apple.kill()

    def check_death(self):
        if self.health <= 0:
            #Particle(self.rect.topleft, self.image, [self.all_sprites], LAYERS['fruit'], 2000)
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.alive = False
            self.player_add('wood')

    def update(self, dt):
        if self.alive:
            self.check_death()

    def create_fruit(self):
        for pos in self.apple_pos:
            if randint(0, 10) < 4:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                apple = Generic(
                    pos=(x, y),
                    surf=self.apple_surf,
                    groups=[self.apple_sprites, self.groups()[0]],  # Ensure apple is added to the correct groups
                    z=LAYERS['fruit']  # Apples should be rendered in the 'fruit' layer
                )
                self.all_sprites.add(apple)  # Add the apple to the main all_sprites group
                print(f"Apple created at {x}, {y}")  # Debug output

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


