# University project - for Games and Multimedia sub-module

import pygame
from settings import *
from sprites import Player, Platform

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


class Game:
    """ Constructor. Create all our attributes and initialize
        the game. """    
    def __init__(self):
        self.score = 0

        # Define groups
        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()

        # Define player
        self.player = Player(WIDTH / 2, HEIGHT - 40, 20, 25, self)
        self.all_sprites.add(self.player)
        self.player_sprites.add(self.player)

        # Define platforms
        self.pt = Platform(0, HEIGHT-40, WIDTH, 40, self.player)
        self.all_sprites.add(self.pt)
        self.platform_sprites.add(self.pt)

        platforms = [[100, 300, 150, 20], [10, 200, 50, 20], [150, 100, 100, 20]]
        for pt in platforms:
            self.newPt = Platform(*pt, self.player)
            self.all_sprites.add(self.newPt)
            self.platform_sprites.add(self.newPt)

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
        self.all_sprites.update()

        # Scroll the screen (done here for simplicity)
        if(self.player.rect.top <= HEIGHT * 0.25):
            self.player.pos.y += abs(self.player.velocity.y)
            for pt in self.platform_sprites:
                pt.rect.y += abs(self.player.velocity.y)
                if(pt.rect.top >= HEIGHT):
                    pt.kill()

        # If player falls out of the screen, end game
        if(self.player.rect.top > HEIGHT):
            self.gameinstance = False


    """ Display everything to the screen for the game. """
    def draw(self):
        screen.fill(BLUE)
        self.all_sprites.draw(screen)
        pygame.display.flip()


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
                    print(running)
                if event.type == pygame.KEYUP:
                    print("hi")
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




running = True
while(running):
    splashScreen("Start")
    game = Game()
    splashScreen("End")

