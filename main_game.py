import pygame
import math
import sys
import subprocess
from shop import run_shop
import json
import os

pygame.mixer.init()
pygame.mixer.music.load('bg_music.mp3')
pygame.mixer.music.play(-1)

GRAY = (100, 100, 100)
WHITE = (255,255,255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


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
        draw_text(f"Left: {pygame.key.name(controls['left'])}", font, WHITE, 100, 100)
        draw_text(f"Right: {pygame.key.name(controls['right'])}", font, WHITE, 100, 180)
        draw_text(f"Up: {pygame.key.name(controls['up'])}", font, WHITE, 100, 260)
        draw_text(f"Down: {pygame.key.name(controls['down'])}", font, WHITE, 100, 340)

        draw_button(left_button_rect, "Change Left")
        draw_button(right_button_rect, "Change Right")  
        draw_button(up_button_rect, "Change Up")
        draw_button(down_button_rect, "Change Down")

        pygame.display.update()

    # Save the updated controls
    with open('controls.json', 'w') as controls_file:
        json.dump(controls, controls_file)




def start_game():

    player_layer = 4
    item_layer = 3
    block_layer = 2
    ground_layer = 1

    red =(255,0,0)
    black = (0,0,0)
    white = (255,255,255)
    green = (0,255,0)
    GRAY = (100, 100, 100)
    WHITE = (255,255,255)

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    tilesize = 32
    tilemap =  [
        'llllllllllllllllllllllllllllll',
        'bbbbb....................bbbbb',
        'bbbbN.........G..........Pbbbb',
        'bbbbb....................bbbbb',
        'BW.........................lll',
        '.B.........................lll',
        'B............C.............lll',
        '.B.........................lBl',
        'B..........llll..............l',
        '.B.........nlll.............Bl',
        'B..........llll..............l',
        '.B.G.......llll.............Bl',
        'B..........llll............G.l',
        '.B..........................Bl',
        'B............................l',
        '.B.........................pll',
        'B........................bbbbb',
        '.B.......................wbbbb',
        'B........................Bbbbb',
        '.Blllllllllllllllllllllll.bbbb',
    ]
    FPS = 30

    starting_gold = {
        "character_gold":300  
        }

    class Spritesheet:
        def __init__(self,file):
            self.sheet = pygame.image.load(file).convert()
            
        def get_sprite(self,x,y,width,height):
            sprite = pygame.Surface([width,height])
            sprite.blit(self.sheet,(0,0),(x,y,width,height))
            sprite.set_colorkey((0,0,0))

            return sprite
        
    class Item(pygame.sprite.Sprite):
        def __init__(self, game, x, y, item):
            self._layer = item_layer
            self.groups = game.sprites, game.coins
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.game = game
            self.item = item
            self.x = x * tilesize
            self.y = y * tilesize
            self.width = tilesize
            self.height = tilesize

            self.image = self.game.coin_spritesheet.get_sprite(174, 170, self.width * 1.25, self.height)
            
            

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
        def __init__(self,game,x,y):
            self.game = game
            self._layer = player_layer
            self.groups = self.game.sprites
            pygame.sprite.Sprite.__init__(self,self.groups) 
            self.bag = Bag()
            self.gold = 0


            #pull controls folder
            with open('controls.json', 'r') as controls_file:
                self.controls = json.load(controls_file)

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

        def save_position(self):
            position = {'x': self.rect.x, 'y': self.rect.y}
            with open('save_file.json', 'w') as save_character_location:
                json.dump(position, save_character_location)
        #loading chracter location

        def load_position(self):
            try:
                with open('save_file.json', 'r') as f:
                    position = json.load(f)
                    self.x = position['x']
                    self.y = position['y']
            except FileNotFoundError:
                    self.x = 13 * tilesize
                    self.y = 6 * tilesize
                    start_spawn_default={
                        'x':13,
                        'y':6
                    }
                    with open('save_file.json', 'w') as default_location:
                        json.dump(start_spawn_default,default_location)

        def collect_items(self):
            hits = pygame.sprite.spritecollide(self, self.game.coins, True)
            for item in hits:
                self.gold += 100
                self.game.current_gold += 100
                with open('character_gold.json', "w") as character_gold_file:
                    character_gold= character_gold_file + self.game.current_gold
                    json.dump (character_gold, character_gold_file)
                self.game.current_gold= character_gold

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

    

    

    class DialogueBox:
        def __init__(self,game,text,x,y):
            print(f"DialogueBox created with text:{text},x:{x},y:{y}")
            self.game = game
            self.font = pygame.font.Font(None, 36)
            self.box_width = 600
            self.box_height = 100
            self.box_x = x
            self.box_y = y
            self.text = text
            self.active = True
            self.buttons = []
            
            
        def add_button(self, text, action):
            button_x = self.box_x + (len(self.buttons) * 150) + 50
            button_y = self.box_y + self.box_height + 10
            button = Button(self.game,text,button_x,button_y,action)
            self.buttons.append(button)
            print(f"Added button: {text}")



        def draw(self, screen):
            # Draw the dialogue box
            print("Drawing DialogueBox")
            pygame.draw.rect(screen, black, (self.box_x, self.box_y, self.box_width, self.box_height))
            pygame.draw.rect(screen, white, (self.box_x, self.box_y, self.box_width, self.box_height), 2)

            # Render the text
            text_surface = self.font.render(self.text, True, white)
            text_rect = text_surface.get_rect(center=(self.box_x + self.box_width // 2, self.box_y + self.box_height // 2))
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

    
    class NPC(pygame.sprite.Sprite):
        def __init__(self,game,x,y,npc_type,npc_id = None):
            self.game = game
            self._layer = block_layer
            self.groups = self.game.sprites,self.game.blocks
            pygame.sprite.Sprite.__init__(self,self.groups)
            print(f"NPC added to groups:{self.groups}")
            self.x = x * tilesize
            self.y = y * tilesize
            self.width = tilesize
            self.height = tilesize * 1.45
            self.npc_type = npc_type
            self.npc_id = npc_id

            if npc_type == "shop":
                self.image = self.game.npc_sprisheet.get_sprite(295, 292, self.width, self.height)


            elif npc_type == "battle":
                if npc_id == 1:
                    self.image = self.game.npc_sprisheet.get_sprite(55, 52, self.width, self.height)

                elif npc_id == 2:
                    self.image = self.game.npc_sprisheet.get_sprite(197, 48, self.width, self.height)

                elif npc_id == 3:
                    self.image = self.game.npc_sprisheet.get_sprite(54, 240, self.width, self.height)

                elif npc_id == 4:
                    self.image = self.game.npc_sprisheet.get_sprite(342, 51, self.width, self.height)

                elif npc_id == 5:
                    self.image = self.game.npc_sprisheet.get_sprite(485, 98, self.width, self.height)

            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

        def interact(self):
        # Check if the player is near the NPC
            print(f"Interaction triggered for {self.npc_type} NPC")
            self.game.dialogue_active = True
            self.game.box_x = (self.game.screen.get_width() - 600) // 2
            self.game.box_y = self.game.screen.get_height() - 150

            if self.npc_type == "shop":
                print("Creating shop dialogue")
                self.game.dialogue_box = DialogueBox(self.game, "Need anything?", self.game.box_x, self.game.box_y)
                self.game.dialogue_box.add_button("Sure!", self.game.show_shop)
                self.game.dialogue_box.add_button("Maybe later.", self.game.close_dialogue)
            elif self.npc_type == "battle":
                print(f"Creating battle dialogue for NPC {self.npc_id}")
                if self.npc_id == 1:
                    dialogue_text = "You dare challenge me? Prepare yourself!"
                elif self.npc_id == 2:
                    dialogue_text = "Ready for a real challenge?"
                elif self.npc_id == 3:
                    dialogue_text = "You'll regret facing me!"
                elif self.npc_id == 4:
                    dialogue_text = "This is going to be fun!"
                elif self.npc_id == 5:
                    dialogue_text = "Prepare for the ultimate battle!"
                else:
                    dialogue_text = "Are you ready to battle?"

                self.game.dialogue_box = DialogueBox(self.game, dialogue_text, self.game.box_x, self.game.box_y)
                self.game.dialogue_box.add_button("Start Battle", self.start_battle)
                print(f"Added 'Start Battle' button for {self.npc_type} NPC")
            
            return True
        
        def start_battle(self):
            print("Starting battle...")
            self.game.close_dialogue()
            self.game.start_battle(self.npc_id)
            




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

    

    class Game:
        def __init__(self):
            pygame.init()
            self.screen = pygame.display.set_mode((960,640))
            self.clock = pygame.time.Clock()
            self.running = True
            self.playing = False

            self.character_spritesheet = Spritesheet('image/player.png')
            self.npc_sprisheet = Spritesheet('image/npc.png')
            self.terrain_spritesheet = Spritesheet('image/terrain.png')
            self.blocks_spritesheet = Spritesheet('image/block01.png')

            self.dialogue_box = None
            self.dialogue_active = False
            self.character = None
            self.npc = pygame.sprite.Group()
            self.show_shop_flag = False
            
            with open('character_gold.json', "r") as character_gold_file:
                character_gold= character_gold_file
            self.current_gold = character_gold
        
            self.coin_spritesheet = Spritesheet('image/coins.png')
            self.coins = pygame.sprite.Group()
            self.bag_button = pygame.Rect(960 - 60, 10, 80, 30)
            self.show_bag = False
            
        def Tilemap(self):
            for i,row in enumerate(tilemap):
                for j,column in enumerate(row):
                    Ground(self,j,i)

                    if column == "B":
                        Block(self,j,i)
                    if column == "b":
                        Block2(self,j,i)
                    if column == "l":
                        Block3(self,j,i)
                    if column == "C":
                        self.character = Character(self,j,i)
                    if column in ["N", "n", "P", "p", "w", "W"]:
                        print(f"Placing NPC of type {column} at position ({j},{i})")
                    if column == "N":
                        NPC(self,j,i,"shop")
                    if column == "n":
                        NPC(self,j,i,"battle",npc_id = 1)
                    if column == "P":
                        NPC(self,j,i,"battle",npc_id = 2)
                    if column == "p":
                        NPC(self,j,i,"battle",npc_id = 3)
                    if column == "w":
                        NPC(self,j,i,"battle",npc_id = 4)
                    if column == "W":
                        NPC(self,j,i,"battle",npc_id = 5)
                    if column == "G":
                        Item(self, j, i, 'gold')
                    
        def start_battle(self, npc_id):
            print(f"Starting battle with NPC {npc_id}")
            self.playing = False  # Pause the main game loop
            battle_process = subprocess.Popen(['python', 'turn-based-combat.py', str(npc_id)])
            battle_process.wait()
            self.update_after_battle()
            self.playing = True

        def update_after_battle(self):
            print("Updating game state after battle")

        def new(self):
            self.playing = True
            self.sprites = pygame.sprite.LayeredUpdates()
            self.blocks = pygame.sprite.LayeredUpdates()
            self.npc = pygame.sprite.LayeredUpdates()
            self.coins = pygame.sprite.LayeredUpdates()
            self.player = self.character
            self.Tilemap()

            for sprite in self.sprites:
                if isinstance(sprite, NPC):
                    self.npc.add(sprite)

        def check_npc_interaction(self):
            player = self.character
            for npc in self.npc:
                distance = math.sqrt((player.rect.centerx - npc.rect.centerx)**2 + (player.rect.centery - npc.rect.centery)**2)
                if distance < tilesize * 1.5:
                    print(f"Interacting with NPC: {npc.npc_type}")
                    npc.interact()
                
                    break
            else:
                print("No nearby NPCs found for interaction")

        def events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.character.save_position()  # Save position when quitting
                    self.playing = False
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.bag_button.collidepoint(event.pos):
                        self.show_bag = not self.show_bag
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.show_bag:
                            self.show_bag = False
                        else:
                            self.open_settings_menu()

                    

                    elif event.key == pygame.K_SPACE:
                        print("Space key pressed, checking for nearby NPCs")
                        self.check_npc_interaction()
                if self.dialogue_active and self.dialogue_box:
                    print("Handling event for dialogue box")
                    self.dialogue_box.handle_event(event)

        def show_shop(self):
            self.dialogue_active = False
            self.show_shop_flag = True
            result = run_shop(self.character)
            if result is not None:
                self.current_gold = result
                self.character.gold = result
            self.show_shop_flag = False

        
        def close_dialogue(self):
            self.dialogue_active = False
            self.dialogue_box = None


        
        def open_settings_menu(self):
            settings()         

        

        def update(self):
            self.sprites.update()

        def draw(self):
            self.screen.fill(black)
            for sprite in self.sprites:
                self.screen.blit(sprite.image, sprite.rect)

            font = pygame.font.Font(None, 36)
            gold_text = font.render(f"Gold: {self.character.gold}", True, (255, 255, 0))
            self.screen.blit(gold_text, (10, 10))

            pygame.draw.rect(self.screen, (200, 200, 200), self.bag_button)
            bag_font = pygame.font.Font(None, 24)
            bag_text = bag_font.render("Bag", True, (0, 0, 0))
            self.screen.blit(bag_text, (self.bag_button.x + 5, self.bag_button.y + 5))

            if self.show_bag:
                self.draw_bag()

            if self.dialogue_active and self.dialogue_box:
                print("Drawing dialogue box: {self.dialogue_box.text}")
                self.dialogue_box.draw(self.screen)
        
            self.clock.tick(FPS)
            pygame.display.update()

        def draw_bag(self):
            bag_surface = pygame.Surface((300, 400))
            bag_surface.fill((200, 200, 200))
            font = pygame.font.Font(None, 24)
            for i, item in enumerate(self.character.bag.items):
                text = font.render(item, True, black)
                bag_surface.blit(text, (10, 10 + i * 30))
            self.screen.blit(bag_surface, (960 // 2 - 150, 640 // 2 - 200))


        def main(self):
            self.playing = True
            while self.playing:
                print("Main game loop iteration")
                print(f"Dialogue active:{self.dialogue_active}")
                print(f"Dialogue box exists: {self.dialogue_box is not None}")
                self.events()
                self.update()
                self.draw()
                if not self.playing:  
                    break
            if self.show_shop_flag:
                self.run_shop()

    
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
    starting_gold = {
    "character_gold":300  
    }
    
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
