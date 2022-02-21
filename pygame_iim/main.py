import pygame
from game_objects import *
import time
from random import randrange
import eval_and_report as ear
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


def npc_talk(npc, msg_button, game_sprites, player, tut_phase, done=False):
    if npc.text_i != tut_phase:
        npc.text_i = tut_phase
    texts = npc.texts[npc.text_i]
    msg_texts = ""
    if not npc.is_talking and msg_button in game_sprites and \
            msg_button.coll_check(player.rect.center, x_offset=50, y_offset=80):
        msg_button.set_hovered()
        msg_button.sound.play()
        npc.is_talking = True
        msg_texts = textfont.render(texts[npc.subtext_i], 1, (0, 0, 0))
    elif npc.is_talking:
        next_button.set_hovered()
        next_button.sound.play()
        npc.subtext_i += 1
        if npc.subtext_i >= len(texts):
            npc.is_talking = False
            npc.text_i += 1
            npc.subtext_i = 0
            msg_button.set_released()
            game_sprites.remove(msg_button)
        else:
            if not done:
                msg_texts = textfont.render(texts[npc.subtext_i], 1, (0, 0, 0))
            else:
                npc.is_talking = False
    return msg_texts

def npc_resp(npc, text):
    if not npc.is_talking:
        npc.is_talking = True
    return textfont.render(text, 1, (0, 0, 0))

def update_frame(player, npc, game_sprites, tool_sprites, core_surface, text_window, msg_texts, text_sprites, door):
    player.move_player()
    if npc:
        npc.move_towards_player(player)
        npc.rect.center = border_check(game_size, npc.rect.center, 32)
    player.rect.center = border_check(game_size, player.rect.center, 32)
    if door.is_open:
         core_surface.blit(title_window, (550, 25))
         core_surface.blit(enemy_title, (560, 33))
    game_enemy.draw(core_surface)
    game_sprites.draw(core_surface)
    game_sprites.update()
    tool_sprites.draw(core_surface)
    tool_sprites.update()
    if npc and npc.is_talking:
        core_surface.blit(text_window, (0, 300))
        core_surface.blit(msg_texts, (75, 440))
        text_sprites.draw(core_surface)
        text_sprites.update()



################################################# INIT STUFF ###########################################################
pygame.init()
game_size = (800, 600)
core_surface, main_menu = game_setup(game_size, 'Tomidos project', 'game_assets/monster.png',
                                     'game_assets/main_menu.png')
text_window = pygame.image.load('game_assets/text_window.PNG')
text_window = pygame.transform.smoothscale(text_window, [825, 400])  # Changes image dims
title_window = pygame.transform.smoothscale(text_window, [100, 50])  # Changes image dims
textfont = pygame.font.SysFont('leelawadeeuisemilight', 20)
level_0 = fit_bg_dims(game_size, 'game_assets/hm_bg.png')
instruct_screen = fit_bg_dims(game_size, 'game_assets/hm_bg.png')
curr_screen = main_menu
clock = pygame.time.Clock()
# TODO add default anchor points for player - npc spawn locations.
text_box_flag = False
text_i = 0
hint_text = "Press k to interact with close objects!"
pop_sound = pygame.mixer.Sound('game_assets/sounds/msg_pop.flac')
knock_sound = pygame.mixer.Sound('game_assets/sounds/door_knock_sound.mp3')
hover_time = 0
lvl = 0
npc_flag = False
choice = None
door_open = False
door_rang = False
running = True
tut_phase = 0
phase_buttons = []
tut_lvl = 0

################################################# CREATE ENEMIES #######################################################

