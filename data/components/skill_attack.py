from . import bullet
import pygame as pg
from .. import constants as c
import time


class Skill_attack(bullet.Bullet):
    def __init__(self, owner, damage, direction, skill_style, owner_name, ):
        super().__init__(owner, damage, direction, skill_style)

        self.skill_style = skill_style
        self.owner_name = owner_name
        if self.skill_style == 'skull' and self.owner_name == 'Spider_prince':
            self.passed_distance = 0
            self.animation_speed = 8
            self.skill_size = (178 // 3, 709 // 4)
            self.image = pg.transform.scale(pg.image.load('images/bullet/' + skill_style + '/0.png'), self.skill_size)
            self.rect = self.image.get_rect()
            self.frame_numbers = 6
            self.decay_distance = [40, 80, 120, 160, 200, 300]
            self.decay_range = 1.2
            self.penetration_mode = 3
        elif self.skill_style == 'cross' and self.owner_name == 'Poena':
            self.animation_speed = 4
            self.skill_size = (137 // 2, 178 // 2)
            self.image = pg.transform.scale(pg.image.load('images/bullet/' + skill_style + '/0.gif').convert(), self.skill_size)
            self.rect = self.image.get_rect()
            self.frame_numbers = 11
        elif self.skill_style == 'servent' and self.owner_name == 'Ghost':
            self.born_time = time.time()
            self.animation_speed = 4
            self.skill_size = (80 // 3, 146 // 3)
            self.image = pg.transform.scale(pg.image.load('images/bullet/' + skill_style + '/0.gif').convert(), self.skill_size)
            self.frame_numbers = 8
            self.rect = self.image.get_rect()
        elif self.skill_style == 'dodge' and self.owner_name == 'Archer':
            self.animation_speed = 4
            self.skill_size = (154 // 3, 150 // 3)
            self.image = pg.transform.scale(pg.image.load('images/bullet/' + skill_style + '/0.gif').convert(), self.skill_size)
            self.frame_numbers = 6
        elif self.skill_style == 'ice_flame' and self.owner_name == 'Iccy':
            self.animation_speed = 4
            self.skill_size = (154 // 3, 150 // 3)
            self.image = pg.transform.scale(pg.image.load('images/bullet/' + skill_style + '/0.png'), self.skill_size)
            self.frame_numbers = 24
            self.rect = self.image.get_rect()

    def update(self):
        if self.skill_style == 'skull' and self.owner_name == 'Spider_prince':
            self.passed_distance += abs(self.x_vel)
            for dis in self.decay_distance:
                if self.passed_distance == dis:
                    if dis == 300:
                        self.kill()
                    else:
                        tmp = self.rect.bottom
                        self.skill_size = (
                            int(self.skill_size[0] / self.decay_range), int(self.skill_size[1] / self.decay_range))
                        self.counter += 1
                        self.counter %= self.frame_numbers * self.animation_speed
                        self.image = pg.transform.scale(
                            pg.image.load(
                                'images/bullet/%s/%s.png' % (self.skill_style, self.counter // self.animation_speed)),
                            self.skill_size)
                        self.rect.size = self.skill_size
                        self.rect.bottom = tmp
            else:
                self.counter += 1
                self.counter %= self.frame_numbers * self.animation_speed
                if self.counter // self.animation_speed != (self.counter - 1) // self.animation_speed:
                    self.image = pg.transform.scale(
                        pg.image.load('images/bullet/%s/%s.png' % (self.skill_style, self.counter // self.animation_speed)),
                        self.skill_size)
        elif self.skill_style == 'cross' and self.owner_name == 'Poena':
            if self.counter != self.frame_numbers * self.animation_speed - 1:
                self.counter += 1
            if self.counter // self.animation_speed != 10:
                self.rect.x -= round(self.x_vel)
            tmp = self.rect.centery
            if self.counter // self.animation_speed < 4:
                self.image = pg.transform.scale(
                    pg.image.load('images/bullet/%s/%s.gif' % (self.skill_style, self.counter // self.animation_speed)).convert(),
                    (268 // 4, 66 // 4))
                self.rect.size = self.image.get_rect().size
            else:
                tmp = self.rect.centery
                self.image = pg.transform.scale(
                    pg.image.load('images/bullet/%s/%s.gif' % (self.skill_style, self.counter // self.animation_speed)).convert(),
                    self.skill_size)
                self.rect.size = self.image.get_rect().size
            self.rect.centery = tmp
            if self.direction == 'left':
                self.image = pg.transform.flip(self.image, True, False)
        elif self.skill_style == 'servent' and self.owner_name == 'Ghost':
            if time.time() - self.born_time >= 1 / 100 and self.counter >= self.frame_numbers * self.animation_speed - 1:
                self.kill()
                return
            if self.counter < self.frame_numbers * self.animation_speed - 1:
                self.counter += 1
                self.image = pg.transform.scale(
                    pg.image.load('images/bullet/%s/%s.gif' % (self.skill_style, self.counter // self.animation_speed)).convert(),
                    self.skill_size)
                if self.direction == c.LEFT:
                    self.image = pg.transform.flip(self.image, True, False)
        elif self.skill_style == 'ice_flame' and self.owner_name == 'Iccy':
            if self.counter < self.frame_numbers * self.animation_speed - 1:
                self.counter += 1
                self.image = pg.image.load('images/bullet/%s/%s.png' % (self.skill_style, self.counter // self.animation_speed))
                self.image = pg.transform.scale(self.image,(self.image.get_rect().size[0] // 2,self.image.get_rect().size[1]//2))
                self.rect.size = self.image.get_rect().size
                if self.direction == c.LEFT:
                    self.image = pg.transform.flip(self.image, True, False)
            else:
                self.kill()
        else:
            self.counter += 1
            self.counter %= self.frame_numbers * self.animation_speed
            self.image = pg.transform.scale(
                pg.image.load('images/bullet/%s/%s.gif' % (self.skill_style, self.counter // self.animation_speed)).convert(),
                self.skill_size)
        super().update()
