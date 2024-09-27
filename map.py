import pygame
import math
import sys
import shop
import json
import os

starting_gold = {
    "character_gold":300  
    }

default_controls = {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'up': pygame.K_UP,
    'down': pygame.K_DOWN
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
button_width_for_keybind = 400
# Button positions
continue_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - button_height - button_spacing), (button_width, button_height))
start_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2), (button_width, button_height))
quit_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + button_height + button_spacing), (button_width, button_height))
left_button_rect = pygame.Rect(400, 100, button_width_for_keybind, button_height)
right_button_rect = pygame.Rect(400, 180, button_width_for_keybind, button_height)
up_button_rect = pygame.Rect(400, 260, button_width_for_keybind, button_height)
down_button_rect = pygame.Rect(400, 340, button_width_for_keybind, button_height)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_button(rect, text):
    pygame.draw.rect(screen, GRAY, rect)
    draw_text(text, font, WHITE, rect.x + 20, rect.y + 5)

#for keybinds
def settings():
    if os.path.isfile('controls.json'):
        with open('controls.json', 'r') as controls_file:
            controls = json.load(controls_file)

    changing_key = None  
    font = pygame.font.Font(None, 36)

    run_settings = True
    while run_settings:
        screen.fill((0, 0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_settings = False  # Return to the game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Return to game if ESC is pressed
                    run_settings = False
                elif changing_key:
                    # Assign the new key to the selected action
                    controls[changing_key] = event.key
                    changing_key = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if left_button_rect.collidepoint(event.pos):
                    changing_key = 'left'
                elif right_button_rect.collidepoint(event.pos):
                    changing_key = 'right'
                elif up_button_rect.collidepoint(event.pos):
                    changing_key = 'up'
                elif down_button_rect.collidepoint(event.pos):
                    changing_key = 'down'

        # Display current key bindings
         # Display current key bindings
        draw_text(f"Left: {pygame.key.name(controls['left'])}", font, WHITE, 100, 100)
        draw_text(f"Right: {pygame.key.name(controls['right'])}", font, WHITE, 100, 180)
        draw_text(f"Up: {pygame.key.name(controls['up'])}", font, WHITE, 100, 260)
        draw_text(f"Down: {pygame.key.name(controls['down'])}", font, WHITE, 100, 340)

        # Check if the mouse is hovering over buttons and change their color
        draw_button(left_button_rect, "Change Left", left_button_rect.collidepoint(mouse_pos))
        draw_button(right_button_rect, "Change Right", right_button_rect.collidepoint(mouse_pos))
        draw_button(up_button_rect, "Change Up", up_button_rect.collidepoint(mouse_pos))
        draw_button(down_button_rect, "Change Down", down_button_rect.collidepoint(mouse_pos))
        pygame.display.update()

    # Save the updated controls
    with open('controls.json', 'w') as controls_file:
        json.dump(controls, controls_file)


pygame.mixer.init()
pygame.mixer.music.load('bg_music.mp3')
pygame.mixer.music.play(-1)

font = pygame.font.Font(None, 36)
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
    'bbbbb....................bbbbb',
    'bbbbb....................Nbbbb',
    'bbbbb.....................bbbb',
    'B..........................lll',
    '.B.........................lll',
    'B............C.............lll',
    '.B.........................lBl',
    'B..........n.................l',
    '.B..........lll.............Bl',
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
        super().__init__()
        self.game = game
        self._layer = player_layer
        self.groups = self.game.sprites

        pygame.sprite.Sprite.__init__(self,self.groups) 
        #pull controls folder
        with open('controls.json', 'r') as controls_file:
            self.controls = json.load(controls_file)

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
            self.check_interaction()
        
        #key binds
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

        def check_interaction(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                for npc in self.game.npcs:
                    if self.rect.colliderect(npc.rect):
                        self.game.dialogue_active = True
                        self.game.dialogue_box.set_text("What would you like to purchase today?")
                        self.game.dialogue_box.set_option(["Show me your wares","Nothing"])

        

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

            self.image = self.game.npc_sprisheet.get_sprite(390,244,self.width,self.height)
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class DialogueBox:
        def __init__(self):
            self.box = pygame.Surface((960, 150))
            self.box.fill(white)
            self.box_rect = self.box.get_rect(bottomleft=(0, 500))
            self.text = ""
            self.current_text = ""
            self.text_index = 0
            self.options = []
            self.selected_option = None

        def set_text(self, text):
            self.text = text

        def set_options(self, options):
            self.options = options

        def draw(self, screen):
            screen.blit(self.box, self.box_rect)
            text_surface = font.render(self.current_text, True, black)
            screen.blit(text_surface, (10, 640 - 140))

            
            for i, option in enumerate(self.options):
                option_surface = font.render(option, True, black)
                option_rect = option_surface.get_rect(topleft=(10, 640 - 100 + i * 30))
                screen.blit(option_surface, option_rect)
                if option_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, (200, 200, 200), option_rect, 2)

        def handle_input(self, pos):
            for i,option in enumerate(self.options):
                option_surface = font.render(option,True,black)
                option_rect = option_surface.get_rect(topleft = (10,640-100 + i *30))
                if option_rect.collidepoint(pos):
                    self.selected_option = option


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
            self.sprites = pygame.sprite.LayeredUpdates()
            self.blocks = pygame.sprite.LayeredUpdates()
            self.npcs = pygame.sprite.LayeredUpdates()

            self.dialogue_box = DialogueBox()
            self.dialogue_active = False


        
            
        def Tilemap(self):
            for i,row in enumerate(tilemap):
                for j,column in enumerate(row):
                    Ground(self,j,i)

                    if column == "B":
                        Block(self,j,i)
                    if column == "C":
                        self.character = Character(self,j,i)
                    if column == "N":
                        NPC(self,j,i)
                    if column == "n":
                        NPC2(self,j,i)
                    if column == "b":
                        Block2(self,j,i)
                    if column == "l":
                        Block3(self,j,i)

        def new(self):
            self.playing = True
            self.Tilemap()

        def events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.character.save_position()  # Save position when quitting
                    self.playing = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.open_settings_menu()

                if self.dialogue_active == True:
                    self.dialogue_box.handle_input(event)
                    if self.dialogue_box.selected_option == "Show me your wares":
                        print("Navigating to shop.py")
                        shop.run()
                    elif self.dialogue_box.selected_option == "Nothing":
                        self.dialogue_active = False
                        self.dialogue_box.selected_option = None

        def open_settings_menu(self):
            settings()         

        def update(self):
            self.sprites.update()
            if self.dialogue_active == True:
                self.dialogue_box.update()

        def draw(self):
            self.screen.fill(black)
            self.sprites.draw(self.screen)
            if self.dialogue_active:
                self.dialogue_box.draw(self.screen)
            pygame.display.flip()



        def main(self):
            while self.playing:
                self.events()
                self.update()
                self.draw()
                self.clock.tick(FPS)


    g = Game()
    g.new()
    while g.running:
        g.main()


    pygame.quit()
    sys.exit()

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
                with open('character_gold.json', "w") as character_gold_file:
                    json.dump(starting_gold, character_gold_file)
                with open('controls.json', 'w') as controls_file:
                    json.dump(default_controls, controls_file)
                start_game()
                run = False
            if search_file_existance and continue_button_rect.collidepoint(event.pos):  
                start_game()
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
