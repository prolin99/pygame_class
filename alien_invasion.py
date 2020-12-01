import sys
import pygame
#import game_functions as gf
from game_functions import Game_functions


def run_game():
    pygame.init()
    pygame.display.set_caption("Alien Invasion")
    gm = Game_functions()



    while True:
        #if gm.stats.game_active:
        gm.check_events()
            #gm.update_ship()
            #gm.update_bullets()
        gm.update_screen()

run_game()
