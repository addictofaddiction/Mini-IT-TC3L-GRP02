import pygame

# Existing configurations
player_layer = 4
item_layer = 3
block_layer = 2
ground_layer = 1

red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

tilesize = 32
tilemap = [
    'llllllllllllllllllllllllllllll',
    'bbbbb....................bbbbb',
    'bbbbN.........G..........Pbbbb',
    'bbbbb....................bbbbb',
    'BW.........................lll',
    '.B.........................lll',
    'B............C.............lll',
    '.B.........................lBl',
    'B..........llll..............l',
    '.B.........nlll............OBl',
    'B..........llll..............l',
    '.B.G.......llll.............Bl',
    'B..........llll............G.l',
    '.B..........................Bl',
    'B............................l',
    '.B.........................pll',
    'B.S......................bbbbb',
    '.B.......................wbbbb',
    'B........................Bbbbb',
    '.Blllllllllllllllllllllll.bbbb',]
FPS = 30

starting_gold = {
    "character_gold":300  
    }

BUTTON_WIDTH = 300
BUTTON_HEIGHT = 50
BUTTON_SPACING = 20
BUTTON_WIDTH_FOR_KEYBIND = 400
left_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH_FOR_KEYBIND // 2, 100), (BUTTON_WIDTH_FOR_KEYBIND, BUTTON_HEIGHT))
right_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH_FOR_KEYBIND // 2, 180), (BUTTON_WIDTH_FOR_KEYBIND, BUTTON_HEIGHT))
up_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH_FOR_KEYBIND // 2, 260), (BUTTON_WIDTH_FOR_KEYBIND, BUTTON_HEIGHT))
down_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH_FOR_KEYBIND // 2, 340), (BUTTON_WIDTH_FOR_KEYBIND, BUTTON_HEIGHT))