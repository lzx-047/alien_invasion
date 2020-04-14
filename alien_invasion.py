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

    gf.creat_fleet(ai_settings,screen,ship,aliens,stats)

    alien=Alien(ai_settings,stats,screen)
    print("The score of aliens:")
    while True:

        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets)
        
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)
#the rules of game
print(
'''1.进入游戏后，点击Start开始游戏，这时屏幕上方的外星人就会开始移动
2.通过电脑键盘的左右键来操控飞船在窗口中左右移动，同时按下空格键可以发射子弹击杀外星人
3.当外星人碰到飞船或碰到窗口底部后，您就失败了，同时，左上角的剩余飞船数就会-1
4.按下快捷键Q就可以快速结束游戏;R:重置游戏
附加说明:
1.在左上角的点数就是本场的点数，玩家可以通过击杀外星人来获得点数
2.最中间的是本场最高分；最左边的飞船图案就是您剩余的飞船数目，当飞船数目没有时，游戏就将重新开始，得分点数就将清零，等级也将会重置
3.在飞船被击中时,系统就会统计得分。当得分是最高分的两倍时，将恢复并奖励一艘飞船
4.当每一波外星人击杀完成后，游戏自动就会进入下一级，外星人的点数就会提高，这时在终端窗口就会显示本级外星人的击杀点数。
如果您认真阅读完此教程,请按下Enter以继续:
''')
agree=input()

run_game()