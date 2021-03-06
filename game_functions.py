import sys

import pygame
from time import sleep

from bullet import Bullet
from alien import Alien


def check_keydown_events(event,ai_settings,screen,ship,bullets,stats,sb,aliens):
    if event.key==pygame.K_RIGHT or event.key==pygame.K_d:
        ship.moving_right=True
    elif event.key==pygame.K_LEFT or event.key==pygame.K_a:
        ship.moving_left=True
    elif event.key==pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key==pygame.K_q:
        pygame.mixer.music.stop()
        sys.exit()
    elif event.key==pygame.K_r:
        stats.ships_left=3
        pygame.mixer.music.load("./musics/game_bgm.mp3")
        pygame.mixer.music.play(-1)
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active=True

        sb.prep_score()
        sb.prep_high_score()
        sb.stats.level=1
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        creat_fleet(ai_settings,screen,ship,aliens,stats)
        ship.center_ship()

def fire_bullet(ai_settings,screen,ship,bullets):
    #创建新子弹加入到编组“bullets”中
    if len(bullets)<ai_settings.bullets_allowed:
        new_bullet=Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def check_keyup_events(event,ship):
    if event.key==pygame.K_RIGHT or event.key==pygame.K_d:
        ship.moving_right=False
    elif event.key==pygame.K_LEFT or event.key==pygame.K_a:
        ship.moving_left=False

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.mixer.music.stop()
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets,stats,sb,aliens)
        elif event.type==pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)   

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):

    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mixer.music.load("./musics/game_bgm.mp3")
        pygame.mixer.music.play(-1)
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active=True

        sb.prep_score()
        sb.prep_high_score()
        sb.stats.level=1
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        creat_fleet(ai_settings,screen,ship,aliens,stats)
        ship.center_ship()
        #重置游戏机制
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    #更新子弹位置
    bullets.update()
    #删除出了屏幕的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)
    
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):

    collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)

    if collisions:
        for aliens in collisions.values():
            stats.score+=ai_settings.alien_points*len(aliens)
            sb.prep_score()
        check_high_score(ai_settings,stats,sb)

    if len(aliens)==0:
        bullets.empty()
        ai_settings.increase_speed()
        creat_fleet(ai_settings,screen,ship,aliens,stats)
        stats.level+=1
        sb.prep_level()

def get_number_aliens_x(ai_settings,alien_width):

    available_space_x=ai_settings.screen_width-2*alien_width
    number_aliens_x=int(available_space_x/(2*alien_width))
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):

    available_space_y=(ai_settings.screen_height-(3*alien_height)-ship_height)
    number_rows=int(available_space_y/(2*alien_height))
    return number_rows

def creat_alien(ai_settings,stats,screen,aliens,alien_number,row_number):

    alien=Alien(ai_settings,stats,screen)
    alien_width=alien.rect.width
    alien.x=alien_width+2*alien_width*alien_number
    alien.rect.x=alien.x
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)

def creat_fleet(ai_settings,screen,ship,aliens,stats):

    alien=Alien(ai_settings,stats,screen)
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            creat_alien(
                ai_settings,stats,screen,aliens,alien_number,row_number
                )

def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break
def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction*=-1

def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
    if stats.ships_left>0:
        stats.ships_left-=1

        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        creat_fleet(ai_settings,screen,ship,aliens,stats)
        ship.center_ship()
        sleep(1)
        

    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,stats,screen,sb,ship,aliens,bullets):
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
            break

def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
    
    check_aliens_bottom(ai_settings,stats,screen,sb,ship,aliens,bullets)

def check_high_score(ai_settings,stats,sb):
    if stats.score>stats.high_score:
        if stats.score>=stats.high_score*2:
            stats.ships_left+=1
        stats.high_score=stats.score
        sb.prep_high_score()