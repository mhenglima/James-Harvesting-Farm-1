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

class Interaction(Generic):
    def __init__(self, pos, size, groups, name):
        surf = pygame.Surface(size) # Create a surface with the specified size
        super().__init__(pos, surf, groups)
        self.name = name

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
        #print(f"[DEBUG] Initializing Tree at position: {pos}, with name: {name}")
        super().__init__(pos, surf, groups)
        self.all_sprites = all_sprites
        
        # Tree attributes
        self.health = 5
        self.alive = True
        stump_path = f'graphics/stumps/{"small" if name == "Small" else "large"}.png'
        try:
            self.stump_surf = pygame.image.load(stump_path).convert_alpha()
            #print(f"[DEBUG] Loaded stump image from: {stump_path}")
        except FileNotFoundError:
            #print(f"Stump image not found: {stump_path}")
            self.stump_surf = pygame.Surface((50, 50))  # Placeholder

        self.invul_timer = Timer(200)

        # Apples and apple positions
        try:
            self.apple_surf = pygame.image.load('graphics/fruit/apple.png').convert_alpha()
            #print(f"[DEBUG] Loaded apple image.")
        except FileNotFoundError:
            #print("Apple image not found at 'graphics/fruit/apple.png'")
            self.apple_surf = pygame.Surface((10, 10))  # Placeholder

        self.apple_pos = APPLE_POS.get(name, [])  # Ensure APPLE_POS has the required name key
        self.apple_sprites = pygame.sprite.Group()
        self.player_add = player_add

        #sounds
        self.axe_sound = pygame.mixer.Sound('audio/axe.mp3')
        
        self.create_fruit()
        #print(f"[DEBUG] Finished initializing Tree at {pos} with {len(self.apple_sprites)} apples.")

    def damage(self):
        # Tree takes damage
        self.health -= 1

        #play sound
        self.axe_sound.play()

        if self.apple_sprites:
            random_apple = choice(self.apple_sprites.sprites())
            self.create_particle_effect(random_apple)
            self.player_add('apple')

    def create_particle_effect(self, apple):
        # Visual effect when an apple is collected
        Particle(
            pos=apple.rect.topleft,
            surf=apple.image,
            groups=[self.all_sprites],
            z=LAYERS['fruit']
        )

    def check_death(self):
        if self.health <= 0:
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.alive = False
            self.player_add('wood')

    def create_fruit(self):
        #print(f"[DEBUG] Creating fruits for Tree at {self.rect.topleft}")
        # Generate apples on the tree
        for pos in self.apple_pos:
            if randint(0, 10) < 4:  # 40% chance to spawn an apple
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                #print(f"[DEBUG] Adding apple at ({x}, {y})")
                apple = Generic(
                    pos=(x, y),
                    surf=self.apple_surf,
                    groups=[self.apple_sprites, self.all_sprites],
                    z=LAYERS['fruit']
                )
                self.apple_sprites.add(apple)
                self.all_sprites.add(apple)
        #print(f"[DEBUG] Total apples created: {len(self.apple_sprites)}")

    def update(self, dt):
        if self.alive:
            self.check_death()


