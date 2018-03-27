import pygame
from random import *

class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/enemy.png").convert_alpha()
        self.destory_image = pygame.image.load("images/destory_image.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = \
                        randint(0,self.width-self.rect.width),\
                        randint(-5*self.height,0)
        self.speed =3
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.bottom < self.height:
            self.rect.top += self.speed
        else:
            self.restar()

    def restar(self):
        self.active = True
        self.rect.left, self.rect.top = \
                        randint(0,self.width-self.rect.width),\
                        randint(-5*self.height,0)

class MiddleEnemy(pygame.sprite.Sprite):
    life = 8.0
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/midenemy.png").convert_alpha()
        self.destory_image = pygame.image.load("images/destory_image.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = \
                        randint(0,self.width-self.rect.width),\
                        randint(-10*self.height,-self.height)
        self.speed = 2
        self.active = True
        self.life = MiddleEnemy.life
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.bottom < self.height:
            self.rect.top += self.speed
        else:
            self.restar()

    def restar(self):
        self.life = MiddleEnemy.life
        self.active = True
        self.rect.left, self.rect.top = \
                        randint(0,self.width-self.rect.width),\
                        randint(-10*self.height,-self.height)
        

class BigEnemy(pygame.sprite.Sprite):
    life = 20.0
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/bigenemy.png").convert_alpha()
        self.destory_image = pygame.image.load("images/destory_image.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = \
                        randint(0,self.width-self.rect.width),\
                        randint(-15*self.height,-8*self.height)
        self.speed = 0.5
        self.active = True
        self.life = BigEnemy.life
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.bottom < self.height:
            self.rect.top += self.speed
        else:
            self.restar()

    def restar(self):
        self.life = BigEnemy.life
        self.active = True
        self.rect.left, self.rect.top = \
                        randint(0,self.width-self.rect.width),\
                        randint(-15*self.height,-8*self.height)






