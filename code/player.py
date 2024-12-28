import pygame
from settings import *
from support import * 
from timer1 import Timer
from sprites import Tree


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites, interaction):
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0 

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.z = LAYERS['main']

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # collision
        self.hitbox = self.rect.copy().inflate((-126, -70))  # Takes rectangle and changes the size of the rectangle
        self.collision_sprites = collision_sprites

        # timers
        self.timers = {
            'tool use': Timer(350, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200)
        }

        # Tools usage
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0 
        self.selected_tool = self.tools[self.tool_index]

        # Seed usage
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

        #Inventory
        self.item_inventory = {
            'wood':   0,
            'apple':  0,
            'corn':   0,
            'tomato': 0
        }
        

        # Interaction
        self.tree_sprites = tree_sprites
        self.interaction = interaction
        self.sleep = False

    def use_tool(self):
        #print('tool use')
        if self.selected_tool == 'hoe':
            pass
        
        if self.selected_tool == 'axe':
            for tree in self.tree_sprites.sprites():
                if isinstance(tree, Tree):  # Check if tree is an instance of the Tree class
                    if tree.rect.collidepoint(self.target_pos):
                        if pygame.key.get_pressed()[pygame.K_SPACE]:  # Check if the player presses the spacebar to cut the tree
                            #print("Cutting tree down")  # For debugging
                            tree.damage()
        
        if self.selected_tool == 'water':
            pass

    def get_target_pos(self):
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

    def use_seed(self):
        pass
        
    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
                           'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
                           'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []}
        
        for animation in self.animations.keys():
            full_path = 'graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['tool use'].active and not self.sleep:
            # directions
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
                
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0
            
            # tool usage
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0 

            # change tool
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index += 1
                # if tool index > length of tools => tool index to 0
                self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0 
                self.selected_tool = self.tools[self.tool_index]

            # seed use
            if keys[pygame.K_LCTRL]:
                self.timers['seed use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0 
                print('use seed')

            # change seed
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seed_index += 1
                # if seed index > length of seeds => seed index to 0
                self.seed_index = self.seed_index if self.seed_index < len(self.seeds) else 0 
                self.selected_seed = self.seeds[self.seed_index]
                print(self.selected_seed)

            #interact with bed
            if keys[pygame.K_RETURN]:
                collided_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction,False)
                if collided_interaction_sprite:
                    if collided_interaction_sprite[0].name == 'Trader':
                        pass
                    else:
                        self.status = 'left_idle'
                        self.sleep = True

    def get_status(self):
        # if the player is not moving (idle):
        if self.direction.magnitude() == 0:
            # add _idle to the status (manipulate string to get status with idle)
            self.status = self.status.split('_')[0] + '_idle'

        # tool use 
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def collision(self, direction):
        for sprites in self.collision_sprites.sprites():  # Change sprite to sprites
            if hasattr(sprites, 'hitbox'):  # Use sprites instead of sprite
                if sprites.hitbox.colliderect(self.hitbox):  # Use sprites
                    if direction == 'horizontal':
                        if self.direction.x > 0:  # Moving right
                            self.hitbox.right = sprites.hitbox.left  # Use sprites
                        if self.direction.x < 0:  # Moving left
                            self.hitbox.left = sprites.hitbox.right  # Use sprites
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx

                    if direction == 'vertical':
                        if self.direction.y > 0:  # Moving down
                            self.hitbox.bottom = sprites.hitbox.top  # Use sprites
                        if self.direction.y < 0:  # Moving up
                            self.hitbox.top = sprites.hitbox.bottom  # Use sprites
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self, dt):

        # normalizing a vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        
        # Horizontal Movement 
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)  # pygame would truncate value - round it to get the exact value
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # Vertical Movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()
        self.move(dt)
        self.animate(dt)
