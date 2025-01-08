import pygame, sys
import random
import json
from save_system import *
from settings import *
from level import Level
import shelve

pygame.init()
font = pygame.font.SysFont("comicsansms", 30)
smallfont = pygame.font.SysFont("comicsansms", 14)
slategrey = (112, 128, 144)
lightgrey = (165, 175, 185)
blackish = (10, 10, 10)
white = (255, 255, 255)
black = (0, 0, 0)
pygame.display.set_caption('James Harvesting Farm')
startYourGame = font.render("Enter the Farm!", True, blackish)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
       
        self.clock = pygame.time.Clock()
        self.level = Level()
      

        # Initialize music player
        self.song_list = [
            'Carly Rae Jepsen - Call Me Maybe.mp3',
            'Grizzly_Hills_WoW.mp3',
            'One Direction - Night Changes.mp3'
        ]
        
        # Randomly select a song from the list  
        self.current_song_index = random.choice(range(len(self.song_list)))
        self.is_playing = False
        self.volume = 0.4  # Set initial volume level (0.0 to 1.0)
        
        pygame.mixer.music.load(self.song_list[self.current_song_index])
        pygame.mixer.music.set_volume(self.volume)
        self.is_playing = False  # Music is initially paused
        #pygame.mixer.music.play(loops=-1, start=0.0)

        # Use Comic Sans MS font with smaller size for song text
        self.font = pygame.font.SysFont('Comic Sans MS', 17)  # Even smaller font size
        

        # Define rainbow colors
        self.rainbow_colors = [
            (255, 0, 0),    # Red
            (255, 127, 0),  # Orange
            (255, 255, 0),  # Yellow
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (75, 0, 130),   # Indigo
            (148, 0, 211)   # Violet
        ]
    
    def run(self, player_name,selected_index):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Detect keypress for pausing or skipping songs
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # 'p' to pause or unpause
                        self.toggle_pause()
                    elif event.key == pygame.K_n:  # 'n' for next song
                        self.next_song()
                    elif event.key == pygame.K_v:  # 'v' to increase volume
                        self.adjust_volume(0.1)
                    elif event.key == pygame.K_b:  # 'b' to decrease volume
                        self.adjust_volume(-0.1)

            dt = self.clock.tick() / 1000  # DeltaTime
           
            self.level.run(dt,player_name)
            SaveSystem.selected_index = selected_index
            self.display_song_info()
            pygame.display.update()

    def toggle_pause(self):
        """Toggle pause for music."""
        if self.is_playing:
            pygame.mixer.music.pause()
        else:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(loops=-1, start=0.0)  # Start playing if not already playing
            else:
                pygame.mixer.music.unpause()
        self.is_playing = not self.is_playing

    def next_song(self):
        """Skip to the next song in the list."""
        self.current_song_index = (self.current_song_index + 1) % len(self.song_list)
        pygame.mixer.music.load(self.song_list[self.current_song_index])
        pygame.mixer.music.play(loops=-1, start=0.0)

    def adjust_volume(self, change):
        """Adjust the volume of the music."""
        self.volume = max(0.0, min(self.volume + change, 1.0))  # Keep volume in range [0.0, 1.0]
        pygame.mixer.music.set_volume(self.volume)

    def display_song_info(self):
        """Display current song and volume information with rainbow text when music is playing."""
        if self.is_playing:  # Only display if music is actively playing
            # Remove the '.mp3' extension from the song name
            song_name = self.song_list[self.current_song_index].replace('.mp3', '')
            
            # Display volume control above song name
            volume_text = f'Volume: {int(self.volume * 100)}%'
            volume_render = self.font.render(volume_text, True, (255, 255, 255))
            self.screen.blit(volume_render, (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 70))

            # Display the song name with rainbow effect
            x_offset = SCREEN_WIDTH - 300  # Starting X position for text (adjusted to right side)
            for i, char in enumerate(song_name):
                color = self.rainbow_colors[i % len(self.rainbow_colors)]  # Cycle through rainbow colors
                char_surface = self.font.render(char, True, color)
                self.screen.blit(char_surface, (x_offset, SCREEN_HEIGHT - 40))
                x_offset += char_surface.get_width()  # Move X position for next character

# Create the screen
screen_width = 1070
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

def create_button(x, y, width, height, hovercolor, defaultcolor):
    mouse = pygame.mouse.get_pos()
    # Mouse get pressed can run without an integer, but needs a 3 or 5 to indicate how many buttons
    click = pygame.mouse.get_pressed(3)
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hovercolor, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, defaultcolor, (x, y, width, height))

