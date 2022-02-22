import pygame
from game_objects import *
import time
from random import randrange
import eval_and_report as ear
import numpy as np

##################################################### MEASURES #########################################################
reaction_times = []
answered_correctly = []
tut_accumulative = []  # TODO: for the learning curve
sandbox_approaches = 0


# TODO: anything else we want to measure?

################################################## MAIN.py FUNCTIONS #####################################################

def fit_bg_dims(game_dims, bg_path):
    bg = pygame.image.load(bg_path).convert()  # Tutorial guy said it's important
    bg = pygame.transform.smoothscale(bg, game_dims)  # Changes image dims
    return bg


def game_setup(game_dims, game_name, icon_path, bg_path):
    screen = pygame.display.set_mode(game_dims)  # add pygame.FULLSCREEN if fullscreen
    pygame.display.set_caption(game_name)
    icon = pygame.image.load(icon_path)
    icon = pygame.transform.smoothscale(icon, (32, 32))
    pygame.display.set_icon(icon)
    return screen, fit_bg_dims(game_dims, bg_path)


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


def npc_talk(npc, msg_button, game_sprites, player, tut_phase, resp_conds, resp_texts, event):
    """
    Determines what the npc should say next (if anything at all)
    :param tut_phase: How far into the tutorial are we
    :param resp_conds: Various conditions for condition-based repsonses
    :param resp_texts: Various responses incasae said condition is met
    :param event: in event.get.
    :return: msg_texts - text to be said by the npc.
    """
    if npc.text_i != tut_phase:
        npc.text_i = tut_phase
    texts = npc.texts[npc.text_i]
    msg_texts = ""
    # Needed if a response is script-dependant.
    action = 0  # 0 == didn't talk, 1 == scripted talking, 2 == responding, 3 == scripted message done, 4 == response message done
    # Can only respond once, looks for the first response condition
    resp_i = np.where(resp_conds)[0]
    resp_cond = resp_conds[resp_i[0]] if resp_i.size else False
    if resp_cond or npc.curr_response:  # Responce
        if not npc.is_talking:
            if resp_cond:  # Npc should respond to something rn.
                npc.is_talking = True
                npc.curr_response = textfont.render(resp_texts[resp_i[0]], 1, (0, 0, 0))
                msg_texts = textfont.render(resp_texts[resp_i[0]], 1, (0, 0, 0))
                action = 2

        else:  # npc is already talking
            if event.type == pygame.KEYDOWN and event.key == pygame.K_l:  # l was pressed to advance
                next_button.set_hovered()
                next_button.sound.play()
                npc.is_talking = False  # Responses are exclusively 1-panel
                npc.curr_response = None
                action = 4
            else:  # Frame idle
                msg_texts = npc.curr_response
                action = 2


    else:  # Scripted talk
        if not npc.is_talking:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_l:  # Npc should start with a scripted message
                if msg_button in game_sprites and msg_button.coll_check(player.rect.center, x_offset=50, y_offset=80):
                    msg_button.set_hovered()
                    msg_button.sound.play()
                    npc.is_talking = True
                    msg_texts = textfont.render(texts[npc.subtext_i], 1, (0, 0, 0))
                    action = 1
        else:  # npc is already talking
            if event.type == pygame.KEYDOWN and event.key == pygame.K_l:  # l was pressed to advance
                next_button.set_hovered()
                next_button.sound.play()
                if msg_button in game_sprites:
                    npc.subtext_i += 1
                    if npc.subtext_i >= len(texts):
                        npc.is_talking = False
                        npc.text_i += 1
                        npc.subtext_i = 0
                        msg_button.set_released()
                        game_sprites.remove(msg_button)
                        action = 3
            else:
                msg_texts = textfont.render(texts[npc.subtext_i], 1, (0, 0, 0))
                action = 1

    return msg_texts, action


def knock_on_door(cond, knocked):
    if cond:
        door_button.set_hovered()
        knock_sound.play()
        knocked = True
    return knocked

