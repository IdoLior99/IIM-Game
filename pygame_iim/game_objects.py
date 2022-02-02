import pygame


# TODO- draw button sprites
class Button(pygame.sprite.Sprite):
    def __init__(self, idle_img_path, pressed_img_path):
        super().__init__()
        self.image = pygame.image.load(idle_img_path)
        self.alt_image = pygame.image.load(pressed_img_path)
        self.rect = self.image.get_rect()
        self.alt_rect = self.alt_image.get_rect()

    def update(self):
        temp = self.rect    
        self.rect = self.alt_rect
        self.alt_rect = temp

