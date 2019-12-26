import pygame
from settings import *
import random as rd
from math import hypot
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

        # Check for PROJECTILE Collision
        collision = pygame.sprite.spritecollide(self, self.game.projectile_sprites, False, pygame.sprite.collide_mask)
        if(collision):
            self.game.gameinstance = False

        # Check for Flag Collision
        collision = pygame.sprite.spritecollide(self, self.game.item_sprites, False, pygame.sprite.collide_mask)
        if(collision):
            flag = collision[0]
            if(flag.captured == False):
                flag.update_Captured()
                self.game.flags_captured += 1

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

    def __init__(self, plat_X, plat_Y, plat_Width, plat_Height, place_flag, game):
        super().__init__()

        # Set the game instance
        self.game = game

        # Load in potential platforms
        self.loadImages()

        # Do we place a flag
        self.place_flag = place_flag

        # Determine image
        self.image = pygame.transform.scale(self.platform_frames[0], (plat_Width, plat_Height))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.topleft = (plat_X, plat_Y)

        # Define the mask (for collision)
        self.mask = pygame.mask.from_surface(self.image)

        self.initialise_Randomness()

    def initialise_Randomness(self):

        # Is the platform going to have a flag?
        if(self.place_flag):
            flag = Flag(rd.randrange(self.rect.left, self.rect.right), self.rect.top, self.game)
            self.game.item_sprites.add(flag)

        # Is the platform going to be moving (only if it has no flag?
        self.movingX = False
        if(not self.place_flag):
            self.movingX_Speed = rd.choice(self.game.platform_movement_speed)
            if(rd.randrange(0, self.game.platform_movement_chance) == 0):
                self.movingX = True


    def update(self):
        # If platform moves horizontally, move it
        if(self.movingX):
            if(self.rect.right > WIDTH or self.rect.left < 0):
                self.movingX_Speed= -self.movingX_Speed
            self.rect.x += self.movingX_Speed

    def loadImages(self):
        self.platform_frames = []
        self.platform_frames.append(self.game.platform_spritesheet.getImageAt(128, 128, 128, 128))




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
        self.velocity = vec(ENEMY_MOVING_SPEED, 0)

    def update(self):

        # If on the screen
        if(self.rect.bottom >= 0 and self.rect.top <= HEIGHT):

            # Animate the enemy
            self.animate()

            # Enemy will bounce off the wall
            if(self.rect.right > WIDTH or self.rect.left < 0):
                self.velocity.x = -self.velocity.x
            self.rect.x += self.velocity.x

            # Produce projectile
            if(rd.randrange(0, 1000) < 1):
                proj = Projectile(self.rect.centerx, self.rect.centery, self.game.player.rect.centerx, self.game.player.rect.centery, self.game)
                self.game.projectile_sprites.add(proj)

            # Update tickcount and speedtick
            self.tickCount += 1

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
        self.walking_frames_l.append(pygame.transform.scale(self.game.enemy_spritesheet.getImageAt(390, 910, 128, 128), (scaleWidth, scaleHeight)))
        self.walking_frames_l.append(pygame.transform.scale(self.game.enemy_spritesheet.getImageAt(390, 650, 128, 128), (scaleWidth, scaleHeight)))
        self.walking_frames_r.append(pygame.transform.scale(pygame.transform.flip(self.game.enemy_spritesheet.getImageAt(390, 910, 128, 128), True, False), (scaleWidth, scaleHeight)))
        self.walking_frames_r.append(pygame.transform.scale(pygame.transform.flip(self.game.enemy_spritesheet.getImageAt(390, 650, 128, 128), True, False), (scaleWidth, scaleHeight)))




''' PROJECTILE CLASS '''
class Projectile(pygame.sprite.Sprite):

    #https://stackoverflow.com/questions/31148730/making-a-bullet-move-to-your-cursor-using-pygame
    def __init__(self, projectile_X, projectile_Y, playerX, playerY, game):
        super().__init__()   

        self.game = game

        self.loadImages()

        self.currentX = projectile_X
        self.destX = playerX 
        self.currentY = projectile_Y
        self.destY = playerY 

        self.speed = 1
 
        self.dx = self.destX - self.currentX
        self.dy = self.destY - self.currentY

        self.image = self.projectileImage

        self.rect = self.image.get_rect()
        self.rect.center = (self.currentX, self.currentY)

        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        if(self.currentX < 0 or self.currentX > WIDTH and self.currentY < 0 or self.currentY > HEIGHT):
            self.kill()

        self.dist = max(1, hypot(self.dx, self.dy))

        self.vx = self.speed * (self.dx / self.dist)
        self.vy = self.speed * (self.dy / self.dist)

        self.currentX += self.vx
        self.currentY += self.vy

        self.rect.center = (self.currentX, self.currentY)

    def loadImages(self):
        scaleWidth = WIDTH // 12
        scaleHeight = HEIGHT // 24
        self.projectileImage = pygame.transform.scale(self.game.items_spritesheet.getImageAt(384, 0, 128, 128), (scaleWidth, scaleHeight))




