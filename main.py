import pygame
import sys
from player import Player
from world import World
from enemy import Enemy
from spike import Spike

# 初始化 Pygame
pygame.init()
clock = pygame.time.Clock()
fps = 60

# 设置窗口
screen_width = 1800
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My First Pygame Window")

# 加载背景图片和音乐
bg_img = pygame.image.load("img/Background/Ocean_1/4.png")
sun_img = pygame.image.load("img/sun.png")
pygame.mixer.music.load("music/game-music-loop.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

# 实例化玩家、敌人组、陷阱组和地图
player = Player(100, screen_height - 130)
slime_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()

# 设定地图数据并生成地图
world_data = [
    # （...在这里放置地图数据...）
]
world = World(world_data, slime_group, spike_group)

# 游戏主循环
running = True
game_over = 0
while running:
    clock.tick(fps)
    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (800, 50))

    # 绘制地图和敌人、陷阱
    world.draw(screen)
    slime_group.draw(screen)
    spike_group.draw(screen)

    # 更新玩家状态
    game_over = player.update(game_over, world, slime_group, spike_group, screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    pygame.display.flip()

pygame.quit()
