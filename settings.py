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

        # 设置飞船移动的速度和距离等信息
        self.ship_speed = 1.5
