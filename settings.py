"""
处理每次给游戏添加新功能时需要引入一些新设置的模块
"""


class Settings:
    """储存游戏中所有与设置有关的类"""

    def __init__(self):
        """初始化游戏设置"""

        # 设置屏幕
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 设置飞船移动的速度
        self.ship_speed = 1.5

        # 设置子弹
        self.bullet_speed = 1.0
        self.bullet_width = 6
        self.bullet_height = 30
        self.bullet_color = (255, 215, 0)
        self.bullets_allowed = 3  # 限制当前屏幕可见区域内子弹大最大数量

        # 外星人设置
        self.alien_speed = 0.2
        self.fleet_drop_speed = 10
        # fleet_direction为1表示向右移动，为-1表示向左移动
        self.fleet_direction = 1
