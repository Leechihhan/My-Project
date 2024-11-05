import pygame

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load("img/Trap1.png")
        self.image = pygame.transform.scale(img, (50, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
