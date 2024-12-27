import pygame
from settings import *

class Overlay:
    def __init__(self, player, display_surface):        
        # General setup
        self.display_surface = display_surface
        self.player = player
        self.font = pygame.font.SysFont('Arial', 24)  # Set font and size
        self.color = (79, 54, 41)  # Deep Brown color (Wooden shade)

        # Item images
        overlay_path = 'graphics/overlay/'  # Path to your item images
        self.item_images = {
            'wood': pygame.image.load(f'{overlay_path}wood.png').convert_alpha(),
            'apple': pygame.image.load(f'{overlay_path}apple.png').convert_alpha(),
            'corn': pygame.image.load(f'{overlay_path}corn.png').convert_alpha(),
            'tomato': pygame.image.load(f'{overlay_path}tomato.png').convert_alpha()
        }

        # Adjust the size of the images (optional, based on your UI design)
        for key in self.item_images:
            self.item_images[key] = pygame.transform.scale(self.item_images[key], (32, 32))  # Scaling images to fit

        # Tools and seeds
        self.tools_surf = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in player.tools}
        self.seeds_surf = {seed: pygame.image.load(f'{overlay_path}{seed}.png').convert_alpha() for seed in player.seeds}

    def display(self):
        # Display tools
        tool_surf = self.tools_surf[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(midbottom=OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(tool_surf, tool_rect)

        # Display seed
        seed_surf = self.seeds_surf[self.player.selected_seed]
        seed_rect = seed_surf.get_rect(midbottom=OVERLAY_POSITIONS['seed'])
        self.display_surface.blit(seed_surf, seed_rect)

        # Display inventory with images and text
        y_offset = 20  # Starting y position for the inventory display
        for item, count in self.player.item_inventory.items():
            item_image = self.item_images.get(item)

            if item_image:
                # Display the image next to the text
                image_rect = item_image.get_rect(topleft=(10, y_offset))
                self.display_surface.blit(item_image, image_rect)

                # Render the text
                text = f'{item.capitalize()}: {count}'
                render_text = self.font.render(text, True, self.color)
                
                # Vertically center the text relative to the item image
                text_rect = render_text.get_rect(midleft=(image_rect.right + 10, image_rect.centery))
                self.display_surface.blit(render_text, text_rect)

            y_offset += 40  # Move down for the next line (image + text)
