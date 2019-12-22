import pygame
from settings import *
vec = pygame.math.Vector2

''' PLAYER SPRITE '''
class Player(pygame.sprite.Sprite):
    
    def __init__(self, player_X, player_Y, player_Width, player_Height, game):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Get the game instance (for collision use)
        self.game = game
        
        # Define the image size, color, etc
        self.image = pygame.Surface([player_Width, player_Height])
        self.image.fill(MAGNETA)
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.midbottom = (player_X, player_Y)

        # Define initial position, velocity, acceleration for player
        self.pos = self.rect.midbottom
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)

    def update(self):
        # Default acceleration is 0 (x-direction) and GRAVITY (y-direction)
        self.acceleration = vec(0, PLAYER_GRAVITY)  # i.e. always accelerting downwards unless changed later
        
        # Determine whether the player is accelerating
        keysPressed = pygame.key.get_pressed()
        if(keysPressed[pygame.K_RIGHT]): 
            self.acceleration.x = PLAYER_ACCELERATION
        if(keysPressed[pygame.K_LEFT]): 
            self.acceleration.x = -PLAYER_ACCELERATION
        if(keysPressed[pygame.K_SPACE]):
            self.jump()

        # Decrease acceleration according friction, update velocity according to acceleration
        self.acceleration.x += self.velocity.x * PLAYER_FRICTION  # Friction only applies to x-range
        self.velocity += self.acceleration

        # Calculate the new position (could remove acceleration part)
        self.pos += self.velocity + 0.5 * self.acceleration

        # Player wraps around the screen if out of bounds
        if(self.pos.x > WIDTH):
            self.pos.x = 0
        if(self.pos.x < 0):
            self.pos.x = WIDTH

        #Check for collison (only if falling - prevents glitching to platforms)
        if(self.velocity.y > 0):  # y velocity > 0 means we're moving downnward
            collision = pygame.sprite.spritecollide(self, self.game.platform_sprites, False)
            if(collision):
                self.platform = collision[0]
                self.pos.y = self.platform.rect.top + 1
                self.velocity.y = 0

        # Updates player position (keep track of bottom, since this is used in collisons)
        self.rect.midbottom = self.pos

    def jump(self):
        self.rect.y += 1
        collision = pygame.sprite.spritecollide(self, self.game.platform_sprites, False)
        self.rect.y -= 1
        print(self.velocity.y)
        # If the player is on an object and not already in motion
        if(collision and self.velocity.y == 0):
            self.velocity.y = -12


    
''' PLATFORM SPRITE (child of SceneObject) '''
class Platform(pygame.sprite.Sprite):

    def __init__(self, plat_X, plat_Y, plat_Width, plat_Height, player):
        super().__init__()
        # Define the image size, color, etc
        self.image = pygame.Surface([plat_Width, plat_Height])
        self.image.fill(YELLOW)
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.x = plat_X
        self.rect.y = plat_Y

        # Define player (for use in scrolling the screen)
        self.player = player


''' ENEMY SPRITE (child of SceneObject) '''
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