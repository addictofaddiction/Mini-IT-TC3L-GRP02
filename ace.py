import pygame
import math
import sys
import subprocess

pygame.mixer.init()
pygame.mixer.music.load('bg_music.mp3')
pygame.mixer.music.play(-1)

player_layer = 3
block_layer = 2
ground_layer = 1
red =(255,0,0)
black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
tilesize = 32
tilemap = [
    'llllllllllllllllllllllllllllll',
    'bbbb.....................bbbbb',
    'bbbbN....................bbbbb',
    'bbbbb....................bbbbb',
    'B..........................lll',
    '.B.........................lll',
    'B............C.............lll',
    '.B.........................lBl',
    'B............................l',
    '.B.........nlll.............Bl',
    'B..........llll..............l',
    '.B.........llll.............Bl',
    'B..........llll..............l',
    '.B..........................Bl',
    'B............................l',
    '.B..........................ll',
    'B........................bbbbb',
    '.B........................bbbb',
    'B.........................bbbb',
    '.B...................bbbbbbbbb',
    
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
        self.height = tilesize * 1.45
        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1


        self.image = self.game.character_spritesheet.get_sprite(55,2,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def update(self):
        self.movement()
        self.animate()
        self.rect.x += self.x_change
        self.collide('x')
        self.rect.y += self.y_change
        self.collide('y')
        self.x_change = 0
        self.y_change = 0
    

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= 5
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.x_change += 5
            self.facing = 'right'
        if keys[pygame.K_UP]:
            self.y_change -= 5
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_change += 5
            self.facing = 'down'

    def collide(self,direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self,self.game.blocks,False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            hits = pygame.sprite.spritecollide(self,self.game.blocks,False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom


    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(55,2,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(5,2,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(105,2,self.width,self.height)]
        
        up_animations = [self.game.character_spritesheet.get_sprite(55,146,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(5,146,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(105,146,self.width,self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(55,50,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(5,50,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(105,50,self.width,self.height)]
        
        right_animations = [self.game.character_spritesheet.get_sprite(55,98,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(5,98,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(105,98,self.width,self.height)]

        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(55,2,self.width,self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop =1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(55,146,self.width,self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop =1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(55,50,self.width,self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop =1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(55,98,self.width,self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop =1

        
               





    
                           

                    

    


class NPC(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = player_layer
        self.groups = self.game.sprites,self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize * 1.45

        self.image = self.game.npc_sprisheet.get_sprite(295,292,self.width,self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def interact(self):
        # Check if the player is near the NPC
        player = self.game.character
        distance = math.sqrt((player.rect.centerx - self.rect.centerx)**2 + (player.rect.centery - self.rect.centery)**2)
        print(f"distance to NPC:{distance}")
        if distance < tilesize * 1.5:
            print("NPC interaction detected!")  # Debugging
            return True
        return False

class DialogueBox:
    def __init__(self,game,text,x,y):
        self.game = game
        self.font = pygame.font.Font(None, 36)
        self.box_width = 600
        self.box_height = 100
        self.box_x = x
        self.box_y = y
        self.text = text
        self.active = True
        self.buttons = []
        print(f"DialogueBox created with text:{text}")

    def add_button(self, text, action):
        button_x = self.box_x + (len(self.buttons) * 150) + 50
        button_y = self.box_y - 50
        button = Button(self.game,text,button_x,button_y,action)
        self.buttons.append(button)



    def draw(self, screen):
        # Draw the dialogue box
        print("Drawing DialogueBox")
        pygame.draw.rect(screen, black, (self.box_x, self.box_y, self.box_width, self.box_height))
        pygame.draw.rect(screen, white, (self.box_x, self.box_y, self.box_width, self.box_height), 2)

        # Render the text
        text_surface = self.font.render(self.text, True, white)
        text_rect = text_surface.get_rect(center=(960 // 2, self.box_y + self.box_height // 2))
        screen.blit(text_surface, text_rect)

        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

        
class Button:
    def __init__(self, game, text, x, y, action):
        self.game = game
        self.text = text
        self.x = x
        self.y = y
        self.width = 140
        self.height = 40
        self.action = action
        self.font = pygame.font.Font(None, 32)

    def draw(self,screen):
        pygame.draw.rect(self.game.screen, white, (self.x, self.y, self.width, self.height))
        text_surface = self.font.render(self.text, True, black)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x <= event.pos[0] <= self.x + self.width and self.y <= event.pos[1] <= self.y + self.height:
                self.action()


class NPC2(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = player_layer
        self.groups = self.game.sprites,self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize * 1.45

        self.image = self.game.npc_sprisheet.get_sprite(55,52,self.width,self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


#tree
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

        
        self.image = self.game.blocks_spritesheet.get_sprite(-2,60,self.width,self.height*2)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

#flower 
class Block2(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
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

   

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((960,640))
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_spritesheet = Spritesheet('image/player.png')
        self.npc_sprisheet = Spritesheet('image/npc.png')
        self.terrain_spritesheet = Spritesheet('image/terrain.png')
        self.blocks_spritesheet = Spritesheet('image/block01.png')

        self.dialogue_box = None
        self.dialogue_active = False
        self.character = None
        self.npc = pygame.sprite.Group()
       
        
    def Tilemap(self):
        for i,row in enumerate(tilemap):
            for j,column in enumerate(row):
                Ground(self,j,i)

                if column == "B":
                    Block(self,j,i)
                if column == "C":
                    self.character = Character(self,j,i)
                if column == "N":
                    npc = NPC(self,j,i)
                    self.npc.add(npc)
                if column == "n":
                    NPC2(self,j,i)
                if column == "b":
                    Block2(self,j,i)
                if column == "l":
                    Block3(self,j,i)

                
                    

    def new(self):
        self.playing = True
        self.sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.npc = pygame.sprite.LayeredUpdates()
        self.Tilemap()


    def show_shop(self):
        self.dialogue_active = False
        subprocess.run(["python", "shop.py"])

    def close_dialogue(self):
        self.dialogue_active = False
        self.dialogue_box = None


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.dialogue_active:
                    print("Space key pressed")
                    print(f"Number of NPCs:{len(self.npc)}")
                    for npc in self.npc:
                        if npc.interact():
                            print("Creating dialogue box")
                            self.dialogue_active = True
                            self.box_x = (self.screen.get_width() - 600) // 2
                            self.box_y = self.screen.get_height() - 150
                            self.dialogue_box = DialogueBox(self, "Need anything?",self.box_x,self.box_y)
                            self.dialogue_box.add_button("Sure!", self.show_shop)
                            self.dialogue_box.add_button("Maybe later.", self.close_dialogue)
                            break

            if self.dialogue_active and self.dialogue_box:
                self.dialogue_box.handle_event(event)


 

    def update(self):
        self.sprites.update()
        





    def draw(self):
        self.screen.fill(black)
        self.sprites.draw(self.screen)
        if self.dialogue_active and self.dialogue_box:
            print("Dialogue is active, drawing dialogue box")
            self.dialogue_box.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()



    def main(self):
        while self.playing:
            print("Main game loop iteration")
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