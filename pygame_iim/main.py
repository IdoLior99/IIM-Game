import pygame
from game_objects import *
import time

##################################################### MEASURES #########################################################
reaction_times = []
answered_correctly = []
tut_accumulative = []  # TODO: for the learning curve


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
curr_screen = main_menu
clock = pygame.time.Clock()
# TODO add default anchor points for player - npc spawn locations.
text_box_flag = False
text_i = 0
hint_text = "Press k to interact with close objects!"
pop_sound = pygame.mixer.Sound('game_assets/sounds/msg_pop.flac')
hover_time = 0
lvl = 0
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
Princess = Enemy("game_images/ToT - Princess", 600, 150, (215, 162), "Princess", img_format='png')  # TODO: Need get?
Robot = Enemy("game_images/ToT - Robot", 600, 150, (215, 162), "Robot", img_format='png')
Farmer = Enemy("game_images/ToT - Farmer", 600, 150, (215, 162), "Farmer", img_format='png')
Cookie = Enemy("game_images/ToT - Cookie Monster Cartoon", 600, 150, (215, 162), "Cookie Monster", img_format='png')
Tooth = Enemy("game_images/ToT - Ghost", 600, 150, (215, 162), "Tooth", img_format='png')  # TODO: change to Toothy pic
Business = Enemy("game_images/ToT - Ghost", 600, 150, (215, 162), "Businessman", img_format='png')  # TODO: correct pic
Ghost = Enemy("game_images/ToT - Ghost", 600, 150, (215, 162), "Ghost", img_format='png')
reg_enemies = [Princess, Robot, Farmer, Cookie, Tooth, Business, Ghost]
hybrid_enemies = []
for i, i_opt in enumerate(single_opts):
    for j in range(i+1, len(single_opts)):
        j_opt = single_opts[j]
        hybrid_enemies.append(Enemy(f"ToT - {i_opt}-{j_opt}", 600, 150, (215, 162), i_opt, j_opt, img_format='png'))
all_enemies = reg_enemies.copy()

# all_enemies.extend(hybrid_enemies)

# Game Enemies

# REVEAL = [Tut_Enemy, ...., Tut_Last_Enemy] # TODO: should cover all basic types and 1 or 2 hybrids?
tut_enemies = [Cookie, Princess, Ghost, hybrid_enemies[0], hybrid_enemies[7], hybrid_enemies[4]]
MAX_LVL = 6
game_enemies = [all_enemies[0], all_enemies[2], all_enemies[3], all_enemies[4], all_enemies[5], all_enemies[6]]
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
player = Player('game_assets/player', 0, 370, 480, (161, 107), 1, img_format='PNG')
npc = NPC('game_assets/skully', 0, 370, 480, (48, 54), 1, loc_offset=100, img_format='PNG')
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
                      sound_path='game_assets/sounds/candy_sound.wav', tag='candy')
fruit_button = Button('game_assets/quit_button', 1, 300, 400, (112, 81),
                      sound_path='game_assets/sounds/button_click.wav', tag='fruit')
money_button = Button('game_assets/quit_button', 1, 500, 600, (112, 81),
                      sound_path='game_assets/sounds/money_sound.wav', tag='money')
trick_button = Button('game_assets/quit_button', 1, 600, 400, (112, 81),
                      sound_path='game_assets/sounds/button_click.wav', tag='trick')

# Door button is excluded from here
tool_sprites.add([candy_button, fruit_button, money_button, trick_button])

# Game Answer outcome
outcome = Outcome(X_sound_path='game_assets/sounds/button_click.wav',
                  V_sound_path='game_assets/sounds/button_click.wav')

cond = False
# door change = False and then if change has happened, load next npc message.
start_time = time.time()
# Finish Screen: #######################################################################################################
finish_screen = fit_bg_dims(game_size, 'game_assets/hm_bg.png')
finish_buttons = pygame.sprite.Group()
finish_button = Button('game_assets/quit_button', 1, 400, 300, (215, 162),
                       sound_path='game_assets/sounds/button_click.wav')
