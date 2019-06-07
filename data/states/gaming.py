import pygame as pg
from pygame.sprite import Group

from .. import tools
from .. import setup
from .. import constants as c
from ..components import hero as ch
from ..components import brick
from ..components import props
from ..components import Darling
from ..components import guan_gong
from ..components import k
from ..components import Archer
from ..components import spider_prince
from ..components import poena
from ..components import ghost
from ..components import iccy
import random
import threading
from ..components import skill_attack

class Gaming(tools._State):
    def __init__(self):
        super(Gaming, self).__init__()

    def startup(self, current_time, persist):
        self.game_info = persist
        self.persist = self.game_info
        self.game_info[c.CURRENT_TIME] = current_time
        self.current_screen_bottom=600
        self.next = c.GAME_OVER

        self.x_collide_counter = 0
        #self.done = True

        self.screen_rect = pg.Rect((0, 0), c.SCREEN_SIZE)

        self.setup_background()
        #self.setup_BGM()

        self.setup_bricks()
        self.setup_characters()
        # self.setup_killing_items()
        self.setup_action_group()
        # self.setup_spritegroups()
        self.setup_props()
        self.setup_splines()
        self.setup_MPsphere()
        self.setup_icons()


    def setup_icons(self):
        self.icons = Group()
        self.icons.add(props.Icon(0, 1, self.game_info[c.P1_CHARACTER]))
        self.icons.add(props.Icon(760, 1, self.game_info[c.P2_CHARACTER]))


    def setup_splines(self):
        self.MaxHP = []
        for character in self.characters_group.sprites():
            self.MaxHP.append(character.HP)
        self.HPSplinesSpace = Group()
        self.HPSplinesSpace.add(props.Spline_Space(0, 0, 6))
        self.HPSplinesSpace.add(props.Spline_Space(630, 0, 6))
        self.HPSplines = Group()
        self.HPSplines.add(props.Spline(40, 0, self.MaxHP[0], 6))
        self.HPSplines.add(props.Spline(630, 0, self.MaxHP[1], 6))

    # noinspection PyArgumentList
    def setup_background(self):
        self.viewport = self.screen_rect
        self.background = pg.transform.scale(pg.image.load('images/game_background.jpg'), c.SCREEN_SIZE)
        self.map = pg.Surface(c.MAP_SIZE).convert()
        self.last_scroll_time = self.current_time
        self.scrolling_up = False
        self.scroll_count = 0


    @staticmethod
    def setup_BGM():
        pg.mixer.music.load('music/{}'.format(c.GAMING_BGM))
        pg.mixer.music.play()


    def setup_MPsphere(self):
        self.MPgroupMAX = [Group(), Group()]
        for i in range(0, 6):
            self.MPgroupMAX[0].add(props.MPsphere(c.MP_POS[0][0] + i * 20, c.MP_POS[0][1]))
            self.MPgroupMAX[1].add(props.MPsphere(c.MP_POS[1][0] - i * 20, c.MP_POS[1][1]))


    def setup_splines(self):
        self.MaxHP = []
        for character in self.characters_group.sprites():
            self.MaxHP.append(character.max_HP)
        self.HPSplinesSpace = Group()
        self.HPSplinesSpace.add(props.Spline_Space(0, 0, 6))
        self.HPSplinesSpace.add(props.Spline_Space(630, 0, 6))
        self.HPSplines = Group()
        self.HPSplines.add(props.Spline(40, 0, self.MaxHP[0], 6))
        self.HPSplines.add(props.Spline(630, 0, self.MaxHP[1], 6))


    def setup_props(self):
        self.prop_count = 0
        self.props_group = Group()


    @staticmethod
    def create_prop(props_group, row, col, prop_kind):
        x = row * c.BRICK_WIDTH
        y = col * c.BRICK_HEIGHT
        props_group.add(props.Prop(x, y, prop_kind))


    def setup_bricks(self):
        #map_num=random.randint(1,100)%3
        map = "images/map"+'0.txt'
        self.bricks_group = Group()
        self.bricks_images = {}
        self.brick_counter = 0
        for brick_kind in tools.kindOfBrick.keys():
            self.bricks_images[brick_kind] = {}
            self.bricks_images[brick_kind]['image'] = []
            if tools.kindOfBrick[brick_kind]['movable']:
                self.bricks_images[brick_kind]['max_frame'] = tools.kindOfBrick[brick_kind]['frame']
                for frame in range(0, self.bricks_images[brick_kind]['max_frame']):
                    self.bricks_images[brick_kind]['image'].append(
                        pg.transform.scale(pg.image.load(tools.kindOfBrick[brick_kind]['name'] + '%d.png' %
                                                        (frame)).convert(),
                                                    (c.BRICK_WIDTH, c.BRICK_HEIGHT)))
            else:
                self.bricks_images[brick_kind]['max_frame'] = 1
                self.bricks_images[brick_kind]['image'].append(
                    pg.transform.scale(pg.image.load(tools.kindOfBrick[brick_kind]['name'] + '.png').convert(),
                                                (c.BRICK_WIDTH, c.BRICK_HEIGHT)))
        with open(map) as file_object:
            lines = file_object.readlines()
            for line in lines:
                line = line.strip().split(',')
                self.create_bricks(self.bricks_group, int(line[0]), int(line[1]), int(line[2]), int(line[3]),
                                   eval(line[4]))
        # self.break_bricks = 0


    def create_bricks(self, bricks, x, y, width, height, ground_kind):  # ground_kind为表示什么砖块条的字符串
        for row in list(range(x, x + width)):
            for col in list(range(y, y + height)):
                if (row == x):
                    self.create_brick(bricks, row, col, tools.kindOfGround[ground_kind][0])
                elif (row == x + width - 1):
                    self.create_brick(bricks, row, col, tools.kindOfGround[ground_kind][2])
                else:
                    self.create_brick(bricks, row, col, tools.kindOfGround[ground_kind][1])


    @staticmethod
    def create_brick(bricks, row, col, brick_kind):
        x = row * c.BRICK_WIDTH
        y = col * c.BRICK_HEIGHT
        bricks.add(brick.Brick(x, y, brick_kind))



    def setup_characters(self):
        characters = [
            {
                c.DARLING: Darling.Darling(),
                c.GUAN_GONG: guan_gong.Guan_gong(),
                c.K: k.K(),
                c.ARCHER: Archer.Archer(),
                c.SPIDER_PRINCE: spider_prince.Spider_prince(),
                c.POENA: poena.Poena(),
                c.GHOST: ghost.Ghost(),
                c.ICCY: iccy.Iccy()
            },
            {
                c.DARLING: Darling.Darling(),
                c.GUAN_GONG: guan_gong.Guan_gong(),
                c.K: k.K(),
                c.ARCHER: Archer.Archer(),
                c.SPIDER_PRINCE: spider_prince.Spider_prince(),
                c.POENA: poena.Poena(),
                c.GHOST: ghost.Ghost(),
                c.ICCY: iccy.Iccy()
            },
        ]

        player_1 = characters[0][self.game_info[c.P1_CHARACTER]]
        player_1.player_num = 0
        player_1.rect.x = 0
        player_1.rect.y = 0
        player_1.state = c.FALLING

        player_2 = characters[1][self.game_info[c.P2_CHARACTER]]
        player_2.player_num = 1
        player_2.rect.right = c.SCREEN_WIDTH
        player_2.rect.y = 0
        player_2.state = c.FALLING

        self.characters_group = Group(player_1, player_2)


    def setup_action_group(self):
        self.action_group = Group()


    def update(self, surface, keys, current_time):
        self.game_info[c.CURRENT_TIME] = self.current_time = current_time
        self.handle_state(keys)
        #self.check_if_finish()
        self.blit_everything(surface)


    def handle_state(self, keys):
        self.update_all_sprites(keys)
        self.update_viewport()


    def update_props(self):
        self.prop_count += 1
        if self.prop_count >= 1000:
            self.create_prop(self.props_group, random.randint(1, 30), 0, 'Prop_MP_potion')
            self.create_prop(self.props_group, random.randint(1, 30), 0, 'Prop_HP_potion')
            self.create_prop(self.props_group, random.randint(1, 30), 0, 'Prop_Shoe')
            #self.create_prop(self.props_group, random.randint(1, 30), 0, 'Prop_HP_Apple')
            #self.create_prop(self.props_group, random.randint(1, 30), 0, 'Prop_HP_Ginseng')
            self.prop_count = 0


    def update_all_sprites(self, keys):
        self.update_props()
        self.update_brick()
        for character in self.characters_group.sprites():
            character.update(keys, tools.keybinding[character.player_num],
                             self.game_info, self.action_group)
        self.adjust_sprite_positions()
        self.action_group.update()
        self.props_group.update()


    def update_brick(self):
        self.brick_counter += 1
        #self.brick_counter %= self.max_frame * c.MOVING_BRICK_SPEED


    def update_viewport(self):
        if self.current_time<=0:
           pass
        elif self.current_screen_bottom>=c.MAP_HEIGHT-50:
            pass
        elif self.current_time - self.last_scroll_time >= c.SCROLL_TIME:
            self.scrolling_up = True
            self.scroll_count = 0
            self.last_scroll_time = self.current_time

        if self.scrolling_up:
            self.viewport.y += 1
            self.scroll_count += 1
            self.current_screen_bottom+=1
            if self.scroll_count == c.SCROLL_LEN:
                self.scrolling_up = False


    def adjust_sprite_positions(self):
        self.adjust_characters_position()
        # self.adjust_bullets_position()
        self.adjust_action_item_position()
        self.adjust_props_position()
        # self.check_swords_collisions()
        self.adjust_bricks_position()


    def adjust_characters_position(self):
        for character in self.characters_group.sprites():
            character.rect.x += round(character.x_vel)
            self.check_character_x_edge(character)
            self.check_character_x_collisions(character)

            character.rect.y += round(character.y_vel)
            self.check_character_under_bottom(character)
            self.check_character_y_collisions(character)
            #self.check_collider_under_bottom(character)


    @staticmethod
    def check_character_x_edge(character):
        if character.rect.left < 0:
            character.rect.left = 0
        if character.rect.right > c.SCREEN_WIDTH:
            character.rect.right = c.SCREEN_WIDTH


    def check_character_x_collisions(self, character):
        brick = pg.sprite.spritecollideany(character, self.bricks_group)
        prop = pg.sprite.spritecollideany(character, self.props_group)
        if character.name == c.GUAN_GONG and character.state == c.SKILLING:
            for ch in self.characters_group.sprites():
                if ch != character:
                    another_character = pg.sprite.collide_rect(character, ch)
            if another_character:
                for ch in self.characters_group:
                    if ch != character:
                        ch.HP -= character.skill_damage
                        ch.state = c.FALLING
                        if ch.HP <= 0:
                            self.reset_character(ch)
                        else:
                            ch.rect.y -= 50
                # another_character.HP -= character.skill_damage
                # if another_character.HP <= 0:
                #     self.reset_character(another_character)
                # else:
                #     another_character.rect.x -= 10
                #     another_character.rect.y -= 10
                character.state = c.FALLING

        if brick:
            if brick.kind != 'water':
                self.adjust_character_for_x_collisions(character, brick)
            if brick.kind == 'fire':
                pass
            if brick.HP<=0:
                brick.kill()
        if prop:
            prop.ActOnCharacters(character)
            prop.kill()


    @staticmethod
    def adjust_character_for_x_collisions(character, collider):

        if character.name == c.GUAN_GONG and character.state == c.SKILLING:
            collider.kill()
        else:
            if character.rect.x < collider.rect.x:
                character.rect.right = collider.rect.left
            else:
                character.rect.left = collider.rect.right

            character.x_vel = 0


    def check_character_y_collisions(self, character):
        brick = pg.sprite.spritecollideany(character, self.bricks_group)
        prop = pg.sprite.spritecollideany(character, self.props_group)

        if brick:
            if brick.kind != 'water':
                self.adjust_character_for_y_collisions(character, brick)
            if brick.kind == 'fire':
                pass
            if brick.HP<=0:
                brick.kill()
        if prop:
            prop.ActOnCharacters(character)
            prop.kill()

        self.check_if_collider_is_falling(character)


    @staticmethod
    def adjust_character_for_y_collisions(character, collider):
        if character.name == c.GUAN_GONG and character.state == c.SKILLING:
            pass
        else:
            if character.rect.y < collider.rect.y:
                character.rect.bottom = collider.rect.top
                character.state = c.WALKING
            else:
                character.rect.top = collider.rect.bottom

            character.y_vel = 0


    def check_character_under_bottom(self, character):
        if character.rect.top >= self.viewport.bottom:
            character.HP = 0
            self.reset_character(character)


    def check_collider_under_bottom(self, collider):
        if collider.rect.top >= self.viewport.bottom:
            collider.kill()


    def check_if_collider_is_falling(self, collider):
        collider.rect.y += 1
        #test_collide_group = pg.sprite.Group(self.bricks_group)
        bricks_list = pg.sprite.spritecollide(collider, self.bricks_group, False)

        if len(bricks_list) == 0:
            if collider.state != c.JUMPING and collider.state != c.SKILLING and \
                            collider.state != c.ACTIONING and collider.state != c.FREEZING:  # 飞起来
                collider.state = c.FALLING
        else:
            for brick in bricks_list:
                brick.ActOnCharacter(collider)
                if collider.HP <= 0:
                    self.reset_character(collider)
                    break

        collider.rect.y -= 1


    def adjust_action_item_position(self):
        for action_item in self.action_group.sprites():
            if action_item.type == c.BULLET:
                self.adjust_bullet_position(action_item)
            elif action_item.type == c.SWORD:
                self.check_sword_collisions(action_item)


    def adjust_bullet_position(self, bullet):
        if bullet.rect.right < 0:
            bullet.kill()
        if bullet.rect.left > c.SCREEN_WIDTH:
            bullet.kill()
        if bullet.rect.bottom < 0:
            bullet.kill()
        self.check_bullet_x_collisions(bullet)


    def check_bullet_x_collisions(self, bullet):
        character = pg.sprite.spritecollideany(bullet, self.characters_group)
        brick = pg.sprite.spritecollideany(bullet, self.bricks_group)

        if character:
            if bullet.owner != character.player_num:
                if (character.vincible):
                    character.HP -= bullet.damage
                if character.HP <= 0:
                    self.reset_character(character)
                if bullet.penetration_mode != 4:
                    bullet.kill()

        if brick:
            tmp = brick.HP
            if bullet.penetration_mode < 3:
                brick.HP -= bullet.damage
            if brick.HP <= 0:
                brick.kill()
            if bullet.penetration_mode == 1:
                bullet.kill()
            elif bullet.penetration_mode == 2:
                bullet.damage -= tmp
                if bullet.damage <= 0:
                    bullet.kill()


    def adjust_props_position(self):
        for prop in self.props_group:
            self.check_and_adjust_prop_for_y_collisions(prop)
            self.check_collider_under_bottom(prop)
            self.check_if_collider_is_falling(prop)


    def check_and_adjust_prop_for_y_collisions(self, prop):
        brick = pg.sprite.spritecollideany(prop, self.bricks_group)
        if brick:
            prop.state = c.STANDING
            prop.rect.bottom = brick.rect.top


    def check_sword_collisions(self, sword):
        bricks = pg.sprite.spritecollide(sword, self.bricks_group, False)
        action_items = pg.sprite.spritecollide(sword, self.action_group, True)
        character = pg.sprite.spritecollideany(sword, self.characters_group)

        if bricks:
            self.apply_swords_damage_to_items(sword, bricks)
            # if self.apply_swords_damage(sword, bricks):
            #    self.break_bricks += 1

        # if bullets:
        #    self.apply_swords_damage(bullets)

        if character:
            self.apply_swords_damage_to_character(sword, character)


    @staticmethod
    def apply_swords_damage_to_items(sword, coll_dict):
        for collider in coll_dict:
            if (collider.vincible):
                collider.HP -= sword.damage
            if collider.HP <= 0:
                collider.kill()
                # return True
        # return False


    def apply_swords_damage_to_character(self, sword, character):
        character.HP -= sword.damage
        if character.HP <= 0:
            self.reset_character(character)


    def adjust_bricks_position(self):
        for brick in self.bricks_group.sprites():
            if brick.rect.bottom < self.viewport.top:
                brick.kill()


    def blit_everything(self, surface):
        self.map.blit(self.background, self.viewport)
        for character in self.characters_group.sprites():
            self.map.blit(character.image, character.show_xy)
        for brick in self.bricks_group.sprites():
            if brick.rect.top < self.viewport.bottom:
                max_frame = self.bricks_images[brick.kind]['max_frame']
                self.map.blit(self.bricks_images[brick.kind]['image'][self.brick_counter % (max_frame * c.MOVING_BRICK_SPEED) // c.MOVING_BRICK_SPEED], brick.rect)
        #self.bricks_group.draw(self.map)
        self.props_group.draw(self.map)
        for action_item in self.action_group.sprites():
            if action_item.type == c.BULLET:
                self.map.blit(action_item.image, action_item.rect)

        surface.blit(self.map, (0, 0), self.viewport)
        # Icons
        for icon in self.icons.sprites():
            surface.blit(icon.image, icon.rect)

        # MP
        for i in range(0, 2):
            for k in range(0, self.characters_group.sprites()[i].MP):
                surface.blit(self.MPgroupMAX[i].sprites()[k].image, self.MPgroupMAX[i].sprites()[k].rect)

        # HP
        for spline_space_item in self.HPSplinesSpace.sprites():
            self.map.blit(spline_space_item.image, spline_space_item.rect)
        for character, spline_item in zip(self.characters_group.sprites(), self.HPSplines.sprites()):
            if character.HP > 0:
                spline_item.scale_change(character.HP)
                surface.blit(spline_item.image, spline_item.rect)
            else:
                spline_item.reset()
                #surface.blit(spline_item.image, spline_item.rect)


    def reset_character(self, character):
        character.heart -= 1
        if character.heart <= 0:
            #character.kill()
            self.finish()
        else:
            #character.HP = 0
            #character.reset_character_state()
            character.rect.left = random.randint(1, c.SCREEN_WIDTH-c.BRICK_WIDTH)
            character.rect.bottom = self.viewport.top
            character.state = c.FREEZING
            character.freeze_time = self.current_time
            #print(self.current_time, character.freeze_time)


    def finish(self):
        for character in self.characters_group.sprites():
            if character.player_num == 0:
                self.game_info[c.P1_HP] = character.HP
                self.game_info[c.P1_HEART] = character.heart
            else:
                self.game_info[c.P2_HP] = character.HP
                self.game_info[c.P2_HEART] = character.heart
        self.done = True
