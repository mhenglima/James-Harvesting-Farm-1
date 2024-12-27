import pygame
from settings import *

class Overlay:
    def __init__(self, player, display_surface):        
        #general setup
        self.display_surface = display_surface
        self.player = player
        self.font = pygame.font.SysFont('Arial', 24)  # Set font and size
        self.color = (255, 255, 255)  # White text

        # Use self to reference instance variables
        overlay_path = 'graphics/overlay/'
        self.tools_surf = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in player.tools}
        self.seeds_surf = {seed: pygame.image.load(f'{overlay_path}{seed}.png').convert_alpha() for seed in player.seeds}

    def display(self):
        #tools
        tool_surf = self.tools_surf[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(midbottom = OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(tool_surf,tool_rect)

        #seed
        seed_surf = self.seeds_surf[self.player.selected_seed]
        seed_rect = seed_surf.get_rect(midbottom = OVERLAY_POSITIONS['seed'])
        self.display_surface.blit(seed_surf,seed_rect)

        # Display inventory in the top-left corner
        inventory_text = 'Inventory:'
        y_offset = 20  # Starting y position for the inventory display
        for item, count in self.player.item_inventory.items():
            text = f'{item.capitalize()}: {count}'
            render_text = self.font.render(text, True, self.color)
            self.display_surface.blit(render_text, (10, y_offset))
            y_offset += 30  # Move down for the next line