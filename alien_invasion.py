#main
import sys

import pygame
from pygame.sprite import Group

import game_functions as gf
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from alien import Alien
from button import Button

def run_game():
    pygame.init()
    pygame.mixer.init()
    ai_settings=Settings()
    screen=pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    play_button=Button(ai_settings,screen,"Start")

    stats=GameStats(ai_settings)
    sb=Scoreboard(ai_settings,screen,stats)

    ship=Ship(ai_settings,screen)

    bullets=Group()
    aliens=Group()

    gf.creat_fleet(ai_settings,screen,ship,aliens)

    alien=Alien(ai_settings,screen)
    while True:

        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets)
        
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)

run_game()