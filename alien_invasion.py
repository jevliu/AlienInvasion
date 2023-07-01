"""
创建一个表示游戏的类，用以创建空的Pygame窗口
"""
import sys
import pygame

from settings import Settings
from ship import Ship


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()  # 用于初始化背景设置
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))  # 创建显示窗口
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)

    # 方法重构，添加辅助方法
    def _check_events(self):
        """响应案件和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    # 将更新屏幕的方法从run_game中转移到_update_screen()方法中
    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        # 让最近绘制的屏幕可见
        pygame.display.flip()


    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 监视键盘和鼠标事件,使用辅助方法
            self._check_events()

            # 每次循环时都重绘屏幕
            self._update_screen()


if __name__ == "__main__":
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
