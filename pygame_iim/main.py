import pygame
from operator import add


def start_setup(game_dims, game_name, icon_path, bg_path):
    home_screen = pygame.display.set_mode(game_dims)

    pygame.display.set_caption(game_name)
    icon = pygame.image.load(icon_path)
    bg = pygame.image.load(bg_path).convert()  # Tutorial guy said it's important
    bg = pygame.transform.smoothscale(bg, game_dims)  # Changes image dims
    pygame.display.set_icon(icon)
    return home_screen, bg


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


def move_player(delts, speed):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            delts[0] -= speed
        if event.key == pygame.K_d:
            delts[0] += speed
        if event.key == pygame.K_w:
            delts[1] -= speed
        if event.key == pygame.K_s:
            delts[1] += speed
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_a or event.key == pygame.K_d:
            delts[0] = 0
        if event.key == pygame.K_w or event.key == pygame.K_s:
            delts[1] = 0


pygame.init()
game_size = (800, 600)
home_screen, bg = start_setup(game_size, 'Tomidos project', 'game_images/monster.png', 'game_images/hm_bg.png')
player_img = pygame.image.load('game_images/hm_player_core.png')
player_img = pygame.transform.smoothscale(player_img, (161, 107))
player_coords = [370, 480]
# The Game Loop
running = True
deltas = [0, 0]
while running:
    home_screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        move_player(deltas, 0.45)
    player_coords = list(map(add, player_coords, deltas))  # should be time efficient
    border_check(game_size, player_coords, 32)
    player(home_screen, player_img, player_coords)
    pygame.display.update()  # TODO bad for perfomance, should keep a list of objects(rects/sprites) that are updated and only update them
