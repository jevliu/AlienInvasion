"""
用于跟踪统计游戏信息的模块
"""


class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.ship_left = None
        self.settings = ai_game.settings
        self.reset_stats()
        # 游戏刚启动时处于非活跃状态
        self.game_active = False

    def reset_stats(self):
        """初始化游戏运行期间可能变化的信息"""
        self.ship_left = self.settings.ship_limit
