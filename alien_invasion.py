import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    '''THe main class that manages the game pieces and overall behavior'''
    def __init__(self):
        '''This initiates the game by creating game resources'''
        pygame.init()
        self.settings = Settings()

        # self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))

        # If you want to make it full screen comment line 15 and uncomment the block of code below
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.bg_color = (230,230,230)

    def _fire_bullets(self):
        '''Creates a new bullet and adds it our bullets list'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    def _check_keydown_events(self, event):
        # Responds to key presses         
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullets()

    def _check_keyup_events(self,event):
        # Responds to key releases
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _check_events(self):
        # Holds keyboard and mouse event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
                
                
    
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Displays the newly drawn screen
        pygame.display.flip()
    
    def _update_bullets(self):
        self.bullets.update()

        # We use copy because python expects us to keep the size of the list constant in the  loop
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def run_game(self):
        '''Starts the game's main loop'''
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

if __name__ == '__main__':
    game = AlienInvasion()
    game.run_game()