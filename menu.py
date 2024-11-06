import pygame
import sys
import cv2

# 初始化 Pygame
pygame.init()

# 设置窗口大小
screen_width = 1400
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu with Video Background")

# 设置颜色和字体
WHITE = (255, 255, 255)
font = pygame.font.Font(None, 50)

# 视频文件路径
video_path = "MenuAsset/main_menu.mp4"  # 确保路径正确
cap = cv2.VideoCapture(video_path)  # 使用 OpenCV 打开视频文件

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
def draw_button(screen, image, y, width, height, text, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # 计算按钮的水平居中 x 坐标
    x = (screen_width - width) // 2  # 居中按钮的 x 坐标
    button_rect = pygame.Rect(x, y, width, height)
    
    # 检查鼠标是否在按钮内
    if button_rect.collidepoint(mouse):
        if click[0] == 1 and action is not None:
            action()

    # 显示按钮图像
    screen.blit(image, (x, y))
    
    # 渲染并绘制按钮文本
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# 主菜单函数
def main_menu(screen):
    global game_running
    game_running = False  # 重置游戏状态

    # 加载 PNG 按钮图像
    start_img = pygame.image.load("img/start_button.png").convert_alpha()
    quit_img = pygame.image.load("img/quit_button.png").convert_alpha()
    start_img = pygame.transform.scale(start_img, (200, 60))
    quit_img = pygame.transform.scale(quit_img, (200, 60))

    while not game_running:
        # 读取视频的下一帧
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 循环播放，重置视频到第一帧
            ret, frame = cap.read()

        # 检查视频帧是否读取成功
        if frame is not None:
            # 模糊处理并翻转、缩放帧
            frame = cv2.GaussianBlur(frame, (51, 51), 0)  # 增加模糊效果
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)  # 顺时针旋转90度
            frame = cv2.flip(frame, 1)  # 左右翻转
            frame = cv2.resize(frame, (850, 1500))  # 拉伸填满屏幕
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 转换颜色格式
            frame_surface = pygame.surfarray.make_surface(frame)  # 转换为 Pygame 表面
            
            # 计算居中位置并显示裁剪后的帧
            frame_rect = frame_surface.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(frame_surface, frame_rect.topleft)  # 居中显示视频帧

        # 绘制标题
        title_text = font.render("MyCat", True, WHITE)
        screen.blit(title_text, ((screen.get_width() - title_text.get_width()) // 2, 100))

        # 绘制按钮，添加文本
        draw_button(screen, start_img, 300, 200, 60, "Start", start_game)  # Start 按钮的 Y 坐标
        draw_button(screen, quit_img, 400, 200, 60, "Exit", quit_game)     # Exit 按钮的 Y 坐标

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
