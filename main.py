# University project - for Games and Multimedia sub-module

import pygame
from settings import *
from sprites import Player

class Game:
    # initialises the program
    def __init__(self):
        pass

    # starts a new game
    def new(self):
        pass

    # runs the game - loop
    def run(self):
        pass

    # Loop = updates
    def update(self):
        pass

    # Loop = events
    def events(self):
        pass

    # Loop = draws
    def draw(self):
        pass

def main():     
    # initialize the pygame module and create a window
    pygame.init()
    pygame.mixer.init()     
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption(Title)
    clock = pygame.time.Clock()
     
    # initialize sprite group
    sprite_list = pygame.sprite.Group()

    # defines player sprite and adds to sprite list
    player = Player()
    sprite_list.add(player)

    # main loop
    running = True
    while running:
        # EVENTS
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # UPDATE
        sprite_list.update()

        # DRAWING
        # drawing, fills the screen with some colour
        screen.fill(BLUE)
        # draw all sprites onto the screen
        sprite_list.draw(screen)
        # pygame is double-buffered, so this displays anything new drawn
        pygame.display.flip()

        # Number of frames per second (FPS)
        clock.tick(FPS)

    pygame.quit()
     
# run the main function only if this module is executed as the main script
if __name__=="__main__":
    main()