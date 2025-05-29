import pygame
from random import randint, choice
import math
import csv


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.force = 0
        self.friction = 0.9
        self.player_stand = pygame.image.load('temp2_player.png').convert_alpha()
        self.player_crouch = pygame.image.load('Player_Crouch.png').convert_alpha()

        self.image = self.player_stand
        self.rect = self.image.get_rect(midbottom=(100, 850))

    def player_input(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] and self.rect.x != 0 and self.rect.x != 700:
            if self.force <= 20:
                self.force += 0.5
            self.rect.x += self.force * self.friction

        elif keys[pygame.K_a] and self.rect.x != 0 and self.rect.x != 700:
            if self.force <= 20:
                self.force += 0.5
            self.rect.x -= self.force * self.friction

        elif keys[pygame.K_d] and self.rect.x == 0:
            self.rect.x += 1

        elif keys[pygame.K_a] and self.rect.x == 700:
            self.rect.x -= 1

        if self.force != 0:
            self.force -= 0.25

        if keys[pygame.K_c]:
            self.image = self.player_crouch
        else:
            self.image = self.player_stand

    def border(self):
        if self.rect.x < 0:
            self.rect.x = 0
            self.force = 0

        elif self.rect.x > 650:
            self.rect.x = 650
            self.force = 0

    def update(self):
        self.player_input()
        self.border()


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, gravity_pos=5):
        super().__init__()
        self.image = pygame.image.load('Asteroid Brown2.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(randint(0, 720), 0))
        self.gravity_pos = gravity_pos

    def gravity(self):
        self.rect.y += self.gravity_pos

    def destroy(self):
        if self.rect.y >= 1100:
            self.kill()

    def update(self):
        self.gravity()
        self.destroy()


class UFO(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('UFO.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(360, 300))

        self.move_statement = True

    def movement(self, move_statement):
        self.move_statement = move_statement
        if self.move_statement:
            self.rect.x += 5
        else:
            self.rect.x -= 5

    def update(self):
        self.movement(move_statement=self.move_statement)


class UFO_Border1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('UFO_border1.png')
        self.rect = self.image.get_rect(midbottom=(1020, 100))


class UFO_Border2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('UFO_border2.png')
        self.rect = self.image.get_rect(midbottom=(-300, 100))


class UFO_lazar(pygame.sprite.Sprite):
    def __init__(self, ufo_pos):
        super().__init__()
        self.image = pygame.image.load('greenlazer.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(ufo_pos, 300))
        self.lazer_sound = pygame.mixer.Sound('LazzerSoundEffect.mp3')
        self.count = 0

    def gravity(self):
        self.rect.y += 10
        if self.count == 0:
            self.lazer_sound.play()
            self.count += 1

    def destroy(self):
        if self.rect.y >= 1100:
            self.kill()

    def update(self):
        self.gravity()
        self.destroy()





            
def collision_sprite1():
    if pygame.sprite.spritecollide(player.sprite, obstacle1, False):
        obstacle1.empty()

        return False
    else:
        return True


def text_animation_define():
    x_values = [i * 2 for i in range(0, 628)]  # 0 to 2*pi with step of 0.01
    frequency = 100  # Increase the frequency to make the wave oscillate more
    y_values = [math.sin(frequency * x) for x in x_values]
    return y_values


def text_animation_apply():
    global text_animation_1_index
    if text_animation_1_index < text_animation_1_len_index:
        text_animation_1_index += 0.1
    else:
        text_animation_1_index = 0


def collision_sprite2():
    global count_movement
    if pygame.sprite.spritecollide(UFO_object.sprite, UFO_border, False):
        if count_movement % 2 == 0:
            UFO_object.sprite.movement(False)
        else:
            UFO_object.sprite.movement(True)
        count_movement += 1

        if count_movement > 100:
            count_movement = 0


def collision_sprite3():
    if pygame.sprite.spritecollide(player.sprite, obstacle_lazer, False):
        obstacle_lazer.empty()
        obstacle1.empty()
        return False
    else:
        return True


def display_score():
    global active_score
    if play and play_2:
        game_time = pygame.time.get_ticks()
        active_score = str(((game_time - start_time) // 1000) + int(pause_score))
        score_surface = game_font_1.render(active_score, False, RED)
        score_rectangle = score_surface.get_rect(midbottom=(400, 200))
        screen.blit(score_surface, score_rectangle)
        return active_score
    else:
        return active_score


def get_random_time():
    return randint(1000, 5000)


def store_score(score_):
    global game_no

    with open('score.csv', 'a', newline ='') as append_file:
        game_no += 1
        write = csv.writer(append_file)
        data = [text_box_text[:-1],game_no,score_]
        write.writerow(data)

def highest_score():
    with open('score.csv', 'r', newline ='\n') as read_file:
        data = list(csv.reader(read_file))
        max_score = max([int(i[2]) for i in data])
        for i in data:
            if max_score == int(i[2]):
                return i[0], i[2]






# pygame setup
pygame.init()
screen = pygame.display.set_mode((720, 900))
clock = pygame.time.Clock()
running = True
play = False
play_2 = False
start = True
pause = False
switch = True
limiter = 30
amplifier = 2
start_time = 0
pause_score = 0
count_movement = 0
game_no = 0

# Class
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle1 = pygame.sprite.Group()

UFO_object = pygame.sprite.GroupSingle()
UFO_object.add(UFO())

UFO_border = pygame.sprite.Group()
UFO_border.add(UFO_Border1())
UFO_border.add(UFO_Border2())

obstacle_lazer = pygame.sprite.Group()




# Assets

# Text

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
YELLOW = (255,255,0)

game_font_1 = pygame.font.Font('Pixeltype.ttf', 50)
game_font_2 = pygame.font.Font('Pixeltype.ttf', 100)

text_1 = 'Game Over'
text_surf_1 = game_font_2.render(text_1, False, RED)

text_2 = 'Click Space to play again'
text_surf_2 = game_font_1.render(text_2, False, WHITE)

text_3 = 'Paused'
text_surf_3 = game_font_1.render(text_3, False, WHITE)

text_4 = 'Enter Your User Name'
text_surf_4 = game_font_1.render(text_4, False, WHITE)




text_animation_1 = text_animation_define()
text_animation_1_len_index = len(text_animation_1) - 1


text_animation_1_index = 0

game_background = pygame.image.load('star background.png').convert_alpha()
game_background_pos = game_background.get_rect(midbottom=(360, 900))

# Text Box

text_box_active_colour = WHITE
text_box_passive_colour = GRAY
text_box_colour = text_box_passive_colour
text_box_rect = pygame.Rect(290, 550, 140, 32)
text_box_text = ''
text_box_active = False



# Obstacle Timers

obstacle_timer_1 = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer_1, 900)
wave0 = True

min_timer_interval = 1000
max_timer_interval = 5000
wave1 = False
random_time = randint(min_timer_interval, max_timer_interval)
obstacle_timer_2 = pygame.USEREVENT + 2
pygame.time.set_timer(obstacle_timer_2, random_time)

obstacle_timer_3 = pygame.USEREVENT + 3
pygame.time.set_timer(obstacle_timer_3, 500)
wave2 = False

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if start:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    play = True
                    play_2 = True
                    start = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if text_box_rect.collidepoint(event.pos):
                        text_box_active = True
                    else:
                        text_box_active = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        text_box_text = text_box_text[:-1]
                    else:
                        text_box_text += event.unicode
                pause_score = 0
                start_time = pygame.time.get_ticks()

        elif play and play_2:
            if wave0:
                if event.type == obstacle_timer_1:
                    obstacle1.add(Asteroid())
            if wave1:
                if event.type == obstacle_timer_2:
                    obstacle_lazer.add(UFO_lazar(UFO_object.sprite.rect.centerx))
                    pygame.time.set_timer(obstacle_timer_2, get_random_time())
            if wave2:
                if event.type == obstacle_timer_3:
                    obstacle1.add(Asteroid(amplifier + 7))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    pause = True
                    play = False
                    play_2 = False

        elif pause:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    pause = False
                    play = True
                    play_2 = True
                    pause_score = score
                    start_time = pygame.time.get_ticks()

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    switch = True
                    play = True
                    play_2 = True
                    start_time = pygame.time.get_ticks()
                    score = 0
                    pause_score = 0
                    wave0 = True
                    wave2 = False
                    obstacle_lazer.empty()

    # START
    if start:
        screen.blit(game_background, game_background_pos)


        if text_box_active:
            text_box_colour = text_box_active_colour
        else:
            text_box_colour = text_box_passive_colour
        pygame.draw.rect(screen, text_box_colour, text_box_rect)
        text_box_surface = game_font_1.render(text_box_text, True, (255, 255, 255))
        screen.blit(text_box_surface,(text_box_rect.x + 5, text_box_rect.y + 5))
        text_box_rect.w = max(100, text_box_surface.get_width() + 10)

        text_animation_apply()
        text_rect_4 = text_surf_4.get_rect(midbottom=(360, 500 + text_animation_1[int(text_animation_1_index)]))

        screen.blit(text_surf_4,text_rect_4)



    # PLAY
    elif play and play_2:

        #  Stage
        screen.blit(game_background, game_background_pos)
        pygame.draw.line(screen, BLACK, (0, 875), (720, 875), 70)

        score = display_score()
        # PLAYER
        player.draw(screen)
        player.update()

        # OBSTACLE

        obstacle1.draw(screen)
        obstacle1.update()

        if score > str(10) and score not in ['2', '3', '4', '5', '6', '7', '8', '9']:
            UFO_object.draw(screen)
            UFO_object.update()

            UFO_border.draw(screen)
            UFO_border.update()

            obstacle_lazer.draw(screen)
            obstacle_lazer.update()
            collision_sprite2()
            play_2 = collision_sprite3()

            wave1 = True

        if int(score) > 20:
            wave2 = True
            wave0 = False

        play = collision_sprite1()
        text_rect_1 = text_surf_1.get_rect(midbottom=(360, 450 + text_animation_1[int(text_animation_1_index)]))

    elif pause:
        text_animation_apply()

        text_rect_3 = text_surf_3.get_rect(midbottom=(360, 500 + text_animation_1[int(text_animation_1_index)]))

        screen.blit(game_background, game_background_pos)
        screen.blit(text_surf_3, text_rect_3)


    else:

        text_animation_apply()
        if switch:
            store_score(score)
            player_name,highest_score_ = highest_score()
            switch = False

        final_score_surf = game_font_1.render(str(display_score()), False, WHITE)
        highest_score_surf = game_font_1.render(f'Highest Score {player_name} : {highest_score_}',False,YELLOW)

        screen.blit(game_background, game_background_pos)
        text_rect_1 = text_surf_1.get_rect(midbottom=(360, 450 + text_animation_1[int(text_animation_1_index)]))
        text_rect_2 = text_surf_2.get_rect(midbottom=(360, 500 + text_animation_1[int(text_animation_1_index)]))
        final_score_rect = final_score_surf.get_rect(
            midbottom=(360, 350 + text_animation_1[int(text_animation_1_index)]))
        highest_score_rect = final_score_surf.get_rect(
            midbottom=(150, 600 + text_animation_1[int(text_animation_1_index)]))

        screen.blit(text_surf_1, text_rect_1)
        screen.blit(text_surf_2, text_rect_2)
        screen.blit(final_score_surf, final_score_rect)
        screen.blit(highest_score_surf,highest_score_rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
