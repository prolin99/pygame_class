import sys
import time

import pygame
from bullet import Bullet
from settings import Settings
from ship import Ship
from alien import Alien
from game_stats import GameStats
from button import Button

from pygame.sprite import Group


class Game_functions():
    def __init__(self):
        self.ai_settings = Settings()
        self.screen= pygame.display.set_mode((self.ai_settings.screen_width, self.ai_settings.screen_height))
        self.ship = Ship(self.ai_settings , self.screen)
        #子彈編組
        self.bullets = Group()

        #外星人

        self.aliens = Group()
        self.create_fleet()

        self.stats = GameStats(self.ai_settings)

        self.play_button = Button(self.ai_settings , self.screen , "Play")

    def check_keydown_events(self):
        if self.event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if self.event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if self.event.key == pygame.K_SPACE:
            self.fire_bullet()
        if self.event.key == pygame.K_q:
            sys.exit()

    def check_keyup_events(self):
        if self.event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if self.event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def check_events(self):
        for self.event in pygame.event.get():
            if self.event.type == pygame.QUIT:
                sys.exit()
            elif self.event.type == pygame.KEYDOWN:
                self.check_keydown_events()
            elif self.event.type == pygame.KEYUP:
                self.check_keyup_events()
            elif self.event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x , mouse_y = pygame.mouse.get_pos()
                self.check_play_button( mouse_x, mouse_y)

    def check_play_button(self, mouse_x , mouse_y):
        if self.play_button.rect.collidepoint(mouse_x, mouse_y) and not self.stats.game_active:
            self.stats.reset_stats()
            self.aliens.empty()
            self.bullets.empty()
            self.ship.center_ship()
            self.create_fleet()
            self.stats.game_active = True

            pygame.mouse.set_visible(False)





    def update_screen(self):
            #畫面重新
            self.screen.fill(self.ai_settings.bg_color)
            self.update_ship()
            self.update_bullets()
            self.update_aliens()
            if not self.stats.game_active:
                self.play_button.draw_button()

            #
            pygame.display.flip()

    def update_bullets(self):
        #位置計算
        self.bullets.update()
        #子彈消失
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)
        #每次都重繪
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        #是否撃中 ，擊中後就會自動刪除 groupcollide(group1, group2, dokill1, dokill2, collided = None) -> Sprite_dict
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens , True, True )

        if len(self.aliens) ==0 :
            self.bullets.empty()
            self.create_fleet()


    def fire_bullet(self):
        if len(self.bullets) < self.ai_settings.bullets_allowed:
            new_bullet = Bullet(self.ai_settings, self.screen, self.ship)
            self.bullets.add(new_bullet)

    def update_ship(self):
        #位置計算
        self.ship.update()
        #繪製
        self.ship.blitme()


    def create_fleet(self):
        #外星人 建立
        alien = Alien(self.ai_settings , self.screen)
        alien_width = alien.rect.width
        alien_height = alien.rect.height

        available_space_x = self.ai_settings.screen_width -2 * alien_width
        number_aliens_x =  int(available_space_x /(2*alien_width))

        available_space_y = self.ai_settings.screen_height - (3 * alien_height) -60
        number_rows =  int(available_space_y /(2*alien_height))

        #行數
        for row_number in range(number_rows):
            #水平可放入幾個
            for alien_number in range(number_aliens_x):
                alien = Alien(self.ai_settings , self.screen )
                alien.x = alien_width +2 * alien_width * alien_number
                alien.rect.x = alien.x
                alien.rect.y = alien.rect.height +2 * alien.rect.height * row_number
                self.aliens.add(alien)

    #外星人更新重繪
    def update_aliens(self):
        self.check_fleet_edges()
        self.aliens.update()
        self.aliens.draw(self.screen)

        #是否碰觸
        if pygame.sprite.spritecollideany(self.ship, self.aliens ):
            self.ship_hit()

        #是否觸底
        self.ckeck_aliens_bottom()


    def ckeck_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom :
                self.ship_hit()
                break


    #觸邊
    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    #方向改變
    def change_fleet_direction(self):
        self.ai_settings.fleet_direction *= -1
        for alien in self.aliens.sprites():
            alien.rect.y += self.ai_settings.fleet_drop_speed
            #alien.ai_settings.fleet_direction = self.ai_settings.fleet_direction

    #生命減1
    def ship_hit(self):
        if self.stats.ships_left >0 :
            self.stats.ships_left -= 1

            self.aliens.empty()
            self.bullets.empty()

            self.create_fleet()
            self.ship.center_ship()
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


        time.sleep(0.5)

