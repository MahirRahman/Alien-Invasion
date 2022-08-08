import traceback

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        '''Initialize statistics.'''
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False

        # High scores should never be reset
        self.high_score = 0
        try:
            file = open('images/high_score_record.txt', 'r')
            for line in file:
                self.high_score = int(line)
            file.close()
        except:
            print('File could not be opened. High scores will not be retained')      

    def reset_stats(self):
        '''Initialize statistics that can change during the game.'''
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1