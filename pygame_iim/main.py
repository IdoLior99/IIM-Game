import pygame
from game_objects import *
import time


def fit_bg_dims(game_dims, bg_path):
    bg = pygame.image.load(bg_path).convert()  # Tutorial guy said it's important
    bg = pygame.transform.smoothscale(bg, game_dims)  # Changes image dims
    return bg


def game_setup(game_dims, game_name, icon_path, bg_path):
    screen = pygame.display.set_mode(game_dims)  # add pygame.FULLSCREEN if fullscreen
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
text_window = pygame.image.load('game_assets/text_window.PNG')
text_window = pygame.transform.smoothscale(text_window, [825, 400])  # Changes image dims

running = True
menu_sprites = pygame.sprite.Group()
game_sprites = pygame.sprite.Group()
text_sprites = pygame.sprite.Group()
player = Player('game_assets/player', 0, 370, 480, (161, 107), 1, img_format='PNG')
npc = NPC('game_assets/skully', 0, 370, 480, (48, 54), 1, loc_offset=100, img_format='PNG')
play_button = Button('game_assets/play_button', 1, 400, 200, (215, 162),
                     sound_path='game_assets/sounds/button_click.wav')
quit_button = Button('game_assets/quit_button', 1, 400, 400, (215, 162),
                     sound_path='game_assets/sounds/button_click.wav')
msg_button = Msg_Button('game_assets/msg_button', 1, 400, 200, (100, 75), npc=npc, y_offset=-60,
                        sound_path='game_assets/sounds/button_click.wav')
next_button = Button('game_assets/next_button', 1, 720, 540, (107, 81),
                     sound_path='game_assets/sounds/button_click.wav')

menu_sprites.add([play_button, quit_button])
game_sprites.add([msg_button, npc, player])
text_sprites.add([next_button])

textfont = pygame.font.SysFont('leelawadeeuisemilight', 20)
level_0 = fit_bg_dims(game_size, 'game_assets/hm_bg.png')
curr_screen = main_menu
clock = pygame.time.Clock()
# TODO add default anchor points for player - npc spawn locations.
text_box_flag = False
text_i = 0
texts = ['hello world', 'woopie doopie poo']
while running:

    core_surface.blit(curr_screen, (0, 0))
    start_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not text_box_flag and event.type == pygame.KEYDOWN:
            player.update_delts(event)
            if event.key == pygame.K_ESCAPE:
                curr_screen = main_menu
        if not text_box_flag and event.type == pygame.KEYUP:
            player.update_delts(event, down=False)

        if event.type == pygame.MOUSEMOTION:
            for button in menu_sprites:
                if button.coll_check(event.pos):
                    button.set_hovered()
                else:
                    button.set_released()

            if msg_button.coll_check(event.pos):
                msg_button.set_hovered()
            else:
                msg_button.set_released()

            if text_box_flag and next_button.coll_check(event.pos):
                next_button.set_hovered()
            else:
                next_button.set_released()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_button.coll_check(event.pos) and curr_screen == main_menu:
                quit_button.sound.play()
                time.sleep(0.3)
                running = False
            elif play_button.coll_check(event.pos) and curr_screen == main_menu:
                play_button.sound.play()
                start_time = time.time()
                curr_screen = level_0
            elif msg_button.coll_check(event.pos) and curr_screen == level_0:
                msg_button.sound.play()
                text_box_flag = True
                text1 = textfont.render(texts[text_i], 1, (0, 0, 0))
                game_sprites.remove(msg_button)

            if next_button.coll_check(event.pos) and curr_screen == level_0:
                next_button.sound.play()
                text_i += 1
                if text_i >= len(texts):
                    text_box_flag = False
                else:
                    text1 = textfont.render(texts[text_i], 1, (0, 0, 0))


    player.move_player()
    npc.move_towards_player(player)
    player.rect.center = border_check(game_size, player.rect.center, 32)
    npc.rect.center = border_check(game_size, npc.rect.center, 32)
    if curr_screen == level_0:
        game_sprites.draw(core_surface)
        game_sprites.update()
        if text_box_flag:
            core_surface.blit(text_window, (0, 300))
            core_surface.blit(text1, (75, 440))
            text_sprites.draw(core_surface)
            text_sprites.update()

    if curr_screen == main_menu:
        menu_sprites.draw(core_surface)
        menu_sprites.update()
    clock.tick()
    #print(clock.get_fps())

    pygame.display.update()  # TODO bad for perfomance, should keep a list of objects(rects/sprites) that are updated and only update them
