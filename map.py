import pygame
import sys

player_layer = 3
ground_layer = 1
black = (0,0,0)
tilesize = 44
tilemap = [
    '...............',
    '...............',
    '...............',
    '...............',
    '...............',
    '...............',
    '.............C.',
    '...............',
    '...............',
    '...............',
    '...............',
    '...............',
    '...............',
    '...............',
    '...............',
]
FPS = 30

class Spritesheet:
    def __init__(self,file):
        self.sheet = pygame.image.load(file).convert()
    def get_sprite(self,x,y,width,height):
        sprite = pygame.Surface([width,height])
        sprite.blit(self.sheet,(0,0),(x,y,width,height))
        sprite.set_colorkey(black)
        return sprite
        
class Character(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = player_layer
        self.groups = self.game.sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize
        self.x_change = 0
        self.y_change = 0


        self.image = self.game.character_spritesheet.get_sprite(55,2,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def update(self):
        self.movement()
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= 5
        if keys[pygame.K_RIGHT]:
            self.x_change += 5
        if keys[pygame.K_UP]:
            self.y_change -= 5
        if keys[pygame.K_DOWN]:
            self.y_change += 5



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

        self.image = self.game.terrain_spritesheet.get_sprite(400,280,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

   

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((660,660))
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_spritesheet = Spritesheet('image/player.png')
        self.terrain_spritesheet = Spritesheet('image/terrain.png')
       
        
    def Tilemap(self):
        for i,row in enumerate(tilemap):
            for j,column in enumerate(row):
                Ground(self,j,i)
                if column == "C":
                    Character(self,j,i)
                    

    def new(self):
        self.playing = True
        self.sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.Tilemap()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.sprites.update()



    def draw(self):
        self.screen.fill(black)
        self.sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()



    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

g = Game()
g.new()
while g.running:
    g.main()


pygame.quit()
sys.exit()