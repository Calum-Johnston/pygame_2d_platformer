import pygame
from settings import *
import random as rd
vec = pygame.math.Vector2

''' PLAYER SPRITE '''
class Player(pygame.sprite.Sprite):
    
    def __init__(self, player_X, player_Y, player_Width, player_Height, game):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Get the game instance (for collision use)
        self.game = game
        
        # Define the image size, color, etc
        self.image = self.game.player_spritesheet.getImageAt(768, 768, 128, 256)
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.midbottom = (player_X, player_Y)

        # Define initial position, velocity, acceleration for player
        self.position = vec(self.rect.midbottom)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)

        # Define variables to determine the action the player is currently taking
        self.idle = True
        self.walking = False
        self.jumping = False

    def update(self):
        # Default acceleration is 0 (x-direction) and GRAVITY (y-direction)
        self.acceleration = vec(0, PLAYER_GRAVITY)  # i.e. always accelerting downwards unless changed later
        
        # Determine whether the player is accelerating
        keysPressed = pygame.key.get_pressed()
        if(keysPressed[pygame.K_RIGHT] or keysPressed[pygame.K_d]): 
            self.acceleration.x = PLAYER_ACCELERATION
        if(keysPressed[pygame.K_LEFT] or keysPressed[pygame.K_a]): 
            self.acceleration.x = -PLAYER_ACCELERATION
        if(keysPressed[pygame.K_SPACE]):
            self.jump()

        # Decrease acceleration according friction, update velocity according to acceleration
        self.acceleration.x += self.velocity.x * PLAYER_FRICTION  # Friction only applies to x-range
        self.velocity += self.acceleration

        # Calculate the new position (could remove acceleration part)
        self.position += self.velocity + 0.5 * self.acceleration

        # Player wraps around the screen if out of bounds
        if(self.position.x > WIDTH):
            self.position.x = 0
        if(self.position.x < 0):
            self.position.x = WIDTH

        #Check for collison (only if moving downward)
        if(self.velocity.y > 0):  # y's default velocity will be 0.5 after applying gravity
            collision = pygame.sprite.spritecollide(self, self.game.platform_sprites, False)
            if(collision):
                self.platform = collision[0]
                for pt in collision:
                    if(pt.rect.bottom > self.platform.rect.bottom):
                        self.platform = pt
                if(self.platform.rect.bottom > self.rect.bottom): 
                    self.position.y = self.platform.rect.top + 1
                    self.velocity.y = 0

        # Updates player position (keep track of bottom, since this is used in collisons)
        self.rect.midbottom = self.position

    def jump(self):
        self.rect.y += 1
        collision = pygame.sprite.spritecollide(self, self.game.platform_sprites, False)
        self.rect.y -= 1
        # If the player is on an object and not already in motion
        if(collision and self.velocity.y == 0):
            self.velocity.y = -13


    
''' PLATFORM SPRITE '''
class Platform(pygame.sprite.Sprite):

    def __init__(self, plat_X, plat_Y, plat_Width, plat_Height, player):
        super().__init__()
        # Define the image size, color, etc
        self.image = pygame.Surface([plat_Width, plat_Height])
        self.image.fill(YELLOW)
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.topleft = (plat_X, plat_Y)

        # Define player (for use in scrolling the screen)
        self.player = player

        # Is the platform going to be moving?
        self.movingX = False
        self.movingX_Speed = PLATFORM_MOVING_SPEED
        if(rd.randrange(0, PLATFORM_MOVING_CHANCE) == 0):
            self.movingX = True
 
    def update(self):
        # If platform moves horizontally, move it
        if(self.movingX):
            if(self.rect.right >= WIDTH):
                self.movingX_Speed= -1
            if(self.rect.left <= 0):
                self.movingX_Speed = 1
            self.rect.x += self.movingX_Speed



''' ENEMY SPRITE '''
class Enemy(pygame.sprite.Sprite):

    def __init__(self, enemy_X, enemy_Y, enemy_Width, enemy_Height, player):
        super().__init__()
        # Define the image size, color, etc
        self.image = pygame.Surface([enemy_Width, enemy_Height])
        self.image.fill(RED)
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.x = enemy_X
        self.rect.y = enemy_Y

        # Define player (for use in scrolling the screen)
        self.player = player
