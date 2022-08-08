import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    '''THe main class that manages the game pieces and overall behavior'''
    def __init__(self):
        '''This initiates the game by creating game resources'''
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))

        # If you want to make it full screen comment line 15 and uncomment the line below
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        pygame.display.set_caption("Alien Invasion")

        # Records statistics
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bg_color = (230,230,230)

        self._create_fleet()

        #Make the Play Button
        self.play_button = Button(self, "Play")

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # As we have options for making screen full sized or any other size, we need to do a get_surface to account for different alien sizes
        screen_width, screen_height = pygame.display.get_surface().get_size()
        available_space_x = screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        number_rows = 2 #! Change

        # Create the first row of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
            # Create an alien and place it in the row
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _fire_bullets(self):
        '''Creates a new bullet and adds it our bullets list'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _ship_hit(self):
        '''Respond to ship being hit'''
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            
            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    
    def _check_aliens_bottom(self):
        '''Check if any alien reached the bottom of the screen'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        '''Drop the entire fleet and change the fleet's direction'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_fleet_edges(self):
        '''Respond appropriately if any aliens have reached an edge.'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        '''Start a new game when the player clicks Play'''
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True

            self.aliens.empty()
            self.bullets.empty()
            
            self._create_fleet()
            self.ship.center_ship()

            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()

            pygame.mouse.set_visible(False)              
                
    
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.scoreboard.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()
        # Displays the newly drawn screen

        pygame.display.flip()
    
    def _update_bullets(self):
        self.bullets.update()

        # We use copy because python expects us to keep the size of the list constant in the  loop
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Check for any bullets if they have hit an alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.stats.score += self.settings.alien_points
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.scoreboard.prep_level()

    def _update_aliens(self):
        '''Check if fleet is at and edge and then updates the position of all aliens in the fleet'''
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def run_game(self):
        '''Starts the game's main loop'''
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                
            self._update_screen()

if __name__ == '__main__':
    game = AlienInvasion()
    game.run_game()