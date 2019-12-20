import pygame

# Sprite class for the player

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([50, 50])
        self.image.fill((0, 255, 128))
        self.image.set_colorkey((255, 255, 255))
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.center = (25, 275)