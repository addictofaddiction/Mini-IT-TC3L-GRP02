import pygame
import config
from ui import DialogueBox, Button

class NPC(pygame.sprite.Sprite):
    def __init__(self, game, x, y, npc_type, npc_id=None):
        self.game = game
        self._layer = config.block_layer
        self.groups = self.game.sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        print(f"NPC added to groups: {self.groups}")
        self.x = x * config.tilesize
        self.y = y * config.tilesize
        self.width = config.tilesize
        self.height = config.tilesize * 1.45
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