# Start menu returns true until we click the Start button
def start_menu():
    

    startText = font.render("Choose Player Profile", True, slategrey)
    newPlayerText = smallfont.render("NEW PLAYER", True, blackish)
    loadPlayerText = smallfont.render("LOAD PLAYER", True, blackish)
    exitText = smallfont.render("   EXIT   ", True, blackish)
   
    while True:
        screen.fill((0, 0, 0))
       
        # (image variable, (left, top))
       
        # The title centered Text
        screen.blit(startText, ((screen_width - startText.get_width()) / 2, 0))

        # start button (left, top, width, height)
        # start_button = create_button(screen_width - 130, 7, 125, 26, lightgrey, slategrey)

        # New Player button
        newPlayerButtton = create_button((screen_width / 2) - 100, int(screen_height * .33), 200, 50, lightgrey, slategrey)

        if newPlayerButtton:
            new_game()

        screen.blit(newPlayerText, ((screen_width / 2) - (newPlayerText.get_width() / 2), int(screen_height * .33)))


        # Load Player button
        loadPlayerButtton = create_button((screen_width / 2) - 100, screen_height / 2, 200, 50, lightgrey, slategrey)

        if loadPlayerButtton:
            load_screen()

        screen.blit(loadPlayerText, ((screen_width / 2) - (loadPlayerText.get_width() / 2), screen_height / 2))

        # Exit button
        exitButtton = create_button((screen_width / 2) - 100, screen_height - 200, 200, 50, lightgrey, slategrey)

        if exitButtton:
            pygame.quit()
            sys.exit()

        screen.blit(exitText, ((screen_width / 2) - (exitText.get_width() / 2), screen_height - 200))

        

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

       

        # Start button text
        #startbuttontext = smallfont.render("Start the Game!", True, blackish)
        #screen.blit(startbuttontext, (screen_width - 125, 9))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
       
        return True


    
def new_game():
    
    newUserName = ""
    userName = ""

    # Used to make the text grey and white when active
    nameActive = False
 

    while True:
        screen.fill((0, 0, 0))

        userNameSurface = font.render(newUserName, True, white)

        # Create the border around the text box with .Rect
        # left, top, width, height
        userNameBorder = pygame.Rect(((screen_width - userNameSurface.get_width()) / 2) - 10, screen_height * .20,
                                     userNameSurface.get_width() + 10, 50)

        # This is the text surface when the user types in their name
        screen.blit(userNameSurface, ((screen_width - userNameSurface.get_width()) / 2, screen_height * .20))

       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse and Keyboard events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if userNameBorder.collidepoint(event.pos):
                    nameActive = True
                else:
                    nameActive = False

            if event.type == pygame.KEYDOWN:
                if nameActive:
                    if event.key == pygame.K_BACKSPACE:
                        newUserName = newUserName[:-1]
                    else:
                        newUserName += event.unicode

        # Handles the click events by swtiching from white, slategrey, and black
        if nameActive:
            pygame.draw.rect(screen, white, userNameBorder, 2)
            userNamePrompt = font.render("Enter your Player Profile Name", True, white)
        else:
            pygame.draw.rect(screen, slategrey, userNameBorder, 2)
            userNamePrompt = font.render("Enter your Player Profile Name", True, slategrey)

        

        screen.blit(userNamePrompt, ((screen_width - userNamePrompt.get_width()) / 2,
                                     (screen_height * .20) + userNameSurface.get_height()))


        submitButtton = create_button((screen_width / 2) - (startYourGame.get_width() / 2) - 5, screen_height * .9,
                                      startYourGame.get_width() + 10, startYourGame.get_height(), lightgrey, slategrey)

        screen.blit(startYourGame, ((screen_width / 2) - (startYourGame.get_width() / 2), int(screen_height * .9)))

        if submitButtton:
            if newUserName != "":
                userName = newUserName
                selected_index = 0
                game = Game()
                game.run(userName,selected_index)
            else:
                print("Please enter player name or choose existing profile.")
               
         

        pygame.display.update()
     
def load_screen():
    # load the existing Profiles
    saved_player = SaveSystem.player_names

    
    
    for i, name in enumerate(saved_player):
        print(f"Loading Profile {i}: {saved_player[i]}")
        try:
            userName = saved_player[i]
            selected_index = i
        except KeyError:
            userName = "No Player Profile Saved"
        
        

   
    startYourGame = font.render("Load Player - Start Game!", True, blackish)

    profileBorder = pygame.Rect(15, 60, 300, 100)

    profileActive = False

    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if profileBorder.collidepoint(event.pos):
                    profileActive = True
                else:
                    profileActive = False

        
        if profileActive:
            welcomeName = font.render(userName, True, white)
            pygame.draw.rect(screen, white, profileBorder, 2)
        else:
            welcomeName = font.render(userName, True, slategrey)
            pygame.draw.rect(screen, black, profileBorder, 2)

        screen.blit(welcomeName, (20, 60))

            
        submitButtton = create_button((screen_width / 2) - (startYourGame.get_width() / 2) - 5, screen_height * .9,
                                      startYourGame.get_width() + 10, startYourGame.get_height(), lightgrey, slategrey)

        screen.blit(startYourGame, ((screen_width / 2) - (startYourGame.get_width() / 2), int(screen_height * .9)))

        if submitButtton:
            if userName != "No Player Profile Saved":
                game = Game()
                game.run(userName,selected_index)
            else:
                print("Please select existing profile to load.")

        pygame.display.update()



sys.dont_write_bytecode = True

#if __name__ == '__main__':


# Game loop
while True:
    start_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
