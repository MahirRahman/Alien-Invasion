import pygame

class Ship:
    '''A class to manage the ship'''
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Loads the ship image and gets its rectangle
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect() 
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        '''Draws the ship in its current position'''
        self.screen.blit(self.image, self.rect)
