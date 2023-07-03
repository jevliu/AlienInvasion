"""
添加爆炸效果
"""
import pygame
from pygame.sprite import Sprite


class Explosion(Sprite):
    """描述爆炸效果的类"""
    def __init__(self,ai_game,center):
        """创建爆炸对象并确定位置"""
        super().__init__()
        self.settings = ai_game.settings
        self.image = pygame.image.load("images/explosion.png")
        self.rect = self.image.get_rect(center=center)



