import pygame
import glob
from PIL import Image, ImageOps
from operator import add
import time
import math
from os import listdir


# TODO - Npc and Player classes
# Toggle between them as the right direction key is pressed.
# In case of an animated button - define the 'sensitive zone'? and find a way to get the button's coordinates.

class Animated_Sprite(pygame.sprite.Sprite):
    def __init__(self, animation_path, animation_speed, pos_x, pos_y, game_size, img_format='png'):
        super().__init__()
        self.sprites = []
        for f in glob.glob(animation_path + '/*.' + img_format):
            img = pygame.image.load(f)
            img = pygame.transform.smoothscale(img, game_size)
            self.sprites.append(img)
        self.current_sprite = 0
        self.speed = animation_speed
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]


class Button(Animated_Sprite):
    def __init__(self, animation_path, animation_speed, pos_x, pos_y, game_size, sound_path=None, img_format='png'):
        super().__init__(animation_path, animation_speed, pos_x, pos_y, game_size, img_format)
        self.button_size = game_size
        self.key_pressed = False
        self.key_released = False
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)

    def set_hovered(self):
        self.key_pressed = True
        self.key_released = False

    def set_released(self):
        self.key_released = True
        self.key_pressed = False

    def update(self):
        if self.key_pressed and self.current_sprite == 0:
            self.current_sprite += self.speed

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0

        if self.key_released:
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

    def coll_check(self, event_pos):
        return (event_pos[0] in range(self.rect.center[0] - self.button_size[0] // 2,
                                      self.rect.center[0] + self.button_size[0] // 2)) and \
               (event_pos[1] in range(self.rect.center[1] - self.button_size[1] // 2,
                                      self.rect.center[1] + self.button_size[1] // 2))


class Player(Animated_Sprite):
    def __init__(self, animation_path, animation_speed, pos_x, pos_y, game_size, move_speed, step_sound_path=None,
                 img_format='png'):
        super().__init__(animation_path, animation_speed, pos_x, pos_y, game_size, img_format)
        self.key_dir_pressed = [False, False]
        self.key_dir_released = [False, False]
        self.deltas = [0, 0]
        self.curr_dir = 0
        if step_sound_path:
            self.sound = pygame.mixer.Sound(step_sound_path)
        self.flipped_sprites = []
        self.player_speed = move_speed
        for f in glob.glob(animation_path + '/*.' + img_format):
            image = Image.open(f)
            image = ImageOps.mirror(image)
            mode = image.mode
            size = image.size
            data = image.tobytes()
            img = pygame.image.fromstring(data, size, mode)
            img = pygame.transform.smoothscale(img, game_size)
            self.flipped_sprites.append(img)

    def set_pressed(self, dir_idx):
        self.key_dir_pressed[dir_idx] = True
        self.key_dir_released[dir_idx] = False

    def set_released(self):
        self.key_dir_pressed = [False, False]
        self.key_dir_released = [True, True]

    def update(self):

        if any(self.key_dir_pressed):
            if self.key_dir_pressed[0]:
                self.curr_dir = 0  # Right
            else:
                self.curr_dir = 1  # Left
            self.current_sprite += self.speed

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0

        if self.key_dir_released:
            self.current_sprite = 0

        if self.curr_dir:
            self.image = self.flipped_sprites[int(self.current_sprite)]
        else:
            self.image = self.sprites[int(self.current_sprite)]

    def update_delts(self, event, down=True):
        if down:
            if event.key == pygame.K_a:
                self.deltas[0] -= self.player_speed
                self.set_pressed(1)
            if event.key == pygame.K_d:
                self.deltas[0] += self.player_speed
                self.set_pressed(0)
            if event.key == pygame.K_w:
                self.deltas[1] -= self.player_speed
            if event.key == pygame.K_s:
                self.deltas[1] += self.player_speed
        else:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                self.deltas[0] = 0
                self.set_released()
            if event.key == pygame.K_w or event.key == pygame.K_s:
                self.deltas[1] = 0

    def move_player(self):
        self.rect.center = list(map(add, list(self.rect.center), self.deltas))


class NPC(Animated_Sprite):
    def __init__(self, animation_path, animation_speed, pos_x, pos_y, game_size, move_speed, loc_offset,
                 step_sound_path=None, img_format='png'):
        super().__init__(animation_path, animation_speed, pos_x, pos_y, game_size, img_format)
        self.key_dir_pressed = [False, False]
        self.key_dir_released = [False, False]
        self.deltas = [0, 0]
        self.curr_dir = 0
        if step_sound_path:
            self.sound = pygame.mixer.Sound(step_sound_path)
        self.flipped_sprites = []
        self.move_speed = move_speed
        for f in glob.glob(animation_path + '/*.' + img_format):
            image = Image.open(f)
            image = ImageOps.mirror(image)
            mode = image.mode
            size = image.size
            data = image.tobytes()
            img = pygame.image.fromstring(data, size, mode)
            img = pygame.transform.smoothscale(img, game_size)
            self.flipped_sprites.append(img)
        self.dx, self.dy = 0, 0
        self.rect.center = [pos_x + loc_offset, pos_y + loc_offset]

    def move_towards_player(self, player):
        self.dx, self.dy = player.rect.center[0] - self.rect.center[0], player.rect.center[1] - self.rect.center[1]
        if abs(self.dx) >= 70 or abs(self.dy) >= 70:
            dist = math.dist(player.rect.center, self.rect.center)
            self.dx, self.dy = self.dx / dist, self.dy / dist  # Normalize
            self.deltas[0] += self.dx * self.move_speed
            self.deltas[1] += self.dy * self.move_speed
        else:
            self.deltas = [0, 0]
        self.rect.center = list(map(add, list(self.rect.center), self.deltas))

    def update(self):
        if self.dx < 0:
            self.curr_dir = 1
        else:
            self.curr_dir = 0
        if self.curr_dir:
            self.image = self.flipped_sprites[int(self.current_sprite)]
        else:
            self.image = self.sprites[int(self.current_sprite)]


class Msg_Button(Button):
    def __init__(self, animation_path, animation_speed, pos_x, pos_y, game_size, y_offset, npc: NPC, sound_path=None,
                 img_format='png'):
        super().__init__(animation_path, animation_speed, pos_x, pos_y, game_size, sound_path, img_format)
        rect_center = [npc.rect.center[0], npc.rect.center[1] + y_offset]
        self.rect.center = rect_center
        self.npc = npc
        self.y_offset = y_offset

    def update(self):
        super().update()
        self.image = self.sprites[int(self.current_sprite)]
        rect_center = [self.npc.rect.center[0], self.npc.rect.center[1] + self.y_offset]
        self.rect.center = rect_center
