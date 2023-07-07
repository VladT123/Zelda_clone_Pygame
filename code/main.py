import pygame
import sys
from settings import *
from debug import debug
from level import Level
from player import Player
 

class Game:
    def __init__(self):

        # Gen Setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Zelda')
        self.clock = pygame.time.Clock()
        self.level = Level()

        # sound
        main_sound = pygame.mixer.Sound('../audio/zelda.wav')
        main_sound.set_volume(0.1)
        main_sound.play(loops=-1)

    def check_game_over(self):
        if not self.level.player.alive:
            self.level.player.stats = self.level.player.base_stats
            game.run()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()
            self.screen.fill(WATER_COLOR)
            self.level.run()
            # self.check_game_over()

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
