import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''A class to manage bullets fired from ship'''

    def __init__(self, ai_game):
        '''Creates a bullet obj at the ship's head'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #Create a bullet rect and then set it in the right position
        self.rect = pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a decimal
        self.y = float(self.rect.y)

    def update(self):
        '''Moves the bullet up the screen'''
        # Update the decimal position of bullet
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)