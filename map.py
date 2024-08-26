import pygame
import sys
import json
import os

starting_gold = {
    "character_gold":300  
    }



pygame.init()

# Create game main menu window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

font = pygame.font.Font(None, 74)

button_width = 300
button_height = 50
button_spacing = 20

# Button positions
continue_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - button_height - button_spacing), (button_width, button_height))
start_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2), (button_width, button_height))
quit_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + button_height + button_spacing), (button_width, button_height))

player_layer = 3
block_layer = 2
ground_layer = 1
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
tilesize = 44
tilemap = [
        '...........BBB.',
        '........BB.....',
        'BB..N..........',
        '..BBB..........',
        '...............',
        '...............',
        '.............C.',
        '...............',
        '...............',
        '..........BB...',
        '........BBB....',
        '...............',
        '...............',
        '...........BBB.',
        '........BBBB...',
    ]
FPS = 30

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_button(rect, text):
    pygame.draw.rect(screen, GRAY, rect)
    draw_text(text, font, WHITE, rect.x + 20, rect.y + 5)



class Spritesheet:
    def __init__(self,file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(black)
        return sprite
            
class Character(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = player_layer
        self.groups = self.game.sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize
        self.x_change = 0
        self.y_change = 0

        self.image = self.game.character_spritesheet.get_sprite(55, 2, self.width, self.height)

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


class NPC(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = player_layer
        self.groups = self.game.sprites,self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.npc_sprisheet.get_sprite(290,290,self.width,self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Block(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = block_layer
        self.groups = self.game.sprites,self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        

        self.image = self.game.terrain_spritesheet.get_sprite(400, 280, self.width, self.height)


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ground_layer
        self.groups = self.game.sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.terrain_spritesheet.get_sprite(400, 280, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((660, 660))
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_spritesheet = Spritesheet('image/player.png')
        self.npc_spritesheet = Spritesheet('image/npc.png')
        self.terrain_spritesheet = Spritesheet('image/terrain.png')

    def Tilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)

                if column == "B":
                    Block(self,j,i)
                if column == "C":
                    Character(self, j, i)
                if column == "N":
                    NPC(self, j, i)

                    

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

# Main menu loop
run = True
while run:
    screen.fill((0, 0, 0))
    
    search_file_existance = os.path.isfile("character_gold.json") 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(event.pos):
<<<<<<< Updated upstream
                with open('character_gold.json', "w") as character_gold_file:
                    json.dump(starting_gold, character_gold_file)
                game_start()  
=======
                g.start()  
>>>>>>> Stashed changes
                run = False
            if search_file_existance and continue_button_rect.collidepoint(event.pos):  
                game_start()  
                run = False
            if quit_button_rect.collidepoint(event.pos):
                run = False
    # Draw buttons
    if search_file_existance: 
        draw_button(continue_button_rect, "Continue") 
    draw_button(start_button_rect, "Start")
    draw_button(quit_button_rect, "Quit")

    pygame.display.update()

pygame.quit()
sys.exit()