"""
创建一个表示游戏的类，用以创建空的Pygame窗口
"""
import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet, BigBullet
from alien import Alien


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()  # 用于初始化背景设置
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))  # 创建显示窗口
        # 创建全屏模式的显示窗口
        # self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        # 创建一个用于储存雍熙统计信息的实例
        self.status = GameStats(self)

        self.ship = Ship(self)
        # 以编组的方式来操作发射出去的子弹
        self.bullets = pygame.sprite.Group()
        self.big_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._creat_fleet()

    def _creat_fleet(self):
        """创建外星人群"""
        # 创建一个外星人并计算一行可容纳多少个外星人
        # 外星人的间距为外星人的宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_alien_x = available_space_x // (2 * alien_width)

        # 计算屏幕可容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # 创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                self._creat_alien(alien_number, row_number)

    # 重构_creat_fleet，将创建外星人的工作转移出来
    def _creat_alien(self, alien_number, row_number):
        """根据alien_number创建外星人并加入到self.aliens中"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """有外星人到达屏幕边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人向下移动，并改变它们的移动方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    # 方法重构，添加辅助方法
    def _check_events(self):
        """响应案件和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # 判断时间是否为能触发游戏相应的按键事件
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            # 当玩家松开按下的右键时将moving_right标志设置为False
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    # 重构_check_events方法，将检查KEYDOWN和KEYUP的事件移到两个辅助方法中
    def _check_keydown_events(self, event):
        """响应按键按下"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = True
        # 当玩家按下'Q'键时结束游戏，无需再使用鼠标进行点击关闭
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_g:
            self._fire_big_bullet()

    def _check_keyup_events(self, event):
        """响应按键松开"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """创建一棵子弹，并将其加入到编组bullets中"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _fire_big_bullet(self):
        """创建一个大号子弹并加入到编组中"""
        if len(self.big_bullets) < self.settings.big_bullet_allowed:
            new_big_bullet = BigBullet(self)
            self.big_bullets.add(new_big_bullet)

    # 将更新屏幕的方法从run_game中转移到_update_screen()方法中
    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for big_bullet in self.big_bullets.sprites():
            big_bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def _update_bullets(self):
        """更新子弹的位置并处置消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()
        self.big_bullets.update()
        # 处理消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        for big_bullet in self.big_bullets.copy():
            if big_bullet.rect.bottom <= 0:
                self.big_bullets.remove(big_bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """"响应子弹和外星人碰撞的方法"""
        # 检查是否有子弹击中了外星人
        # 如果是，就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        big_collisions = pygame.sprite.groupcollide(self.big_bullets, self.aliens, False, True)

        if not self.aliens:
            # 删除现有子弹并新建一群外星人
            self.bullets.empty()
            self.big_bullets.empty()
            self._creat_fleet()

    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

        # 检查是否有外星人到达屏幕底部
        self._check_aliens_bottom()

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.status.ship_left > 0:
            # 将ship_left的数目减少一个
            self.status.ship_left -= 1

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人，并将飞船重新移动到屏幕底部的中央
            self._creat_fleet()
            self.ship.center_ship()

            # 暂停一下
            sleep(0.5)
        else:
            self.status.game_active = False

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底部"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 向飞船撞到外星人一样进行处理
                self._ship_hit()
                break

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 监视键盘和鼠标事件,使用辅助方法
            self._check_events()
            # 飞船的位置将在检测到键盘事件后，但在更新屏幕前进行更新
            if self.status.game_active:
                # 仅在游戏处于活动状态时才运行下面的代码
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            # 每次循环时都重绘屏幕
            self._update_screen()


if __name__ == "__main__":
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