finish_buttons.add(finish_button)

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
                    curr_screen = level_0
        menu_sprites.draw(core_surface)
        menu_sprites.update()

    # Game Screen Stuff
    elif curr_screen == level_0:
        if tut_phase == 0:
            # TODO: intro of NPC
            door_button.set_hovered()
            # TODO: NPC interaction "go to door"
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_k:
                        if door_button.coll_check(player.rect.center) and not door_button.is_open:
                            door_button.is_open = not door_button.is_open
                            door_button.sound.play()
                            curr_enemy = tut_enemies[tut_lvl]
                            tut_lvl += 1
                            game_enemy.add([curr_enemy])
                            enemy_title = textfont.render(curr_enemy.title, 1, (0, 0, 0))
                            tut_phase += 1

        elif tut_phase == 1:
            # TODO: NPC explains rules
            for event in pygame.event.get():
                if candy_button.coll_check(player.rect.center):
                    candy_button.set_hovered()
                else:
                    candy_button.set_released()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_k:
                        if candy_button.coll_check(player.rect.center):
                            candy_button.sound.play()
                            choice = button.tag
                            cond = True
                            print(choice)
                        if door_button.coll_check(player.rect.center):  # TODO: Use Enemy coll check
                            if choice:
                                final_choice = choice
                                choice = None
                                new_outcome = outcome.check_choice(final_choice, curr_enemy)
                                new_outcome.sound.play()  # TODO: ALSO DISPLAY "HURRAY" AND "OOPS" messages
                                # TODO: NPC says "GOOD JOB"
                                game_enemy.remove([curr_enemy])
                                door_button.is_open = not door_button.is_open
                                ts = time.time()
                                tut_phase += 1
        elif tut_phase == 2:
            for event in pygame.event.get():
                if time.time() - ts > 1 and not door_rang:
                    door_button.sound.play()
                    door_rang = True
                if door_button.coll_check(player.rect.center):
                    door_button.set_hovered()
                else:
                    door_button.set_released()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_k:
                        if door_button.coll_check(player.rect.center) and not door_button.is_open:
                            door_button.is_open = not door_button.is_open
                            door_button.sound.play()
                            curr_enemy = tut_enemies[tut_lvl]
                            tut_lvl += 1
                            game_enemy.add([curr_enemy])
                            enemy_title = textfont.render(curr_enemy.title, 1, (0, 0, 0))
                            if enemy_title == "Princess":
                                phase_buttons = [candy_button, fruit_button]
                            elif enemy_title == "Ghost":
                                phase_buttons = [candy_button, fruit_button, money_button]
                        if door_button.is_open:
                            for button in phase_buttons:
                                if button.coll_check(player.rect.center):
                                    button.set_hovered()
                                else:
                                    button.set_released()
                                if button.coll_check(player.rect.center):
                                    button.sound.play()
                                    choice = button.tag
                                    cond = True
                                    print(choice)
                            if door_button.coll_check(player.rect.center):  # TODO: Use Enemy coll check
                                if choice:
                                    final_choice = choice
                                    choice = None
                                    new_outcome = outcome.check_choice(final_choice, curr_enemy)
                                    new_outcome.sound.play()  # TODO: ALSO DISPLAY "HURRAY" AND "OOPS" messages
                                    # TODO: NPC says "GOOD JOB"
                                    game_enemy.remove([curr_enemy])
                                    door_button.is_open = not door_button.is_open
                                    ts = time.time()
                                    if enemy_title == "Ghost":
                                        tut_phase += 1
        elif tut_phase == 3:
            # TODO: NPC reveals LEGEND
            # TODO: ADD LEGEND BUTTON MECHANISM WITH COLL CHECK AND EVERYTHING.
            tut_phase += 1

        elif tut_phase == 4:
            for event in pygame.event.get():
                if time.time() - ts > 1 and not door_rang:
                    door_button.sound.play()
                    door_rang = True
                if door_button.coll_check(player.rect.center):
                    door_button.set_hovered()
                else:
                    door_button.set_released()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_k:
                        if door_button.coll_check(player.rect.center) and not door_button.is_open:
                            door_button.is_open = not door_button.is_open
                            door_button.sound.play()
                            curr_enemy = tut_enemies[tut_lvl]
                            tut_lvl += 1
                            game_enemy.add([curr_enemy])
                            enemy_title = textfont.render(curr_enemy.title, 1, (0, 0, 0))
                            if enemy_title == "Princess-Robot":
                                # TODO: NPC explains "Hybrids"
                                pass
                            if enemy_title == "Robot-Cookie Monster":
                                # TODO: NPC ANOTHER ONE DDDDDJJJJJJJ KHALLLEDDDDD
                                pass
                            if enemy_title == "Princess-Businessman":
                                phase_buttons = [candy_button, fruit_button, money_button, trick_button]
                                # TODO: NPC explains "Trick"
                        if door_button.is_open:
                            for button in phase_buttons:
                                if button.coll_check(player.rect.center):
                                    button.set_hovered()
                                else:
                                    button.set_released()
                                if button.coll_check(player.rect.center):
                                    button.sound.play()
                                    choice = button.tag
                                    cond = True
                                    print(choice)
                            if door_button.coll_check(player.rect.center):  # TODO: Use Enemy coll check
                                if choice:
                                    final_choice = choice
                                    choice = None
                                    new_outcome = outcome.check_choice(final_choice, curr_enemy)
                                    new_outcome.sound.play()  # TODO: ALSO DISPLAY "HURRAY" AND "OOPS" messages
                                    # TODO: NPC says "GOOD JOB"
                                    game_enemy.remove([curr_enemy])
                                    door_button.is_open = not door_button.is_open
                                    ts = time.time()
                                    if enemy_title == "Princess-Businessman":
                                        tut_phase += 1
        elif tut_phase == 5:
            # TODO: NPC INTRODUCES SANDBOX
            for event in pygame.event.get():
                if time.time() - ts > 1 and not door_rang:
                    door_button.sound.play()
                    door_rang = True
                if door_button.coll_check(player.rect.center):
                    door_button.set_hovered()
                else:
                    door_button.set_released()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_k:
                        # TODO: SKIP TUTORIAL BUTTON
                        if door_button.coll_check(player.rect.center) and not door_button.is_open:
                            door_button.is_open = not door_button.is_open
                            door_button.sound.play()
                            curr_enemy = tut_enemies[tut_lvl]
                            tut_lvl += 1
                            game_enemy.add([curr_enemy])
                            enemy_title = textfont.render(curr_enemy.title, 1, (0, 0, 0))
                        if door_button.is_open:
                            for button in tool_sprites:
                                if button.coll_check(player.rect.center):
                                    button.set_hovered()
                                else:
                                    button.set_released()
                                if button.coll_check(player.rect.center):
                                    button.sound.play()
                                    if button.tag not in curr_enemy.correct_answers and npc.type is "Hyper":
                                        # TODO: NPC says "Not this one"
                                        pass
                                    choice = button.tag
                                    cond = True
                                    print(choice)
                            if door_button.coll_check(player.rect.center):  # TODO: Use Enemy coll check
                                if choice:
                                    final_choice = choice
                                    choice = None
                                    new_outcome = outcome.check_choice(final_choice, curr_enemy)
                                    new_outcome.sound.play()  # TODO: ALSO DISPLAY "HURRAY" AND "OOPS" messages
                                    # TODO: NPC says "GOOD JOB"
                                    game_enemy.remove([curr_enemy])
                                    door_button.is_open = not door_button.is_open
                                    ts = time.time()
        elif tut_phase >= 6:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for button in tool_sprites:
                    if button.coll_check(player.rect.center):
                        button.set_hovered()
                    else:
                        button.set_released()
                if door_button.coll_check(player.rect.center) and not door_button.shifted:
                    door_button.set_hovered()
                else:
                    door_button.set_released()
                if event.type == pygame.KEYDOWN:
                    if not text_box_flag:
                        player.update_delts(event)
                    # if curr_screen == level_0: MAYBE NECESSARY
                    if event.key == pygame.K_ESCAPE:
                        curr_screen = main_menu
                    if event.key == pygame.K_l:
                        if not text_box_flag and msg_button in game_sprites and \
                                msg_button.coll_check(player.rect.center, x_offset=50, y_offset=80):
                            msg_button.set_hovered()
                            msg_button.sound.play()
                            text_box_flag = True
                            msg_texts = textfont.render(npc.texts[text_i], 1, (0, 0, 0))
                        elif text_box_flag:
                            next_button.set_hovered()
                            if not hover_time:
                                hover_time = time.time()
                            next_button.sound.play()
                            npc.subtext_i += 1
                            if npc.subtext_i >= len(npc.texts):
                                text_box_flag = False
                                msg_button.set_released()
                                game_sprites.remove(msg_button)
                            else:
                                msg_texts = textfont.render(npc.texts[npc.subtext_i], 1, (0, 0, 0))
                        if event.key == pygame.K_k:
                            if door_button.coll_check(player.rect.center):
                                door_button.is_open = not door_button.is_open
                                door_button.sound.play()
                            if door_open:  # door_button.is_open
                                for button in tool_sprites:
                                    if button.coll_check(player.rect.center):
                                        button.sound.play()
                                        choice = button.tag
                                        cond = True
                                        print(choice)
                                # TODO: door button needs to encapsulate entire door
                                if door_button.coll_check(player.rect.center):
                                    if choice:
                                        door_open = False
                                        print("Door Closed!")
                                        final_choice = choice
                                        # TODO: stop the stopwatch
                                        choice = None
                                        new_outcome = outcome.check_choice(final_choice, curr_enemy)
                                        new_outcome.sound.play()  # TODO: ALSO DISPLAY "HURRAY" AND "OOPS" messages
                                        game_enemy.remove([curr_enemy])
                                        answered_correctly.append(outcome.right)
                                        # TODO: also append times. intervals between figure shows (door click) to choice (mouse click)
                                        # TODO: close the door
                                        time.sleep(2)  # TO DISPLAY CORRECTNESS OF ANSWER
                                        # TODO: Next code line: Delete previous Enemy pic before waiting for next "Knock"
                                        game_enemy.draw(core_surface)
                                        if lvl == MAX_LVL:
                                            curr_screen = finish_screen
                                        else:
                                            time.sleep(2)
                                            door_button.sound.play()  # TODO: KNOCK KNOCK KNOCK
                            elif not door_open:
                                if door_button.coll_check(player.rect.center):
                                    door_open = True
                                    print("Door Opened")
                                    # TODO: Start stopwatch
                                    # TODO: Open the door
                                    curr_enemy = game_enemies[lvl]
                                    game_enemy.add([curr_enemy])
                                    enemy_title = textfont.render(curr_enemy.title, 1, (0, 0, 0))
                                    lvl += 1

                if event.type == pygame.KEYUP:
                    if not text_box_flag:
                        player.update_delts(event, down=False)
                    if event.key == pygame.K_l:
                        next_button.set_released()

            player.move_player()
            # TODO - ONLY FOR TESTING, will be changed once everything is in motion.
            if choice and cond:
                npc.update_texts()
                game_sprites.add(msg_button)
                pop_sound.play()
                cond = False
            npc.move_towards_player(player)
            player.rect.center = border_check(game_size, player.rect.center, 32)
            npc.rect.center = border_check(game_size, npc.rect.center, 32)
            game_sprites.draw(core_surface)
            game_sprites.update()
            tool_sprites.draw(core_surface)
            tool_sprites.update()
            if text_box_flag:
                core_surface.blit(text_window, (0, 300))
                core_surface.blit(msg_texts, (75, 440))
                text_sprites.draw(core_surface)
                text_sprites.update()
            if door_open: # TODO: NEEDS PHYSICAL IMPROVING
                core_surface.blit(title_window, (550, 25))
                core_surface.blit(enemy_title, (560, 33))
            game_enemy.draw(core_surface)

    elif curr_screen == finish_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                for button in finish_buttons:
                    if button.coll_check(event.pos):
                        button.set_hovered()
                    else:
                        button.set_released()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if finish_button.coll_check(event.pos):
                    finish_button.sound.play()
                    time.sleep(0.3)
                    running = False
        finish_buttons.draw(core_surface)
        finish_buttons.update()



    clock.tick()
    # print(clock.get_fps())
    pygame.display.update()  # TODO bad for perfomance, should keep a list of objects(rects/sprites) that are updated and only update them
