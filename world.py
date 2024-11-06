import pygame
from enemy import Enemy
from spike import Spike

class World:
    def __init__(self, data, slime_group, spike_group):
        self.tile_list = []

        dirt_img = pygame.image.load("img/ground0.png")
        ground2_img = pygame.image.load("img/ground2.png")

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (40, 40))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * 40
                    img_rect.y = row_count * 40
                    self.tile_list.append((img, img_rect))
                elif tile == 2:
                    img = pygame.transform.scale(ground2_img, (40, 40))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * 40
                    img_rect.y = row_count * 40
                    self.tile_list.append((img, img_rect))
                elif tile == 3:
                    slime = Enemy(col_count * 40, row_count * 40 + 5)
                    slime_group.add(slime)
                elif tile == 6:
                    spike = Spike(col_count * 40, row_count * 40 + 25)
                    spike_group.add(spike)
                col_count += 1
            row_count += 1

    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)