''' FLAG CLASS '''
class Flag(pygame.sprite.Sprite):

    def __init__(self, flag_X, flag_Y, game):
        super().__init__()

        # Get the game instance (for collision use)
        self.game = game

        # Load in the sprites images
        self.loadImages()

        # Define variables to determine the action the player is currently taking
        self.currentImage = 0
        self.tickCount = 0

        # Define the image size, color, etc
        self.image = self.moving_frames[0]
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.left = flag_X - 2
        self.rect.bottom = flag_Y

        # Define the enemy mask
        self.mask = pygame.mask.from_surface(self.image)

        # Define captured variable
        self.captured = False

    def update(self):
        # Animate the enemy
        self.animate()
        # Update tick count
        self.tickCount += 1

    def animate(self):
        if(self.tickCount > 15 and self.captured == False):
            self.tickCount = 0
            self.currentImage = (self.currentImage + 1) % len(self.moving_frames)
            self.image = self.moving_frames[self.currentImage]

            currentX, currentY = self.rect.midbottom
            self.rect = self.image.get_rect()
            self.rect.midbottom = (currentX, currentY)
            self.mask = pygame.mask.from_surface(self.image)

    def update_Captured(self):
        self.captured = True
        self.image = self.captured_frames[0]
        currentX, currentY = self.rect.midbottom
        self.rect = self.image.get_rect()
        self.rect.midbottom = (currentX, currentY)
        self.mask = pygame.mask.from_surface(self.image)

    def loadImages(self):
        self.moving_frames = []
        self.captured_frames = []

        number = rd.randrange(0, 4)

        scaleWidth = WIDTH // 6
        scaleHeight = HEIGHT // 6

        # Blue flag
        if(number == 0):
            self.moving_frames.append(pygame.transform.scale(self.game.items_spritesheet.getImageAt(256, 0, 128, 128), (scaleWidth, scaleHeight)))
            self.moving_frames.append(pygame.transform.scale(self.game.items_spritesheet.getImageAt(128, 384, 128, 128), (scaleWidth, scaleHeight)))
            self.captured_frames.append(pygame.transform.scale(self.game.items_spritesheet.getImageAt(256, 128, 128, 128), (scaleWidth, scaleHeight)))
        # Green flag
        elif(number == 1):
            self.moving_frames.append(pygame.transform.scale(self.game.items_spritesheet.getImageAt(128, 128, 128, 128), (scaleWidth, scaleHeight)))
            self.moving_frames.append(pygame.transform.scale(self.game.items_spritesheet.getImageAt(128, 0, 128, 128), (scaleWidth, scaleHeight)))
            self.captured_frames.append(pygame.transform.scale(self.game.items_spritesheet.getImageAt(128, 256, 128, 128), (scaleWidth, scaleHeight)))
        # Red flag
        elif(number == 2):
            self.moving_frames.append(pygame.transform.scale(self.game.items_spritesheet.getImageAt(0, 256, 128, 128), (scaleWidth, scaleHeight)))
            self.moving_frames.append(pygame.transform.scale(self.game.items_spritesheet.getImageAt(0, 128, 128, 128), (scaleWidth, scaleHeight)))
            self.captured_frames.append(pygame.transform.scale(self.game.items_spritesheet.getImageAt(0, 384, 128, 128), (scaleWidth, scaleHeight)))
        # Yellow flag
        else:
            self.moving_frames.append(pygame.transform.scale(self.game.items_spritesheet.getImageAt(256, 384, 128, 128), (scaleWidth, scaleHeight)))
            self.moving_frames.append(pygame.transform.scale(self.game.items_spritesheet.getImageAt(640, 256, 128, 128), (scaleWidth, scaleHeight)))
            self.captured_frames.append(pygame.transform.scale(self.game.items_spritesheet.getImageAt(0, 0, 128, 128), (scaleWidth, scaleHeight)))


        
