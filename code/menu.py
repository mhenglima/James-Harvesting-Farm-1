import pygame
from settings import *
from timer1 import *



class Menu:
    def __init__(self, player, toggle_menu):

        #general setup
        self.player = player #turn player into attribute
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('font/LycheeSoda.ttf', 30)

        #Options
        self.width = 400
        self.space = 10
        self.padding = 8

        #Entries
        self.options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())
        self.sell_boarder = len(self.options) - len(self.player.seed_inventory) - 1
        self.setup()

        #movement
        self.index = 0
        self.timer = Timer(200)

    def display_money(self):
        text_surf = self.font.render(f'${self.player.money}', False, 'black')
        text_rect = text_surf.get_rect(midbottom = (SCREEN_WIDTH/2, SCREEN_HEIGHT - 20)) #offsetted from bottom of window

        pygame.draw.rect(self.display_surface, 'white', text_rect.inflate(10, 10),0, 6) #determines rounding
        self.display_surface.blit(text_surf, text_rect)

    def setup(self):

        # Dynamically refresh the options
        self.options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())
        self.sell_boarder = len(self.player.item_inventory) - 1

        #create the text surfaces
        self.text_surfaces = []
        self.total_height = 0

        for item in self.options:
            text_surf = self.font.render(item, False, 'black')
            self.text_surfaces.append(text_surf)
            self.total_height += text_surf.get_height() + (self.padding * 2)

        self.total_height += (len(self.text_surfaces) - 1) * self.space
        self.menu_top = SCREEN_HEIGHT/2 - self.total_height /2
        self.main_rect = pygame.Rect(SCREEN_WIDTH/2 - self.width/2,self.menu_top,self.width,self.total_height)

        #buy or sell surface
        self.buy_text = self.font.render('buy',False,'black')
        self.sell_text = self.font.render('sell',False,'black')

    def input(self):
        #if player hits escape then exit the menu
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

        if not self.timer.active:
            if keys[pygame.K_UP]:
                self.index -= 1
                self.timer.activate()

            if keys[pygame.K_DOWN]: #checks 100 times per second - register 20 times even if press once
                self.index += 1
                self.timer.activate()

            if keys[pygame.K_SPACE]:
                self.timer.activate()

                #get item
                current_item = self.options[self.index]
                #print(current_item)

                #sell item
                if self.index <= self.sell_boarder:
                    current_item = self.options[self.index]
                    if self.player.item_inventory.get(current_item, 0) > 0:
                        if current_item in SALE_PRICES:
                            self.player.item_inventory[current_item] -= 1
                            self.player.money += SALE_PRICES[current_item]
                            #print(f"Sold {current_item} for ${SALE_PRICES[current_item]}")
                        #else:
                            #print(f"[WARNING] No sale price defined for {current_item}")

                #buy item
                else:
                    seed_price = PURCHASE_PRICES[current_item]
                    if self.player.money >= seed_price:
                        self.player.seed_inventory[current_item] += 1
                        self.player.money -= PURCHASE_PRICES[current_item]


        #claim the values
        if self.index < 0:
            self.index = len(self.options) - 1
        if self.index > len(self.options) - 1:
            self.index = 0

    def show_entry(self, text_surf, amount, top, selected):

        #background
        bg_rect = pygame.Rect(self.main_rect.left,top,self.width,text_surf.get_height() + self.padding * 2)
        pygame.draw.rect(self.display_surface, 'white', bg_rect, 0, 4)

        #text
        text_rect = text_surf.get_rect(midleft = (self.main_rect.left + 20,bg_rect.centery))
        self.display_surface.blit(text_surf, text_rect)

        #amount
        amount_surf = self.font.render(str(amount), False, 'black') #String for render method
        amount_rect = amount_surf.get_rect(midright = (self.main_rect.right - 20 , bg_rect.centery))
        self.display_surface.blit(amount_surf,amount_rect)

        #selected
        if selected:
            pygame.draw.rect(self.display_surface, 'black', bg_rect, 4, 4)
            if self.index <= self.sell_boarder: #sell
                pos_rect = self.sell_text.get_rect(midleft =(self.main_rect.left + 150 ,bg_rect.centery))
                self.display_surface.blit(self.sell_text, pos_rect)
            else: #buy
                pos_rect = self.buy_text.get_rect(midleft =(self.main_rect.left + 150 ,bg_rect.centery))
                self.display_surface.blit(self.buy_text, pos_rect)

    def update(self):
        self.input()
        self.display_money()
        for text_index, text_surf in enumerate(self.text_surfaces):
            top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
            amount_list = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values())
            amount = amount_list[text_index]
            self.show_entry(text_surf, amount, top, self.index == text_index)