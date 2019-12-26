import pygame
from settings import *

''' CAMERA  '''
class Camera():

    def __init__(self, game, player, platforms, enemies, projectiles, items):
        self.distanceMoved = 0
        self.game = game
        self.player = player
        self.platforms = platforms
        self.enemies = enemies
        self.projectiles = projectiles
        self.items = items

    def update(self):
        # Move camera upward if player is moving update
        if self.player.rect.top <= HEIGHT * 0.3:
            # Update player
            self.player.position.y += abs(self.player.velocity.y)
            self.distanceMoved += abs(self.player.velocity.y)

            # Update platforms
            for platform in self.platforms:
                current = platform.rect.y
                platform.rect.y += abs(self.player.velocity.y)
                if platform.rect.top >= HEIGHT:
                    platform.kill()
                    self.game.score += 1 
            
            # Update enemies
            for enemy in self.enemies:
                current = enemy.rect.y
                enemy.rect.y += abs(self.player.velocity.y)
                if enemy.rect.top >= HEIGHT:
                    enemy.kill()
                    self.game.score += 1 

            # Update projectiles
            for proj in self.projectiles:
                proj.currentY += abs(self.player.velocity.y)

            # Update items
            for item in self.items:
                item.rect.y += abs(self.player.velocity.y)


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
        image.set_colorkey(BLACK) 
        return image
