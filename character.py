import pygame
import json
import math
import config


class Item(pygame.sprite.Sprite):
        def __init__(self, game, x, y, item_type):
            self._layer = config.item_layer
            self.groups = game.sprites, game.items
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.game = game
            self.item_type = item_type
            self.x = x * config.tilesize
            self.y = y * config.tilesize
            self.width = config.tilesize
            self.height = config.tilesize

            
            if item_type == 'gold':
                self.image = self.game.coin_spritesheet.get_sprite(174, 170, self.width * 1.25, self.height)
            
            elif item_type == 'potion':
                self.image = self.game.item_spritesheet.get_sprite(341, 6, self.width * 1.5, self.height * 1.5)
            elif item_type == 'super_potion':
                self.image = self.game.item_spritesheet.get_sprite(388, 2, self.width * 1.5, self.height * 1.5)


            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

class Bag:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def use_item(self, item_index):
        if 0 <= item_index < len(self.items):
            item = self.items.pop(item_index)
            return item
        return None

class Character(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = config.player_layer
        self.groups = self.game.sprites
        pygame.sprite.Sprite.__init__(self, self.groups) 
        self.bag = Bag()
        self.gold = 0

        # Pull controls folder
        with open('controls.json', 'r') as controls_file:
            self.controls = json.load(controls_file)

        self.x = x * config.tilesize    
        self.y = y * config.tilesize
        self.width = config.tilesize
        self.height = config.tilesize * 1.45
        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(55, 2, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def save_position(self):
        position = {'x': self.rect.x, 'y': self.rect.y}
        with open('save_file.json', 'w') as save_character_location:
            json.dump(position, save_character_location)

    def load_position(self):
        try:
            with open('save_file.json', 'r') as f:
                position = json.load(f)
                self.x = position['x']
                self.y = position['y']
        except FileNotFoundError:
            self.x = 13 * config.tilesize
            self.y = 6 * config.tilesize
            start_spawn_default = {
                'x': 13,
                'y': 6
            }
            with open('save_file.json', 'w') as default_location:
                json.dump(start_spawn_default, default_location)

    def collect_items(self):
            hits = pygame.sprite.spritecollide(self, self.game.items, True)
            for item in hits:
                if item.item_type == 'gold':
                    self.gold += 100 
                    self.game.current_gold += 100
                else:
                    self.bag.add_item(item.item_type)


    def update(self):
        self.movement()
        self.animate()
        self.rect.x += self.x_change
        self.collide('x')
        self.rect.y += self.y_change
        self.collide('y')
        self.x_change = 0
        self.y_change = 0
        self.collect_items()

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[self.controls['left']]:
            self.x_change -= 5
            self.facing = 'left'
        if keys[self.controls['right']]:
            self.x_change += 5
            self.facing = 'right'
        if keys[self.controls['up']]:
            self.y_change -= 5
            self.facing = 'up'
        if keys[self.controls['down']]:
            self.y_change += 5
            self.facing = 'down'

    def collide(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(55, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(5, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(105, 2, self.width, self.height)]
        
        up_animations = [self.game.character_spritesheet.get_sprite(55, 146, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(5, 146, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(105, 146, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(55, 50, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(5, 50, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(105, 50, self.width, self.height)]
        
        right_animations = [self.game.character_spritesheet.get_sprite(55, 98, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(5, 98, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(105, 98, self.width, self.height)]

        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(55, 2, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(55, 146, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(55, 50, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(55, 98, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
