import pygame
from game_objects import *
import time


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


def player_up(h_screen, p_img, p_coords):
    h_screen.blit(p_img, p_coords)


def border_check(game_dims, p_coords, player_size):
    temp = list(p_coords)
    if p_coords[0] <= 0:
        temp[0] = 0
    elif p_coords[0] >= game_dims[0] - player_size:
        temp[0] = game_dims[0] - player_size
    if p_coords[1] <= 0:
        temp[1] = 0
    elif p_coords[1] >= game_dims[1] - player_size:
        temp[1] = game_dims[1] - player_size
    p_coords = tuple(temp)
    return p_coords


pygame.init()
game_size = (800, 600)
core_surface, main_menu = game_setup(game_size, 'Tomidos project', 'game_assets/monster.png',
                                    'game_assets/main_menu.png')
player_img = pygame.image.load('game_assets/player/hm_player_core.png')
player_img = pygame.transform.smoothscale(player_img, (161, 107))
player_coords = [370, 480]

# The Game Loop
running = True
deltas = [0, 0]
buttons = pygame.sprite.Group()
characters = pygame.sprite.Group()
player = Player('game_assets/player', 0, 370, 480, (161, 107), 1, img_format='PNG')
play_button = Button('game_assets/play_button', 1, 400, 200, (215, 162),
                     sound_path='game_assets/sounds/button_click.wav')
quit_button = Button('game_assets/quit_button', 1, 400, 400, (215, 162),
                     sound_path='game_assets/sounds/button_click.wav')

buttons.add(play_button)
buttons.add(quit_button)
characters.add(player)

level_0 = fit_bg_dims(game_size, 'game_assets/hm_bg.png')
curr_screen = main_menu
clock = pygame.time.Clock()
while running:
    core_surface.blit(curr_screen, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            player.update_delts(event)

            if event.key == pygame.K_ESCAPE:
                curr_screen = main_menu
        if event.type == pygame.KEYUP:
            player.update_delts(event, down=False)

        if event.type == pygame.MOUSEMOTION:
            if play_button.coll_check(event.pos):
                play_button.set_hovered()
            else:
                play_button.set_released()
            if quit_button.coll_check(event.pos):
                quit_button.set_hovered()
            else:
                quit_button.set_released()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_button.coll_check(event.pos) and curr_screen == main_menu:
                quit_button.sound.play()
                time.sleep(0.3)
                running = False
            elif play_button.coll_check(event.pos) and curr_screen == main_menu:
                play_button.sound.play()
                curr_screen = level_0

    player.move_player()
    player.rect.center = border_check(game_size, player.rect.center, 32) # Cant do it like that rn, is a tuple
    if curr_screen == level_0:
        characters.draw(core_surface)
        characters.update()

    if curr_screen == main_menu:
        buttons.draw(core_surface)
        buttons.update()
    clock.tick()
    #print(clock.get_fps())

    pygame.display.update()  # TODO bad for perfomance, should keep a list of objects(rects/sprites) that are updated and only update them

