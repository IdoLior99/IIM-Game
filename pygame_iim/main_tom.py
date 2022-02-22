import pygame
from game_objects import *
import time


##################################################### MEASURES #########################################################

reaction_times = []
answered_correctly = []
tut_accumulative = []  # TODO: for the learning curve

################################################## END OF MEASURES #####################################################


def fit_bg_dims(game_dims, bg_path):
    bg = pygame.image.load(bg_path).convert()  # Tutorial guy said it's important
    bg = pygame.transform.smoothscale(bg, game_dims)  # Changes image dims
    return bg


def game_setup(game_dims, game_name, icon_path, bg_path):
    screen = pygame.display.set_mode(game_dims) # add pygame.FULLSCREEN if fullscreen
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

################################################# CREATE ENEMIES #######################################################

# TODO: use For loop
single_opts = ["Princess", "Robot", "Farmer", "Cookie Monster", "Tooth", "Businessman", "Ghost"]
Princess = Enemy("ToT - Princess", 600, 150, (215, 162), "Princess", img_format='png') # TODO: Need get?
Robot = Enemy("ToT - Robot", 600, 150, (215, 162), "Robot", img_format='png')
Farmer = Enemy("ToT - Farmer", 600, 150, (215, 162), "Farmer", img_format='png')
Cookie = Enemy("ToT - Cookie Monster - cartoon", 600, 150, (215, 162), "Cookie Monster", img_format='png')
Tooth = Enemy("ToT - Toothy", 600, 150, (215, 162), "Tooth", img_format='png')
Business = Enemy("ToT - Businessman", 600, 150, (215, 162), "Business", img_format='png')
Ghost = Enemy("ToT - Ghost", 600, 150, (215, 162), "Ghost", img_format='png')
reg_enemies = [Princess, Robot, Farmer, Cookie, Tooth, Business, Ghost]
hybrid_enemies = []
for i, i_opt in enumerate(single_opts):
    for j in range(i+1, len(single_opts)):
        j_opt = single_opts[j]
        hybrid_enemies.append(Enemy(f"ToT - {i_opt}-{j_opt}", 600, 150, (215, 162), i_opt, j_opt, img_format='png'))
all_enemies = reg_enemies.copy()
all_enemies.extend(hybrid_enemies)
################################################# ENEMIES DONE #########################################################

################################################# INIT STUFF ###########################################################

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

################################################# INIT DONE ############################################################


################################################# SCREENS ##############################################################

################################################# MENU SCREEN ##########################################################

# Main Menu Buttons
menu_buttons = pygame.sprite.Group()
play_button = Button('game_assets/play_button', 1, 400, 200, (215, 162),
                     sound_path='game_assets/sounds/button_click.wav')
quit_button = Button('game_assets/quit_button', 1, 400, 400, (215, 162),
                     sound_path='game_assets/sounds/button_click.wav')
menu_buttons.add(play_button, quit_button)

################################################# GAME SCREEN ##########################################################

# Game Background
level_0 = fit_bg_dims(game_size, 'game_assets/hm_bg.png')

# Game Buttons
lvl_buttons = pygame.sprite.Group()
candy_button = Button('game_assets/quit_button', 1, 100, 400, (215, 162),
                     sound_path='game_assets/sounds/button_click.wav')
fruit_button = Button('game_assets/quit_button', 1, 300, 400, (215, 162),
                     sound_path='game_assets/sounds/button_click.wav')
money_button = Button('game_assets/quit_button', 1, 500, 400, (215, 162),
                     sound_path='game_assets/sounds/button_click.wav')
trick_button = Button('game_assets/quit_button', 1, 700, 400, (215, 162),
                     sound_path='game_assets/sounds/button_click.wav')
door_button = Button('game_assets/quit_button', 1, 600, 150, (160, 200),
                     sound_path='game_assets/sounds/button_click.wav')
lvl_buttons.add(candy_button, fruit_button, money_button, trick_button, door_button)
lvl_buttons_list = [candy_button, fruit_button, money_button, trick_button, door_button]

# Game Answer outcome
outcome = Outcome(X_sound_path='game_assets/sounds/button_click.wav',
                  V_sound_path='game_assets/sounds/button_click.wav')

# Game characters
characters = pygame.sprite.Group()
player = Player('game_assets/player', 0, 370, 480, (161, 107), 1, img_format='PNG')
npc = NPC('game_assets/skully', 0, 370, 480, (48, 54), 1, loc_offset=100, img_format='PNG')
characters.add(npc)
characters.add(player)

# Game Enemies

