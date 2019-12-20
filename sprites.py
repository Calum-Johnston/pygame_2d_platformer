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
        self.image.fill(MAGNETA)
        self.image.set_colorkey((255, 255, 255))
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

        # Define initial position, velocity, acceleration for player
        self.pos = (WIDTH / 2, HEIGHT / 2)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)

    def update(self):
        # Default acceleration is 0 (x-direction) and GRAVITY (y-direction)
        self.acceleration = vec(0, PLAYER_GRAVITY)
        
        # Determine whether the player is accelerating
        keysPressed = pygame.key.get_pressed()
        if(keysPressed[pygame.K_RIGHT]): 
            self.acceleration.x = PLAYER_ACC
        if(keysPressed[pygame.K_LEFT]): 
            self.acceleration.x = -PLAYER_ACC

        # Decrease acceleration according friction, update velocity according to acceleration
        self.acceleration.x += self.velocity.x * PLAYER_FRICTION  # Friction only applies to x-range
        self.velocity += self.acceleration

        # Calculate the new position
        self.pos += self.velocity + 0.5 * self.acceleration

        # Player wraps around the screen if out of bounds
        if(self.pos.x > WIDTH):
            self.pos.x = 0
        if(self.pos.x < 0):
            self.pos.x = WIDTH

        # Updates player position
        self.rect.midbottom = self.pos

    def jump():
        pass

class Platform(pygame.sprite.Sprite):

    def __init__(self, plat_X, plat_Y, plat_Width, plat_Height):
        super().__init__()
        # Define the image size, color, etc
        self.image = pygame.Surface([plat_Width, plat_Height])
        self.image.fill(YELLOW)
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.x = plat_X
        self.rect.y = plat_Y