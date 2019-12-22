import pygame
from settings import *

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