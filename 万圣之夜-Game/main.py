# -*- coding: utf-8 -*-
import pygame
import sys
import traceback
import myplane
import enemy
import bullet
import supply
from random import *
from pygame.locals import *


pygame.init()
pygame.mixer.init()

bg_size=width,height=500,650
screen = pygame.display.set_mode(bg_size, 0, 32)
pygame.display.set_caption("打飞机")
background = pygame.image.load('images/background.jpg').convert()
White = (255,255,255)
Red = (255,0,0)
Green = (0,255,0)
Black = (0,0,0)

#载入音乐
pygame.mixer.music.load("musics/bgmusic.ogg")
pygame.mixer.music.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("musics/9135.ogg")
upgrade_sound.set_volume(0.4)
bomb_sound = pygame.mixer.Sound("musics/6688.ogg")
bomb_sound.set_volume(0.3)

def  add_small_enemies(group1,group2,num):
    for i in range(num):
        e1=enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)
def  add_mid_enemies(group1,group2,num):
    for i in range(num):
        e2=enemy.MiddleEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)
def  add_big_enemies(group1,group2,num):
    for i in range(num):
        e3=enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)
def add_speed(target, add):
    for e in target:
        e.speed += add


is_star = False
running = True


def main():
    global is_star
    pygame.mixer.music.play(-1)
    #开始画面
    star_background_image = pygame.image.load("images/star_background.png").convert_alpha()
    star_background_rect = star_background_image.get_rect()
    stargame_image = pygame.image.load("images/stargame_image.png").convert_alpha()
    stargame_font = pygame.font.Font("type/FZXQJW.TTF", 20) 
    #等级
    level = 1

    #生成飞机
    player = myplane.MyPlane(bg_size)

    #生成敌军
    enemies = pygame.sprite.Group()
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies,enemies,15)
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies,enemies,5)
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies,enemies,2)

    #生成普通子弹
    bullets = []
    bullet1 = []
    bullet1_index = 0
    bullet1_num = 4
    for i in range(bullet1_num):
        bullet1.append(bullet.Bullet(player.rect.midtop))

    #生成Double子弹
    bullet2 = []
    bullet2_index = 0
    bullet2_num = 8
    for i in range(bullet2_num//2):
        bullet2.append(bullet.Bullet2((player.rect.centerx-30,player.rect.centery)))
        bullet2.append(bullet.Bullet2((player.rect.centerx+27,player.rect.centery)))

    #生命数量
    life_image = pygame.image.load("images/plane1.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_font = pygame.font.Font("type/NeonTech.ttf", 30)
    

    #全屏炸弹
    bomb_font = pygame.font.Font("type/NeonTech.ttf", 48)
    bomb_num = 3
    bomb_image = pygame.image.load("images/Bomb_Supply1.png").convert_alpha()

    #发放补给
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, 30*1000)


    #Double 子弹
    DOUBLEBULLET_TIME = USEREVENT + 1
    shoot_double_bullet = False

    #重生护盾
    INVINCIBLE_TIME = USEREVENT + 2

    
    #统计得分
    score = 0
    score_font = pygame.font.Font("type/NeonTech.ttf", 36)

    #更新分数
    recorded = False

    #结束画面
    new_score_font = pygame.font.Font("type/NeonTech.ttf", 55)    
    gameover_image = pygame.image.load("images/quitgame_image.png").convert_alpha()
    newgame_image = pygame.image.load("images/newgame_image.png").convert_alpha()
    

    #检测暂停
    paused = False
    paused_nor_image =pygame.image.load("images/paused_nor_image.png").convert_alpha()
    paused_pressed_image =pygame.image.load("images/paused_pressed_image.png").convert_alpha()
    resume_nor_image =pygame.image.load("images/resume_nor_image.png").convert_alpha()
    resume_pressed_image =pygame.image.load("images/resume_pressed_image.png").convert_alpha()
    paused_rect = paused_nor_image.get_rect()
    paused_rect.left,paused_rect.top = width-paused_rect.width-10, 10
    paused_image =paused_nor_image
    
    clock = pygame.time.Clock()

    

    #延迟
    delay = 0
    
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                         pygame.mixer.music.pause()
                         pygame.time.set_timer(SUPPLY_TIME, 0)
                    else:
                        pygame.mixer.music.unpause()
                        pygame.time.set_timer(SUPPLY_TIME, 30*1000)
                        
            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        pause_image = resume_pressed_image
                    else:
                        paused_image = paused_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = paused_nor_image
            elif  event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_sound.play()
                        bomb_num -= 1
                        for e in enemies:
                            if e.rect.bottom >0:
                                e.active = False
            elif event.type == SUPPLY_TIME:
                if choice([True,False]):
                    bullet_supply.restar()
                else:
                    bomb_supply.restar()
            elif event.type == DOUBLEBULLET_TIME:
                shoot_double_bullet = False
                pygame.time.set_timer( DOUBLEBULLET_TIME, 0)
            elif event.type == INVINCIBLE_TIME:
                player.invincible = False
                pygame.time.set_timer( INVINCIBLE_TIME, 0)

        screen.blit(background,(0,0))
        
        #开始界面
        if not is_star:
            screen.blit(star_background_image, star_background_rect)
            stargame_rect = stargame_image.get_rect()
            stargame_rect.left, stargame_rect.top = 320,500
            screen.blit(stargame_image, stargame_rect)
            if pygame.mouse.get_pressed()[0]:
                pos_one= pygame.mouse.get_pos()
                if stargame_rect.left < pos_one[0] < stargame_rect.right and\
                       stargame_rect.top < pos_one[1] < stargame_rect.bottom:
                    is_star = True
               

        
        
        #增加等级
        if level == 1  and score > 2000:
            level = 2
            upgrade_sound.play()
            add_small_enemies(small_enemies,enemies,3)
            add_mid_enemies(mid_enemies,enemies,2)
            add_big_enemies(big_enemies,enemies,1)
            add_speed(small_enemies,1)           
        elif level == 2  and score > 8000:
             level = 3
             upgrade_sound.play()
             add_small_enemies(small_enemies,enemies,5)
             add_mid_enemies(mid_enemies,enemies,3)
             add_big_enemies(big_enemies,enemies,1)
             add_speed(small_enemies,1)
             add_speed(mid_enemies,1)
             add_speed(big_enemies,1) 
        elif level == 3  and score > 20000:
             level = 4
             upgrade_sound.play()
             add_small_enemies(small_enemies,enemies,5)
             add_mid_enemies(mid_enemies,enemies,3)
             add_big_enemies(big_enemies,enemies,2)
             add_speed(small_enemies,1)
             add_speed(mid_enemies,1)
             add_speed(big_enemies,1)
        elif level == 4  and score > 40000:
             level = 5
             upgrade_sound.play()
             add_small_enemies(small_enemies,enemies,5)
             add_mid_enemies(mid_enemies,enemies,3)
             add_big_enemies(big_enemies,enemies,2)
             add_speed(small_enemies,1)
             add_speed(mid_enemies,1)
             add_speed(big_enemies,1) 


        if player.life and not paused and is_star: 
            #检测飞机运动
            key_pressed = pygame.key.get_pressed()

            if key_pressed[K_UP]:
                player.moveUp()
            if key_pressed[K_DOWN]:
                player.moveDown()
            if key_pressed[K_LEFT]:
                player.moveLeft()
            if key_pressed[K_RIGHT]:
                player.moveRight()
           

            #发射子弹
            if not(delay % 10):
                if shoot_double_bullet:
                    bullets = bullet2
                    bullet2[bullet2_index].restar((player.rect.centerx-30,player.rect.centery))
                    bullet2[bullet2_index + 1].restar((player.rect.centerx+27,player.rect.centery))
                    bullet2_index = (bullet2_index + 2) % bullet2_num
                else:
                    bullets = bullet1
                    bullet1[bullet1_index].restar(player.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % bullet1_num

            #子弹是否碰撞
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image,b.rect)
                    enemies_hit = pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
                    if enemies_hit:
                        b.active = False
                        for e in enemies_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.life -= 1
                                if e.life == 0:
                                    e.active = False
                            else:
                                e.active = False
                
                   
            #绘制全屏炸弹补给
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, player):
                    if bomb_num <3:
                        bomb_num += 1
                    bomb_supply.active = False

            #绘制Double子弹补给
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, player):
                    shoot_double_bullet = True
                    pygame.time.set_timer(   DOUBLEBULLET_TIME , 20*1000)
                    bullet_supply.active = False

            #绘制敌军
            #小型敌机
            for e in  small_enemies:
                if e.active:
                    e.move()
                    screen.blit(e.image,e.rect)
                #毁灭
                else:
                    screen.blit(e.destory_image,e.rect)
                    if not (delay % 3):
                        score += 100
                        e.restar()

            #中型敌机
            for e in mid_enemies:
                if e.active:
                    e.move()
                    screen.blit(e.image,e.rect)
                    #绘制血槽
                    pygame.draw.line(screen,Black,(e.rect.left, e.rect.top - 5),(e.rect.right, e.rect.top - 5),2)
                    enemy_remain = e.life / enemy.MiddleEnemy.life
                    if enemy_remain > 0.2:
                        remain_color = Green
                    else:
                        remain_color = Red
                    pygame.draw.line(screen,remain_color,(e.rect.left, e.rect.top - 5),\
                                         (e.rect.left +  e.rect.width*enemy_remain, e.rect.top - 5),2)

                #毁灭
                else:
                    screen.blit(e.destory_image,e.rect)
                    if not (delay % 3):
                        score += 500
                        e.restar()

            #大型敌机                
            for e in  big_enemies:
                if e.active:
                    e.move()
                    screen.blit(e.image,e.rect)
                    #绘制血槽
                    pygame.draw.line(screen,White,(e.rect.left, e.rect.top - 5),(e.rect.right, e.rect.top - 5),2)
                    enemy_remain = e.life / enemy.BigEnemy.life
                    if enemy_remain > 0.2:
                        remain_color = Green
                    else:
                        remain_color = Red
                    pygame.draw.line(screen,remain_color,(e.rect.left, e.rect.top - 5),\
                                         (e.rect.left + e.rect.width*enemy_remain, e.rect.top - 5),2)
                #毁灭
                else:
                    screen.blit(e.destory_image,e.rect)
                    if not (delay % 3):
                        score += 1000
                        e.restar()

            #检验飞机是否碰撞
            if not player.invincible:
                enemies_down = pygame.sprite.spritecollide(player,enemies,False,pygame.sprite.collide_mask)
                if enemies_down:
                    player.life -= 1
                    if not (delay % 10):
                        screen.blit(player.destory_image,player.rect)
                    player.restar()
                    pygame.time.set_timer(INVINCIBLE_TIME, 3*1000)
                    for e in enemies_down:
                        e.active = False

            #绘制我机
            if player.active:
                screen.blit(player.image,player.rect)
            else:
                #毁灭
                if not (delay % 3):
                    screen.blit(player.destory_image,e.rect)

            #绘制分数
            score_text = score_font.render("score: %d" %(score),True,White)
            screen.blit(score_text,(10,5))
            #绘制全屏炸弹
            bomb_text = score_font.render("x %d" %(bomb_num),True,White)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_text,(80, height-15-text_rect.height))
            screen.blit(bomb_image,(0, height-100))
            #绘制生命数
            life_text = life_font.render(" x %d" %(player.life),True,White)
            life_text_rect = life_text.get_rect()
            screen.blit(life_text,(width-life_text_rect.width-10,\
                                   height-15-life_text_rect.height))
            screen.blit(life_image,(width-life_rect.width-life_text_rect.width+10,\
                                    height-life_rect.height))
            
        #游戏结束
        elif player.life == 0:
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            pygame.time.set_timer( SUPPLY_TIME, 0)
            if not recorded:
                with open("record.txt","r") as f:
                    record_score = int(f.read())
                recorded = True
                if score > record_score:
                    with open("record.txt","w") as f:
                        f.write(str(score))
        
            #绘制结束界面
            best_score_text = score_font.render("best score: %d" %(record_score),True,White)
            screen.blit(best_score_text,(10,5))
            new_score_text1= new_score_font.render("Your Score" ,True,White)
            new_score_text1_rect = new_score_text1.get_rect()
            new_score_text1_rect.left,new_score_text1_rect.top = \
                                                               (width - new_score_text1_rect.width) / 2, 150           
            screen.blit(new_score_text1, new_score_text1_rect)
            new_score_text2= new_score_font.render("%d" %(score),True,White)
            new_score_text2_rect = new_score_text2.get_rect()
            new_score_text2_rect.left,  new_score_text2_rect.top =\
                                       (width - new_score_text2_rect.width) / 2,\
                                       new_score_text1_rect.bottom+20
            screen.blit(new_score_text2, new_score_text2_rect)
            gameover_rect = gameover_image.get_rect()
            gameover_rect.left, gameover_rect.top =\
                              (width - gameover_rect.width) / 2 , new_score_text2_rect.bottom-20
            screen.blit(gameover_image, gameover_rect)
            newgame_rect = newgame_image.get_rect()
            newgame_rect.left,  newgame_rect.top = \
                               (width-newgame_rect.width) / 2, gameover_rect.bottom-50
            screen.blit(newgame_image,newgame_rect)
            #检测鼠标操作
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if newgame_rect.left < pos[0] < newgame_rect.right and\
                   newgame_rect.top < pos[1] < newgame_rect.bottom:
                    main()
                elif gameover_rect.left < pos[0] < gameover_rect.right and\
                  gameover_rect.top < pos[1] < gameover_rect.bottom:
                    pygame.quit()
                    exit()

        #绘制暂停
        screen.blit(paused_image, paused_rect)
            
        delay += 1
        if delay == 100:
            delay = 0



        pygame.display.flip()
        clock.tick(60)


        

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
    
























