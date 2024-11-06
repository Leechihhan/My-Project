import pygame
import sys
import cv2
import numpy as np

# 初始化 Pygame
pygame.init()

# 设置窗口大小
screen_width = 1400
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu with Blurred Background")

# 加载图片并进行旋转、翻转、模糊处理
image_path = "MenuAsset/menu_bg.png"  # 确保路径正确
original_image = cv2.imread(image_path)

# 检查图像是否加载成功
if original_image is None:
    print("Failed to load the image.")
    sys.exit()

# 顺时针旋转 90 度
rotated_image = cv2.rotate(original_image, cv2.ROTATE_90_CLOCKWISE)

# 水平翻转
flipped_image = cv2.flip(rotated_image, 1)

# 缩放图像以适应窗口
# flipped_image = cv2.resize(flipped_image, (screen_width, screen_height))

# 模糊处理
blurred_image = cv2.GaussianBlur(flipped_image, (21, 21), 0)

# 将 OpenCV 图像转换为 Pygame 表面
blurred_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2RGB)  # 转换颜色格式
blurred_surface = pygame.surfarray.make_surface(blurred_image)  # 转换为 Pygame 表面

# 加载 PNG 按钮图像
start_img = pygame.image.load("img/start_button.png").convert_alpha()
quit_img = pygame.image.load("img/quit_button.png").convert_alpha()
start_img = pygame.transform.scale(start_img, (200, 60))
quit_img = pygame.transform.scale(quit_img, (200, 60))

# 游戏主循环的标志
game_running = False

# 开始游戏的函数
def start_game():
    global game_running
    game_running = True

# 退出游戏的函数
def quit_game():
    pygame.quit()
    sys.exit()

# 定义按钮函数
def draw_button(screen, image, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # 按钮的矩形区域
    button_rect = pygame.Rect(x, y, width, height)
    if button_rect.collidepoint(mouse):
        if click[0] == 1 and action is not None:
            action()
    # 显示按钮图像
    screen.blit(image, (x, y))

# 主菜单函数
def main_menu(screen):
    global game_running
    game_running = False  # 重置游戏状态

    while not game_running:
        # 显示模糊背景
        screen.blit(blurred_surface, (0, 0))

        # 绘制标题
        font = pygame.font.Font(None, 50)
        title_text = font.render("MyCat", True, (255, 255, 255))
        screen.blit(title_text, ((screen.get_width() - title_text.get_width()) // 2, 100))

        # 绘制按钮
        draw_button(screen, start_img, 300, 250, 200, 60, start_game)
        draw_button(screen, quit_img, 300, 350, 200, 60, quit_game)

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

    return game_running  # 返回游戏状态，用于切换到游戏主循环

# 运行主菜单
if __name__ == "__main__":
    main_menu(screen)
