# University project - for Games and Multimedia sub-module

import pygame
from settings import *
from sprites import Player, Platform, Enemy
from utilities import Camera, SpriteSheet
import random as rd
import math

# Defines global variables
global screen
global clock
global running

# Initialises game window, etc
pygame.init()
pygame.mixer.init()     
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(TITLE)
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

# Read in pre-built platform sections
easy = []
medium = []
hard = []
for x in range(0, 5):
    with open("sections/easy/easy_%i.txt" % (x + 1)) as textFile:
        easy.append([line.split() for line in textFile])
    with open("sections/medium/medium_%i.txt" % (x + 1)) as textFile:
        medium.append([line.split() for line in textFile])
    with open("sections/hard/hard_%i.txt" % (x + 1)) as textFile:
        hard.append([line.split() for line in textFile])



class Game:
    """ Constructor. Create all our attributes and initialize
        the game. """    
    def __init__(self):

        # Read in spritesheet data
        self.player_spritesheet = SpriteSheet(PLAYER_SPRITESHEET)
        self.enemy_spritesheet = SpriteSheet(ENEMY_SPRITESHEET)
        self.platform_spritesheet = SpriteSheet(PLATFORM_SPRITESHEET)
        self.items_spritesheet = SpriteSheet(ITEM_SPRITESHEET)
        self.tiles_spritesheet = SpriteSheet(TILES_SPRITESHEET)

        # Read in pre-built platform sections
        easy = []; medium = []; hard = []
        for x in range(0, 5):
            with open("sections/easy/easy_%i.txt" % (x + 1)) as textFile:
                easy.append([line.split() for line in textFile])
            with open("sections/medium/medium_%i.txt" % (x + 1)) as textFile:
                medium.append([line.split() for line in textFile])
            with open("sections/hard/hard_%i.txt" % (x + 1)) as textFile:
                hard.append([line.split() for line in textFile])


    """ Setups basic game variables """
    def setupGame(self):
        # Define the player's score
        self.scoreToNextDiff = 50
        self.score = 0

        # Flag related variables
        self.flags_captured = 0
        self.place_flag = False

        # Define DIFFICULTY SETTINGS
        self.difficulty = 0
        self.difficulty_platform_dist = 40
        self.platform_movement_speed = [PLATFORM_MOVING_SPEED]
        self.platform_movement_chance = PLATFORM_MOVING_CHANCE
        self.enemy_spawn_chance = ENEMY_SPAWN_CHANCE
        self.enemy_moving_speed = ENEMY_MOVING_SPEED

        # Define sprite groups
        self.player_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.projectile_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.upgrade_sprites = pygame.sprite.Group()

        # Define player sprite
        self.player = Player(WIDTH / 2, HEIGHT - 50, 40, 50, self)
        self.player_sprites.add(self.player)

        # Define starting platforms
        self.loadNewPlatforms(True)
        self.loadNewPlatforms(False)
        self.distanceToNextBuild = HEIGHT

        # Create the camera
        self.camera = Camera(self, self.player, self.platform_sprites, self.enemy_sprites,
         self.projectile_sprites, self.item_sprites)


    """ Runs the game. Defines the main game loop. """ 
    def run(self):
        self.setupGame()
        self.gameinstance = True
        while(self.gameinstance):
            self.events()
            self.update()
            self.draw()
            clock.tick(FPS)


    """ Process all of the events. Return a "True" if we need
        to close the window. """
    def events(self):
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                running = False
                self.gameinstance = False
            if event.type == pygame.KEYUP:
                self.player.tickCount = FPS
            


    """ Updates game objects (animations, position, etc) """
    def update(self):
        # Update player sprite and then camera
        self.sprite_Update()
        self.camera_Update()
        self.difficulty_Update()
    
    """ Update sprites in the game """
    def sprite_Update(self):
        self.player_sprites.update()
        self.platform_sprites.update()
        self.enemy_sprites.update()
        self.projectile_sprites.update()
        self.item_sprites.update()

    """ Updates camera & builds new platforms """
    def camera_Update(self):
        self.camera.update()

        # Generate next part of level (both randomly & prebuilt)
        if self.camera.distanceMoved > self.distanceToNextBuild:
            self.buildRandomPlatforms()
            self.camera.distanceMoved = 0

    """ Updates game variables, difficulty, enemies and more """
    def difficulty_Update(self):
        # If player falls out of the screen, end game
        if(self.player.rect.top > HEIGHT):
            self.gameinstance = False

        if(self.scoreToNextDiff == 0):
            self.scoreToNextDiff = 50
            if(len(self.platform_movement_speed) < 3):
                self.platform_movement_speed.append(self.platform_movement_speed[len(self.platform_movement_speed) - 1] + 1)
            if(self.platform_movement_chance > 2):
                self.platform_movement_chance -= 2
            if(self.difficulty_platform_dist < 120):
                self.difficulty_platform_dist += 10
            if(self.enemy_spawn_chance > 100):
                self.enemy_spawn_chance -= 50

            # Put a new flag down!
            self.place_flag = True
            

    """ Display everything to the screen for the game. """
    def draw(self):
        # If player is invincible!
        if(self.player.invincibleTime > 0):
            screen.fill(RED)
        else:
            screen.fill(SKY_BLUE)
        self.platform_sprites.draw(screen)
        self.item_sprites.draw(screen)
        self.enemy_sprites.draw(screen)
        self.projectile_sprites.draw(screen)
        self.player_sprites.draw(screen)
        if(not self.gameinstance):
            self.fade()
            self.gameOver()
        self.drawText("Score: " + str(self.score), 60, HEIGHT - 20, 36, BLACK)
        self.drawText("Flags: " + str(self.flags_captured), WIDTH - 60,  HEIGHT - 20, 36, BLACK)
        pygame.display.flip()


    """ Produces the game over screen """
    def gameOver(self):
        self.drawText("GAME OVER", WIDTH // 2, HEIGHT // 16 * 7, 46, WHITE)
        self.drawText("Score:" + str(self.score), WIDTH // 2, HEIGHT // 16 * 8, 32, GREY)
        self.drawText("Flags captured: " + str(self.flags_captured), WIDTH // 2, HEIGHT // 16 * 9, 32, GREY)
        self.drawText("Press ESC to return!", WIDTH / 2, HEIGHT - 40, 30, MAROON)
        pygame.display.flip()
        keyPressed = False
        while(not keyPressed):
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYUP:
                    if(event.key == pygame.K_ESCAPE):
                        keyPressed = True

    """ Loads pre-built platforms into the game (just out of view)
        based on textfiles read in previously. 
        CURRENTLY ONLY IN USE FOR INITIALISATION"""  
    def loadNewPlatforms(self, newGame):
        if(newGame): 
            new_Section = easy[0]
        else: 
            if(self.difficulty == 0):
                new_Section = easy[rd.randrange(1, len(easy))]
            elif(self.difficulty == 1):
                new_Section = medium[rd.randrange(0, len(medium))]
            elif(self.difficulty == 2):
                new_Section = hard[rd.randrange(0, len(hard))]

        start_X = 0; start_Y = 0; width_pt = 0
        for y in range(0, len(new_Section) - 1) :
            for x in range(0, len(new_Section[y][0]) - 1):
                if(new_Section[y][0][x] != "#"):
                    if(new_Section[y][0][x] == "x" and new_Section[y][0][x - 1] != "x"):
                        start_X  = x * 20 - 20; start_Y = y * 20 - 20
                    if(new_Section[y][0][x] == "x" and new_Section[y][0][x + 1] != "x"):
                        width_pt = (x * 20) - start_X
                        if(newGame): self.pt = Platform(start_X, start_Y, width_pt, 20, self.place_flag, self)
                        else: self.pt = Platform(start_X, start_Y - HEIGHT, width_pt, 20, self.place_flag, self)
                        self.platform_sprites.add(self.pt)

        self.distanceToNextBuild = HEIGHT
    
    
    """ Bulids random platforms to cushion prebuilt platforms - gives
        the appearance of entirely randomised level. """
    def buildRandomPlatforms(self):
        # Get closest platform
        closestPlatform_Distance = 1000
        for pt in self.platform_sprites:
            if(pt.rect.top < closestPlatform_Distance):
                closestPlatform_Distance = pt.rect.top
        
        firstPositionY = 0
        for i in range(0, 6):
            width = rd.randrange(RANDOM_WIDTH_MIN, RANDOM_WIDTH_MAX)
            x = rd.randrange(0, WIDTH - width)
            y = rd.randrange(min(closestPlatform_Distance - 130, -1), min(closestPlatform_Distance - self.difficulty_platform_dist, 1)) 
            
            if(self.place_flag):
                pt = Platform(x, y, width, 20, self.place_flag, self)
                self.place_flag = False
            else:
                pt = Platform(x, y, width, 20, self.place_flag, self)
            self.platform_sprites.add(pt)

            closestPlatform_Distance = y
        
        self.distanceToNextBuild = abs(firstPositionY - closestPlatform_Distance)

    """ Draws text onto the screen """
    def drawText(self, text, text_X, text_Y, text_Size, text_Colour):
        font = pygame.font.Font(None, text_Size)
        text = font.render(text, True, text_Colour)
        text_rect = text.get_rect()
        text_rect.center = (text_X, text_Y)
        screen.blit(text, text_rect)

    """ Returns the score """
    def getScore(self):
        return self.score

    """ Fades the screen tp black """
    def fade(self):
        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.fill((0, 0, 0))
        for alpha in range(0, 300):
            fade.set_alpha(alpha)
            screen.fill((255, 255, 255))
            screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(5)


class startScreen():
    def __init__(self, highscore):
        self.highscore = highscore
        self.runSplashScreen()

    def runSplashScreen(self):
        self.drawSplashScreen()
        self.wait = True
        while(self.wait):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.wait = False
                    running = False
                if event.type == pygame.KEYUP:
                    self.wait = False
            clock.tick(FPS)

    def drawSplashScreen(self):
        screen.fill(SKY_BLUE)
        self.drawText(TITLE, WIDTH / 2, 40, 40, SALMON)
        self.drawText("RULES!", WIDTH / 2, 100, 24, DARK_SKATE_BLUE)
        self.drawText("Collect the treasures (10 to find!)", WIDTH / 2, 120, 24, GREY)
        self.drawText("Watch out for monsters", WIDTH / 2, 140, 24, GREY)
        self.drawText("CONTROLS!", WIDTH / 2, 180, 24, DARK_SKATE_BLUE)
        self.drawText("LEFT/RIGHT = Left/Right Key or W/D!", WIDTH / 2, 200, 24, GREY)
        self.drawText("JUMP = Space bar!", WIDTH / 2, 220, 24, GREY)
        self.drawText("CROUCH = Ctrl / Down Key!", WIDTH / 2, 240, 24, GREY)
        self.drawText("POWERUPS!", WIDTH / 2, 280, 24, DARK_SKATE_BLUE)
        self.drawText("Spring = Super high jump!", WIDTH / 2, 300, 24, GREY)
        self.drawText("Mushroom = Invincibility!", WIDTH / 2, 320, 24, GREY)
        self.drawText("CURRENT HIGHSCORE = " + str(self.highscore), WIDTH / 2, 400, 26, BLACK)
        self.drawText("Press any key to start!", WIDTH / 2, 460, 30, MAROON)
        pygame.display.flip()

    def drawText(self, text, text_X, text_Y, text_Size, text_Colour):
        font = pygame.font.Font(None, text_Size)
        text = font.render(text, True, text_Colour)
        text_rect = text.get_rect()
        text_rect.center = (text_X, text_Y)
        screen.blit(text, text_rect)
    



# Main program
running = True
highscore = 0
game = Game()
while(running):
    startScreen(highscore)
    game.run()
    score = game.getScore()
    if(score > highscore):
        highscore = score