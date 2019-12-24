import pygame
from settings import *

''' CAMERA  '''
class Camera():

    def __init__(self):
        self.distanceMoved = 0

    def update(self, player, objects):
        # Move camera upward if player is moving update
        if player.rect.top <= HEIGHT * 0.3:
            player.position.y += abs(player.velocity.y)
            for obj in objects:
                obj.rect.y += abs(player.velocity.y)
                if obj.rect.top >= HEIGHT:
                    obj.kill()
            self.distanceMoved += abs(player.velocity.y)


''' SPRITESHEET '''
#http://programarcadegames.com/python_examples/en/sprite_sheets/
class SpriteSheet():

    def __init__(self, filename):
        try:
            self.spritesheet = pygame.image.load("res/img/" + filename).convert()
        except pygame.error as message:
            print("Failed to load spritesheet image " , filename)
            raise SystemExit(message)    
        
    def getImageAt(self, x, y, width, height):
        # Create a new blank image
        image = pygame.Surface([width, height]).convert()
 
        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))

        # Rescale the image to work with current size
        # MAKE THIS SO IT'S RELATIVE TO SCALE!!!
        image = pygame.transform.scale(image, (WIDTH // 8, HEIGHT // 8))
 
        # Assuming black works as the transparent color (removes black background)
        image.set_colorkey(BLACK)
 
        # Return the image
        return image