def update_frame(player, npc, game_sprites, tool_sprites, core_surface, text_window, msg_texts, text_sprites, door):
    player.move_player()
    if npc:
        npc.move_towards_coords(player.rect.center)
        npc.rect.center = border_check(game_size, npc.rect.center, 32)
    player.rect.center = border_check(game_size, player.rect.center, 32)
    if door.is_open:
        core_surface.blit(title_window, (420, 25))
        core_surface.blit(enemy_title, (435, 45))
    tool_sprites.draw(core_surface)
    tool_sprites.update()
    game_enemy.draw(core_surface)
    game_sprites.draw(core_surface)
    game_sprites.update()
    if msg_texts == '' and npc and npc.is_talking:
        print("hi")
    if npc and npc.is_talking:
        core_surface.blit(noopcie_pic, (20, 265))
        core_surface.blit(text_window, (0, 300))
        core_surface.blit(msg_texts, (75, 440))
        text_sprites.draw(core_surface)
        text_sprites.update()


################################################# INIT STUFF ###########################################################
pygame.init()
game_size = (800, 600)
core_surface, main_menu = game_setup(game_size, 'Tomidos project', 'game_assets_f/Tools/Candy/candy_i.png',
                                     'game_assets_f/Backgrounds/mm_bg.png')
text_window = pygame.image.load('game_assets_f/text_window.PNG')
text_window = pygame.transform.smoothscale(text_window, [825, 400])  # Changes image dims
title_window = pygame.transform.smoothscale(text_window, [250, 70])  # Changes image dims
textfont = pygame.font.SysFont('leelawadeeuisemilight', 20)
basefont = pygame.font.Font(None, 32)

level_0 = fit_bg_dims(game_size, 'game_assets_f/Backgrounds/lvl_bg.png')
instruct_screen = fit_bg_dims(game_size, 'game_assets_f/Backgrounds/instruct_bg.png')
pause_screen = fit_bg_dims(game_size, 'game_assets_f/Backgrounds/pause_bg.png')
name_screen = fit_bg_dims(game_size, 'game_assets_f/Backgrounds/name_bg.png')
curr_screen = main_menu

clock = pygame.time.Clock()
pop_sound = pygame.mixer.Sound('game_assets_f/sounds/msg_pop.flac')
knock_sound = pygame.mixer.Sound('game_assets_f/sounds/door_knock_sound.mp3')
npc_flag = False
choice = None
door_open = False
door_rang = False
running = True
tut_phase = 0
phase_buttons = []
tut_lvl = 0
msg_texts = ''
ts = 0
already_named = False
################################################# CREATE ENEMIES #######################################################

game_enemy = pygame.sprite.Group()
# TODO: use For loop
single_opts = ["Princess", "Robot", "Farmer", "Cookie Monster", "Tooth", "Businessman", "Ghost"]
Princess = Enemy("game_assets_f/game_enemies/Princess", 500, 190, (215, 162), "Princess", img_format='png')
Robot = Enemy("game_assets_f/game_enemies/Robot", 500, 190, (215, 162), "Robot", img_format='png')
Farmer = Enemy("game_assets_f/game_enemies/Farmer", 500, 190, (215, 162), "Farmer", img_format='png')
Cookie = Enemy("game_assets_f/game_enemies/Cookie Monster", 500, 190, (215, 162), "Cookie Monster", img_format='png')
Tooth = Enemy("game_assets_f/game_enemies/Tooth", 500, 190, (215, 162), "Tooth", img_format='png')
Business = Enemy("game_assets_f/game_enemies/Businessman", 500, 190, (215, 162), "Businessman", img_format='png')
Ghost = Enemy("game_assets_f/game_enemies/Ghost", 500, 190, (215, 162), "Ghost", img_format='png')
reg_enemies = [Princess, Robot, Farmer, Cookie, Tooth, Business, Ghost]
hybrid_enemies = []
for i, i_opt in enumerate(single_opts):
    for j in range(i + 1, len(single_opts)):
        j_opt = single_opts[j]
        hybrid_enemies.append(
            Enemy(f"game_assets_f/game_enemies/ToT - {i_opt}-{j_opt}", 500, 190, (215, 162), i_opt, j_opt,
                  img_format='png'))
all_enemies = reg_enemies.copy()
all_enemies.extend(hybrid_enemies)

tut_enemies = [Cookie, Princess, Ghost, hybrid_enemies[1], hybrid_enemies[13], hybrid_enemies[4]]
game_enemies = [all_enemies[0], all_enemies[2]]  # all_enemies[3], all_enemies[4], all_enemies[5], all_enemies[6]]

################################################# SCREENS ##############################################################

