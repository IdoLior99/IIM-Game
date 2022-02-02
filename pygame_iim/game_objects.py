import pygame
import glob


# TODO - Make Animated_Sprite class abstract, create Button ,Npc and Player classes appropriately, should look better.
# Toggle between them as the right direction key is pressed.
# In case of an animated button - define the 'sensitive zone'? and find a way to get the button's coordinates.

class Animated_Sprite(pygame.sprite.Sprite):
    def __init__(self, animation_path, speed, pos_x, pos_y, game_size, stationary=True, interactable=True, img_format='png', flip=False):
        super().__init__()
        self.sprites = []
        for f in glob.glob(animation_path + '/*.' + img_format):
            img = pygame.image.load(f)
            img = pygame.transform.smoothscale(img, game_size)
            self.sprites.append(img)
        self.current_sprite = 0
        self.speed = speed
        self.key_pressed = False
        self.key_released = False
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

        # Button = stat+inter, Player = !stat+!inter, Npc = !stat + inter, Background Torch = stat + !inter :
        self.is_stat = stationary
        self.is_inter = interactable

    def set_pressed(self):
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
                # self.is_animating = False
        if self.key_released:
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

    def coll_check(self, event_pos):
        return (event_pos[0] in range(self.rect.center[0]-100, self.rect.center[0]+100)) and \
               (event_pos[1] in range(self.rect.center[1]-50, self.rect.center[1]+50))
