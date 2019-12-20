import pygame
from settings import *
vec = pygame.math.Vector2

# Sprite class for the player

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Define the image size, color, etc
        self.image = pygame.Surface([20, 25])
        self.image.fill(BLUE)
        self.image.set_colorkey((255, 255, 255))
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.center = (25, 275)

        # Define initial position, velocity, acceleration for player
        self.pos = (25, 275)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)


    def update(self):
        self.acceleration = vec(0, PLAYER_GRAVITY)
        
        keysPressed = pygame.key.get_pressed()
        if(keysPressed[pygame.K_RIGHT]): 
            self.acceleration.x = PLAYER_ACC
        if(keysPressed[pygame.K_LEFT]): 
            self.acceleration.x = -PLAYER_ACC

        # Apply equations of motion to incorporate acceleration
        self.acceleration.x += self.velocity.x * PLAYER_FRICTION  # Only apply friction to x direction
        self.velocity += self.acceleration
        self.pos += self.velocity + 0.5 * self.acceleration
        if(self.pos.x > WIDTH):
            self.pos.x = 0
        if(self.pos.x < 0):
            self.pos.x = WIDTH
        self.rect.center = self.pos

class Platform(pygame.sprite.Sprite):

    def __init__(self, plat_X, plat_Y, plat_Width, plat_Height):
        super().__init__()
        # Define the image size, color, etc
        self.image = pygame.Surface([plat_Width, plaat_])
        self.image.fill(YELLO)
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.x = plat_X
        self.rect.y = plat_Y