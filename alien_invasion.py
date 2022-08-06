import sys

import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
    '''THe main class that manages the game pieces and overall behavior'''
    def __init__(self):
        '''This initiates the game by creating game resources'''
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bg_color = (230,230,230)

    def run_game(self):
        '''Starts the game's main loop'''
        while True:
            # Holds keyboard and mouse event handlers
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            # Displays the newly drawn screen
            pygame.display.flip()
if __name__ == '__main__':
    game = AlienInvasion()
    game.run_game()