game_enemy = pygame.sprite.Group()
# TODO: use For loop
single_opts = ["Princess", "Robot", "Farmer", "Cookie Monster", "Tooth", "Businessman", "Ghost"]
Princess = Enemy("game_images/ToT - Princess", 700, 180, (215, 162), "Princess", img_format='png')  # TODO: Need get?
Robot = Enemy("game_images/ToT - Robot", 700, 180, (215, 162), "Robot", img_format='png')
Farmer = Enemy("game_images/ToT - Farmer", 700, 180, (215, 162), "Farmer", img_format='png')
Cookie = Enemy("game_images/ToT - Cookie Monster Cartoon", 700, 180, (215, 162), "Cookie Monster", img_format='png')
Tooth = Enemy("game_images/ToT - Ghost", 700, 180, (215, 162), "Tooth", img_format='png')  # TODO: change to Toothy pic
Business = Enemy("game_images/ToT - Ghost", 700, 180, (215, 162), "Businessman", img_format='png')  # TODO: correct pic
Ghost = Enemy("game_images/ToT - Ghost", 700, 180, (215, 162), "Ghost", img_format='png')
reg_enemies = [Princess, Robot, Farmer, Cookie, Tooth, Business, Ghost]
hybrid_enemies = []
for i, i_opt in enumerate(single_opts):
    for j in range(i+1, len(single_opts)):
        j_opt = single_opts[j]
        #hybrid_enemies.append(Enemy(f"game_images/ToT - {i_opt}-{j_opt}", 600, 150, (215, 162), i_opt, j_opt, img_format='png'))
        # For Testing purposes:
        hybrid_enemies.append(Enemy(f"game_images/ToT - Robot", 700, 180, (215, 162), i_opt, j_opt, img_format='png'))
all_enemies = reg_enemies.copy()
all_enemies.extend(hybrid_enemies)

# Game Enemies

# REVEAL = [Tut_Enemy, ...., Tut_Last_Enemy] # TODO: should cover all basic types and 1 or 2 hybrids?
tut_enemies = [Cookie, Princess, Ghost, Cookie, Princess, Ghost]#, hybrid_enemies[0], hybrid_enemies[7], hybrid_enemies[4]]
MAX_LVL = 2
game_enemies = [all_enemies[0], all_enemies[2]] #all_enemies[3], all_enemies[4], all_enemies[5], all_enemies[6]]
# MAX_LVL = 10
# game_enemies = [all_enemies[0], all_enemies[17], all_enemies[26], all_enemies[4], all_enemies[16], all_enemies[6],
#            all_enemies[11], all_enemies[13], all_enemies[3], all_enemies[9]]  # TODO: in len MAX_LVL

################################################# SCREENS ##############################################################

# Main Menu Screen: ####################################################################################################
menu_sprites = pygame.sprite.Group()
play_button = Button('game_assets/play_button', 1, 400, 200, (215, 162),
                     sound_path='game_assets/sounds/button_click.wav')
quit_button = Button('game_assets/quit_button', 1, 400, 400, (215, 162),
                     sound_path='game_assets/sounds/button_click.wav')
menu_sprites.add([play_button, quit_button])

# Game Screen: #########################################################################################################
game_sprites = pygame.sprite.Group()
player = Player('game_assets/player', 0, 370, 480, (161, 107), 2, img_format='PNG')
npc_types = ["Favorite", "Hyper", "Aloof"]
random_type = randrange(0, 3)
chosen_npc = npc_types[random_type]
# TODO: change friend_name to input from player (maybe construct it mid-game).
FRIEND = "FRIEND"
npc = NPC('game_assets/skully', 0, 370, 480, (48, 54), 2, loc_offset=100, img_format='PNG',
          type=chosen_npc, friend_name=FRIEND)
msg_button = Msg_Button('game_assets/msg_button', 1, 400, 200, (100, 75), npc=npc, y_offset=-60,
                        sound_path='game_assets/sounds/button_click.wav')
text_sprites = pygame.sprite.Group()
next_button = Button('game_assets/next_button', 1, 720, 540, (107, 81),
                     sound_path='game_assets/sounds/button_click.wav')
door_button = Door('game_assets/door', 1, 700, 180, (300, 240),
                     sound_path='game_assets/sounds/door_open.wav')

# TODO add enemy sprites and what not
game_sprites.add([door_button, msg_button, npc, player])
text_sprites.add([next_button])

tool_sprites = pygame.sprite.Group()

candy_button = Button('game_assets/quit_button', 1, 100, 200, (112, 81),
                      sound_path='game_assets/sounds/candy_sound.wav', tag='Candy')
fruit_button = Button('game_assets/quit_button', 1, 300, 400, (112, 81),
                      sound_path='game_assets/sounds/button_click.wav', tag='Fruit')
money_button = Button('game_assets/quit_button', 1, 500, 600, (112, 81),
                      sound_path='game_assets/sounds/money_sound.wav', tag='Money')
