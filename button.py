import pygame

# Button class
class Button():
    def __init__(self, surface, x, y, image, size_x, size_y):
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface
        self.hovered = False 
        
    def draw(self, hover_effect=False):
        action = False

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            self.hovered = True
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        else:
            self.hovered = False

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw button
        if hover_effect and self.hovered:
            # Optional hover effect (increase brightness or outline)
            hover_image = pygame.transform.scale(self.image, (int(self.rect.width * 1.1), int(self.rect.height * 1.1)))
            hover_rect = hover_image.get_rect(center=self.rect.center)
            self.surface.blit(hover_image, hover_rect.topleft)
        else:
            self.surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