# REVEAL = [Tut_Enemy, ...., Tut_Last_Enemy] # TODO: should cover all basic types and 1 or 2 hybrids?
# TUTORIAL = [Tut_Enemy, ...., Tut_Last_Enemy] # TODO: Random mixtures of all options?
MAX_LVL = 10
game_enemies = [all_enemies[0], all_enemies[17], all_enemies[26], all_enemies[4], all_enemies[16], all_enemies[6],
           all_enemies[11], all_enemies[13], all_enemies[3], all_enemies[9]]  # TODO: in len MAX_LVL


################################################# FINISH SCREEN ########################################################

# Finish screen Background
finish_screen = fit_bg_dims(game_size, 'game_assets/hm_bg.png')

# Finish Screen Buttons

finish_buttons = pygame.sprite.Group()
finish_button = Button('game_assets/quit_button', 1, 400, 300, (215, 162),
                     sound_path='game_assets/sounds/button_click.wav')
finish_buttons.add(finish_button)

################################################# SCREENS DONE #########################################################






curr_screen = main_menu
curr_screen_flag = main_menu
lvl = 0
choice = None
door_mode = True
clock = pygame.time.Clock()
#TODO add default anchor points for player - npc spawn locations.
while running:
    core_surface.blit(curr_screen, (0, 0))

    if curr_screen == main_menu:
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
                if curr_screen == main_menu:
                    if play_button.coll_check(event.pos):
                        play_button.set_hovered()
                    else:
                        play_button.set_released()
                    if quit_button.coll_check(event.pos):
                        quit_button.set_hovered()
                    else:
                        quit_button.set_released()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if curr_screen == main_menu:
                    if quit_button.coll_check(event.pos):
                        quit_button.sound.play()
                        time.sleep(0.3)
                        running = False
                    elif play_button.coll_check(event.pos):
                        play_button.sound.play()
                        curr_screen_flag = level_0

    elif curr_screen == level_0:
        # THIS HAPPENS WHEN THE PLAYER IS NEAR THE "Buttons" like MOUSEMOTION but its player motion
        for button in lvl_buttons_list:
            if button.coll_check(player.rect.center):
                button.set_hovered()
            else:
                button.set_released()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                player.update_delts(event)
                # TODO: this is very wrong. only a test
                # TODO: Sounds: Use Right\Wrong sound for when the . like "Woohoo" and "ohhh :(".
                # TODO: there's already a KEYDOWN in beginning of running. maybe use it.
                if event.key == pygame.K_k and not door_mode:
                    print("AND IT WAS K")
                    if candy_button.coll_check(player.rect.center):
                        print("TOOK A CANDY")
                        candy_button.sound.play()  # TODO: If Candy pressed "SWEET!" sound
                        choice = "Candy"
                    elif fruit_button.coll_check(player.rect.center):
                        fruit_button.sound.play()  # TODO: If Fruit pressed "WOOHOO" sound
                        choice = "Fruit"
                    elif money_button.coll_check(player.rect.center):
                        money_button.sound.play()  # TODO: If Money pressed "Ka-ching $$$" sound
                        choice = "Money"
                    elif trick_button.coll_check(player.rect.center):
                        trick_button.sound.play()  # TODO: If Trick pressed "Ha Ha" sound
                        choice = "Trick"
                    elif door_button.coll_check(player.rect.center):
                        door_mode = True
                        final_choice = choice
                        choice = None
                        outcome = outcome.check_choice(final_choice, curr_enemy)
                        outcome.sound.play()
                        answered_correctly.append(outcome.right)
                        # TODO: also append times. intervals between figure shows (door click) to choice (mouse click)
                        # TODO: close the door
                        if lvl == MAX_LVL:
                            curr_screen_flag = finish_screen
                        else:
                            time.sleep(2)
                            door_button.sound.play()  # TODO: KNOCK KNOCK KNOCK
                if event.key == pygame.K_k and door_mode:
                    if door_button.coll_check(player.rect.center):
                        # TODO: Start stopwatch
                        door_mode = False
                        curr_enemy = game_enemies[lvl]
                        # TODO: deploy the enemty
                        lvl += 1

                if event.key == pygame.K_ESCAPE:
                    curr_screen = main_menu
            if event.type == pygame.KEYUP:
                player.update_delts(event, down=False)




    player.move_player()
    npc.move_towards_coords(player)
    player.rect.center = border_check(game_size, player.rect.center, 32)
    npc.rect.center = border_check(game_size, npc.rect.center, 32)
    curr_screen = curr_screen_flag
    if curr_screen == level_0:
        characters.draw(core_surface)
        characters.update()
        lvl_buttons.draw(core_surface)
        lvl_buttons.update()

    if curr_screen == main_menu:
        menu_buttons.draw(core_surface)
        menu_buttons.update()

    if curr_screen == finish_screen:
        finish_buttons.draw(core_surface)
        finish_buttons.update()
    clock.tick()
    #print(clock.get_fps())

    pygame.display.update()  # TODO bad for perfomance, should keep a list of objects(rects/sprites) that are updated and only update them