trick_button = Button('game_assets/quit_button', 1, 600, 400, (112, 81),
                      sound_path='game_assets/sounds/button_click.wav', tag='Trick')

legend_button = Button('game_assets/play_button', 1, 400, 400, (112, 81),
                     sound_path='game_assets/sounds/button_click.wav')

# Door button is excluded from here
tool_sprites.add([candy_button, fruit_button, money_button, trick_button,legend_button])

# Game Answer outcome
# TODO: find sound for wrong answer and put it in X_sound_path
outcome = Outcome(X_sound_path='game_assets/sounds/button_click.wav',
                  V_sound_path='game_assets/sounds/cheering_ppl.wav')

cond = False
# door change = False and then if change has happened, load next npc message.
start_time = time.time()

# Finish Screen: #######################################################################################################
finish_screen = fit_bg_dims(game_size, 'game_assets/hm_bg.png')
finish_buttons = pygame.sprite.Group()
finish_button = Button('game_assets/quit_button', 1, 400, 300, (215, 162),
                       sound_path='game_assets/sounds/button_click.wav')
finish_buttons.add(finish_button)

# Legend Screen: #######################################################################################################
legend_screen = fit_bg_dims(game_size, 'game_assets/legend_bg.png')
legend_buttons = pygame.sprite.Group()
cont_button = Button('game_assets/continue_button', 1, 400, 300, (215, 162),
                       sound_path='game_assets/sounds/button_click.wav')
legend_buttons.add(cont_button)

