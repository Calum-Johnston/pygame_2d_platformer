# University project - for Games and Multimedia sub-module

import pygame
from settings import *
from sprites import Player

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

        self.sprite_list = pygame.sprite.Group()
        self.player = Player()
        self.sprite_list.add(self.player)

        self.run()

    """ Runs the game. Defines the main game loop. """ 
    def run(self):
        self.gameinstance = True
        while(self.gameinstance):
            clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

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
        self.sprite_list.update()


    """ Display everything to the screen for the game. """
    def draw(self):
        screen.fill(BLUE)
        self.sprite_list.draw(screen)
        pygame.display.flip()

class startScreen:
    def __init__(self):
        pass

running = True
while(running):
    startScreen()
    game = Game()

