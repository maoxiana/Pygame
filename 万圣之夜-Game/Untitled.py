﻿#载入音乐
pygame.mixer.music.load()
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.music.Sound()
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.music.Sound()
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.music.Sound()
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.music.Sound()
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.music.Sound()
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.music.Sound()
upgrade_sound.set_volume(0.2)
enemy1_sound = pygame.mixer.music.Sound()
enemy1_sound.set_volume(0.1)
enemy2_sound = pygame.mixer.music.Sound()
enemy2_sound.set_volume(0.2)
enemy3_sound = pygame.mixer.music.Sound()
enemy3_sound.set_volume(0.5)
gameover_sound = pygame.mixer.music.Sound()
gameover_sound.set_volume(0.2)

    pygame.mixer.music.play(-1)