msg_texts = ''
available_tools = [candy_button]
ts=0
knocked = False
phase_0_talked = False
phase_done_talking = False
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
                    start_time = time.time()
                    curr_screen = instruct_screen
        menu_sprites.draw(core_surface)
        menu_sprites.update()

    # TODO: Add before this a personal info screen for players to insert info.
    elif curr_screen == instruct_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    cont_button.set_hovered()
                    cont_button.sound.play()
                    if tut_phase == 4:
                        tut_phase += 1
                    curr_screen = level_0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_k:
                    cont_button.set_released()
        legend_buttons.draw(core_surface)
        legend_buttons.update()

    # Game Screen Stuff
    elif curr_screen == level_0:
        if tut_phase == 0:
            if phase_0_talked:
                door_button.set_hovered()
            for event in pygame.event.get():
                if phase_0_talked and time.time() - door_sw >2 :
                    knock_sound.play()
                    msg_texts = npc_resp(npc, npc.resps["knock"])
                    knocked = True
                    phase_0_talked = False
                if event.type == pygame.QUIT:
                    running = False
                if npc.is_talking:
                    player.deltas = [0, 0]
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        curr_screen = main_menu
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
                            if msg_button not in game_sprites:
                                game_sprites.add(msg_button)
                    if event.key == pygame.K_l:
                        msg_texts = npc_talk(npc, msg_button, game_sprites, player, tut_phase,done=phase_done_talking)
                        if not npc.is_talking and not phase_done_talking:
                            door_sw = time.time()
                            phase_0_talked = True
                            phase_done_talking = True

                if event.type == pygame.KEYUP:
                    if not npc.is_talking:
                        player.update_delts(event, down=False)
                    if event.key == pygame.K_l:
                        next_button.set_released()
            update_frame(player, npc, game_sprites, tool_sprites, core_surface, text_window, msg_texts, text_sprites,door_button)

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
                        curr_screen = main_menu
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
                        if curr_enemy.coll_check(player.rect.center):  # TODO: Use Enemy coll check
                            if choice:
                                final_choice = choice
                                choice = None
                                new_outcome = outcome.check_choice(final_choice, curr_enemy)
                                new_outcome.sound.play()
                                if new_outcome.right:
                                    msg_texts = npc_resp(npc, npc.npc_good())
                                    game_enemy.remove([curr_enemy])
                                    door_button.is_open = not door_button.is_open
                                    ts = time.time()
                                    tut_phase += 1
                                    if tut_phase == 8:
                                        sandbox_time = time.time()
                                    if tut_phase == 4:
                                        game_sprites.add(msg_button)
                                        available_tools.append(legend_button)
                                    knocked = False
                                    print("Now at phase {}".format(tut_phase))
                                else:
                                    msg_texts = npc_resp(npc, npc.resps["try"])

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

                    if event.key == pygame.K_l:
                        msg_texts = npc_talk(npc, msg_button, game_sprites, player, tut_phase)

                if event.type == pygame.KEYUP:
                    if not npc.is_talking:
                        player.update_delts(event, down=False)
                    if event.key == pygame.K_l:
                        next_button.set_released()
            update_frame(player, npc, game_sprites, tool_sprites, core_surface, text_window, msg_texts,
                         text_sprites, door_button)

        elif tut_phase == 4.5:
            # This tells the player that the LEGEND is always available
            msg_texts = npc_resp(npc, npc.resps["legend"])
            tut_phase += 0.5
            update_frame(player, npc, game_sprites, tool_sprites, core_surface, text_window, msg_texts,
                     text_sprites, door_button)

        elif tut_phase == 4: #Legend
            door_button.set_released()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if legend_button.coll_check(player.rect.center):
                    legend_button.set_hovered()
                else:
                    legend_button.set_released()
                if event.type == pygame.KEYDOWN:
                    if not npc.is_talking:
                        player.update_delts(event)
                    if event.key == pygame.K_ESCAPE:
                        curr_screen = main_menu
                    if event.key == pygame.K_k:
                        if legend_button.coll_check(player.rect.center):
                            legend_button.sound.play()
                            curr_screen = legend_screen
                    if event.key == pygame.K_l:
                        msg_texts = npc_talk(npc, msg_button, game_sprites, player, tut_phase)

                if event.type == pygame.KEYUP:
                    if not npc.is_talking:
                        player.update_delts(event, down=False)
                    if event.key == pygame.K_l:
                        next_button.set_released()
            update_frame(player, npc, game_sprites, tool_sprites, core_surface, text_window, msg_texts,
                         text_sprites, door_button)

        elif tut_phase == 8: #8 is sandbox phase
            for event in pygame.event.get():
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
                        curr_screen = main_menu
                    if event.key == pygame.K_n:
                        npc_flag = True
                        game_sprites.remove(npc, msg_button)
                        tut_phase = 10
                        tut_lvl = 0
                        sandbox_time = time.time() - sandbox_time
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
                        if curr_enemy.coll_check(player.rect.center):  # TODO: Use Enemy coll check
                            if choice:
                                final_choice = choice
                                choice = None
                                new_outcome = outcome.check_choice(final_choice, curr_enemy)
                                new_outcome.sound.play()
                                game_enemy.remove([curr_enemy])
                                door_button.is_open = not door_button.is_open
                                tut_accumulative.append(time.time() - tut_ts) # For the learning curve
                                ts = time.time()
                                knocked = False
                                print("Now at phase {}".format(tut_phase))

                            elif not door_button.is_open and time.time() - ts > 1:
                                door_button.is_open = not door_button.is_open
                                door_button.sound.play()
                                curr_enemy_num = randrange(0, 28)
                                print(curr_enemy_num)
                                tut_ts = time.time()
                                curr_enemy = all_enemies[curr_enemy_num]
                                game_enemy.add(curr_enemy)
                                enemy_title = textfont.render(curr_enemy.title, 1, (0, 0, 0))
                            else:
                                # TODO: NPC says "First pick an item"
                                pass

                    if event.key == pygame.K_l:
                        msg_texts = npc_talk(npc, msg_button, game_sprites, player, tut_phase)
                        sandbox_approaches += 1

                if event.type == pygame.KEYUP:
                    if not npc.is_talking:
                        player.update_delts(event, down=False)
                    if event.key == pygame.K_l:
                        next_button.set_released()
                    if event.key == pygame.K_n:
                        next_button.set_released()
            if npc_flag:
                npc = None  # TODO: line is controversial. might not work.
            update_frame(player, npc, game_sprites, tool_sprites, core_surface, text_window, msg_texts,
                         text_sprites, door_button)


        else: # Not tutorial
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
                        curr_screen = main_menu
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
                                reaction_times.append(time.time() - perf_ts)  # For the learning curve
                                ts = time.time()
                                knocked = False
                                if tut_lvl > len(game_enemies)-1:
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    cont_button.set_hovered()
                    cont_button.sound.play()
                    if tut_phase == 4:
                        tut_phase += 0.5
                    curr_screen = level_0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_k:
                    cont_button.set_released()
        legend_buttons.draw(core_surface)
        legend_buttons.update()

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