# Main Menu Screen: ####################################################################################################
menu_sprites = pygame.sprite.Group()
play_button = Button('game_assets_f/Buttons/play_button', 1, 400, 200, (215, 162),
                     sound_path='game_assets_f/sounds/button_click.wav')
quit_button = Button('game_assets_f/Buttons/quit_button', 1, 400, 400, (215, 162),
                     sound_path='game_assets_f/sounds/button_click.wav')
menu_sprites.add([play_button, quit_button])

# Pause Menu Screen: ###################################################################################################
pause_sprites = pygame.sprite.Group()
p_res_button = Button('game_assets_f/Buttons/continue_button', 1, 400, 400, (215, 162),
                      sound_path='game_assets_f/sounds/button_click.wav')
p_quit_button = Button('game_assets_f/Buttons/quit_button', 1, 400, 500, (215, 162),
                       sound_path='game_assets_f/sounds/button_click.wav')
pause_sprites.add([p_res_button, p_quit_button])

# Name Menu Screen: ###################################################################################################
name_sprites = pygame.sprite.Group()
n_res_button = Button('game_assets_f/Buttons/continue_button', 1, 400, 490, (215, 162),
                      sound_path='game_assets_f/sounds/button_click.wav')
name_sprites.add(n_res_button)
user_name = ''
text_input_rect = pygame.Rect(450, 285, 140, 32)
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('lightskyblue2')
color = color_passive
active = False

# Game Screen: #########################################################################################################
game_sprites = pygame.sprite.Group()
player = Player('game_assets_f/player', 0, 370, 480, (97, 100), 2, img_format='PNG')
npc_types = ["Favorite", "Hyper", "Aloof"]
random_type = randrange(0, 3)
#random_type = 2
chosen_npc = npc_types[random_type]
#chosen_npc = 'Aloof'
noopcie_pic = pygame.image.load('game_assets_f/Noopcie/{}/Noopcie_{}.png'.format(chosen_npc, random_type + 1))
noopcie_pic = pygame.transform.smoothscale(noopcie_pic, [214, 162])
FRIEND = "FRIEND"
npc = NPC('game_assets_f/Noopcie/{}'.format(chosen_npc), 0, 608, 84, (82, 65), 2, loc_offset=100, img_format='PNG',
          type=chosen_npc, friend_name=FRIEND)
msg_button = Msg_Button('game_assets_f/Buttons/msg_button', 1, 400, 200, (100, 75), npc=npc, y_offset=-60,
                        sound_path='game_assets_f/sounds/button_click.wav')
text_sprites = pygame.sprite.Group()
next_button = Button('game_assets_f/Buttons/next_button', 1, 720, 540, (107, 81),
                     sound_path='game_assets_f/sounds/button_click.wav')
door_button = Door('game_assets_f/Buttons/door_button', 1, 500, 190, (300, 185),
                   sound_path='game_assets_f/sounds/door_open.wav')

game_sprites.add([door_button, msg_button, npc, player])
text_sprites.add([next_button])

tool_sprites = pygame.sprite.Group()

candy_button = Button('game_assets_f/Tools/Candy', 1, 220, 175, (112, 81),
                      sound_path='game_assets_f/sounds/candy_sound.wav', tag='Candy')
fruit_button = Button('game_assets_f/Tools/Fruit', 1, 610, 475, (112, 81),
                      sound_path='game_assets_f/sounds/button_click.wav', tag='Fruit')
money_button = Button('game_assets_f/Tools/Money', 1, 100, 395, (90, 64),
                      sound_path='game_assets_f/sounds/money_sound.wav', tag='Money')
trick_button = Button('game_assets_f/Tools/Trick', 1, 120, 95, (112, 81),
                      sound_path='game_assets_f/sounds/button_click.wav', tag='Trick')

legend_button = Button('game_assets_f/Tools/Legend', 1, 500, 40, (112, 81),
                       sound_path='game_assets_f/sounds/button_click.wav')
available_tools = [candy_button]
tool_sprites.add([candy_button, fruit_button, money_button, trick_button, legend_button])

# Game Answer outcome
# TODO: find sound for wrong answer and put it in X_sound_path
outcome = Outcome(X_sound_path='game_assets_f/sounds/button_click.wav',
                  V_sound_path='game_assets_f/sounds/cheering_ppl.wav')

