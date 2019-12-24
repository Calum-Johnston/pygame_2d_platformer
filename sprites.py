import pygame
from settings import *
import random as rd
vec = pygame.math.Vector2

''' PLAYER SPRITE '''
class Player(pygame.sprite.Sprite):
    
    def __init__(self, player_X, player_Y, player_Width, player_Height, game):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Get the game instance
        self.game = game

        # Load in the sprites images
        self.loadImages()

        # Define variables to determine the action the player is currently taking
        self.idle = False
        self.walking = False
        self.jumping = False
        self.crouching = False
        self.currentImage = 0
        self.tickCount = 0

        # Define the image size, color, etc
        self.image = self.idle_frames[0]
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.midbottom = (player_X, player_Y)

        # Define the mask (for collision)
        self.mask = pygame.mask.from_surface(self.image)

        # Define initial position, velocity, acceleration for player
        self.position = vec(self.rect.midbottom)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)

    def update(self):

        # Default acceleration is 0 (x-direction) and GRAVITY (y-direction)
        self.acceleration = vec(0, PLAYER_GRAVITY)  # i.e. always accelerting downwards unless changed later
        
        # Default crouching to False, so you only crouch when the key is pressed
        self.crouching = False

        # Determine the key pressed
        keysPressed = pygame.key.get_pressed()
        if(keysPressed[pygame.K_RIGHT] or keysPressed[pygame.K_d]): 
            self.acceleration.x = PLAYER_ACCELERATION
        if(keysPressed[pygame.K_LEFT] or keysPressed[pygame.K_a]): 
            self.acceleration.x = -PLAYER_ACCELERATION
        if(keysPressed[pygame.K_SPACE]):
            self.jump()
        if(keysPressed[pygame.K_DOWN] and self.jumping == False):
            self.crouching = True

        # Decrease acceleration according friction, update velocity according to acceleration
        self.acceleration.x += self.velocity.x * PLAYER_FRICTION  # Friction only applies to x-range
        self.velocity += self.acceleration

        # Reset velocity when it gets too small
        if(abs(self.velocity.x) < 0.5):
            self.velocity.x = 0

        # Calculate the new position (could remove acceleration part)
        self.position += self.velocity + 0.5 * self.acceleration

        # Player wraps around the screen if out of bounds
        if(self.position.x > WIDTH):
            self.position.x = 0
        if(self.position.x < 0):
            self.position.x = WIDTH

        # Updates player position (keep track of bottom, since this is used in collisons)
        self.rect.midbottom = self.position

        self.checkCollisions()
        self.animate()

        # Update the tick count 
        self.tickCount += 1

    def checkCollisions(self):
        #Check for PLATFORM collision
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
    
        # Check for ENEMY Collision
        collision = pygame.sprite.spritecollide(self, self.game.enemy_sprites, False, pygame.sprite.collide_mask)
        if(collision):
            self.game.gameinstance = False

    def jump(self):
        self.rect.y += 1
        collision = pygame.sprite.spritecollide(self, self.game.platform_sprites, False)
        self.rect.y -= 1
        # If the player is on an object and not already in motion
        if(collision and not self.jumping):
            self.velocity.y = -13

    def animate(self):
        self.updateStates()
        if(self.crouching):
            if(self.tickCount > 15):
                self.tickCount = 0
                self.currentImage = (self.currentImage + 1) % len(self.crouching_frames)
                self.image = self.crouching_frames[self.currentImage]
                currentX, currentY = self.rect.midbottom
                self.rect = self.image.get_rect()
                self.rect.midbottom = (currentX, currentY)
        if(self.idle):
            if(self.tickCount > 30):
                self.tickCount = 0
                self.currentImage = (self.currentImage + 1) % len(self.idle_frames)
                self.image = self.idle_frames[self.currentImage]
                currentX, currentY = self.rect.midbottom
                self.rect = self.image.get_rect()
                self.rect.midbottom = (currentX, currentY)
        elif(self.jumping):
            if(self.tickCount > 15):
                self.tickCount = 0
                self.currentImage = (self.currentImage + 1) % len(self.jumping_frames)
                self.image = self.jumping_frames[self.currentImage]
                currentX, currentY = self.rect.midbottom
                self.rect = self.image.get_rect()
                self.rect.midbottom = (currentX, currentY)
        elif(self.walking):
            if(self.tickCount > 15):
                self.tickCount = 0
                self.currentImage = (self.currentImage + 1) % len(self.walking_frames_r)
                if(self.velocity.x > 0): self.image = self.walking_frames_r[self.currentImage]
                else: self.image = self.walking_frames_l[self.currentImage]
                currentX, currentY = self.rect.midbottom
                self.rect = self.image.get_rect()
                self.rect.midbottom = (currentX, currentY)
        self.mask = pygame.mask.from_surface(self.image)

    def updateStates(self):
        # Update idle state
        if(self.velocity.x == 0 and self.velocity.y == 0):
            self.idle = True
        else:
            self.idle = False

        # Update walking state (only if not jumping)
        if(not self.jumping):
            if(self.velocity.x != 0):
                self.walking = True
            else:
                self.walking = False

        # Update jumping state (more complicated)
        if(self.velocity.y != 0):
            self.jumping = True
        else:
            collisions = pygame.sprite.spritecollide(self, self.game.platform_sprites, False)
            if(len(collisions) == 0):
                self.jumping = True
            else:
                platform = collisions[0]
                for pt in collisions:
                    if(pt.rect.bottom > platform.rect.bottom):
                        platform = pt
                if(platform.rect.bottom > self.rect.bottom):
                    self.jumping = False
                else:
                    self.jumping = True
        
    def loadImages(self):

        self.idle_frames = []
        self.walking_frames_r = []
        self.walking_frames_l = []
        self.jumping_frames = []
        self.crouching_frames = []

        scaleWidth = WIDTH // 6
        scaleHeight = HEIGHT // 6
        
        # Update idle frame
        self.idle_frames.append(pygame.transform.scale(self.game.player_spritesheet.getImageAt(768, 0, 128, 256), (scaleWidth, scaleHeight)))
        self.idle_frames.append(pygame.transform.scale(self.game.player_spritesheet.getImageAt(768, 768, 128, 256), (scaleWidth, scaleHeight)))

        # Update walking frames
        self.walking_frames_r.append(pygame.transform.scale(self.game.player_spritesheet.getImageAt(640, 1280, 128, 256), (scaleWidth, scaleHeight)))
        self.walking_frames_r.append(pygame.transform.scale(self.game.player_spritesheet.getImageAt(640, 1024, 128, 256), (scaleWidth, scaleHeight)))
        self.walking_frames_l.append(pygame.transform.scale(pygame.transform.flip(self.game.player_spritesheet.getImageAt(640, 1280, 128, 256), True, False), (scaleWidth, scaleHeight)))
        self.walking_frames_l.append(pygame.transform.scale(pygame.transform.flip(self.game.player_spritesheet.getImageAt(640, 1024, 128, 256), True, False), (scaleWidth, scaleHeight)))

        # Update jumping frames
        self.jumping_frames.append(pygame.transform.scale(self.game.player_spritesheet.getImageAt(768, 256, 128, 256), (scaleWidth, scaleHeight)))

        # Update crouching frames
        self.crouching_frames.append(pygame.transform.scale(self.game.player_spritesheet.getImageAt(768, 1024, 128, 256), (scaleWidth, scaleHeight)))
    


