class Settings:
    '''A class to store all settings for Alien INvasion.'''
    def __init__(self):
        '''Initialize the game's settings'''
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (230,230,230)

        # Ship settings like speed
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 3.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3
        
        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 20
        # Fleet directions: 1 means -> (to the right) and -1 means <- (to the left)
        self.fleet_direction = 1

        # Dynamic settings
        self.speedup_scale = 2.0
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''Reset to first level'''
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        self.alien_points = 50

        self.fleet_direction = 1

    def increase_speed(self):
        '''Increase speed settings'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.score_scale * self.alien_points)

    