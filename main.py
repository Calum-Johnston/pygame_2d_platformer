# University project - for Games and Multimedia sub-module

import pygame
from settings import *
from sprites import Player, Platform
from camera import Camera
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
pygame.display.set_caption(Title)
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
        # Define the player's score
        self.score = 0
        # Define groups
        self.player_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()
        # Define player
        self.player = Player(WIDTH / 2, HEIGHT - 40, 40, 50, self)
        self.player_sprites.add(self.player)
        # Define starting platforms
        self.loadNewPlatforms(True)
        self.loadNewPlatforms(False)
        self.distanceToNextBuild = HEIGHT
        # Create the camera
        self.camera = Camera()
        # Run the game
        self.run()


    """ Runs the game. Defines the main game loop. """ 
    def run(self):
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


    """ This method is run each time through the frame. It
        updates positions and checks for collisions. """
    def update(self):
        # Update player sprite and then camera
        self.player_sprites.update()
        self.camera.update(self.player, self.platform_sprites)

        # If player falls out of the screen, end game
        if(self.player.rect.top > HEIGHT):
            self.gameinstance = False

        # Generate next part of level (both randomly & prebuilt)
        if self.camera.distanceMoved > self.distanceToNextBuild:
            if(rd.randrange(0, 20) < 1):
                self.loadNewPlatforms(False)
            else:
                self.buildRandomPlatforms()
            self.camera.distanceMoved = 0


    """ Display everything to the screen for the game. """
    def draw(self):
        screen.fill(BLUE)
        self.player_sprites.draw(screen)
        self.platform_sprites.draw(screen)
        pygame.display.flip()


    """ Loads pre-built platforms into the game (just out of view)
        based on textfiles read in previously. """
    def loadNewPlatforms(self, newGame):
        if(newGame): new_Section = easy[0]
        else: new_Section = easy[0] # rd.randrange(0, 5)

        start_X = 0; start_Y = 0; width_pt = 0
        for y in range(0, len(new_Section) - 1) :
            for x in range(0, len(new_Section[y][0]) - 1):
                if(new_Section[y][0][x] != "#"):
                    if(new_Section[y][0][x] == "x" and new_Section[y][0][x - 1] != "x"):
                        start_X  = x * 20 - 20; start_Y = y * 20 - 20
                    if(new_Section[y][0][x] == "x" and new_Section[y][0][x + 1] != "x"):
                        width_pt = (x * 20) - start_X
                        if(newGame): self.pt = Platform(start_X, start_Y, width_pt, 20, self.player)
                        else: self.pt = Platform(start_X, start_Y - HEIGHT, width_pt, 20, self.player)
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
        for x in range(0, rd.randrange(0, 6)):
            width = rd.randrange(RANDOM_WIDTH_MIN, RANDOM_WIDTH_MAX)
            x = rd.randrange(0, WIDTH - width)
            y = rd.randrange(closestPlatform_Distance - 130, min(closestPlatform_Distance - 60, 0))  # 60 is arbitrary, 130 is based on jump height
            pt = Platform(x, y, width, 20, self.player)
            self.platform_sprites.add(pt)
            if(x == 0):
                firstPositionY = y
            closestPlatform_Distance = y # Reset y, and restart
        
        self.distanceToNextBuild = abs(firstPositionY - closestPlatform_Distance)





class splashScreen():
    def __init__(self, typeScreen):
        if typeScreen == "Start":
            self.startSplash()
        elif typeScreen == "End":
            self.endSplash()

    def startSplash(self):
        self.drawStartSplash()
        self.wait = True
        while(self.wait):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.wait = False
                    running = False
                if event.type == pygame.KEYUP:
                    self.wait = False
            clock.tick(FPS)

    def drawStartSplash(self):
        screen.fill(BLACK)
        self.drawText("Start Game!", WIDTH / 2, HEIGHT / 2, 36, WHITE)
        self.drawText("Press any key to start!", WIDTH / 2, HEIGHT * 5 / 8, 24, WHITE)
        pygame.display.flip()

    def endSplash(self):
        self.drawEndSplash()
        self.wait = True
        while(self.wait):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.wait = False
                    running = False
                if event.type == pygame.KEYUP:
                    self.wait = False
            clock.tick(FPS)
    
    def drawEndSplash(self):
        screen.fill(BLACK)
        self.drawText("Game Over", WIDTH / 2, HEIGHT / 2, 36, WHITE)
        self.drawText("Press any key to start again", WIDTH / 2, HEIGHT * 5 / 8, 24, WHITE)
        pygame.display.flip()

    def drawText(self, text, text_X, text_Y, text_Size, text_Colour):
        font = pygame.font.Font(None, text_Size)
        text = font.render(text, True, text_Colour)
        text_rect = text.get_rect()
        text_rect.center = (text_X, text_Y)
        screen.blit(text, text_rect)



# Main program
running = True
while(running):
    splashScreen("Start")
    game = Game()
    splashScreen("End")