''' PLATFORM SPRITE '''
class Platform(pygame.sprite.Sprite):

    def __init__(self, plat_X, plat_Y, plat_Width, plat_Height, game):
        super().__init__()

        # Set the game instance
        self.game = game

        # Load in potential platforms
        self.loadImages()

        # Determine image
        self.image = pygame.transform.scale(self.platform_frames[0], (plat_Width, plat_Height))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.topleft = (plat_X, plat_Y)

        # Define the mask (for collision)
        self.mask = pygame.mask.from_surface(self.image)

        # Is the platform going to be moving?
        self.movingX = False
        self.movingX_Speed = PLATFORM_MOVING_SPEED
        if(rd.randrange(0, PLATFORM_MOVING_CHANCE) == 0):
            self.movingX = True
 
    def update(self):
        # If platform moves horizontally, move it
        if(self.movingX):
            if(self.rect.right > WIDTH or self.rect.left < 0):
                self.movingX_Speed= -self.movingX_Speed
            self.rect.x += self.movingX_Speed

    def loadImages(self):
        self.platform_frames = []
        self.platform_frames.append(self.game.platform_spritesheet.getImageAt(128, 128, 128, 128)) #Full
        #self.platform_frames.append(self.game.platform_spritesheet.getImageAt(0, 1024, 128, 128)) #Full




''' ENEMY SPRITE '''
class Enemy(pygame.sprite.Sprite):

    def __init__(self, enemy_X, enemy_Y, enemy_Width, enemy_Height, game):
        super().__init__()

        # Get the game instance (for collision use)
        self.game = game

        # Load in the sprites images
        self.loadImages()

        # Define variables to determine the action the player is currently taking
        self.currentImage = 0
        self.tickCount = 0

        # Define the image size, color, etc
        self.image = self.walking_frames_r[0]
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.x = enemy_X
        self.rect.y = enemy_Y

        # Define the enemy mask
        self.mask = pygame.mask.from_surface(self.image)

        # Define velocity varaible
        self.velocity = vec(1, 0)

        # Define player (for use in scrolling the screen)
        self.game = game

    def update(self):
        self.animate()
        # Enemy will bounce off the wall
        if(self.rect.right > WIDTH or self.rect.left < 0):
            self.velocity.x = -self.velocity.x
        self.rect.x += self.velocity.x

    def animate(self):
        if(self.tickCount > 15):
            self.tickCount = 0
            self.currentImage = (self.currentImage + 1) % len(self.walking_frames_r)
            if(self.velocity.x > 0): self.image = self.walking_frames_r[self.currentImage]
            else: self.image = self.walking_frames_l[self.currentImage]
            currentX, currentY = self.rect.midbottom
            self.rect = self.image.get_rect()
            self.rect.midbottom = (currentX, currentY)
            self.mask = pygame.mask.from_surface(self.image)

    def loadImages(self):
        self.walking_frames_r = []
        self.walking_frames_l = []

        scaleWidth = WIDTH // 4
        scaleHeight = HEIGHT // 8

        # Update walking frames
        self.walking_frames_r.append(pygame.transform.scale(self.game.enemy_spritesheet.getImageAt(390, 910, 128, 128), (scaleWidth, scaleHeight)))
        self.walking_frames_r.append(pygame.transform.scale(self.game.enemy_spritesheet.getImageAt(390, 650, 128, 128), (scaleWidth, scaleHeight)))
        self.walking_frames_l.append(pygame.transform.scale(pygame.transform.flip(self.game.enemy_spritesheet.getImageAt(390, 910, 128, 128), True, False), (scaleWidth, scaleHeight)))
        self.walking_frames_l.append(pygame.transform.scale(pygame.transform.flip(self.game.enemy_spritesheet.getImageAt(390, 650, 128, 128), True, False), (scaleWidth, scaleHeight)))
