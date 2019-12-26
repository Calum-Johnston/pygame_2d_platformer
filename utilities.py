import pygame
import random as rd
from settings import *
from sprites import Enemy

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
        # Move camera upward if player is moving upward above a certain point
        if (self.player.rect.top <= HEIGHT * 0.3 and abs(self.player.velocity.y) > 0):
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
                    self.game.scoreToNextDiff -= 1
            
            # Update enemies
            for enemy in self.enemies:
                current = enemy.rect.y
                enemy.rect.y += abs(self.player.velocity.y)
                if enemy.rect.top >= HEIGHT:
                    enemy.kill()

            # Update projectiles
            for proj in self.projectiles:
                proj.currentY += abs(self.player.velocity.y)
                if(proj.rect.top >= HEIGHT):
                    proj.kill()

            # Update items
            for item in self.items:
                item.rect.y += abs(self.player.velocity.y)
                if(item.rect.top >= HEIGHT):
                    item.kill()

            # Spawn new enemies (only when screen is generated)   
            if(rd.randrange(0, self.game.enemy_spawn_chance) < 1 and len(self.game.enemy_sprites) < 3):
                self.enemy = Enemy(rd.randrange((WIDTH // 2) - (WIDTH // 4), (WIDTH // 2) + (WIDTH // 4)), 0 - (HEIGHT / 2), 40, 50, self.game)
                self.game.enemy_sprites.add(self.enemy)


''' SPRITESHEET '''
class SpriteSheet():
    # http://programarcadegames.com/python_examples/en/sprite_sheets/
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
