import pygame
from config import block_layer, ground_layer, tilesize


#tree
class Block(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        super().__init__()
        self.game = game
        self._layer = block_layer
        self.groups = self.game.sprites,self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        
        self.image = self.game.blocks_spritesheet.get_sprite(-2,60,self.width,self.height*2)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

#flower 
class Block2(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        super().__init__()
        self.game = game
        self._layer = block_layer
        self.groups = self.game.sprites,self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        
        self.image = self.game.blocks_spritesheet.get_sprite(366,450,self.width,self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

#bush      
class Block3(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        super().__init__()
        self.game = game
        self._layer = block_layer
        self.groups = self.game.sprites,self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        
        self.image = self.game.blocks_spritesheet.get_sprite(240,0,self.width,self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = ground_layer
        self.groups = self.game.sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.terrain_spritesheet.get_sprite(300,300,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