# Finish Screen: #######################################################################################################
finish_screen = fit_bg_dims(game_size, 'game_assets_f/Backgrounds/lvl_bg.png')
finish_buttons = pygame.sprite.Group()
finish_button = Button('game_assets_f/Buttons/quit_button', 1, 400, 300, (215, 162),
                       sound_path='game_assets_f/sounds/button_click.wav')
finish_buttons.add(finish_button)

# Legend Screen: #######################################################################################################
legend_screen = fit_bg_dims(game_size, 'game_assets_f/Backgrounds/legend_bg.png')
legend_buttons = pygame.sprite.Group()
cont_button = Button('game_assets_f/Buttons/continue_button', 1, 400, 500, (215, 162),
                     sound_path='game_assets_f/sounds/button_click.wav')
legend_buttons.add(cont_button)
start_time = time.time()

# Phase-specific variables: ############################################################################################
knocked = False
last_talk_action = 0
done_talking_flag = 0
new_outcome = outcome

legend_const_action = 0
legend_last_talk_action = 0
visited_legend = False
################################################# GAME LOOP #########################################################
while running:
    core_surface.blit(curr_screen, (0, 0))
    # Main Menu Stuff
    if curr_screen == main_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                for button in menu_sprites:
                    if button.coll_check(event.pos):
                        button.set_hovered()
                    else:
                        button.set_released()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.coll_check(event.pos):
                    quit_button.sound.play()
                    time.sleep(0.3)
                    running = False
                elif play_button.coll_check(event.pos):
                    play_button.sound.play()
                    if not already_named:
                        curr_screen = name_screen
                        already_named = True
                    else:
                        curr_screen = level_0
        menu_sprites.draw(core_surface)
        menu_sprites.update()

    elif curr_screen == name_screen:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if n_res_button.coll_check(event.pos):
                    n_res_button.set_hovered()
                else:
                    n_res_button.set_released()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

                if n_res_button.coll_check(event.pos):
                    n_res_button.sound.play()
                    if len(user_name) >= 2:
                        print(user_name)
                        npc.update_texts(player_name=user_name)
                    curr_screen = instruct_screen

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]
                else:
                    user_name += event.unicode

        if active:
            color = color_active
        else:
            color = color_passive
        name_sprites.draw(core_surface)
        name_sprites.update()
        pygame.draw.rect(core_surface, color, text_input_rect)
        text_surface = basefont.render(user_name, True, (255, 255, 255))
        core_surface.blit(text_surface, (text_input_rect.x + 5, text_input_rect.y + 5))

    elif curr_screen == pause_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    p_res_button.set_hovered()
                    p_res_button.sound.play()
                elif event.key == pygame.K_l:
                    p_quit_button.set_hovered()
                    p_quit_button.sound.play()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_k:
                    p_res_button.set_released()
                    curr_screen = level_0
                elif event.key == pygame.K_l:
                    p_quit_button.set_released()
                    running = False

        pause_sprites.draw(core_surface)
        pause_sprites.update()

    elif curr_screen == instruct_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    cont_button.set_hovered()
                    cont_button.sound.play()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_k:
                    cont_button.set_released()
                    start_time = time.time()
                    curr_screen = level_0
        legend_buttons.draw(core_surface)
        legend_buttons.update()

    # Game Screen Stuff
    elif curr_screen == level_0:

        if tut_phase == 0:
            # knocked = knock_on_door(const_action == 3 and not knocked, knocked)
            if done_talking_flag == 3 and not knocked:
                door_button.set_hovered()
                knock_sound.play()
                knocked = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if npc.is_talking:
                    player.deltas = [0, 0]
                phase_0_if = done_talking_flag == 3 and not knocked
                msg_texts, last_talk_action = npc.npc_talk(msg_button, game_sprites, player, tut_phase,
                                                       [phase_0_if], [npc.resps["knock"]], event, next_button, textfont)
                if done_talking_flag != 3:
                    done_talking_flag = last_talk_action
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        curr_screen = pause_screen
                    if not npc.is_talking:
                        player.update_delts(event)
                    if event.key == pygame.K_k:
                        if not npc.is_talking and door_button.coll_check(player.rect.center) and not \
                                door_button.is_open and knocked:
                            knocked = False
                            door_button.is_open = True
                            door_button.sound.play()
                            curr_enemy = tut_enemies[tut_lvl]
                            tut_lvl += 1
                            game_enemy.add([curr_enemy])
                            enemy_title = textfont.render(curr_enemy.title, 1, (0, 0, 0))
                            tut_phase += 1
                            phase_0_if = False
                            print("Now at phase {}".format(tut_phase))
                            if msg_button not in game_sprites:
                                game_sprites.add(msg_button)
                            break

                if event.type == pygame.KEYUP:
                    if not npc.is_talking:
                        player.update_delts(event, down=False)
                    if event.key == pygame.K_l:
                        next_button.set_released()
            if time.time() - start_time > 2:
                update_frame(player, npc, game_sprites, tool_sprites, core_surface, text_window, msg_texts,
                             text_sprites,
                             door_button)
            else:
                update_frame(player, None, game_sprites, tool_sprites, core_surface, text_window, msg_texts,
                             text_sprites,
                             door_button)

        elif 0 < tut_phase < 4 or 5 <= tut_phase <= 7:  # Before and After legend
            if tut_phase == 2 and fruit_button not in available_tools:
                available_tools.append(fruit_button)
            if tut_phase == 3 and money_button not in available_tools:
                available_tools.append(money_button)
            if tut_phase == 7 and trick_button not in available_tools:
                available_tools.append(trick_button)

            for event in pygame.event.get():
                if npc.is_talking:
                    player.deltas = [0, 0]
                if time.time() - ts > 1 and not knocked:
                    if tut_phase != 1:
                        knock_sound.play()
                    knocked = True
                if event.type == pygame.QUIT:
                    running = False
                msg_texts, last_talk_action = npc.npc_talk(msg_button, game_sprites, player, tut_phase,
                                        [new_outcome.wrong, new_outcome.right],
                                        [npc.resps['try'], npc.npc_good()], event, next_button, textfont)
                if last_talk_action == 4: #Finished responding
                    new_outcome.reset()
                    last_talk_action = 0
                    done_talking_flag = 0
                    npc.curr_response = None

                for button in tool_sprites:
                    if button in available_tools:
                        if door_button.is_open and button.coll_check(player.rect.center):
                            button.set_hovered()
                        else:
                            button.set_released()
                if door_button.coll_check(player.rect.center):
                    door_button.set_hovered()
                else:
                    door_button.set_released()
                if event.type == pygame.KEYDOWN:
                    if not npc.is_talking:
                        player.update_delts(event)
                    if event.key == pygame.K_ESCAPE:
                        curr_screen = pause_screen
                    if event.key == pygame.K_k:
                        for button in tool_sprites:
                            if button in available_tools:
                                if door_button.is_open and button.coll_check(player.rect.center):
                                    button.sound.play()
                                    choice = button.tag
                                    print(choice)
                        if legend_button in available_tools and legend_button.coll_check(player.rect.center):
                            legend_button.sound.play()  # for hybrid, after legend is intro'd
                            curr_screen = legend_screen
                        if door_button.coll_check(player.rect.center):
                            if choice:
                                final_choice = choice
                                choice = None
                                new_outcome = outcome.check_choice(final_choice, curr_enemy)
                                new_outcome.sound.play()
                                if new_outcome.right:
                                    game_enemy.remove([curr_enemy])
                                    door_button.is_open = not door_button.is_open
                                    ts = time.time()
                                    tut_phase += 1
                                    knocked = False
                                    print("Now at phase {}".format(tut_phase))
                                    if tut_phase == 8:
                                        sandbox_time = time.time()
                                        game_sprites.add(msg_button)
                                        last_talk_action, done_talking_flag = 0, 0
                                        break
                                    if tut_phase == 4:
                                        game_sprites.add(msg_button)
                                        available_tools.append(legend_button)
                                        break

                            elif not door_button.is_open and time.time() - ts > 1:
                                door_button.is_open = not door_button.is_open
                                door_button.sound.play()
                                if msg_button not in game_sprites:
                                    pop_sound.play()
                                    game_sprites.add(msg_button)
                                curr_enemy = tut_enemies[tut_lvl]
                                game_enemy.add([curr_enemy])
                                tut_lvl += 1
                                enemy_title = textfont.render(curr_enemy.title, 1, (0, 0, 0))

                            else:
                                # TODO: NPC says "First pick an item"
                                pass

                    # if event.key == pygame.K_l:
                    #     msg_texts = npc_talk(npc, msg_button, game_sprites, player, tut_phase)

                if event.type == pygame.KEYUP:
                    if not npc.is_talking:
                        player.update_delts(event, down=False)
                    if event.key == pygame.K_l:
                        next_button.set_released()
            update_frame(player, npc, game_sprites, tool_sprites, core_surface, text_window, msg_texts,
                         text_sprites, door_button)


        elif tut_phase == 4:  # Legend
            door_button.set_released()
            for event in pygame.event.get():
                if legend_last_talk_action == 4:
                    tut_phase += 1
                    print("Now at phase {}".format(tut_phase))
                    break
                if event.type == pygame.QUIT:
                    running = False
                msg_texts, legend_last_talk_action = npc.npc_talk(msg_button, game_sprites, player, tut_phase,
                                                           [legend_const_action == 3 and visited_legend],
                                                           [npc.resps['legend']], event, next_button,
                                                           textfont)
                if legend_const_action != 3:
                    legend_const_action = legend_last_talk_action
                if legend_button.coll_check(player.rect.center):
                    legend_button.set_hovered()
                else:
                    legend_button.set_released()
                if event.type == pygame.KEYDOWN:
                    if not npc.is_talking:
                        player.update_delts(event)
                    if event.key == pygame.K_ESCAPE:
                        curr_screen = pause_screen
                    if event.key == pygame.K_k:
                        if legend_button.coll_check(player.rect.center):
                            legend_button.sound.play()
                            curr_screen = legend_screen
                    # if event.key == pygame.K_l:
                    #     msg_texts = npc_talk(npc, msg_button, game_sprites, player, tut_phase)

                if event.type == pygame.KEYUP:
                    if not npc.is_talking:
                        player.update_delts(event, down=False)
                    if event.key == pygame.K_l:
                        next_button.set_released()
            update_frame(player, npc, game_sprites, tool_sprites, core_surface, text_window, msg_texts,
                         text_sprites, door_button)

        elif tut_phase == 8:

            for event in pygame.event.get():
                msg_texts, last_talk_action = npc.npc_talk(msg_button, game_sprites, player, tut_phase,
                                        [npc_flag, new_outcome.wrong, new_outcome.right],
                                        [npc.resps['done'], npc.resps['try'], npc.npc_good()], event, next_button, textfont)
                if last_talk_action == 3:
                    done_talking_flag = last_talk_action
                if last_talk_action == 4: #Finished respondings
                    new_outcome.reset()
                    last_talk_action = 0
                    npc.curr_response = None
                    if npc_flag:
                        game_sprites.remove(npc, msg_button)
                        tut_phase = 10
                        tut_lvl = 0
                        break
                if npc.is_talking:
                    player.deltas = [0, 0]
                if time.time() - ts > 1 and not knocked:
                    knock_sound.play()
                    knocked = True
                if event.type == pygame.QUIT:
                    running = False

                for button in tool_sprites:
                    if button in available_tools:
                        if door_button.is_open and button.coll_check(player.rect.center):
                            button.set_hovered()
                        else:
                            button.set_released()
                if door_button.coll_check(player.rect.center):
                    door_button.set_hovered()
                else:
                    door_button.set_released()
                if event.type == pygame.KEYDOWN:
                    if not npc.is_talking:
                        player.update_delts(event)
                    if event.key == pygame.K_ESCAPE:
                        curr_screen = pause_screen
                    if event.key == pygame.K_n:
                        npc_flag = True
                        sandbox_time = time.time() - sandbox_time
                        #break
                    if event.key == pygame.K_k:
                        for button in tool_sprites:
                            if button in available_tools:
                                if door_button.is_open and button.coll_check(player.rect.center):
                                    button.sound.play()
                                    choice = button.tag
                                    print(choice)
                        if legend_button in available_tools and legend_button.coll_check(player.rect.center):
                            legend_button.sound.play()  # for hybrid, after legend is intro'd
                            curr_screen = legend_screen
                        if door_button.coll_check(player.rect.center):
                            if choice:
                                final_choice = choice
                                choice = None
                                new_outcome = outcome.check_choice(final_choice, curr_enemy)
                                new_outcome.sound.play()
                                new_outcome.sound.play()
                                if new_outcome.right:
                                    game_enemy.remove([curr_enemy])
                                    door_button.is_open = not door_button.is_open
                                    knocked = False
                                    tut_accumulative.append(time.time() - tut_ts)  # For the learning curve
                                    ts = time.time()

                            elif not door_button.is_open and time.time() - ts > 1:
                                door_button.is_open = not door_button.is_open
                                door_button.sound.play()
                                curr_enemy_num = randrange(0, 28)
                                print(curr_enemy_num)
                                tut_ts = time.time()
                                curr_enemy = all_enemies[curr_enemy_num]
                                game_enemy.add(curr_enemy)
                                enemy_title = textfont.render(curr_enemy.title, 1, (0, 0, 0))

                    if event.key == pygame.K_l:
                        sandbox_approaches += 1

                if event.type == pygame.KEYUP:
                    if not npc.is_talking:
                        player.update_delts(event, down=False)
                    if event.key == pygame.K_l:
                        next_button.set_released()
                    if event.key == pygame.K_n:
                        next_button.set_released()
            update_frame(player, npc, game_sprites, tool_sprites, core_surface, text_window, msg_texts,
                         text_sprites, door_button)


        else:  # Not tutorial
            for event in pygame.event.get():
                if time.time() - ts > 1 and not knocked:
                    pop_sound.play()
                    knocked = True
                if event.type == pygame.QUIT:
                    running = False
                for button in tool_sprites:
                    if button in available_tools:
                        if door_button.is_open and button.coll_check(player.rect.center):
                            button.set_hovered()
                        else:
                            button.set_released()
                if door_button.coll_check(player.rect.center):
                    door_button.set_hovered()
                else:
                    door_button.set_released()
                if event.type == pygame.KEYDOWN:
                    player.update_delts(event)
                    if event.key == pygame.K_ESCAPE:
                        curr_screen = pause_screen
                    if event.key == pygame.K_k:
                        for button in tool_sprites:
                            if button in available_tools:
                                if door_button.is_open and button.coll_check(player.rect.center):
                                    button.sound.play()
                                    choice = button.tag
                                    print(choice)
                        if legend_button in available_tools and legend_button.coll_check(player.rect.center):
                            legend_button.sound.play()  # for hybrid, after legend is intro'd
                            curr_screen = legend_screen
                        if door_button.coll_check(player.rect.center):  # TODO: Use Enemy coll check
                            if choice:
                                final_choice = choice
                                choice = None
                                new_outcome = outcome.check_choice(final_choice, curr_enemy)
                                new_outcome.sound.play()
                                answered_correctly.append(new_outcome.right)
                                game_enemy.remove([curr_enemy])
                                door_button.is_open = not door_button.is_open
                                #reaction_times.append(time.time() - perf_ts)  # For the learning curve
                                ts = time.time()
                                knocked = False
                                if tut_lvl > len(game_enemies) - 1:
                                    curr_screen = finish_screen
                                    acc = ear.accuracy(answered_correctly)
                                    time = ear.avg_time(reaction_times)
                                    ear.report_performance_mail(acc, time, sandbox_approaches, tut_accumulative,
                                                                answered_correctly, chosen_npc, FRIEND)
                            elif not door_button.is_open and time.time() - ts > 1:
                                door_button.is_open = not door_button.is_open
                                door_button.sound.play()
                                curr_enemy = game_enemies[tut_lvl]
                                game_enemy.add([curr_enemy])
                                tut_lvl += 1
                                perf_ts = time.time()
                                enemy_title = textfont.render(curr_enemy.title, 1, (0, 0, 0))
                if event.type == pygame.KEYUP:
                    player.update_delts(event, down=False)

            update_frame(player, None, game_sprites, tool_sprites, core_surface, text_window, msg_texts,
                         text_sprites, door_button)

    elif curr_screen == legend_screen:
        visited_legend = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    curr_screen = level_0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_k:
                    cont_button.set_released()

    # TODO: Add player performance stats for the player to see?
    elif curr_screen == finish_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    finish_button.set_hovered()
                    finish_button.sound.play()
                    running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_k:
                    finish_button.set_released()
        finish_buttons.draw(core_surface)
        finish_buttons.update()

    clock.tick()
    # print(clock.get_fps())
    pygame.display.update()  # TODO bad for perfomance, should keep a list of objects(rects/sprites) that are updated and only update them
