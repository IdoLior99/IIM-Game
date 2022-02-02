import pygame
from operator import add
from game_objects import *


def fit_bg_dims(game_dims, bg_path):
    bg = pygame.image.load(bg_path).convert()  # Tutorial guy said it's important
    bg = pygame.transform.smoothscale(bg, game_dims)  # Changes image dims
    return bg


def game_setup(game_dims, game_name, icon_path, bg_path):

    screen = pygame.display.set_mode(game_dims)
    pygame.display.set_caption(game_name)
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)
    return screen, fit_bg_dims(game_dims, bg_path)


def player(h_screen, p_img, p_coords):
    h_screen.blit(p_img, p_coords)


def border_check(game_dims, p_coords, player_size):
    if p_coords[0] <= 0:
        p_coords[0] = 0
    elif p_coords[0] >= game_dims[0] - player_size:
        p_coords[0] = game_dims[0] - player_size
    if p_coords[1] <= 0:
        p_coords[1] = 0
    elif p_coords[1] >= game_dims[1] - player_size:
        p_coords[1] = game_dims[1] - player_size


def move_player(delts, speed, down=True):
    if down:
        if event.key == pygame.K_a:
            delts[0] -= speed
        if event.key == pygame.K_d:
            delts[0] += speed
        if event.key == pygame.K_w:
            delts[1] -= speed
        if event.key == pygame.K_s:
            delts[1] += speed
    else:
        if event.key == pygame.K_a or event.key == pygame.K_d:
            delts[0] = 0
        if event.key == pygame.K_w or event.key == pygame.K_s:
            delts[1] = 0


pygame.init()
game_size = (800, 600)
core_screen, main_menu = game_setup(game_size, 'Tomidos project', 'game_images/monster.png', 'game_images/main_menu.png')
player_img = pygame.image.load('game_images/player/hm_player_core.png')
player_img = pygame.transform.smoothscale(player_img, (161, 107))
player_coords = [370, 480]

# The Game Loop
running = True
deltas = [0, 0]
buttons = pygame.sprite.Group()
play_button = Animated_Sprite('game_images/play_button', 1, 400, 200, (215, 162))
quit_button = Animated_Sprite('game_images/quit_button', 1, 400, 400, (215, 162))
buttons.add(play_button)
buttons.add(quit_button)

level_0 = fit_bg_dims(game_size, 'game_images/hm_bg.png')
curr_screen = main_menu

while running:
    core_screen.blit(curr_screen, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            move_player(deltas, 1)
        if event.type == pygame.KEYUP:
            move_player(deltas, 1, down=False)
        if event.type == pygame.MOUSEMOTION:
            if play_button.coll_check(event.pos):
                play_button.set_pressed()
            else:
                play_button.set_released()
            if quit_button.coll_check(event.pos):
                quit_button.set_pressed()
            else:
                quit_button.set_released()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_button.coll_check(event.pos) and curr_screen == main_menu:
                running = False
            elif play_button.coll_check(event.pos) and curr_screen == main_menu:
                curr_screen = level_0

    player_coords = list(map(add, player_coords, deltas))  # should be time efficient
    border_check(game_size, player_coords, 32)
    if curr_screen == level_0:
        player(core_screen, player_img, player_coords)
    if curr_screen == main_menu:
        buttons.draw(core_screen)
        buttons.update()

    pygame.display.update()  # TODO bad for perfomance, should keep a list of objects(rects/sprites) that are updated and only update them
