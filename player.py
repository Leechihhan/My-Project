import pygame

class Player:
    def __init__(self, x, y):
        # 初始化玩家图片和其他属性
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f"img/cat/Run{num}.png")
            img_right = pygame.transform.scale(img_right, (80, 50))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        # 加载死亡图像和两种方向的受伤图像
        self.dead_image = pygame.image.load("img/cat/dead.png")
        self.dead_image = pygame.transform.scale(self.dead_image, (80, 50))
        self.hurt_image_right = pygame.image.load("img/cat/hurt.png")  # 右侧受伤图像
        self.hurt_image_right = pygame.transform.scale(self.hurt_image_right, (80, 50))
        self.hurt_image_left = pygame.transform.flip(self.hurt_image_right, True, False)  # 左侧受伤图像

        # 设置初始图像和位置
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0  # 1 表示右，-1 表示左
        self.health = 3  # 初始血量为 3
        self.invincible = False  # 是否无敌
        self.invincible_timer = 0  # 无敌时间计数
        self.hurt_timer = 0  # 受伤显示时间计时器

         # 设置初始血量和加载心形图标
        self.health = 3  # 假设初始血量为 3
        self.max_health = 3  # 最大血量
        self.heart_image = pygame.image.load("img/heart.png")  # 替换为心形图标的路径
        self.heart_image = pygame.transform.scale(self.heart_image, (30, 30))  # 调整图标大小


        # 加载受伤音效
        self.hurt_sound = pygame.mixer.Sound("music/hurt.MP3")


        # 新增：绘制血量图标的方法
    def draw_health_icons(self, screen):
        x, y = 40, 20  # 心形图标在左上角的起始位置
        for i in range(self.health):  # 根据当前血量绘制相应数量的图标
            screen.blit(self.heart_image, (x + i * 35, y))  # 每个图标之间有一定间隔


    

    # 定义 update 方法

    def update(self, game_over, screen, world, slime_group, spike_group):
        current_time = pygame.time.get_ticks()  # 记录当前时间
        dx = 0
        dy = 0
        walk_cooldown = 5

        if game_over == 0:
            # 控制玩家移动
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and not self.jumped:
                self.vel_y = -15
                self.jumped = True
            if not key[pygame.K_SPACE]:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1

            # 动画控制
            if not (key[pygame.K_LEFT] or key[pygame.K_RIGHT]):
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # 重力和碰撞检测
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        
            # 添加边界检测
            screen_width, screen_height = screen.get_size()

            # 水平方向边界检测
            if self.rect.x + dx < 0:  # 碰到左边缘
               dx = -self.rect.x
            elif self.rect.x + dx + self.width > screen_width:  # 碰到右边缘
               dx = screen_width - (self.rect.x + self.width)

            # 垂直方向边界检测
            if self.rect.y + dy < 0:  # 碰到顶部边缘
               dy = -self.rect.y
            elif self.rect.y + dy + self.height > screen_height:  # 碰到底部边缘
               dy = screen_height - (self.rect.y + self.height)

            
            

            # 玩家与敌人（史莱姆）的碰撞检测
            if pygame.sprite.spritecollide(self, slime_group, False) and not self.invincible:
                self.health -= 1  # 每次碰撞扣除 1 点血量
                self.invincible = True  # 设置无敌状态，防止重复扣血
                self.invincible_timer = current_time  # 使用当前时间记录无敌开始时间
                self.hurt_timer = current_time  # 设置受伤开始时间
                self.hurt_sound.play()  # 播放受伤音效

                # 根据方向切换到对应的受伤图像
                if self.direction == 1:
                    self.image = self.hurt_image_right
                else:
                    self.image = self.hurt_image_left

                if self.health <= 0:
                    game_over = -1  # 如果血量为 0，游戏结束

            # 处理无敌状态的计时
            if self.invincible:
                # 持续1秒无敌状态
                if current_time - self.invincible_timer > 1000:
                    self.invincible = False

                # 受伤图像显示200毫秒
                if current_time - self.hurt_timer > 500 and self.hurt_timer > 0:
                    # 恢复正常图像
                    self.image = self.images_right[self.index] if self.direction == 1 else self.images_left[self.index]
                    self.hurt_timer = 0  # 重置受伤计时器
                
                
    

            # 更新玩家的位置
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            # 显示死亡图像
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 5

        # 把玩家画到屏幕上
        screen.blit(self.image, self.rect)
       
        # 绘制角色轮廓线
        outline_surface = pygame.Surface((self.width + 4, self.height + 4), pygame.SRCALPHA)
        mask = pygame.mask.from_surface(self.image)  # 从角色图像创建掩膜
        outline_mask = mask.outline()  # 获取掩膜的轮廓
        for point in outline_mask:
        # 绘制轮廓点，稍微偏移以绘制在图像周围
           outline_surface.set_at((point[0] + 2, point[1] + 2), (255, 255, 255))  # 白色轮廓
        screen.blit(outline_surface, (self.rect.x - 2, self.rect.y - 2))  # 在屏幕上绘制轮廓


        # 返回游戏状态
        return game_over
