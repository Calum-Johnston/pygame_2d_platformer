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

        # Define power up variables (used for powerups)
        self.boostPowerUp = False  
        self.invincibleTime = 0   

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

        # Define a default direction
        self.direction = "R"

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
        if(keysPressed[pygame.K_SPACE] or keysPressed[pygame.K_w] or keysPressed[pygame.K_UP]):
            self.jump()
        if((keysPressed[pygame.K_DOWN] or keysPressed[pygame.K_LCTRL] or keysPressed[pygame.K_s]) and self.jumping == False):
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

        # Once movement complete, check for collisions and animate
        self.checkCollisions()
        self.animate()

        # Update the tick count 
        self.tickCount += 1

        if(self.invincibleTime > 0):
            self.invincibleTime -= 1

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
                    if(self.jumping):
                        self.tickCount = FPS
                    self.jumping = False
                    self.boostPowerUp = False
    
        # Check for ENEMY Collision
        if(not self.boostPowerUp and self.invincibleTime == 0):
            collision = pygame.sprite.spritecollide(self, self.game.enemy_sprites, False, pygame.sprite.collide_mask)
            if(collision):
                self.game.gameinstance = False

        # Check for PROJECTILE Collision
        if(not self.boostPowerUp and self.invincibleTime == 0):
            collision = pygame.sprite.spritecollide(self, self.game.projectile_sprites, False, pygame.sprite.collide_mask)
            if(collision):
                self.game.gameinstance = False

        # Check for Flag Collision
        collision = pygame.sprite.spritecollide(self, self.game.item_sprites, False, pygame.sprite.collide_mask)
        if(collision):
            for item in collision:
                if(item.type == "flag"):
                    if(item.captured == False):
                        item.update_Captured()
                        self.game.flags_captured += 1
                elif(item.type == "boost"):
                    if(item.used == False):
                        self.velocity.y = BOOST_POWER
                        self.boostPowerUp = True
                        item.isUsed()
                elif(item.type == "invincible"):
                    if(item.used == False):
                        self.invincibleTime = rd.randrange(INVINCIBLE_MINIMUM_DURATION, INVINCIBLE_MAXIMUM_DURATION) 
                        item.isUsed()

    def jump(self):
        # Checks whether a player is standing on an object
        self.rect.y += 1
        collision = pygame.sprite.spritecollide(self, self.game.platform_sprites, False)
        self.rect.y -= 1

        # If the player is on an object and not already in motion
        if(collision and not self.jumping):
            self.jumping = True
            self.velocity.y = -13

    def animate(self):
        self.updateStates()

        # Updates image (in order of priority)
        if(self.crouching):
            self.tickCount = 0
            self.currentImage = (self.currentImage + 1) % len(self.crouching_frames)
            self.image = self.crouching_frames[self.currentImage]
        elif(self.idle):
            if(self.tickCount > FPS / 2):
                self.tickCount = 0
                self.currentImage = (self.currentImage + 1) % len(self.idle_frames)
                self.image = self.idle_frames[self.currentImage]
        elif(self.jumping):
            self.tickCount = 0
            self.currentImage = (self.currentImage + 1) % len(self.jumping_frames_r)
            if(self.direction == "R"):
                self.image = self.jumping_frames_r[self.currentImage]
            else:
                self.image = self.jumping_frames_l[self.currentImage]
        elif(self.walking):
            if(self.tickCount > FPS / 4):
                self.tickCount = 0
                self.currentImage = (self.currentImage + 1) % len(self.walking_frames_r)
                if(self.velocity.x > 0): 
                    self.image = self.walking_frames_r[self.currentImage]
                else: 
                    self.image = self.walking_frames_l[self.currentImage]

        # Update image rect and mask
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

        # Update direction state (doesn't update at 0)
        # (so hence acts as last direction moved as well)
        if(self.velocity.x > 0):
            self.direction = "R"
        elif(self.velocity.x < 0):
            self.direction = "L"

        # Jumping state updated elsewhere
        
    def loadImages(self):
        self.idle_frames = []
        self.walking_frames_r = []
        self.walking_frames_l = []
        self.jumping_frames_r = []
        self.jumping_frames_l = []
        self.crouching_frames = []

        scaleWidth = WIDTH // 6
        scaleHeight = HEIGHT // 6
        
        # Update idle frame
        self.idle_frames.append(pygame.transform.scale(self.game.player_spritesheet.getImageAt(768, 0, 128, 256), (scaleWidth, scaleHeight)))
        self.idle_frames.append(pygame.transform.scale(self.game.player_spritesheet.getImageAt(768, 768, 128, 256), (scaleWidth, scaleHeight)))
        self.idle_frames.append(pygame.transform.scale(pygame.transform.flip(self.game.player_spritesheet.getImageAt(768, 0, 128, 256), True, False), (scaleWidth, scaleHeight)))
        self.idle_frames.append(pygame.transform.scale(self.game.player_spritesheet.getImageAt(768, 768, 128, 256), (scaleWidth, scaleHeight)))

        # Update walking frames
        self.walking_frames_r.append(pygame.transform.scale(self.game.player_spritesheet.getImageAt(640, 1280, 128, 256), (scaleWidth, scaleHeight)))
        self.walking_frames_r.append(pygame.transform.scale(self.game.player_spritesheet.getImageAt(640, 1024, 128, 256), (scaleWidth, scaleHeight)))
        self.walking_frames_l.append(pygame.transform.scale(pygame.transform.flip(self.game.player_spritesheet.getImageAt(640, 1280, 128, 256), True, False), (scaleWidth, scaleHeight)))
        self.walking_frames_l.append(pygame.transform.scale(pygame.transform.flip(self.game.player_spritesheet.getImageAt(640, 1024, 128, 256), True, False), (scaleWidth, scaleHeight)))

        # Update jumping frames
        self.jumping_frames_r.append(pygame.transform.scale(self.game.player_spritesheet.getImageAt(768, 256, 128, 256), (scaleWidth, scaleHeight)))
        self.jumping_frames_l.append(pygame.transform.scale(pygame.transform.flip(self.game.player_spritesheet.getImageAt(768, 256, 128, 256), True, False), (scaleWidth, scaleHeight)))

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

        self.movingX = False
        self.movingX_Speed = 0

        # If no flag
        if(not self.place_flag):

            # Is the platform going to be moving (only if it has no flag?
            if(rd.randrange(0, self.game.platform_movement_chance) == 0):
                self.movingX_Speed = rd.choice(self.game.platform_movement_speed)
                self.movingX = True

            # Is the platform going to have a boost upgrade
            if(rd.randrange(0, BOOST_SPAWN_CHANCE) == 0):
                upgrade = Upgrade(rd.randrange(self.rect.left, self.rect.right), self.rect.top, "boost",
                    self, self.game)
                self.game.item_sprites.add(upgrade)

            # Is the platform going to have an invincibility upgrade
            elif(rd.randrange(0, INVINCIBLE_SPAWN_CHANCE) == 0):
                upgrade = Upgrade(rd.randrange(self.rect.left, self.rect.right), self.rect.top, "invincible",
                    self, self.game)
                self.game.item_sprites.add(upgrade)

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
            if(rd.randrange(0, ENEMY_SHOOT_CHANCE) < 1):
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

        # Define the type of item it is
        self.type = "flag"

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



        
''' UPGRADE CLASS '''
class Upgrade(pygame.sprite.Sprite):

    def __init__(self, upgrade_X, upgrade_Y, upgrade_Type, plat, game):
        super().__init__()

        # Get the game instance (for collision use)
        self.game = game

        # Defines the type of upsgrade
        self.type = upgrade_Type

        # Load in the sprites images
        self.loadImages()

        # Define platform that connects it
        self.plat = plat

        # Define whether it has been used or not
        self.used = False

        # Define moving variables
        self.movingX = self.plat.movingX
        self.movingX_Speed = self.plat.movingX_Speed

        # Define the image size, color, etc
        self.image = self.boost_frames[0]
  
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.left = upgrade_X - 2
        self.rect.bottom = upgrade_Y

        # Define the enemy mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # If item  moves horizontally, move it
        if(self.movingX):
            if(self.plat.rect.right > WIDTH or self.plat.rect.left < 0):
                self.movingX_Speed= -self.movingX_Speed
            self.rect.x += self.movingX_Speed

    def isUsed(self):
        self.used = True
        self.image = self.boost_frames[1]
        currentX, currentY = self.rect.midbottom
        self.rect = self.image.get_rect()
        self.rect.midbottom = (currentX, currentY)
        self.mask = pygame.mask.from_surface(self.image)

    def loadImages(self):
        self.boost_frames = []

        scaleWidth = WIDTH // 12
        scaleHeight = HEIGHT // 12

        if(self.type == "boost"):
            self.boost_frames.append(pygame.transform.scale(self.game.tiles_spritesheet.getImageAt(128, 1792, 128, 128), (scaleWidth, scaleHeight)))
            self.boost_frames.append(pygame.transform.scale(self.game.tiles_spritesheet.getImageAt(128, 1664, 128, 128), (scaleWidth, scaleHeight)))
        elif(self.type == "invincible"):
            self.boost_frames.append(pygame.transform.scale(self.game.tiles_spritesheet.getImageAt(256, 1024, 128, 128), (scaleWidth, scaleHeight)))
            self.boost_frames.append(pygame.transform.scale(self.game.tiles_spritesheet.getImageAt(512, 1024, 128, 128), (scaleWidth, scaleHeight)))