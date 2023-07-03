"""
处理每次给游戏添加新功能时需要引入一些新设置的模块
"""


class Settings:
    """储存游戏中所有与设置有关的类"""

    def __init__(self):
        """初始化游戏静态设置"""

        # 设置屏幕

        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 设置飞船移动的速度
        self.ship_speed = 0.5
        self.ship_limit = 3

        # 设置子弹
        self.bullet_speed = 1
        self.bullet_width = 5
        self.bullet_height = 20
        self.bullet_color = (100,149,137)
        self.bullets_allowed = 3  # 限制当前屏幕可见区域内子弹大最大数量

        # 设置大号子弹的型形状
        self.big_bullet_width = 300
        self.big_bullet_height = 10
        self.big_bullet_color = (220,20,60)
        self.big_bullet_allowed = 1

        # 外星人设置
        # self.alien_speed = 0.1
        self.fleet_drop_speed = 10
        # fleet_direction为1表示向右移动，为-1表示向左移动
        # self.fleet_direction = 1

        # 加快游戏节奏的速度
        self.speed_scale = 1.5
        # 外星人分数提高速度
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置，外星人移动的越来越快"""
        # self.ship_speed = 0.5
        # self.bullet_speed = 1
        self.alien_speed = 0.1
        # 计分
        self.alien_points = 50
        # self.ship_limit = 3


        # fleet_direction为1表示向右，为-1表示向左
        self.fleet_direction = 1

    def increase_speed(self):
        """提高速度设置"""
        # self.ship_speed *= self.speed_scale
        # self.bullet_speed *= self.speed_scale
        self.alien_speed *= self.speed_scale
        self.alien_points = int(self.alien_points * self.score_scale)
