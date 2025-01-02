import pygame, sys
import random
from settings import *
from level import Level 

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('James Harvesting Farm')
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
    
    def run(self):
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
            self.level.run(dt)
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

sys.dont_write_bytecode = True

if __name__ == '__main__':
    game = Game()
    game.run()
