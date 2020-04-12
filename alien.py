import pygame
from pygame.sprite import Sprite

class Alien(Sprite):

    def __init__(self,ai_settings,stats,screen):
        super().__init__()
        self.screen=screen
        self.ai_settings=ai_settings

        if stats.level==1:
            self.image=pygame.image.load(r"./images/alien.bmp")
        if 1<stats.level<=3:
            self.image=pygame.image.load(r"./images/alien_2.bmp")
        if 3<stats.level<=5:
            self.image=pygame.image.load(r"./images/alien_3.bmp")
        if 5<stats.level<=7:
            self.image=pygame.image.load(r"./images/alien_4.bmp")
        if 7<stats.level<=9:
            self.image=pygame.image.load(r"./images/alien_5.bmp")
        if 9<stats.level<=11:
            self.image=pygame.image.load(r"./images/alien_6.bmp")
        if stats.level>11:
            self.image=pygame.image.load(r"./images/alien_7.bmp")
        self.rect=self.image.get_rect()

        self.rect.x=self.rect.width
        self.rect.y=self.rect.height

        self.x=float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image,self.rect)
        
    def check_edges(self):
        screen_rect=self.screen.get_rect()
        if self.rect.right>=screen_rect.right:
            return True
        elif self.rect.left<=0:
            return True

    def update(self):
        self.x+=(self.ai_settings.alien_speed_factor*self.ai_settings.fleet_direction)
        self.rect.x=self.x