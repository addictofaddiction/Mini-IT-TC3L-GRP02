import pygame
import math
from config import block_layer, tilesize
from ui import DialogueBox, Button
import subprocess



class NPC(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = block_layer
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
    
class NPC2(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = block_layer
        self.groups = self.game.sprites,self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.npc_sprisheet.get_sprite(55,52,self.width,self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def interact(self):
        # Check if the player is near the NPC2
        player = self.game.character
        distance = math.sqrt((player.rect.centerx - self.rect.centerx)**2 + (player.rect.centery - self.rect.centery)**2)
        if distance < tilesize * 1.5:
            # Display the dialogue box
            self.game.dialogue_active = True
            self.game.box_x = (self.game.screen.get_width() - 600) // 2
            self.game.box_y = self.game.screen.get_height() - 150
            self.game.dialogue_box = DialogueBox(self.game, "You dare challenge me? Prepare yourself!", self.game.box_x, self.game.box_y)
            self.game.dialogue_box.add_button("Start Battle", self.start_battle)
            self.game.dialogue_box.add_button("Cancel", self.game.close_dialogue)
            return True
        return False

    def start_battle(self):
        # Call the turn-based combat code
        subprocess.call(['python', 'turn-based-combat.py'])
        self.game.close_dialogue()

class NPC2(pygame.sprite.Sprite):
        def __init__(self,game,x,y):
            self.game = game
            self._layer = block_layer
            self.groups = self.game.sprites,self.game.blocks
            pygame.sprite.Sprite.__init__(self,self.groups)
            self.x = x * tilesize
            self.y = y * tilesize
            self.width = tilesize
            self.height = tilesize

            self.image = self.game.npc_sprisheet.get_sprite(55,52,self.width,self.height)
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y


        def interact(self):
            # Check if the player is near the NPC2
            player = self.game.character
            distance = math.sqrt((player.rect.centerx - self.rect.centerx)**2 + (player.rect.centery - self.rect.centery)**2)
            if distance < tilesize * 1.5:
                # Display the dialogue box
                self.game.dialogue_active = True
                self.game.box_x = (self.game.screen.get_width() - 600) // 2
                self.game.box_y = self.game.screen.get_height() - 150
                self.game.dialogue_box = DialogueBox(self.game, "You dare challenge me? Prepare yourself!", self.game.box_x, self.game.box_y)
                self.game.dialogue_box.add_button("Start Battle", self.start_battle)
                self.game.dialogue_box.add_button("Cancel", self.game.close_dialogue)
                return True
            return False

        def start_battle(self):
            # Call the turn-based combat code
            subprocess.call(['python', 'turn-based-combat.py'])
            self.game.close_dialogue()