import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    '''A class to manage the ship'''
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Loads the ship image and gets its rectangle
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect() 
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self):
        '''Ship position is updated based on the movement flag'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # This allows us to record the changes in self.x to our rectangle
        self.rect.x = self.x

    def blitme(self):
        '''Draws the ship in its current position'''
        self.screen.blit(self.image, self.rect)
