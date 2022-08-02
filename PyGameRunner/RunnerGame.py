import pygame
import random
import sys


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        walk1 = pygame.image.load("graphics/player_walk_1.png").convert_alpha()
        walk2 = pygame.image.load("graphics/player_walk_2.png").convert_alpha()
        self.player_jump = pygame.image.load("graphics/jump.png").convert_alpha()
        self.player_walk = [walk1, walk2]
        self.player_walk_index = 0
        self.image = self.player_walk[self.player_walk_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.jump_sound = pygame.mixer.Sound("sound/audio_jump.mp3")
        self.jump_sound.set_volume(.3)
        self.gravity = 0
        self.jump_count= 0

    def player_input(self, floor_rect):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.jump_count == 0:
            self.gravity = -14
            self.jump_count = 1
            self.jump_sound.play()

    def apply_gravity(self, floor_rect):
        self.rect.y += self.gravity
        if self.rect.colliderect(floor_rect) is False:
            self.gravity += .6
        else:
            self.jump_count = 0
            self.rect.bottom = floor_rect.top+1

    def update(self, floor_rect):
        self.apply_gravity(floor_rect)
        self.animation_state(floor_rect)
        self.player_input(floor_rect)

    def animation_state(self, floor_rect):
        if self.rect.colliderect(floor_rect) is False:
            self.image = self.player_jump
        else:
            self.image = self.player_walk[int(self.player_walk_index)]
            self.player_walk_index += .1
            if self.player_walk_index >= len(self.player_walk):
                self.player_walk_index = 0


class Enemy(pygame.sprite.Sprite):

    def __init__(self, creature_type):
        super().__init__()
        self.type = creature_type
        self.size = 1
        self.speed =6
        if self.type == "Fly":
            fly_frame1 = pygame.image.load("graphics/Fly1.png").convert_alpha()
            fly_frame2 = pygame.image.load("graphics/Fly2.png").convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            self.speed = 6
            y_pos = random.randint(170, 270)
        elif self.type == "ScaryFly":
            self.size = 1.2
            scary_fly_frame1 = pygame.image.load("graphics/ScaryFly1.png").convert_alpha()
            scary_fly_frame2 = pygame.image.load("graphics/ScaryFly2.png").convert_alpha()
            scary_fly_frame1 = pygame.transform.rotozoom(scary_fly_frame1, 0, self.size)
            scary_fly_frame2 = pygame.transform.rotozoom(scary_fly_frame2, 0, self.size)
            self.frames = [scary_fly_frame1, scary_fly_frame2]
            self.speed = 7
            y_pos = random.randint(170, 270)
        elif self.type == "BlackSnail":
            black_snail_frame1 = pygame.image.load("graphics/BlackSnail1.png").convert_alpha()
            black_snail_frame2 = pygame.image.load("graphics/BlackSnail2.png").convert_alpha()
            self.frames = [black_snail_frame1, black_snail_frame2]
            self.size = 1
            self.speed = 7
            y_pos = 300
        elif self.type == "BlueSnail":
            self.size = .7
            blue_snail_frame1 = pygame.image.load("graphics/BlueSnail1.png").convert_alpha()
            blue_snail_frame2 = pygame.image.load("graphics/BlueSnail2.png").convert_alpha()
            blue_snail_frame1 = pygame.transform.rotozoom(blue_snail_frame1, 0, self.size)
            blue_snail_frame2 = pygame.transform.rotozoom(blue_snail_frame2, 0, self.size)
            self.frames = [blue_snail_frame1, blue_snail_frame2]
            self.speed = 9
            y_pos = 300
        elif self.type == "GreenSnail":
            self.size = 1.7
            green_snail_frame1 = pygame.image.load("graphics/GreenSnail1.png").convert_alpha()
            green_snail_frame2 = pygame.image.load("graphics/GreenSnail2.png").convert_alpha()
            green_snail_frame1 = pygame.transform.rotozoom(green_snail_frame1, 0, self.size)
            green_snail_frame2 = pygame.transform.rotozoom(green_snail_frame2, 0, self.size)
            self.frames = [green_snail_frame1, green_snail_frame2]
            self.speed = 2
            y_pos = 300
        else:
            snail_frame1 = pygame.image.load("graphics/snail1.png").convert_alpha()
            snail_frame2 = pygame.image.load("graphics/snail2.png").convert_alpha()
            self.frames = [snail_frame1, snail_frame2]
            self.speed = 5
            y_pos = 300
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= self.speed
        self.destroy()


class EnemyDeath(pygame.sprite.Sprite):

    def __init__(self, enemy):
        super().__init__()
        self.animation_index = 0
        death_frame1 = pygame.image.load("graphics/explode1.png").convert_alpha()
        death_frame2 = pygame.image.load("graphics/explode2.png").convert_alpha()
        death_frame3 = pygame.image.load("graphics/explode3.png").convert_alpha()
        death_frame1 = pygame.transform.rotozoom(death_frame1, 0, enemy.size + .35)
        death_frame2 = pygame.transform.rotozoom(death_frame2, 0, enemy.size + .4)
        death_frame3 = pygame.transform.rotozoom(death_frame3, 0, enemy.size + .45)
        self.frames = [death_frame1, death_frame2, death_frame3]
        self.image = self.frames[int(self.animation_index)]
        self.rect = self.image.get_rect(center=(enemy.rect.x + 20, enemy.rect.y + 20))
        self.puff_sound = pygame.mixer.Sound("sound/landing_on_enemy.flac")
        self.puff_sound.set_volume(.7)

    def animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.puff_sound.play()
            self.kill()
            the_player.sprite.jump_count = 0
        else:
            self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation()


def collision_sprite():

    collision_tolerance = 15
    if pygame.sprite.spritecollide(the_player.sprite, enemy_group, False):
        for enemy in enemy_group:
            landing = abs(enemy.rect.top - the_player.sprite.rect.bottom)
            if landing < collision_tolerance:
                enemy.kill()
                enemy_death_group.add(EnemyDeath(enemy))
                the_player.sprite.gravity = -7
                the_player.sprite.jump_count = 0
                return True
            else:
                return False
    else:
        return True


def display_score():
    current_time = int(pygame.time.get_ticks()/1000)-start_time
    score_surf = game_font.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(midbottom=(350, 80))
    screen.blit(score_surf, score_rect)
    return current_time


pygame.init()

TS_Music = pygame.mixer.Sound("sound/Tittle_Screen.wav")
TS_Music.set_volume(.2)
bg_Music = pygame.mixer.Sound("sound/backgound_sound.wav")
bg_Music.set_volume(.3)

start_time = 0
score = 0
# Game Screen Background
screen = pygame.display.set_mode((700, 400))
ground_surface = pygame.image.load("graphics/ground2.png").convert_alpha()
ground_rect = ground_surface.get_rect(midtop=(350, 300))
sky_surface = pygame.image.load("graphics/sky.png")
sky_rect = sky_surface.get_rect(midtop=(350, 0))
# Title Page
game_font = pygame.font.Font("graphics/Pixeltype.ttf", 50)
player_stand = pygame.image.load("graphics/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(350, 170))
game_restart_surf = game_font.render("Press P To Play", False, (64, 64, 64))
game_restart_rect = game_restart_surf.get_rect(midbottom=(350, 320))
game_restart_surf2 = game_font.render("Use SpaceBar To Jump", False, (64, 64, 64))
game_restart_rect2 = game_restart_surf2.get_rect(midbottom=(350, 360))

game_active = False
clock = pygame.time.Clock()
exit = False
game_backgroundsound = 0
title_sound =0

# Groups
player1 = Player()
the_player = pygame.sprite.GroupSingle()
the_player.add(player1)
enemy_group = pygame.sprite.Group()
enemy_death_group = pygame.sprite.Group()

# Events
enemy_spawn = pygame.USEREVENT + 1
# Setting timers to events
pygame.time.set_timer(enemy_spawn, 1800)

while exit is False:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            player1.player_input(ground_rect)
        if event.type == pygame.QUIT:
            exit = True
        if game_active:
            if event.type == enemy_spawn:
               enemy_group.add(Enemy(random.choice(["Fly", "Fly", "ScaryFly", "ScaryFly", "BlackSnail", "BlueSnail", "GreenSnail", "Snail"])))

    if game_active:
        TS_Music.stop()
        title_sound=0
        game_backgroundsound += 1
        if game_backgroundsound == 1:
            bg_Music.play(loops=-1)
        screen.blit(sky_surface, sky_rect)
        screen.blit(ground_surface, ground_rect)
        score = display_score()
        the_player.draw(screen)
        the_player.update(ground_rect)
        enemy_group.draw(screen)
        enemy_group.update()
        enemy_death_group.draw(screen)
        enemy_death_group.update()
        game_active = collision_sprite()
    else:
        bg_Music.stop()
        game_backgroundsound = 0
        title_sound+=1
        if title_sound==1:
            TS_Music.play(loops=-1)
        enemy_group.empty()
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_restart_surf, game_restart_rect)
        screen.blit(game_restart_surf2, game_restart_rect2)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            start_time = int(pygame.time.get_ticks()/1000)
            game_active = True
    pygame.display.update()
    clock.tick(60)

pygame.quit()