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

        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()

        # Define player
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.player_sprites.add(self.player)

        # Define platforms
        self.pt = Platform(0, HEIGHT-40, WIDTH, 40)
        self.all_sprites.add(self.pt)
        self.platform_sprites.add(self.pt)

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    """ This method is run each time through the frame. It
        updates positions and checks for collisions. """
    def update(self):
        self.all_sprites.update()
        #Check for collison (only if falling - prevents glitching to platforms)
        if(self.player.velocity.y > 0):
            collision = pygame.sprite.spritecollide(self.player, self.platform_sprites, False)
            if(collision):
                self.platform = collision[0]
                self.player.pos.y = self.platform.rect.top + 1
                self.player.velocity.y = 0




    """ Display everything to the screen for the game. """
    def draw(self):
        screen.fill(BLUE)
        self.all_sprites.draw(screen)
        pygame.display.flip()

class startScreen:
    def __init__(self):
        pass

running = True
while(running):
    startScreen()
    game = Game()

