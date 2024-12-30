import pygame
from settings import *

class Menu:
    def __init__(self, player, toggle_menu):

        #general setup
        self.player = player #turn player into attribute
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('font/LycheeSoda.ttf', 30)

    def input(self):
        #if player hits escape then exit the menu
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()


    def update(self):
        self.input()
        self.display_surface.blit(pygame.Surface((1000,1000)), (0,0))
