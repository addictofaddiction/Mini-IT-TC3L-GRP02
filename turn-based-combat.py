import pygame
import random
import sys
import button

pygame.init()

clock = pygame.time.Clock()
fps = 60


#game window
bottom_panel =150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')

#define game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 60
attack = False
potion = False
potion_effect = 15
clicked  = False # will look for a mouse click


#define fonts
font = pygame.font.SysFont('Times New Roman', 26)

#define colours
red = (255, 0, 0)
green = (0, 255, 0)


#load imagaes
#background image
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
#panel image
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()
#button images
potion_img = pygame.image.load('img/Icons/potion.png').convert_alpha()
#sword imagae
sword_img = pygame.image.load('img/Icons/sword.png').convert_alpha()

#create function for drawing text
def draw_text(text, front, text_col, x, y):
    img = front.render(text, True, text_col)
    screen.blit(img, (x, y))


#function for drawing background
def draw_bg():
    screen.blit(background_img, (0, 0))


#function for drawing panel
def draw_panel():
    #drawn panel rectangle
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    #show player's creature's  stats
    draw_text(f'{player_creature.name} HP: {player_creature.hp}', font, red, 100, screen_height - bottom_panel +10)
    for count, i in enumerate(bandit_list):
        #show name and health
         draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - bottom_panel +10) + count * 60)


def win_lose_text(result):
    if result == 'win':
        draw_text('You Win!', font, green, screen_width // 2 - 100, screen_height // 2)
    elif result == 'lose':
        draw_text('You Lose!', font, red, screen_width // 2 - 100, screen_height // 2)


#fighter
class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        img = pygame.image.load(f'img/{self.name}/idle/0.png')
        self.image = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def attack(self, target):
        #deal damage to enemy
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        #check if target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)




    def draw(self):
        screen.blit(self.image, self.rect)

def win_lose_text(result):
    if result == 'win':
        draw_text('You Win!', font, green, screen_width // 2 - 100, screen_height // 2)
    elif result == 'lose':
        draw_text('You Lose!', font, red, screen_width // 2 - 100, screen_height // 2)


class HealthBar():
    def __init__(self, x ,y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
    
    
    def draw(self, hp):
        #update with new health
        self.hp = hp
        #calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))
                


class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0


    def update(self):
        #move damage text up
        self.rect.y -= 1
        #delete the text after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()





damage_text_group = pygame.sprite.Group()

player_creature = Fighter(200, 260, 'player_creature', 30, 10, 3)
bandit1 = Fighter(550, 270, 'Bandit', 20, 6, 1)
bandit2 = Fighter(700, 270, 'Bandit', 20, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

player_creature_health_bar = HealthBar(100, screen_height - bottom_panel + 40, player_creature.hp, player_creature.max_hp)
bandit1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, bandit2.hp, bandit2.max_hp)

#create buttons
potion_button = button.Button(screen,100, screen_height - bottom_panel + 70, potion_img, 64, 64)


run = True
game_over = False
result = None

run = True
game_over = False
result = None

while run:
    clock.tick(fps)

    #draw background
    draw_bg()

    #draw panel
    draw_panel()
    player_creature_health_bar.draw(player_creature.hp)
    bandit1_health_bar.draw(bandit1.hp)
    bandit2_health_bar.draw(bandit2.hp)

    #check if game over
    if game_over == False:
        #draw fighters
        player_creature.draw()
        for bandit in bandit_list:
            if bandit.alive:  # Hide bandit if not alive
                bandit.draw()

        #draw the damage text
        damage_text_group.update()
        damage_text_group.draw(screen)

        #control player actions
        #reset action variables
        attack = False
        potion = False
        target = None
        #this one here to make sure the mouse is visible
        pygame.mouse.set_visible(True)
        pos = pygame.mouse.get_pos()
        for count, bandit in enumerate(bandit_list):
            if bandit.rect.collidepoint(pos) and bandit.alive:  # Only allow attacking alive enemies
                pygame.mouse.set_visible(False)
                screen.blit(sword_img, pos)
                if clicked == True:
                    attack = True
                    target = bandit_list[count]

        if potion_button.draw():
            potion = True
        # show number of potions remaining
        draw_text(str(player_creature.potions), font, red, 150, screen_height - bottom_panel + 70)

        #player action
        if player_creature.alive == True:
            if current_fighter == 1:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    #look for player action
                    if attack == True and target != None:
                        player_creature.attack(target)
                        current_fighter += 1
                        action_cooldown = 0

                    if potion == True and player_creature.potions > 0:
                        heal_amount = min(potion_effect, player_creature.max_hp - player_creature.hp)
                        player_creature.hp += heal_amount
                        player_creature.hp = min(player_creature.hp, player_creature.max_hp)
                        player_creature.potions -= 1
                        damage_text = DamageText(player_creature.rect.centerx, player_creature.rect.y, str(heal_amount), green)
                        damage_text_group.add(damage_text)
                        current_fighter += 1
                        action_cooldown = 0

        #enemy action
        for count, bandit in enumerate(bandit_list):
            if current_fighter == 2 + count:
                if bandit.alive == True:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        #check if bandit needs to heal first
                        if (bandit.hp / bandit.max_hp) < 0.5 and bandit.potions > 0:
                            heal_amount = min(potion_effect, bandit.max_hp - bandit.hp)
                            bandit.hp += heal_amount
                            bandit.hp = min(bandit.hp, bandit.max_hp)
                            bandit.potions -= 1
                            damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
                        else:                   
                            #attack
                            bandit.attack(player_creature)
                            current_fighter += 1
                            action_cooldown = 0
                else:
                    current_fighter += 1

        #if all fighters have had a turn then reset
        if current_fighter > total_fighters:
            current_fighter = 1

        #check if all enemies are defeated
        if all(bandit.alive == False for bandit in bandit_list):
            game_over = True
            result = 'win'

        #check if player is defeated
        if player_creature.alive == False:
            game_over = True
            result = 'lose'
    else:
        # Draw win/lose message
        win_lose_text(result)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()

pygame.quit()
sys.exit()



  