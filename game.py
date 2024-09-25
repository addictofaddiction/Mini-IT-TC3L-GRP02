import pygame
import subprocess
from character import Character, Camera
from npc import *
from blocks import Block, Block2, Block3, Ground
from config import FPS, tilemap, black
from main import settings
from ui import DialogueBox
from spritesheet import Spritesheet
from shop import run_shop


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
        self.current_gold = 0
        self.camera = Camera((960,640))
    
        
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
        self.sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.npc = pygame.sprite.LayeredUpdates()
        self.Tilemap()

    def show_shop(self):
        self.dialogue_active = False
        self.show_shop_flag = True
        result = run_shop()
        if result is not None:
            self.current_gold = result
        self.show_shop_flag = False

    def run_shop(current_gold):
        print("Running shop")
        result = run_shop(current_gold)
        return result
    
    def close_dialogue(self):
        self.dialogue_active = False
        self.dialogue_box = None

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.character.save_position()  # Save position when quitting
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.open_settings_menu()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.dialogue_active:
                    for npc in self.npc:
                        if isinstance(npc,NPC2) and npc.interact():
                            print("Creating dialogue box")
                            self.dialogue_active = True
                            self.box_x = (self.screen.get_width() - 600) // 2
                            self.box_y = self.screen.get_height() - 150
                            self.dialogue_box = DialogueBox(self, "Need anything?",self.box_x,self.box_y)
                            self.dialogue_box.add_button("Sure!", self.show_shop)
                            self.dialogue_box.add_button("Maybe later.", self.close_dialogue)
                            break
                elif event.key == pygame.K_ESCAPE:
                    if self.dialogue_active:
                        self.close_dialogue()
                    else:
                        self.playing = False
                        self.running = False
            if self.dialogue_active and self.dialogue_box:
                self.dialogue_box.handle_event(event)

    def open_settings_menu(self):
        settings()         

    def check_collisions(self):
        for block in self.blocks:
            if self.player.rect.colliderect(block.rect):
                # Adjust player position
                if self.player.velocity.x > 0:
                    self.player.rect.right = block.rect.left
                elif self.player.velocity.x < 0:
                    self.player.rect.left = block.rect.right
                if self.player.velocity.y > 0:
                    self.player.rect.bottom = block.rect.top
                elif self.player.velocity.y < 0:
                    self.player.rect.top = block.rect.bottom

    def update(self):
        self.sprites.update()
        self.camera.update(self.player)

    def draw(self):
        self.screen.fill(black)
        self.sprites.draw(self.screen)
        if self.dialogue_active and self.dialogue_box:
            print("Dialogue is active, drawing dialogue box")
            self.dialogue_box.draw(self.screen)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.clock.tick(FPS)
        pygame.display.update()



    def main(self):
        self.playing = True
        while self.playing:
            print("Main game loop iteration")
            self.events()
            self.update()
            self.draw()
        if self.show_shop_flag:
            self.run_shop()