import pygame
import math
import subprocess
from shop import run_shop
import json
import os
from spritesheet import Spritesheet
from character import Character, Bag, Item
from npc import NPC
from blocks import Block, Block2, Block3, Ground
from ui import settings, DialogueBox, Button
from config import * 

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
        
            self.item_spritesheet = Spritesheet('image/items.png')
            self.items = pygame.sprite.Group()
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
                    elif column == "O":
                        Item(self, j, i, 'potion')
                    elif column == "S":
                        Item(self, j, i, 'super_potion')

                    
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
            self.items = pygame.sprite.LayeredUpdates()
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