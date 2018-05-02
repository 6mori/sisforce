import pygame as pg
from pygame.sprite import Group

from .. import tools, setup
from .. import constants as c
from .. components import brick
from .. components import Darling


class gaming(tools._State):
    def __init__(self):
        super(gaming, self).__init__()

    #def get_event(self, event):

    def startup(self, current_time, persist,screen):
        self.game_info = persist
        self.persist = self.game_info
        self.game_info[c.CURRENT_TIME] = current_time

        self.setup_bricks()
        self.setup_characters(screen)
        self.setup_bullets()
        #self.setup_spritegroups()


    def setup_bricks(self):
        self.bricks_group = Group()
        self.create_bricks(self.bricks_group, 0, 10, 18, 1,'grass_surface')
        self.create_bricks(self.bricks_group, 18, 14, 2, 1,'grass_surface')
        self.create_bricks(self.bricks_group, 17, 0, 1, 7,'long_wood')
        self.create_bricks(self.bricks_group, 17, 11, 1, 4,'grass_soil')
        self.create_bricks(self.bricks_group, 10, 0, 3, 7,'long_wood')
        self.create_bricks(self.bricks_group, 0, 7, 7, 1,'grass_surface')
        self.create_bricks(self.bricks_group, 0, 8, 7, 1, 'grass_soil')
        self.create_bricks(self.bricks_group, 0, 9, 7, 1, 'grass_soil')
        self.create_bricks(self.bricks_group, 0, 10, 7, 1, 'grass_soil')



    def create_bricks(self, bricks, x, y, width, height,ground_kind):#ground_kind为表示什么砖块条的字符串
        for row in list(range(x, x+width)):
            for col in list(range(y, y+height)):
                if(row==x):
                    self.create_brick(bricks,row,col,tools.kindOfGround[ground_kind][0])
                elif(row==x+width-1):
                    self.create_brick(bricks, row, col, tools.kindOfGround[ground_kind][2])
                else:
                    self.create_brick(bricks, row, col, tools.kindOfGround[ground_kind][1])


    def create_brick(self, bricks, row, col,brick_kind):
        x = row * c.BRICK_WIDTH
        y = col * c.BRICK_HEIGHT
        bricks.add(brick.Brick(x, y,brick_kind))



    def setup_characters(self,screen):
        player_1 = Darling.Darling(screen,1)
        player_1.rect.x = 0
        player_1.rect.y = 0
        player_1.state = c.FALL
        player_1.name = 'cindy'

        player_2 = Darling.Darling(screen,2)
        player_2.rect.right = c.SCREEN_WIDTH
        player_2.rect.y = 0
        player_2.state = c.FALL
        player_2.name = 'candy'

        self.characters_group = Group(player_1, player_2)


    def setup_bullets(self):
        self.bullets_group = Group()


    def update(self, surface, keys, current_time):
        self.game_info[c.CURRENT_TIME] = self.current_time = current_time
        self.handle_state(keys)
        self.blit_everything(surface)


    def handle_state(self, keys):
        self.update_all_sprites(keys)


    def update_all_sprites(self, keys):
        for character, keybinding in zip(self.characters_group.sprites(), tools.keybinding):
            character.update(keys, keybinding,  self.game_info, self.bullets_group)
        self.adjust_sprite_positions()
        self.bullets_group.update()


    def adjust_sprite_positions(self):
        self.adjust_characters_position()
        self.adjust_bullets_position()


    def adjust_characters_position(self):
        for character in self.characters_group.sprites():
            character.rect.x += round(character.x_vel)
            self.check_character_x_edge(character)
            self.check_character_x_collisions(character)

            character.rect.y += round(character.y_vel)
            self.check_character_y_collisions(character)


    def check_character_x_edge(self, character):
        if character.rect.left < 0:
            character.rect.left = 0
        if character.rect.right > c.SCREEN_WIDTH:
            character.rect.right = c.SCREEN_WIDTH


    def check_character_x_collisions(self, character):
        brick = pg.sprite.spritecollideany(character, self.bricks_group)

        if brick:
            self.adjust_character_for_x_collisions(character, brick)


    def adjust_character_for_x_collisions(self, character, collider):
        print(character.rect.x, collider.rect.x)
        if character.rect.x < collider.rect.x:
            character.rect.right = collider.rect.left
        else:
            character.rect.left = collider.rect.right

        character.x_vel = 0


    def check_character_y_collisions(self, character):
        brick = pg.sprite.spritecollideany(character, self.bricks_group)

        if brick:
            self.adjust_character_for_y_collisions(character, brick)

        self.check_if_character_is_falling(character)


    def adjust_character_for_y_collisions(self, character, collider):
        print(character.rect.y, collider.rect.y)
        if character.rect.y < collider.rect.y:
            character.rect.bottom = collider.rect.top
            character.state = c.WALK
        else:
            character.rect.top = collider.rect.bottom

        character.y_vel = 0


    def check_if_character_is_falling(self, character):
        character.rect.y += 1
        test_collide_group = pg.sprite.Group(self.bricks_group)

        if pg.sprite.spritecollideany(character, test_collide_group) is None:
                if character.state != c.JUMP and character.state != c.SKILL:        #飞起来
                    character.state = c.FALL
        character.rect.y -= 1


    def adjust_bullets_position(self):
        for bullet in self.bullets_group:
            if bullet.rect.left < 0:
                bullet.kill()
            if bullet.rect.right > c.SCREEN_WIDTH:
                bullet.kill()
            self.check_bullet_x_collisions(bullet)


    def check_bullet_x_collisions(self, bullet):
        character = pg.sprite.spritecollideany(bullet, self.characters_group)
        brick = pg.sprite.spritecollideany(bullet, self.bricks_group)

        if character:
            if bullet.owner != character.name:
                character.HP -= bullet.damage
                if character.HP <= 0:
                    character.kill()
                    self.done = True
                bullet.kill()

        if brick:
            brick.dur -= bullet.damage
            if brick.dur <= 0:
                brick.kill()
            bullet.kill()



    def blit_everything(self, surface):
        # For test
        surface.fill(c.BG_COLOR)
        for character in self.characters_group.sprites():
            character.blitme()
        for brick in self.bricks_group.sprites():
            brick.blitme(surface)
        for bullet in self.bullets_group.sprites():
            bullet.blitme(surface)
