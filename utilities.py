import pygame
from settings import *

''' CAMERA  '''
class Camera():

    def __init__(self, game):
        self.distanceMoved = 0
        self.game = game

    def update(self, player, objects):
        # Move camera upward if player is moving update
        if player.rect.top <= HEIGHT * 0.3:
            player.position.y += abs(player.velocity.y)
            for obj in objects:
                obj.rect.y += abs(player.velocity.y)
                if obj.rect.top >= HEIGHT:
                    obj.kill()
                    self.game.score += 1  # Update score
            self.distanceMoved += abs(player.velocity.y)


''' SPRITESHEET '''
# http://programarcadegames.com/python_examples/en/sprite_sheets/
class SpriteSheet():

    def __init__(self, filename):
        try:
            self.spritesheet = pygame.image.load("res/img/" + filename).convert()
        except pygame.error as message:
            print("Failed to load spritesheet image " , filename)
            raise SystemExit(message)    
        
    def getImageAt(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        if(width == height):
            image = pygame.transform.scale(image, (WIDTH // 8, HEIGHT // 16))
        else:
            image = pygame.transform.scale(image, (WIDTH // 8, HEIGHT // 8))
        image.set_colorkey(BLACK) 
        return image
